from setuptools import setup, find_packages
from os import path
import pysat

VERSION = pysat.__version__
here = path.abspath(path.dirname(__file__))

# TODO PyPi requires a README.rst file, not a README.md
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name="PYSAT",
    version=VERSION,
    author="Jay Laura",
    author_email="jlaura@usgs.gov",
    description="TODO Add description...",
    # long_description=long_description,
    url="https://github.com/USGS-Astrogeology/PySAT",
    license="Public Domain",
    extras_requires=[
        'copy',
        'cvxopt',
        'fnmatch',
        'functools',
        'glob',
        'itertools',
        'json',
        'matplotlib',
        'numpy',
        'osgeo',
        'pandas',
        'pickle',
        'pvl',
        'PyQt5',
        'pysat',
        'pywt',
        'scipy',
        'shutil',
        'sklearn',
        'tempfile',
        'time',
        'unittest',
        'warnings',
        'yaml'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Spectral Analysis",
        "License :: Public Domain",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords="planetary io",
    packages=(
        'pysat',
        'pysat.examples',
        'pysat.fileio',
        'pysat.fileio.tests',
        'pysat.plotting',
        'pysat.regression',
        'pysat.spectral',
        'pysat.spectral.baseline_code',
        'pysat.spectral.tests',
        'pysat.utils',
        'pysat.utils.tests'
    ),
)
