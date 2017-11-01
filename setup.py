from setuptools import setup, find_packages
from os import path
import libpysat

VERSION = libpysat.__version__
here = path.abspath(path.dirname(__file__))

# TODO PyPi requires a README.rst file, not a README.md
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name="libpysat",
    version=VERSION,
    author="Jay Laura",
    author_email="jlaura@usgs.gov",
    description="A tool to extract Spectral Profiler data and visualize the resultant spectra",
    # long_description=long_description,
    url="https://github.com/USGS-Astrogeology/PySAT",
    license="Public Domain",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: Public Domain",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords="planetary io",
    packages=(
        'libpysat',
        'libpysat.examples',
        'libpysat.fileio',
        'libpysat.fileio.tests',
        'libpysat.plotting',
        'libpysat.regression',
        'libpysat.spectral',
        'libpysat.spectral.baseline_code',
        'libpysat.spectral.tests',
        'libpysat.utils',
        'libpysat.utils.tests'
    ), install_requires=['pandas', 'numpy', 'scipy', 'pvl', 'matplotlib', 'sklearn']
)
