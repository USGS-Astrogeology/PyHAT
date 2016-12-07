# This code is used to read individual ChemCam CCS files
# Header data is stored as attributes of the data frame
# White space is stripped from the column names
import os
import numpy as np
import pandas as pd
import scipy
from pysat.fileio.utils import file_search
from pysat.fileio.lookup import lookup
from pysat.spectral.spectral_data import spectral_data
import time

def CCS(input_data):
    t=time.time()
    
    try:
        df = pd.read_csv(input_data, header=14,engine='c')
        cols=list(df.columns.values)
        df.columns=[i.strip().replace('# ','') for i in cols] #strip whitespace from column names
        df.set_index(['wave'],inplace=True) #use wavelengths as indices
        #read the file header and put information into the dataframe as new columns
        metadata=pd.read_csv(input_data,sep='=',nrows=14,comment=',',engine='c',index_col=0,header=None)
    
    except: #handle files with an extra header row containing temperature
        df = pd.read_csv(input_data, header=15,engine='c')
        cols=list(df.columns.values)
        df.columns=[i.strip().replace('# ','') for i in cols] #strip whitespace from column names
        df.set_index(['wave'],inplace=True) #use wavelengths as indices
        #read the file header and put information into the dataframe as new columns
        metadata=pd.read_csv(input_data,sep='=',nrows=15,comment=',',engine='c',index_col=0,header=None)
    
    df.index=[['wvl']*len(df.index),df.index.values.round(4)]  #create multiindex so spectra can be easily extracted with a single key
    df=df.T   #transpose so that each spectrum is a row
           
    #remove extraneous stuff from the metadataindices    
    metadata.index=[i.strip().strip('# ').replace(' FLOAT','').lower() for i in metadata.index.values]
    metadata=metadata.T
    
     #extract info from the file name
    fname=os.path.basename(input_data)
    metadata['sclock']=fname[4:13]
    metadata['seqid']=fname[25:34].upper()
    metadata['Pversion']=fname[34:36]   
    
    dt=time.time()-t
    t=time.time()
    #duplicate the metadata for each row in the df
    metadata=metadata.append([metadata]*(len(df.index)-1),ignore_index=True)    
    metadata.index=df.index #make the indices match
    metadata.columns=[['meta']*len(metadata.columns),metadata.columns.values] #make the columns into multiindex
    df=pd.concat([metadata,df],axis=1) #combine the spectra with the metadata
    dt2=time.time()-t
    return df
        
def CCS_SAV(input_data,ave=True):
        
    #read the IDL .SAV file
    data=scipy.io.readsav(input_data,python_dict=True)
    
    #put the spectra into data frames and combine them
    df_UV=pd.DataFrame(data['uv'],index=data['defuv'])
    df_VIS=pd.DataFrame(data['vis'],index=data['defvis'])
    df_VNIR=pd.DataFrame(data['vnir'],index=data['defvnir'])
    df_spect=pd.concat([df_UV,df_VIS,df_VNIR])
    df_spect.columns=['shot'+str(i+1) for i in df_spect.columns] #add 1 to the columns so they correspond to shot number
    
    df_aUV=pd.DataFrame(data['auv'],index=data['defuv'],columns=['average'])
    df_aVIS=pd.DataFrame(data['avis'],index=data['defvis'],columns=['average'])
    df_aVNIR=pd.DataFrame(data['avnir'],index=data['defvnir'],columns=['average'])
    df_ave=pd.concat([df_aUV,df_aVIS,df_aVNIR])
    
    df_mUV=pd.DataFrame(data['muv'],index=data['defuv'],columns=['median'])
    df_mVIS=pd.DataFrame(data['mvis'],index=data['defvis'],columns=['median'])
    df_mVNIR=pd.DataFrame(data['mvnir'],index=data['defvnir'],columns=['median'])
    df_med=pd.concat([df_mUV,df_mVIS,df_mVNIR])            
    
    df=pd.concat([df_spect,df_ave,df_med],axis=1)
    #create multiindex to access wavelength values
    #also, round the wavlength values to a more reasonable level of precision
    df.index=[['wvl']*len(df.index),df.index.values.round(4)]
    #transpose so that spectra are rows rather than columns   
    df=df.T
    
    #extract metadata from the file name and add it to the data frame
    #use the multiindex label "meta" for all metadata

    fname=os.path.basename(input_data)

    #for some reason, some ChemCam files have the 'darkname' key, others call it 'darkspect'
    #this try-except pair converts to 'darkname' when needed
    try:
        data['darkname']
    except:
        data['darkname']=data['darkspec']
        
    metadata=[fname,
              fname[4:13],
              fname[25:34].upper(),
              fname[34:36],
              data['continuumvismin'],
              data['continuumvnirmin'],
              data['continuumuvmin'],
              data['continuumvnirend'],
              data['distt'],
              data['darkname'],
              data['nshots'],
              data['dnoiseiter'],
              data['dnoisesig'],
              data['matchedfilter']]
    metadata=np.tile(metadata,(len(df.index),1))
    metadata_cols=list(zip(['meta']*len(df.index),['file',
                   'sclock',
                   'seqid',
                   'Pversion',
                   'continuumvismin',
                   'continuumvnirmin',
                   'continuumuvmin',
                   'continuumvnirend',
                   'distt',
                   'dark',
                   'nshots',
                   'dnoiseiter',
                   'dnoisesig',
                   'matchedfilter']))
    metadata=pd.DataFrame(metadata,columns=pd.MultiIndex.from_tuples(metadata_cols),index=df.index) 

    df=pd.concat([metadata,df],axis=1)            
    if ave==True:
        df=df.loc['average']
        df=df.to_frame().T
    else:
        pass
                  
    return df    

def ccs_batch(directory,searchstring='*CCS*.csv',is_sav=False,to_csv=None,lookupfile=None,ave=True):
    #Determine if the file is a .csv or .SAV
    if 'SAV' in searchstring:
        is_sav=True
    else:
        is_sav=False
    filelist=file_search(directory,searchstring)
    basenames=np.zeros_like(filelist)
    sclocks=np.zeros_like(filelist)
    P_version=np.zeros_like(filelist,dtype='int')
    
    #Extract the sclock and version for each file and ensure that only one 
    #file per sclock is being read, and that it is the one with the highest version number
    for i,name in enumerate(filelist):
        basenames[i]=os.path.basename(name)
        sclocks[i]=basenames[i][4:13] #extract the sclock
        P_version[i]=basenames[i][-5:-4] #extract the version
    sclocks_unique=np.unique(sclocks) #find unique sclocks
    filelist_new=np.array([],dtype='str')
    for i in sclocks_unique:
        match=(sclocks==i) #find all instances with matching sclocks
        maxP=P_version[match]==max(P_version[match])  #find the highest version among these files
        filelist_new=np.append(filelist_new,filelist[match][maxP]) #keep only the file with thei highest version
        
    filelist=filelist_new
    #Should add a progress bar for importing large numbers of files    
    dt=[]
    for i in filelist:
        print(i)
        if is_sav:
            t=time.time()
            tmp=CCS_SAV(i,ave=ave)
            dt.append(time.time()-t)
        else:
            t=time.time()
            tmp=CCS(i)
            
            dt.append(time.time()-t)
        if i==filelist[0]:
            combined=tmp
            
        else:
            #This ensures that rounding errors are not causing mismatches in columns            
            cols1=list(combined['wvl'].columns)
            cols2=list(tmp['wvl'].columns)
            if set(cols1)==set(cols2):
                combined=pd.concat([combined,tmp])
            else:
                print("Wavelengths don't match!")

    combined.loc[:,('meta','sclock')]=pd.to_numeric(combined.loc[:,('meta','sclock')])
        
    if lookupfile is not None:
        combined=lookup(combined,lookupfile=lookupfile)
    if to_csv is not None:
        combined.to_csv(to_csv)
    return spectral_data(combined)
    
        