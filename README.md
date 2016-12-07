[![Build Status](https://travis-ci.org/USGS-Astrogeology/PySAT.svg?branch=master)](https://travis-ci.org/USGS-Astrogeology/PySAT)
[![Coverage Status](https://coveralls.io/repos/github/USGS-Astrogeology/PySAT/badge.svg?branch=master)](https://coveralls.io/github/USGS-Astrogeology/PySAT?branch=master)
# Installation

  - Click and download [Anaconda Python 4.1.1](https://repo.continuum.io/archive/Anaconda3-4.1.1-Windows-x86.exe).  The pysat package and UI has been designed specifically with 4.1.1. Newer versions of Anaconda breaks this package. 
  - If you're using a non-Windows machine go to Anaconda's [download page](https://www.continuum.io/downloads) and pick up the 4.1.1 package
  - Download or clone this repository
  - `cd` into this repository and execute `conda env create`.  This will read the `environment.yml` file and install (using conda) all dependencies in a self-contained environment.
  - `source activate pysat` to activate said environment.
  
# Demo

  - Execute the `jupyter notebook` that will open a new browser tab with the Jupyter homepage.
  - Launch (click) the `Kaguya_Spectral_Profiler.ipynb` notebook.



# PYSAT UI in C++
![PYSAT](https://github.com/tisaconundrum2/PySAT/blob/master/src/installer/splash.png)  
- This program was compiled in C++ it's backend does not rely on python
This was done for rapid protoyping purposes.
Please note that this is not a functional version of PYSAT.
It is a prototype and only displays what we want to accomplish in a working UI

- Download the installer in this path: [\PYSAT\src\installer](https://github.com/tisaconundrum2/PySAT/tree/master/src/installer) and click on the installer.
- choose where you'd like to run it. Click on [PYSatGuiII.exe](#pysat-ui)
- move qwindows.dll to ./platforms/ 
- if the folder "platforms" doesn't exist make it.

# PYSAT UI in Python

- This version of PYSAT has a backend that has been created in Python.
- This version is being built to work as close to the original libraries as physically possible

Current Road Ahead
- [x] Working Modules on UI
- [x] Selecting functions from Menubar adds functions dynamically
- [x] Shortcuts such as Ctrl S to save
- [ ] Embedded Plots and Graphs from data collected
- [x] ~~Package all python packages: sklearn, scipy, numpy, matplotlib, pysat for user consumption~~ It has been discovered that the user can download Anaconda, and run our files as normal.
- [ ] Add ability to save plots in personal files
- [ ] Add ability to save state of GUI, i.e. all number that user inputs will be there again after closing GUI
- [ ] Add ability to save data frame at any point in the workflow 
- [ ] Setup a way to select points on a scatter plot.

## Control Flow

![PYSAT](https://github.com/tisaconundrum2/PySAT/blob/master/src/installer/Flowchart.png)

- The user begins by starting PYSAT_MAIN.
- PYSAT_MAIN will begin by loading the splash screen and all necessary UI pieces
- PYSAT_MAIN will then forward control to PYSAT_UI
- PYSAT_UI displays the mainframe in which the UI's submodules will be loaded into
- PYSAT_UI will then foward control to each submodule of focus
- Each submodule builds the collective UI library
- Each submodule fowards control to PYAT_FUNC which holds all the necessary logic functions
- These logic functions then forward commands to the various PYSAT and Anaconda libraries
- The values are then returned back up to PYSAT_FUNC which will then deal with changed data
