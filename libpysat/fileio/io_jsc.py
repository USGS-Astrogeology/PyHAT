import os

import numpy as np
import pandas as pd
from pandas.core.common import array_equivalent

from libpysat.fileio.utils import file_search
from libpysat.spectral.spectral_data import spectral_data


# This function reads the lookup tables used to expand metadata from the file names
# This is separated from parsing the filenames so that for large lists of files the
# lookup tables don't need to be read over and over
#
# Info in the tables is stored in a dict of dataframes so that only one variable
# (the dict) needs to be passed between functions
def read_refdata(LUT_files):
    ID_info = pd.read_csv(LUT_files['ID'], index_col=0)
    spectrometer_info = pd.read_csv(LUT_files['spect'], index_col=0)
    # spectrometer_info.reset_index(inplace=True)
    laser_info = pd.read_csv(LUT_files['laser'], index_col=0)
    # laser_info.reset_index(inplace=True)
    exp_info = pd.read_csv(LUT_files['exp'], index_col=0)
    # exp_info.reset_index(inplace=True)
    sample_info = pd.read_csv(LUT_files['sample'], index_col=0)
    # sample_info.reset_index(inplace=True)
    refdata = {'spect': spectrometer_info, 'laser': laser_info, 'exp': exp_info, 'sample': sample_info, 'ID': ID_info}
    return refdata


# This function parses the file names to record metadata related to the observation
def jsc_filename_parse(filename, refdata):
    filename = os.path.basename(filename)  # strip the path off of the file name
    filename = filename.split('_')  # split the file name on underscores
    libs_ID = filename[0]
    laserID = filename[4][0]
    expID = filename[5]
    spectID = filename[6]

    try:
        sampleID = refdata['ID'].loc[libs_ID].values[0]
        file_info = pd.DataFrame(refdata['sample'].loc[sampleID])
        if file_info.columns.shape[0] < file_info.index.shape[0]:
            file_info = file_info.T
        if file_info.index.shape[0] > 1:
            print('More than one matching row for ' + sampleID + '!')
            tempID = 'Unknown'
            file_info = pd.DataFrame(refdata['sample'].loc[tempID])
            if file_info.columns.shape[0] < file_info.index.shape[0]:
                file_info = file_info.T


    except:
        sampleID = 'Unknown'
        file_info = pd.DataFrame(refdata['sample'].loc[sampleID])
        if file_info.columns.shape[0] < file_info.index.shape[0]:
            file_info = file_info.T

    file_info['Sample ID'] = sampleID
    file_info['LIBS ID'] = libs_ID
    file_info.reset_index(level=0, inplace=True, drop=True)
    file_info['loc'] = int(filename[1])
    file_info['lab'] = filename[2]
    file_info['gas'] = filename[3][0]
    file_info['pressure'] = float(filename[3][1:])

    if laserID in refdata['laser'].index:
        laser_info = pd.DataFrame(refdata['laser'].loc[laserID]).T
        laser_info.index.name = 'Laser Identifier'
        laser_info.reset_index(level=0, inplace=True)
        file_info = pd.concat([file_info, laser_info], axis=1)

    file_info['laser_power'] = float(filename[4][1:])
    if expID in refdata['exp'].index:
        exp_info = pd.DataFrame(refdata['exp'].loc[expID]).T
        exp_info.index.name = 'Exp Identifier'
        exp_info.reset_index(level=0, inplace=True)
        file_info = pd.concat([file_info, exp_info], axis=1)

    file_info['spectrometer'] = spectID
    if spectID in refdata['spect'].index:
        temp = refdata['spect'].loc[spectID]
        temp = [temp[2], temp[4:]]
        spect_info = pd.DataFrame(refdata['spect'].loc[spectID]).T
        spect_info.index.name = 'Spectrometer Identifier'
        spect_info.reset_index(level=0, inplace=True)
        file_info = pd.concat([file_info, spect_info], axis=1)

    return file_info


def JSC(input_files, refdata):
    try:
        # read the first file
        data = pd.read_csv(input_files[0], skiprows=14, sep='\t', engine='c')
        data = data.rename(columns={data.columns[0]: 'time1', data.columns[1]: 'time2'})
        metadata = pd.concat([jsc_filename_parse(input_files[0], refdata)] * len(data.index))
        metadata.drop('spectrometer', axis=1, inplace=True)

        # read the next files and merge them with the first
        for file in input_files[1:]:
            datatemp = pd.read_csv(file, skiprows=14, sep='\t', engine='c')
            datatemp = datatemp.rename(columns={datatemp.columns[0]: 'time1', datatemp.columns[1]: 'time2'})
            data = data.merge(datatemp)

        time = data[['time1', 'time2']]  # split the two time columns from the data frame
        data.drop(['time1', 'time2'], axis=1, inplace=True)  # trim the data frame so it is just the spectra

        # make a multiindex for each wavlength column so they can be easily isolated from metadata later
        data.columns = [['wvl'] * len(data.columns), np.array(data.columns.values, dtype='float').round(4)]

        metadata.index = data.index
        metadata = pd.concat([metadata, time], axis=1)
        compcols = ['SiO2', 'TiO2', 'Al2O3', 'Cr2O3', 'Fe2O3T', 'MnO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5',
                    'SO3 LOI Residue', 'Total', 'Total Includes', '%LOI', 'FeO',
                    'Fe2O3', 'SO3 Actual', 'Fe(3+)/Fe(Total)', 'Rb (ug/g)', 'Sr (ug/g)', 'Y (ug/g)', 'Zr (ug/g)',
                    'V (ug/g)', 'Ni (ug/g)', 'Cr (ug/g)',
                    'Nb (ug/g)', 'Ga (ug/g)', 'Cu (ug/g)', 'Zn (ug/g)', 'Co (ug/g)', 'Ba (ug/g)', 'La (ug/g)',
                    'Ce (ug/g)', 'U (ug/g)', 'Th (ug/g)', 'Sc (ug/g)',
                    'Pb (ug/g)', 'Ge (ug/g)', 'As (ug/g)', 'Cl (ug/g)']
        compdata = metadata[compcols]
        metadata.drop(compcols, axis=1, inplace=True)
        metadata.columns = [['meta'] * len(metadata.columns), metadata.columns.values]
        compdata.columns = [['comp'] * len(compdata.columns), compdata.columns.values]
        data = pd.concat([data, metadata, compdata], axis=1)

        data[('meta', 'Scan #')] = data.index
        data.set_index(('meta', 'time2'), drop=False, inplace=True)

        return data
    except:
        print('Problem reading:' + input_file)
        print('Moving to Problem_Files')
        os.rename(input_file,
                  r"C:\\Users\\rbanderson\\Documents\\Projects\\LIBS PDART\\Database\\LIBS USGS\\Problem_Files\\" + os.path.basename(
                      input_file))
        return None


def jsc_batch(directory, LUT_files, searchstring='*.txt', to_csv=None):
    # Read in the lookup tables to expand filename metadata
    refdata = read_refdata(LUT_files)
    # get the list of files that match the search string in the given directory
    filelist = file_search(directory, searchstring)
    spectIDs = []  # create an empty list to hold the spectrometer IDs
    libsIDs = []
    timestamps = []
    locs = []
    for file in filelist:
        filesplit = os.path.basename(file).split('_')
        spectIDs.append(filesplit[6])  # get the spectrometer IDs for each file in the list
        libsIDs.append(filesplit[0])
        timestamps.append(filesplit[-1].split('.')[0])
        locs.append(filesplit[1])
    spectIDs_unique = np.unique(spectIDs)  # get the unique spectrometer IDs
    libsIDs_unique = np.unique(libsIDs)
    dfs = []  # create an empty list to hold the data frames for each spectrometer

    # loop through each LIBS ID
    alldata = []
    for ID in libsIDs_unique:
        print('Working on : ' + str(ID))
        sublist = filelist[np.in1d(libsIDs, ID)]
        locs = []
        for file in sublist:
            locs.append(os.path.basename(file).split('_')[1])
        locs_unique = np.unique(locs)
        # loop through each location for that libs ID
        for loc in locs_unique:
            print(loc)
            sub_sublist = sublist[np.in1d(locs, loc)]  # get the files for that LIBSID and location
            data = JSC(sub_sublist, refdata)
            alldata.append(data)
            pass

    combined = pd.concat(alldata)
    if to_csv is not None:
        print('Writing combined data to: ' + to_csv)
        combined.to_csv(to_csv)
    return spectral_data(combined)


# got this function from stack overflow: http://stackoverflow.com/questions/14984119/python-pandas-remove-duplicate-columns
# it's slow but doesn't crash python like combined.T.drop_duplicates().T does in some cases with very large sets of data
def duplicate_columns(frame):
    groups = frame.columns.to_series().groupby(frame.dtypes).groups
    dups = []

    for t, v in groups.items():

        cs = frame[v].columns
        vs = frame[v]
        lcs = len(cs)

        for i in range(lcs):
            ia = vs.iloc[:, i].values
            for j in range(i + 1, lcs):
                ja = vs.iloc[:, j].values
                if array_equivalent(ia, ja):
                    dups.append(cs[i])
                    break

    return dups
