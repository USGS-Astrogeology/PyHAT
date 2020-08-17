import numpy as np
import pandas as pd

from pysptools.eea import FIPPI, PPI, NFINDR, ATGP
from libpyhat.data.spectra import Spectra

def emi(data, emi_method, **kwargs):
    supported_methods = ("FIPPI", "PPI", "NFINDR", "ATGP")
    try:
        if emi_method.upper() in supported_methods:
            method = globals()[emi_method.upper()]()
        else:
            print(f"{emi_method} is not a supported method.  Supported methods are {supported_methods}")
            return 1
    except KeyError:
        print(f"Unable to instantiate class from {emi_method}.")
        return 1

    spectra = data['wvl'].to_numpy()
    if len(spectra.shape) == 2:
        spectra = np.expand_dims(spectra, 0)

    endmembers = method.extract(spectra, **kwargs)
    endmember_indices = [i[0] for i in method.get_idx()]
    indices = np.zeros(spectra.shape[1], dtype=int)
    indices[endmember_indices] = 1
    data[("endmembers", emi_method)] = indices
    return endmember_indices
