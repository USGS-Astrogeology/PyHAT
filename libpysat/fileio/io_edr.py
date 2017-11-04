import os

import numpy as np
import pandas as pd


def EDR(input_file):
    f = open(input_file, 'rb')  # read as bytes so python won't complain about the binary part of the file

    # read lines of the header until reaching the end of the libs table (collecting other metadata along the way)
    end_of_libs_table = False
    while end_of_libs_table is False:
        line = str(f.readline(), 'utf-8').replace('\r', '').replace('\n',
                                                                    '')  # convert the current line to a string and get rid of newline characters
        line = line.split('=')  # split the line on equals sign if present
        # look for the name of the value we want, if the current line has it, then set the value
        if 'RECORD_BYTES' in line[0]:
            rbytes = int(line[1])
        if 'LABEL_RECORDS' in line[0]:
            lrecs = int(line[1])
        if 'SPACECRAFT_CLOCK_START_COUNT' in line[0]:
            sclock = int(line[1].replace('"', '').split('.')[0])
        if 'SEQUENCE_ID' in line[0]:
            seqID = line[1].replace('"', '')
        if 'INSTRUMENT_FOCUS_DISTANCE' in line[0]:
            focus_dist = int(line[1])

        if 'INSTRUMENT_TEMPERATURE' in line[0]:
            instrument_temps = line[1] \
                               + str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '') \
                               + str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '') \
                               + str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '')
            instrument_temps = [float(i) for i in
                                instrument_temps.replace('<degC>', '').replace('(', '').replace(')', '').replace(' ',
                                                                                                                 '').split(
                                    ',')]
            instrument_temps_name = str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '')
            instrument_temps_name = instrument_temps_name.split('=')[1] \
                                    + str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '') \
                                    + str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '') \
                                    + str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '') \
                                    + str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '')
            instrument_temps_name = instrument_temps_name.replace(' ', '').replace('(', '').replace(')', '').replace(
                '"', '').split(',')
            f.readline()
            pass
        try:
            if 'CCAM_LIBS_DATA_CONTAINER' in line[1]:
                nshots = int(str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '').split('=')[1])
                start_byte = int(str(f.readline(), 'utf-8').replace('\r', '').replace('\n', '').split('=')[1])
            if 'END_OBJECT' in line[0] and 'CCAM_LIBS_TABLE' in line[1]:
                end_of_libs_table = True
        except:
            pass

    f.close()

    header_skip = lrecs * rbytes  # calculate the number of header bytes to skip to get to the real data

    with open(input_file, "rb") as f:
        f.seek(header_skip + start_byte - 1, 0)
        spectra = []
        while spectra.__len__() < nshots:
            spectrum = []
            while spectrum.__len__() < 6444:
                spectrum.append(int.from_bytes(f.read(2), byteorder='big', signed=False))
            spectra.append(spectrum)
    spectra = np.array(spectra, dtype='int')
    cols = np.array(list(range(spectra.shape[1]))) + 1
    cols = [('channel', i) for i in cols]
    inds = np.array(list(range(spectra.shape[0]))) + 1
    sp = pd.DataFrame(spectra, columns=pd.MultiIndex.from_tuples(cols), index=inds)
    sp[('meta', 'EDR_file')] = os.path.basename(input_file)
    sp[('meta', 'Spacecraft_Clock')] = sclock
    sp[('meta', 'Shot')] = sp.index
    sp[('meta', 'SeqID')] = seqID
    sp[('meta', 'Focus_Distance')] = focus_dist
    for ind, name in enumerate(instrument_temps_name):
        sp[('meta', name + '_temp')] = instrument_temps[ind]
    sp.to_csv('test.csv')
    return sp
