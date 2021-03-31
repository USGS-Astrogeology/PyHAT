import numpy as np
import pandas as pd
from pysptools.noise import MNF as mnf
from libpyhat import Spectra

class MNF():
    def __init__(self, n_components = 4):
        self.n_components = n_components

    def fit_transform(self,data):
        '''
        Description: Minimum Noise Fraction (MNF) wrapper for pysptools implementation
        Rationale: Removes noise while preserving information
        '''
        # Convert Series to ndarray
        if issubclass(type(data), pd.Series) or isinstance(data, Spectra) or issubclass(type(data), pd.DataFrame):
            np_data = data.to_numpy()
        elif issubclass(type(data), np.ndarray):
            np_data = data
        else:
            raise ValueError("Input for MNF must inherit from pd.Series or np.ndarray")
    
        cube_data, num_dimensions = make_3d(np_data)
    
        # Open and apply MNF module
        pysp_mnf = mnf()
        res = pysp_mnf.apply(cube_data)
        res_spect = pysp_mnf.inverse_transform(res)
        components = pysp_mnf.get_components(self.n_components)
        # Return result in dimensionality of input
        if num_dimensions == 2:
            return np.squeeze(components), np.squeeze(res_spect)
        else:
            return components, res_spect
    
def make_3d(data):
    # Ensure 3 dimensional input for MNF
    num_dimensions = len(data.shape)
    if num_dimensions == 2:
        # Add arbitrary 3rd dimension
        cube_data = np.expand_dims(data, axis=0)
    elif num_dimensions == 3:
        cube_data = data
    else:
        raise ValueError("Input must be 2 or 3 dimensional")
    return cube_data, num_dimensions


