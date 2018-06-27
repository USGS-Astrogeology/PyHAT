import inspect
import numpy as np

from unittest import mock

from plio.io import io_moon_minerology_mapper as iomm
from libpysat.derived import pipe, supplemental, new, crism
from tests.derived.m3 import conftest

def run_algos(module):
    package_funcs = inspect.getmembers(module)
    img = conftest.m3_img()
    not_called = []
    for function in package_funcs:
        if callable(function[1]) and not function[0].endswith('__'):
            try:
                function[1](img)

            except:
                not_called.append(function[0])
                continue

    print('\nThese functions were not called in {} : {}'.format(module, not_called))

if __name__ == '__main__':
    module_list = [pipe, new, supplemental, crism]
    for module in module_list:
        run_algos(module)
