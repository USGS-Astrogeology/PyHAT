import pandas as pd
from libpyhat.transform.interp import interp

def shift_spect(df,shift):
    """This function takes a data frame containing spectra and shifts them by a specified amount.

    Arguments:
    df = The data frame. Spectra should be stored in rows, with each column having a multi-indexed column name. The
        top level should be 'wvl', the second level should be a floating point value indicating the wavelength.
    shift = The amount by which the spectra should be shifted. """

    wvls = df['wvl'].columns.values #get the original wavelength values
    df_spect = df['wvl'] #extract just the spectra from the data frame
    df = df.drop('wvl',axis=1) #keep all non-spectral information in df
    newcols = [('wvl',i+shift) for i in df_spect.columns.values] #add the shift amount to the wavelengths
    df_spect.columns = pd.MultiIndex.from_tuples(newcols) #replace the original column names with the new, shifted ones
    df = pd.concat([df_spect, df], axis=1) #recombine the spectra with any other data from the original data frame
    df = interp(df,wvls) #interpolate the shifted data back onto the original set of wavelengths
    df[('meta','Shift')] = shift #record the amount of shift applied as a metadata column
    return df
