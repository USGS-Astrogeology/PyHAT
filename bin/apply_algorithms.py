import inspect
import numpy as np
import argparse

from unittest import mock
from plio.io import io_moon_minerology_mapper as iomm
from plio.io.io_gdal import array_to_raster
from libpysat.derived import pipe, supplemental, new, crism
from plio.io.io_moon_minerology_mapper import open as m3_open
from plio.io.io_crism import open as crism_open
import os

def parse_args():
    parser = argparse.ArgumentParser()

    # Add args here
    parser.add_argument('module', help='Module of which you want to run algorithms (m3 or crism)')
    parser.add_argument('image', type=str, help='Full path to M3 or CRISM image img_tiff')
    parser.add_argument('filepath', type=str, help='Directory to write tiffs produced.')

    return parser.parse_args()

def run_algos(module, img, filepath, crism=False):
    """
    Parameters
    ----------
    module : Name of python module you want to run functions out of

    img : Full path to M3 image img_tiff

    filepath: Path to where you want the new tiffs to be generated

    Returns
    -------
     : tiff image
    """
    # Grabs all functions in a module
    package_funcs = inspect.getmembers(module)


    if crism:
        img_tiff = crism_open(img)
    # Makes a readable img

    else:
        img_tiff = m3_open(img)

    not_called = []
    for function in package_funcs:
        # If a callable function, call it with the img specified above
        if callable(function[1]) and not function[0].endswith('__'):
            try:
                # Converts array to tiff
                # Writes new img to tiff using the image name and function name
                array_to_raster(function[1](img_tiff), filepath + str(img).split('/')[-1].split('.')[0] + '_' + str(function[0]) + '.tiff',  bittype='GDT_Float32')
            except:
                not_called.append(function[0])
                continue

    # Keeps track of which functions are and are not called
    if not_called:
        print('\nThese functions were not called in {} : {}'.format(module, not_called))
    else:
        print('\nAllfunctions were called in {}.'.format(module))

def main(args):
    # List of modules (algorithms) you want to run and output tiffs
    m3_module_list = [pipe, new, supplemental]
    crism_module_list = [crism]

    # Path of image file to which you want to run the algorithms on (passed in)
    img = args.image

    # Path to where you want to store new tiffs (passed in)
    new_img_path = args.filepath

    if args.module == 'm3':

        # Calls all functions in module_list
        for module in m3_module_list:
            run_algos(module, img, new_img_path)

    if args.module == 'crism':

        # Calls all functions in module_list
        for module in crism_module_list:
            run_algos(module, img, new_img_path, crism=True)

if __name__ == '__main__':
    main(parse_args())
