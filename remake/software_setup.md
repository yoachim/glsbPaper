Noting how I setup python

conda create -n glsb
conda activate glsb
conda install numpy matplotlib

python -m pip install fsps
python -m pip install astro-sedpy
python -m pip install astro-prospector

export SPS_HOME="/path/where/you/want/to/download/fsps"
git clone https://github.com/cconroy20/fsps.git $SPS_HOME

conda install emcee
pip install dynesty
