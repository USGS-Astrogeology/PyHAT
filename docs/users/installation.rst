Installation
============

We assume that you have a default Python environment that is already configured on your computer and you wish to install PySAT into that environment.  If you would like to create a [virtualenv](https://virtualenv.pypa.io/en/stable/) or [conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html) to keep PySAT isolated from your main installation, please follow instructions at the linked resources.

There are two ways that you can install PySAT into your environment.

1. Using Anaconda Python
2. Using Development installation

1. Using Anaconda Python
------------------------

We suggest using [Anaconda Python](https://conda.io/docs/user-guide/install/index.html) and the Anaconda package management system for PySAT.  This installation method lets the Anaconda package manager handle all dependencies (installation of GDAL manually or via `pip` can be challenging).

To install on Windows (64-bit), Linux (64-bit), and Mac OSX::

   conda install -c usgs-astrogeology pysat


Using a Development Installation
--------------------------------

Install the PySAT development version if either you wish to work at the cutting edge (with the associated risks) or you wish to develop for the PySAT project.

Before beginning, uninstall the version of PySAT that you might already have installed::

   conda uninstall pysat

Now clone the PySAT repository::

    git clone https://github.com/USGS-Astrogeology/PySAT

Now checkout the `dev` (development) branch where we actively workon the project::

    git checkout dev

We use a `dev`/`master` model where active work is performed in the `dev` branch and then merged into the `master` branch at release time.  Next, install the necessary dependencies using conda and our `environment.yml` file.::

    cd PySAT
    conda env create -f environment.yml
    source activate libpysat

Finally, install PySAT in development mode using::

    python setup.py develop

This will soft link the PySAT directory (that was previously cloned) into the `<conda_home>/envs/libpysat/lib/python3.x/site-packages` directory.  You are not ready to develop PySAT.

Build Requirements
------------------

Runtime Requirements
--------------------

Optional Requirements
---------------------

* `Jupyter Notebook <http://test-jupyter.readthedocs.io/en/rtd-theme/install.html>' To be able to run our notebook examples
* `Matplotlib <https://github.com/conda-forge/matplotlib-feedstock>` To be able to run the visualizations within the notebook examples
* `nbsphinx <>` For compiling jupyter notebooks in the documentation



Using the QGIS Plugin
---------------------
To be released in 2018.
