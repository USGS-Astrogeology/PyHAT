import numpy as np
import pandas as pd
import pvl

from libpysat.spectral.spectra import Spectra
from libpysat.utils.utils import find_in_dict


# TODO: The spectra should inhert from a SpectraABC, monkey patch smoothing in.
class Spectral_Profiler(object):
    """
    Attributes
    ----------

    spectra : dict
              A dictionary with k as the integer observation id and value
              as a pandas DataFrame.

    ancillary_data : dataframe
                     A pandas DataFrame of the parsed ancillary data (PVL label)

    label : object
            The raw PVL label object
    """

    def __init__(self, input_data, cleaned=True, qa_threshold=2000):
        """
        Read the .spc file, parse the label, and extract the spectra

        Parameters
        ----------

        input_data : string
                     The PATH to the input .spc file

        cleaned : boolean
                  If True, mask the data based on the QA array.
        """

        label_dtype_map = {'IEEE_REAL': 'f',
                           'MSB_INTEGER': 'i',
                           'MSB_UNSIGNED_INTEGER': 'u'}

        label = pvl.load(input_data)
        self.label = label
        with open(input_data, 'rb') as indata:
            # Extract and handle the ancillary data
            ancillary_data = find_in_dict(label, "ANCILLARY_AND_SUPPLEMENT_DATA")
            nrows = ancillary_data['ROWS']
            ncols = ancillary_data['COLUMNS']
            rowbytes = ancillary_data['ROW_BYTES']

            columns = []
            bytelengths = []
            datatypes = []
            ancillary_data_offset = find_in_dict(label, "^ANCILLARY_AND_SUPPLEMENT_DATA").value
            indata.seek(ancillary_data_offset - 1)
            for i in ancillary_data.items():
                if i[0] == 'COLUMN':
                    entry = i[1]
                    # Level 2B2 PVL has entries with 0 bytes, e.g. omitted.
                    if entry['BYTES'] > 0:
                        columns.append(str(entry['NAME']))
                        datatypes.append(label_dtype_map[entry['DATA_TYPE']])
                        bytelengths.append(entry['BYTES'])
                    else:
                        ncols -= 1
            strbytes = map(str, bytelengths)
            rowdtype = list(zip(columns, map(''.join, zip(['>'] * ncols, datatypes, strbytes))))
            d = np.fromstring(indata.read(rowbytes * nrows), dtype=rowdtype,
                              count=nrows)
            self.ancillary_data = pd.DataFrame(d, columns=columns,
                                               index=np.arange(nrows))

            assert (ncols == len(columns))

            keys = []
            array_offsets = []
            for d in ['WAV', 'RAW', 'REF', 'REF1', 'REF2', 'DAR', 'QA']:
                search_key = '^SP_SPECTRUM_{}'.format(d)
                result = find_in_dict(label, search_key)
                if result:
                    array_offsets.append(result.value)
                    keys.append('SP_SPECTRUM_{}'.format(d))

            offsets = dict(zip(keys, array_offsets))

            arrays = {}
            for k, offset in offsets.items():
                indata.seek(offset - 1)
                newk = k.split('_')[-1]

                d = find_in_dict(label, k)
                unit = d['UNIT']
                lines = d['LINES']
                scaling_factor = d['SCALING_FACTOR']

                arr = np.fromstring(indata.read(lines * 296 * 2), dtype='>H').astype(np.float64)
                arr = arr.reshape(lines, -1)

                # If the data is scaled, apply the scaling factor
                if isinstance(scaling_factor, float):
                    arr *= scaling_factor
                arrays[newk] = arr

            self.wavelengths = pd.Series(arrays['WAV'][0])

            self.spectra = {}
            for i in range(nrows):
                self.spectra[i] = pd.DataFrame(index=self.wavelengths)
                for k in keys:
                    k = k.split('_')[-1]
                    if k == 'WAV':
                        continue
                    self.spectra[i][k] = arrays[k][i]

                if cleaned:
                    self.spectra[i] = self.spectra[i][self.spectra[i]['QA'] < qa_threshold]

                self.spectra[i] = Spectra(self.spectra[i])


"""
class SpectralSeries(pd.Series):
    def __init__(self, **kwargs):
        super(SpectralSeries, self).__init__(*args, **kwargs)


def parse_coefficients(coefficient_table):
    '''
    Parameters
    ----------

    coefficient_table     type: file path
                          The CSV file to be parsed

    Returns
    -------
    supplemental          type: list of lists
                          List of coefficients where index is the sequentially increasing wavelength.  This data is 'cleaned'.  The r_{mean} at 1003.6 is set to -999, a NoDataValue.
    '''
    d = open(coefficient_table)
    supplemental = []
    for line in d:
        line = line.split(",")
        supplemental.append([float(s) for s in line[1:]])

    return supplemental

def photometric_correction(wv, ref_vec,coefficient_table, angles):
    '''
    TODO: Docs here
    This function performs the photometric correction.
    '''
    incidence_angle = angles[:,0]
    emission_angle = angles[:,1]
    phase_angle = angles[:,2]


    def _phg(g, phase_angle):
        '''This function allows positive and neg. g to be passed in'''
        phg = (1.0-g**2) / (1.0+g**2-2.0*g*np.cos(np.radians(phase_angle))**(1.5))
        return phg

    #The ref_array runs to the detector limit, but the coefficient table truncates at 1652.1, we therefore only correct the wavelengths that we know the coefficents for.
    #Column  = ref_array[:,wv]
    b_naught = coefficient_table[wv][0]
    h = coefficient_table[wv][1]
    c = coefficient_table[wv][2]
    g = coefficient_table[wv][3]

    #Compute the phase function with fixed values
    p = ((1-c)/2) * _phg(g,30) + ((1+c)/2) * _phg((-1 * g),30)
    b = b_naught / (1+(np.tan(np.radians(30/2.0))/h))
    f_fixed = (1+b)*p

    #Compute the phase function with the observation phase
    p = (((1-c)/2) * _phg(g,phase_angle)) + (((1+c)/2)* _phg((-1 * g),phase_angle))
    b = b_naught / (1+(np.tan(np.radians(phase_angle/2.0))/h))
    f_observed = (1+b)*p

    f_ratio = f_fixed / f_observed

    #Compute the lunar lambert function
    l = 1.0 + (c1*phase_angle) + (c2*phase_angle**2) + (c3*phase_angle**3)
    cosi = np.cos(np.radians(incidence_angle))
    cose = np.cos(np.radians(emission_angle))
    xl_observed = 2 * l * (cosi / (cosi + cose)) + ((1-l)*cosi)
    xl_ratio = xl_fixed / xl_observed

    #Compute the photometrically corrected reflectance
    ref_vec = ref_vec * xl_ratio * f_ratio
    return ref_vec

def continuum_correction(bands, mask_ref, masked_wv, obs_id):
    y2 = mask_ref[obs_id][bands[1]]
    y1 = mask_ref[obs_id][bands[0]]
    wv2 = masked_wv[bands[1]]
    wv1 =masked_wv[bands[0]]

    m = (y2-y1) / (wv2 - wv1)
    b =  y1 - (m * wv1)
    y = m * masked_wv + b

    continuum_corrected_ref_array = mask_ref[obs_id] / y
    return continuum_corrected_ref_array, y

def regression_correction(wavelength, reflectance):
    m, b, r_value, p_value, stderr = ss.linregress(wavelength, reflectance)
    regressed_continuum = m * wavelength + b
    return reflectance / regressed_continuum

def horgan_correction(wavelengths, reflectance, a, b, c):
    numwv = len(wavelengths)
    maxa = reflectance[:a].argmax()
    maxb = reflectance[b:c + 1].argmax() + b
    maxc = reflectance[numwv-10:numwv-3].argmax() + numwv-10
    iterating = True
    while iterating:
        reflectance.dtype = np.float64
        x = np.asarray([wavelengths[maxa], wavelengths[maxb], wavelengths[maxc]])
        y = np.asarray([reflectance[maxa], reflectance[maxb], reflectance[maxc]])
        fit = np.polyfit(x,y,2)
        horgan_continuum = np.polyval(fit, wavelengths)
        horgan_correction = reflectance / horgan_continuum
        iterating = False
    return horgan_correction

def save_reflectance(wv_array, rad_array, ref_array, qa_array, outname):
    nobs = ref_array.shape[0]
    header = 'wavelength\tquality\t'
    for i in range(nobs):
        header += 'rad{}\tref{}\t'.format(i, i)
    ncols = nobs * 2 + 2
    stacked = np.empty((ref_array.shape[1], ncols))
    stacked[:,0] = wv_array
    #This assumes that the QS is static across all observations
    stacked[:,1] = qa_array[0]
    alt_shape = stacked[:,2::2].shape
    stacked[:,2::2] = rad_array.reshape(rad_array.size, order='F').reshape((rad_array.shape[1], rad_array.shape[0]))
    stacked[:,3::2] = ref_array.reshape(ref_array.size, order='F').reshape((ref_array.shape[1], ref_array.shape[0]))
    np.savetxt(outname + '.txt', stacked, fmt='%10.5f', header=header, delimiter='\t')

def observation_list(nrows, ncols, nobs):
    midpoint = ncols / 2.0
    obs_interval = float(nrows) / nobs
    x = np.empty(nobs)
    x[:] = midpoint
    y = np.empty(nobs)
    y[:] = obs_interval
    y[0] = obs_interval / 2
    y = np.cumsum(y)
    labels = np.arange(nobs,dtype=np.int)
    c = 0
    pt_to_obs = {}
    for i, j, k in zip(x,y,labels):
        pt_to_obs[j] = k
    return x,y, pt_to_obs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Spectral Profiler Reflectance Extraction Tool')
    parser.add_argument('input_data', action='store', help='The ".spc" file shipped with the SP data.')
    parser.add_argument('albedo_tab', action='store', help='The albedo table for the chosen overall reflectance (high, medium, or low).')
    parser.add_argument('-w', action='store',dest='wv_limits', default=1652, nargs=1, help='The limit wavelength to visualize to.')
    parser.add_argument('-s', '--save', default=False, action='store_true', dest='save', help='Save output to a CSV file.')
    parser.add_argument('-o', '--outputname', dest='outputname', help='Custom output name for the CSV file.')
    parser.add_argument('-p', default=True, action='store_false', dest='check_photometric', help='Disable photometric correction')
    parser.add_argument('observation', default=0,type=int, nargs='+', help='The range of observations to visualize.')
    args = parser.parse_args()

    #Read in the spc file, extract necessary info, and clean the data
    wv_array, rad_array, ref_array, angles, qa_array = openspc(args.input_data, args.save)
    #Using the QA data, mask the array.
    if args.save is False:
        masked_wv, mask_ref = cleandata(qa_array, wv_array, ref_array)

        maxwv = int(args.wv_limits)
        extent = np.where(masked_wv<= maxwv)
        #Copy the unphotometrically corrected array
        input_refarray = np.copy(mask_ref)


    #Parse the supplemental table to get photometric correction coefficients
    coefficient_table = parse_coefficients(args.albedo_tab)

    if args.check_photometric is True:
        #Perform the photometric correction
        for wv in range(len(coefficient_table)):
            mask_ref[:,wv] = photometric_correction(wv, mask_ref[:,wv], coefficient_table, angles)

        #Copy the photometrically corrected array
        photometrically_corrected_ref_array = np.copy(mask_ref)
        continuum_slope_array = np.empty(mask_ref.shape)

    #Continuum correction
    if args.save is True:
        if args.outputname != None:
            out = args.outputname
        else:
            out = args.input_data.split('/')[-1].split('.')[0]
        save_reflectance(wv_array, rad_array, ref_array, qa_array, out)

    else:
        #Continuum correct all observations
        for obs_id in range(len(ref_array)):
            bands = getbandnumbers(masked_wv, 752.8, 1547.7)
            mask_ref[obs_id],continuum_slope_array[obs_id] = continuum_correction(bands, mask_ref, obs_id)

        for obs in range(len(args.observation)):
            #Do the plotting
            fig = plt.figure(args.observation[obs], figsize=(8,12))
            fig.subplots_adjust(hspace=0.75)

            ax1 = subplot(411)
            grid(alpha=.5)
            plot(masked_wv[extent],input_refarray[obs][extent], linewidth=1.5)
            xlabel('Wavelength', fontsize=10)
            ax1.set_xticks(masked_wv[extent][::4])
            ax1.set_xticklabels(masked_wv[extent][::4], rotation=45, fontsize=8)
            ax1.set_xlim(masked_wv[extent].min()-10, masked_wv[extent].max()+10)
            ylabel('Reflectance', fontsize=10)
            ax1.set_yticklabels(input_refarray[obs][extent],fontsize=8)
            title('Level 2B2 Data', fontsize=12)

            ax2 = subplot(412)
            grid(alpha=.5)
            plot(masked_wv[extent],photometrically_corrected_ref_array[obs][extent], linewidth=1.5)
            xlabel('Wavelength', fontsize=10)
            ax2.set_xticks(masked_wv[extent][::4])
            ax2.set_xticklabels(masked_wv[extent][::4], rotation=45, fontsize=8)
            ax2.set_xlim(masked_wv[extent].min()-10, masked_wv[extent].max()+10)
            ylabel('Reflectance', fontsize=10)
            ax2.set_yticklabels(input_refarray[obs][extent],fontsize=8)
            title('Photometrically Corrected Data', fontsize=12)

            ax3 = subplot(413)
            grid(alpha=.5)
            plot(masked_wv[extent],photometrically_corrected_ref_array[obs][extent], label='Photometrically Corrected Spectrum', linewidth=1.5)
            plot(masked_wv[extent], continuum_slope_array[obs][extent],'r--', label='Spectral Continuum', linewidth=1.5)
            xlabel('Wavelength', fontsize=10)
            ax3.set_xticks(masked_wv[extent][::4])
            ax3.set_xticklabels(masked_wv[extent][::4], rotation=45, fontsize=8)
            ax3.set_xlim(masked_wv[extent].min()-10, masked_wv[extent].max()+10)
            ylabel('Reflectance', fontsize=10)
            ax3.set_yticklabels(input_refarray[obs][extent],fontsize=8)
            title('Continuum Slope', fontsize=12)

            ax4 = subplot(414)
            grid(alpha=.5)
            plot(masked_wv[extent], mask_ref[obs][extent], linewidth=1.5)
            xlabel('Wavelength', fontsize=10)
            ax4.set_xticks(masked_wv[extent][::4])
            ax4.set_xticklabels(masked_wv[extent][::4], rotation=45, fontsize=8)
            ax4.set_xlim(masked_wv[extent].min()-10, masked_wv[extent].max()+10)
            ylabel('Reflectance', fontsize=10)
            #ax4.set_yticklabels(mask_ref[obs][extent],fontsize=8)
            title('Continuum Removed Spectrum', fontsize=12)

            draw()

            fig2 = plt.figure(args.observation[obs] + 1, figsize=(8,8))
            grid(alpha=.5)
            plot(masked_wv[extent], mask_ref[obs][extent], linewidth=1.5)
            xlabel('Wavelength', fontsize=10)
            xticks(masked_wv[extent][::4], rotation=90)

            xlim(masked_wv[extent].min()-10, masked_wv[extent].max()+10)
            ylabel('Reflectance', fontsize=10)
            title('Continuum Removed Spectrum', fontsize=12)
    show()
"""
