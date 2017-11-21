# Load one set of data that will be used to create the model
import pandas as pd

from libpysat.spectral.spectral_data import spectral_data

data1 = "G:/.csvfile/full_db_mars_corrected_dopedTiO2_pandas_format.csv"
data1 = spectral_data(pd.read_csv(data1, header=[0, 1], verbose=True))
# Load a second set of data that will serve as the "unknown" (even though in this test case I'm using some known data I had on hand)
data2 = "G:/.csvfile/lab_data_averages_pandas_format.csv"
data2 = spectral_data(pd.read_csv(data2, header=[0, 1], verbose=True))
# Interpolate the "unknown" data to the same wavelengths as the "known" data
data1.interp(data2.df['wvl'].columns)
# Mask out unwanted portions the first data set (example mask files are now included in the "inputs" directory)
maskfile = "G:/.csvfile/mask_minors_noise.csv"
data1.mask(maskfile, maskvar='wvl')
# Apply the same mask to the second data set
maskfile = "G:/.csvfile/mask_minors_noise.csv"
data2.mask(maskfile, maskvar='wvl')
# Normalize the spectra in the first data set so that the sum of each spectrum (from 0-1000 nm) is 1
data1.norm([(0, 1000)], 'wvl')
# Same normalization on the second data set
data2.norm([(0, 1000)], 'wvl')
# Get rid of rows in the first data set that don't have compositions for SiO2 (if you don't do this, it causes problems later on...) For JSC data


# Divide the first data set into 5 folds with similar distributions of SiO2 compositions. Set fold 3 to be used as the test set, use the remaining folds as a training set.
colname = ('comp', 'SiO2')
nfolds = 3
testfold = 2
data1.stratified_folds(nfolds=nfolds, sortby=colname)
data1_train = data1.rows_match(('meta', 'Folds'), [testfold], invert=True)
data1_test = data1.rows_match(('meta', 'Folds'), [testfold])

# Run cross validation for PLS from 1 to 15 components


# Plot the cross validation results as a function of number of components (RMSECV = root mean squared error of cross validation. i.e. how does the model do when each fold is held out in turn and a model is trained with the remaining folds?)

# Overplot the RMSEC results (i.e. how well does the training set predict itself? This tends to always be overly-optimistic)

# Based on these plots, the error stops improving significantly around 8 components, so that's what should be used.
