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


---------------

OK, I'm leaning more towards bagpipes now. Let's see if we can install that

conda activate glsb
pip install bagpipes

uuugh, need to update macports. Which needs new xcode. Fantastic.


This seemed to install gfortran properly:
sudo port install gcc11 +gfortran; sudo port select --set gcc mp-gcc11

This gets multinest to compile:
cmake -DCMAKE_C_COMPILER=/opt/local/bin/x86_64-apple-darwin21-gcc-11.2.0 -DCMAKE_CXX_COMPILER=/opt/local/bin/x86_64-apple-darwin21-g++-mp-11  ..
make
sudo make install

Looks like that installs at: /usr/local/bin/


-----------

Need to do again for new M2 laptop. Probably going to try homebrew this time.

conda activate glsb
pip install bagpipes

brew install gcc
brew install cmake
brew install open-mpi
pip install mpi4py
conda install -c conda-forge jupyter

export DYLD_LIBRARY_PATH="/opt/homebrew/lib"

cmake -DCMAKE_C_COMPILER=/opt/homebrew/bin/gcc-13 -DCMAKE_Fortran_COMPILER=/opt/homebrew/bin/gfortran -DCMAKE_CXX_COMPILER=/opt/homebrew/bin/g++-13 ..

make
sudo make install

