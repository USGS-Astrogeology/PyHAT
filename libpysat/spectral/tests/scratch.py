from libpysat.fileio import io_ccam_pds
import libpysat.spectral.spectral_data as sd
import pandas as pd
import numpy as np

path=r"C:\Users\rbanderson\Desktop\test_data\pdl"
db=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Sample_Data\full_db_mars_corrected_dopedTiO2_pandas_format.csv"
data=io_ccam_pds.ccam_batch(path,'*CCS*.SAV',ave=True)
#data.peak_area()
db=sd.spectral_data(pd.read_csv(db, header=[0, 1]))
db.peak_area()

pass