import numpy as np
from scipy.io import readsav
import bagpipes as pipes
import argparse


def load_malin2(ID):
    if not hasattr(load_malin2, 'f1'):
        load_malin2.f1 = readsav('Malin2binned.sav')
    # Do some stuff to load up data for the object with the correct ID number
    ID = int(ID)
    rough_spec = load_malin2.f1['binned_spec'][ID, :] + 0 
    rough_err = load_malin2.f1['binned_err'][ID, :] + 0
    # Rough cut to chop off bad pixels
    
    bp = np.where((rough_spec < 0) | (rough_spec > 4))[0]
    
    rough_spec[bp] = 0
    rough_err[bp] = 1e6
    wave = np.exp(load_malin2.f1['wave'])
    bp = np.where((wave > 5565) & (wave < 5590))
    
    rough_spec[bp] = 0
    rough_err[bp] = 1e6
    
    bp = np.where(wave > 5780)
    rough_spec[bp] = 0
    rough_err[bp] = 1e6
    
    if ID == 5:
        bp = np.where(wave > 5770)
        rough_spec[bp] = 0
        rough_err[bp] = 1e6
        
        bp = np.where(wave < 3570)
        rough_spec[bp] = 0
        rough_err[bp] = 1e6
    
    rough_err[0:5] = 1e6
    
    good = np.where(rough_err < 1e6)
    
    spectrum = np.vstack([np.exp(load_malin2.f1['wave'])[good],
                         rough_spec[good]*1e-18,
                         rough_err[good]*1e-18])

    return spectrum.T


def load_ugc(ID):
    if not hasattr(load_ugc, 'f1'):
        load_ugc.f1 = readsav('UGC06614binned.sav')
    # Do some stuff to load up data for the object with the correct ID number
    ID = int(ID)
    rough_spec = load_ugc.f1['binned_spec'][ID, :] + 0 
    rough_err = load_ugc.f1['binned_err'][ID, :] + 0
    # Rough cut to chop off bad pixels
    bp = np.where((rough_spec < 0) | (rough_spec > 4))[0]
    
    rough_spec[bp] = 0
    rough_err[bp] = 1e6
    
    wave = np.exp(load_ugc.f1['wave'])
    good = np.where((3900 < wave) & (wave < 5500) & (rough_err < 1e6) & (rough_spec > 0))[0]
    
    spectrum = np.vstack([np.exp(load_ugc.f1['wave'])[good], rough_spec[good]*1e-18, rough_err[good]*1e-18])
    
    return spectrum.T


def setting():

    # mostly from https://github.com/ACCarnall/bagpipes/blob/master/examples/Example%205%20-%20Fitting%20spectroscopic%20data.ipynb
    dblplaw = {}                        
    dblplaw["tau"] = (0., 15.)            
    dblplaw["alpha"] = (0.01, 1000.)
    dblplaw["beta"] = (0.01, 1000.)
    dblplaw["alpha_prior"] = "log_10"
    dblplaw["beta_prior"] = "log_10"
    dblplaw["massformed"] = (.1, 15.)
    dblplaw["metallicity"] = (0.05, 5.)
    dblplaw["metallicity_prior"] = "log_10"

    nebular = {}
    nebular["logU"] = -3.

    dust = {}
    dust["type"] = "CF00"
    dust["eta"] = 2.
    dust["Av"] = (0., 2.0)
    dust["n"] = (0.3, 2.5)
    dust["n_prior"] = "Gaussian"
    dust["n_prior_mu"] = 0.7
    dust["n_prior_sigma"] = 0.3

    fit_instructions = {}
    fit_instructions["redshift"] = (0.0, 0.1)
    fit_instructions["t_bc"] = 0.01
    #fit_instructions["redshift_prior"] = "Gaussian"
    #fit_instructions["redshift_prior_mu"] = 0.9
    #fit_instructions["redshift_prior_sigma"] = 0.05
    fit_instructions["dblplaw"] = dblplaw 
    fit_instructions["nebular"] = nebular
    fit_instructions["dust"] = dust

    fit_instructions["veldisp"] = (1., 2000.)   #km/s
    fit_instructions["veldisp_prior"] = "log_10"

    calib = {}
    calib["type"] = "polynomial_bayesian"

    calib["0"] = (0.5, 1.5)  # Zero order is centred on 1, at which point there is no change to the spectrum.
    calib["0_prior"] = "Gaussian"
    calib["0_prior_mu"] = 1.0
    calib["0_prior_sigma"] = 0.25

    calib["1"] = (-0.5, 0.5)  # Subsequent orders are centred on zero.
    calib["1_prior"] = "Gaussian"
    calib["1_prior_mu"] = 0.
    calib["1_prior_sigma"] = 0.25

    calib["2"] = (-0.5, 0.5)
    calib["2_prior"] = "Gaussian"
    calib["2_prior_mu"] = 0.
    calib["2_prior_sigma"] = 0.25

    fit_instructions["calib"] = calib

    # XXX--does this actually get passed in?
    mlpoly = {}
    mlpoly["type"] = "polynomial_max_like"
    mlpoly["order"] = 2

    noise = {}
    noise["type"] = "white_scaled"
    noise["scaling"] = (1., 10.)
    noise["scaling_prior"] = "log_10"
    fit_instructions["noise"] = noise

    return fit_instructions


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ugc",
        dest="ugc",
        default=False,
        action="store_true",
    )
    parser.add_argument("--id", type=int, default=0)
    args = parser.parse_args()

    ID_number = args.id
    ugc = args.ugc

    fit_instructions = setting()

    if ugc:
        galaxy = pipes.galaxy(ID_number, load_ugc, photometry_exists=False)
        fit = pipes.fit(galaxy, fit_instructions, run="ugc_%i" % ID_number)

    else:
        galaxy = pipes.galaxy(ID_number, load_malin2, photometry_exists=False)
        fit = pipes.fit(galaxy, fit_instructions, run="malin2_%i" % ID_number)

    fit.fit(verbose=True)
