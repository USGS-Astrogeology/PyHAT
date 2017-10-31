# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 12:29:20 2014

@author: rbanderson
"""

import matplotlib.pyplot as plot
import pandas as pd

from libpysat.spectral.spectral_data import spectral_data

# import mlpy.wavelet

filename = r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Sample_Data\JSC_data_combined_20170307.csv"
data = spectral_data(pd.read_csv(filename, header=[0, 1]))
data = data.df.ix[0:5]
colcheck = data_spect.columns.values < 350
data_spect = data_spect.iloc[:, colcheck]
data = spectral_data(data_spect)
data.remove_baseline(method='ccam', params={'int_flag_': 2, 'lvmin_': 6, 'lv_': 10})
x = data.df.columns.values
plot.figure(figsize=[11, 8])
plot.plot(x, data_orig, label='Original', linewidth=0.5)
plot.plot(x, data.df.iloc[0], label='Continuum Removed', linewidth=0.5)
plot.plot(x, data.df_baseline.iloc[0], label='Continuum', linewidth=0.5)
plot.legend()
plot.savefig('cont_test.png', dpi=1000)
plot.show()

# plot.figure(figsize=[11,8])
# plot.plot(x,data.df_baseline['wvl'].iloc[0]-data2['data_cont'])
# plot.savefig('cont_diff.png',dpi=400)
# plot.show()

pass
