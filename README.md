
## Status

| OS    | Status |
|-------|--------|
| OSX   | [![Build Status](https://travis-ci.org/USGS-Astrogeology/PySAT.svg?branch=dev)](https://travis-ci.org/USGS-Astrogeology/CSM-CyCSM) |
|Linux  | [![Build Status](https://travis-ci.org/USGS-Astrogeology/PySAT.svg?branch=dev)](https://travis-ci.org/USGS-Astrogeology/CSM-CyCSM) |
|Windows| [![Build status](https://ci.appveyor.com/api/projects/status/orfb1txhicspo7ap/branch/dev?svg=true)](https://ci.appveyor.com/project/jlaura/pysat/branch/dev)|


[![Coverage Status](https://coveralls.io/repos/github/USGS-Astrogeology/PySAT/badge.svg?branch=dev)](https://coveralls.io/github/USGS-Astrogeology/PySAT?branch=dev)
[![Join the chat at https://gitter.im/USGS-Astrogeology/PySAT](https://badges.gitter.im/USGS-Astrogeology/PySAT.svg)](https://gitter.im/USGS-Astrogeology/PySAT?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# Installation - For Users
  - Install [Anaconda Python](https://www.continuum.io/downloads).  Be sure to get Python 3.x
  - Create a conda env for PySAT: `conda create -n pysat`
  - Add conda forge to your channels list: `conda config --add channels conda-forge`
  - Activate the PySAT environment: `source activate pysat` (for windows: `activate pysat`)
  - To install: `conda install -c usgs-astrogeology pysat`

# Installation - For Developers
  - Install [Anaconda Python](https://www.continuum.io/downloads).  Be sure to get Python 3.x
  - Add conda forge to your channels list: `conda config --add channels conda-forge`
  - Clone this repo: `git clone https://github.com/USGS-Astrogeology/PySAT`
  - Enter the cloned repo: `cd PySAT`
  - Pull the `dev` branch: `git fetch && git checkout dev`
  - Install the dependencies: `conda create -f environment.yml`
  
# Demo

  - Execute the `jupyter notebook` that will open a new browser tab with the Jupyter homepage.
  - Launch (click) the `Kaguya_Spectral_Profiler.ipynb` notebook.

