
import pandas as pd
from pysat.fileio.header_parser import header_parser

def EDR(input_data):
    with open(input_data, 'r') as f:
        header={}
        for i, row in enumerate(f.readlines()):
            
            if i<2 or i==28:
                pass
            elif i<28:
                header.update(header_parser(row,':')) #read the header values into a dict
            elif i==29:
                row=row.split()
                shotnums=list(range(1,len(row)+1))
                shots=['shot'+str(i) for i in shotnums]

    df = pd.read_csv(input_data, sep='    ',skiprows=29,names=shots)        
    df=df.transpose()
            #insert the header metadata as columns
    for label,data in header.items(): 
        df[label]=data
    return df
          
          
                    
