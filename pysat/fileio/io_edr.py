import csv

import numpy as np
import pandas as pd

from pysat.fileio.header_parser import header_parser


class io_edr_reader():
    def __init__(self, input_data):
        self.input_data = input_data
        self.start_byte = 0
        self.end_byte = 0

    def EDR(self):
        with open(self.input_data, 'r') as f:
            header = {}
            for i, row in enumerate(f.readlines()):

                if i < 2 or i == 28:
                    pass
                elif i < 28:
                    header.update(header_parser(row, ':'))  # read the header values into a dict
                elif i == 29:
                    row = row.split()
                    shotnums = list(range(1, len(row) + 1))
                    shots = ['shot' + str(i) for i in shotnums]

        df = pd.read_csv(self.input_data, sep='    ', skiprows=29, names=shots)
        df = df.transpose()
        # insert the header metadata as columns
        for label, data in header.items():
            df[label] = data
        return df

    def getHeaderInformation(self):
        objectData = ["NAME", "REPETITIONS", "START_BYTE", "BYTES", "DESCRIPTION", "OBJECT", "NAME", "DATA_TYPE",
                      "START_BYTE", "BYTES", "ITEMS", "ITEM_BYTES", "DESCRIPTION"]
        f = open(self.input_data, 'r')  # read each line and find where the libs data is.
        content = f.readline()
        while "CCAM_LIBS_DATA_CONTAINER" not in content:     # this loop will get us to where our data is
            content = f.readline()                           # update the content for the while loop
        while "END_OBJECT" not in content:                   # continue going through file as long as we haven't hit the end
            for item in objectData:                          # check to see what the content is.
                if item in content:                          #

                    header = {}
        header.update()

    def seekPastHeader(self):
        pass

    def readInFile(self):
        f = open(self.file, "rb")
        data = np.fromfile(f, dtype=np.uint16)
        data = data.byteswap()
        data = data / 1000
        return data

    def toCSVFile(self, file, data):
        out = []
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            i = 0
            while i < len(data) - 1:
                i += 1
                out.append(data[i])
                mod_ = 30
                if i % mod_ == 0 and i >= mod_:
                    print(out)
                    writer.writerow(out)
                    out = []


read = io_edr_reader("cl5_398736801edr_f0030004ccam01014m1.dat")
read.getHeaderInformation()