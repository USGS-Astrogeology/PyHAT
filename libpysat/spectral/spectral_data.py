# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:53:23 2015

@author: rbanderson
"""
import numpy as np
import pandas as pd
import scipy as sp
from matplotlib import pyplot as plot
from libpysat.spectral.baseline_code.airpls import AirPLS
from libpysat.spectral.baseline_code.als import ALS
from libpysat.spectral.baseline_code.ccam_remove_continuum import ccam_br
from libpysat.spectral.baseline_code.dietrich import Dietrich
from libpysat.spectral.baseline_code.fabc import FABC
from libpysat.spectral.baseline_code.kajfosz_kwiatek import KajfoszKwiatek as KK
from libpysat.spectral.baseline_code.mario import Mario
from libpysat.spectral.baseline_code.median import MedianFilter
from libpysat.spectral.baseline_code.polyfit import PolyFit
from libpysat.spectral.baseline_code.rubberband import Rubberband
from libpysat.spectral.jade import jadeR as jade
from libpysat.spectral.lra import low_rank_align as LRA
from sklearn import cross_validation
from sklearn.decomposition import PCA, FastICA
from sklearn.preprocessing import StandardScaler


def norm_total(df):
    df = df.div(df.sum(axis=1), axis=0)
    return df


class spectral_data(object):
    def __init__(self, df):

        uppercols = df.columns.levels[0]
        lowercols = list(df.columns.levels[1].values)
        for i, val in enumerate(lowercols):
            try:
                lowercols[i] = float(val)
            except:
                lowercols[i] = val

        levels = [uppercols, lowercols]
        df.columns.set_levels(levels, inplace=True)
        self.df = df

    def interp(self, xnew):
        xnew = np.array(xnew, dtype='float')

        metadata_cols = self.df.columns.levels[0] != 'wvl'
        metadata = self.df[self.df.columns.levels[0][metadata_cols]]
        old_wvls = np.array(self.df['wvl'].columns, dtype='float')
        old_spectra = np.array(self.df['wvl'])
        new_spectra = np.empty([len(old_spectra[:, 0]), len(xnew)]) * np.nan
        interp_index = (xnew > min(old_wvls)) & (xnew < max(old_wvls))

        f = sp.interpolate.interp1d(old_wvls, old_spectra, axis=1)
        new_spectra[:, interp_index] = f(xnew[interp_index])

        xnew = list(xnew)
        for i, x in enumerate(xnew):
            xnew[i] = ('wvl', x)

        new_df = pd.DataFrame(new_spectra, columns=pd.MultiIndex.from_tuples(xnew), index=self.df.index)
        new_df = pd.concat([new_df, metadata], axis=1)

        self.df = new_df

    def cal_tran(self, refdata, matchcol_ref, matchcol_transform, method, methodparams):
        C_matrix = []
        col = np.array([j.upper() for j in self.df[('meta', matchcol_transform)]])
        col_ref = np.array([j.upper() for j in refdata[('meta', matchcol_ref)]])
        for i in col:
            matches = np.where(col_ref == i, 1, 0)
            C_matrix.append(matches)

        C_matrix = np.transpose(np.array(C_matrix))

        if method == 'LRA - Low Rank Alignment':
            refdata_trans, transdata_trans = LRA(np.array(refdata['wvl']), np.array(self.df['wvl']), C_matrix,
                                                 methodparams['d'])
            refdata_trans = pd.DataFrame(refdata_trans)
            transdata_trans = pd.DataFrame(transdata_trans)
            pass
        if method == 'PDS Piecewise Direct Standardization':
            print('PDS not implemented yet!!')

        pass

    # This function masks out specified ranges of the data
    def mask(self, maskfile, maskvar='wvl'):
        df_spectra = self.df[maskvar]  # extract just the spectra from the data frame
        metadata_cols = self.df.columns.levels[0] != maskvar  # extract just the metadata
        metadata = self.df[self.df.columns.levels[0][metadata_cols]]

        mask = pd.read_csv(maskfile, sep=',')  # read the mask file
        tmp = []
        for i in mask.index:
            tmp.append((np.array(self.df[maskvar].columns, dtype='float') >= mask.ix[i, 'min_wvl']) & (
                np.array(self.df[maskvar].columns, dtype='float') <= mask.ix[i, 'max_wvl']))

        # combine the indexes for each range in the mask file into a single masking vector and use that to mask the spectra
        masked = np.any(np.array(tmp), axis=0)
        spectcols = list(df_spectra.columns)  # get the list of columns in the spectra dataframe
        for i, j in enumerate(masked):  # change the first level of the tuple from 'wvl' to 'masked' where appropriate
            if j == True:
                spectcols[i] = ('masked', spectcols[i])
            else:
                spectcols[i] = (maskvar, spectcols[i])
        df_spectra.columns = pd.MultiIndex.from_tuples(
            spectcols)  # assign the multiindex columns based on the new tuples
        self.df = pd.concat([df_spectra, metadata], axis=1)  # merge the masked spectra back with the metadata

    def multiply_vector(self, vectorfile):
        df_spectra = self.df['wvl']
        # TODO: check to make sure wavelengths match before multiplying

        vector = np.array(pd.read_csv(vectorfile, sep=',', header=None))[:, 1]
        if df_spectra.shape[1] == vector.shape[0]:
            self.df['wvl'] = df_spectra.multiply(vector, axis=1)
        else:
            print('Vector is not the same size as the spectra!')

    def peak_area(self, peaks_mins_file=None):
        df = self.df  # create a copy of the data
        wvls = df['wvl'].columns.values  # get the wavelengths

        if peaks_mins_file is not None:
            peaks_mins = pd.read_csv(peaks_mins_file, sep=',')
            peaks = peaks_mins['peaks']
            mins = peaks_mins['mins']
            pass
        else:
            ave_spect = np.average(np.array(df['wvl']), axis=0)  # find the average of the spectra in the data frame
            peaks = wvls[
                sp.signal.argrelextrema(ave_spect, np.greater_equal)[0]]  # find the maxima in the average spectrum
            mins = wvls[sp.signal.argrelextrema(ave_spect, np.less_equal)[0]]  # find the maxima in the average spectrum

        wvls = df['wvl'].columns.values  # get the wavelengths

        spectra = np.array(df['wvl'])
        for i in range(len(peaks)):

            # get the wavelengths between two minima
            try:
                low = mins[np.where(mins < peaks[i])[0][-1]]
            except:
                low = mins[0]

            try:
                high = mins[np.where(mins > peaks[i])[0][0]]
            except:
                high = mins[-1]

            peak_indices = np.all((wvls > low, wvls < high), axis=0)
            # plot.plot(wvls,ave_spect)
            # plot.plot(wvls[peak_indices],ave_spect[peak_indices])
            # plot.show()
            df[('peak_area', peaks[i])] = spectra[:, peak_indices].sum(axis=1)

        self.df = df
        return peaks, mins

    # This function divides the data up into a specified number of random folds
    def random_folds(self, nfolds=5, seed=10, groupby=None):
        self.df[('meta', 'Folds')] = np.nan  # Create an entry in the data frame that holds the folds
        foldslist = np.array(self.df[('meta', 'Folds')])
        if groupby == None:  # if no column name is listed to group on, just create random folds
            n = len(self.df.index)
            folds = cross_validation.KFold(n, nfolds, shuffle=True, random_state=seed)
            i = 1
            for train, test in folds:
                foldslist[test] = i
                i = i + 1

        else:
            # if a column name is provided, get all the unique values and define folds
            # so that all rows of a given value fall in the same fold
            # (this is useful to ensure that training and test data are truly independent)
            unique_inds = np.unique(self.df[groupby])
            folds = cross_validation.KFold(len(unique_inds), nfolds, shuffle=True, random_state=seed)
            foldslist = np.array(self.df[('meta', 'Folds')])
            i = 1
            for train, test in folds:
                tmp = unique_inds[test]
                tmp_full_list = np.array(self.df[groupby])
                tmp_ind = np.in1d(tmp_full_list, tmp)
                foldslist[tmp_ind] = i
                i = i + 1

        self.df[('meta', 'Folds')] = foldslist

    # this function divides the data up into a specified number of folds, using sorting
    # To try to get folds that look similar to each other
    def stratified_folds(self, nfolds=5, sortby=None):
        self.df[('meta', 'Folds')] = np.NaN  # Create an entry in the data frame that holds the folds
        self.df.sort_values(by=sortby, inplace=True)  # sort the data frame by the column of interest
        uniqvals = np.unique(self.df[sortby])  # get the unique values from the column of interest

        # assign folds by stepping through the unique values
        fold_num = 1
        for i in uniqvals:
            ind = self.df[sortby] == i  # find where the data frame matches the unique value
            self.df.set_value(self.df.index[ind], ('meta', 'Folds'), fold_num)
            # Inrement the fold number, reset to 1 if it is greater than the desired number of folds
            fold_num = fold_num + 1
            if fold_num > nfolds:
                fold_num = 1

        # sort by index to return the df to its original order
        self.df.sort_index(inplace=True)
        # self.folds_hist(sortby,50)

    def folds_hist(self, col_to_plot, nbins, xlabel='wt.%', ylabel='# of spectra'):
        folds_uniq = np.unique(self.df[('meta', 'Folds')])
        for f in folds_uniq:
            temp = self.rows_match(('meta', 'Folds'), [f])
            vals = np.array(temp.df[col_to_plot])
            bins = np.linspace(0, np.max(vals), nbins)
            plot.hist(vals, linewidth=0.5, edgecolor='k')
            plot.xlabel(xlabel)
            plot.ylabel(ylabel)
            plot.title(str(col_to_plot[1]) + '- Fold ' + str(f))
            fig = plot.gcf()
            fig.savefig('hist_fold_' + str(f) + '_' + col_to_plot[1] + '.png')
            plot.close()

    # This function normalizes specified ranges of the data by their respective sums
    def norm(self, ranges, col_var='wvl'):
        df_tonorm = self.df[col_var]
        top_level_cols = self.df.columns.levels[0]
        top_level_cols = top_level_cols[top_level_cols != col_var]
        df_other = self.df[top_level_cols]
        cols = df_tonorm.columns.values

        df_sub_norm = []
        allind = []
        for i in ranges:
            # Find the indices for the range
            ind = (np.array(cols, dtype='float') >= i[0]) & (np.array(cols, dtype='float') <= i[1])
            # find the columns for the range
            normcols = cols[ind]
            # keep track of the indices used for all ranges
            allind.append(ind)
            # normalize over the current range
            df_sub_norm.append(norm_total(df_tonorm[normcols]))

        # collapse the list of indices used to a single array
        allind = np.sum(allind, axis=0)
        # identify columns that were not used by where the allind array is less than 1
        cols_excluded = cols[np.where(allind < 1)]
        # create a separate data frame containing the un-normalized columns
        df_masked = df_tonorm[cols_excluded]
        # combine the normalized data frames into one
        df_norm = pd.concat(df_sub_norm, axis=1)

        # make the columns into multiindex
        df_masked.columns = [['masked'] * len(df_masked.columns), df_masked.columns]
        df_norm.columns = [[col_var] * len(df_norm.columns), df_norm.columns.values]

        # combine the normalized data frames, the excluded columns, and the metadata into a single data frame
        df_new = pd.concat([df_other, df_norm, df_masked], axis=1)
        self.df = df_new

    # This function applies baseline removal to the data
    def remove_baseline(self, method='ALS', segment=True, params=None):
        wvls = np.array(self.df['wvl'].columns.values, dtype='float')
        spectra = np.array(self.df['wvl'], dtype='float')

        # set baseline removal object (br) to the specified method
        if method == 'ALS':
            br = ALS()
        elif method == 'Dietrich':
            br = Dietrich()
        elif method == 'Polyfit':
            br = PolyFit()
        elif method == 'AirPLS':
            br = AirPLS()
        elif method == 'FABC':
            br = FABC()
        elif method == 'KK':
            br = KK()
        elif method == 'Mario':
            br = Mario()
        elif method == 'Median':
            br = MedianFilter()
        elif method == 'Rubberband':
            br = Rubberband()
        elif method == 'CCAM':
            br = ccam_br()
            # if method == 'wavelet':
            #   br=Wavelet()
        else:
            print(method + ' is not recognized!')

        # if parameters are provided, use them to set the parameters of br
        if params is not None:
            for i in params.keys():
                try:
                    setattr(br, i, params[i])
                except:
                    print('Required keys are:')
                    print(br.__dict__.keys())
                    print('Exiting without removing baseline!')
                    return
        br.fit(wvls, spectra, segment=segment)
        self.df_baseline = self.df.copy()
        self.df_baseline['wvl'] = br.baseline
        self.df['wvl'] = self.df['wvl']-self.df_baseline['wvl']
    # This function finds rows of the data frame where a specified column has
    # values matching a specified set of values
    # (Useful for extracting folds)
    def rows_match(self, column_name, isin_array, invert=False):
        if invert:
            new_df = self.df.loc[-self.df[column_name].isin(isin_array)]
        else:
            new_df = self.df.loc[self.df[column_name].isin(isin_array)]
        return spectral_data(new_df)

    # This function takes the sum of data over two specified wavelength ranges,
    # calculates the ratio of the sums, and adds the ratio as a column in the data frame
    def ratio(self, range1, range2, rationame=''):
        cols = self.df['wvl'].columns.values
        cols1 = cols[(cols >= range1[0]) & (cols <= range1[1])]
        cols2 = cols[(cols >= range2[0]) * (cols <= range2[1])]

        df1 = self.df['wvl'].loc[:, cols1]
        df2 = self.df['wvl'].loc[:, cols2]

        sum1 = df1.sum(axis=1)
        sum2 = df2.sum(axis=1)

        ratio = sum1 / sum2

        self.df[('ratio', rationame)] = ratio

    def standard_scale(self, col):
        self.df[col] = StandardScaler().fit_transform(self.df[col])

    # create an all-purpose dimensionality reduction option to replace the individual PCA, ICA, etc. functions
    def dim_red(self, col, method, params, kws, load_fit=None):
        if method == 'PCA':
            self.do_dim_red = PCA(*params, **kws)
        if method == 'FastICA':
            self.do_dim_red = FastICA(*params, **kws)
        # TODO: Add ICA-JADE here
        if load_fit:
            self.do_dim_red = load_fit
        else:
            self.do_dim_red.fit(self.df[col])
        dim_red_result = self.do_dim_red.transform(self.df[col])
        for i in list(range(1, dim_red_result[0].shape[
            0] + 1)):  # will need to revisit this for other methods that don't use n_components to make sure column names still mamke sense
            self.df[(method, str(i))] = dim_red_result[:, i - 1]

        return self.do_dim_red

    def pca(self, col, nc=None, load_fit=None):
        if nc:
            self.do_pca = PCA(n_components=nc)
            self.do_pca.fit(self.df[col])
        if load_fit:  # use this to load a previous fit rather than fit the current data
            self.do_pca = load_fit
        pca_result = self.do_pca.transform(self.df[col])
        for i in list(range(1, self.do_pca.n_components + 1)):
            self.df[('PCA', i)] = pca_result[:, i - 1]

    def ica(self, col, nc=None, load_fit=None):
        if nc:
            self.do_ica = FastICA(n_components=nc)
            self.do_ica.fit(self.df[col])
        if load_fit:  # use this to load a previous fit rather than fit the current data
            self.do_ica = load_fit
        ica_result = self.do_ica.transform(self.df[col])
        for i in list(range(1, self.do_ica.n_components + 1)):
            self.df[('ICA', i)] = ica_result[:, i - 1]

    def ica_jade(self, col, nc=None, load_fit=None, corrcols=None):
        if load_fit is not None:  # use this to load a previous fit rather than fit the current data
            scores = np.dot(load_fit, self.df[col])
        else:
            scores = jade(self.df[col].values, m=nc, verbose=False)
        loadings = np.dot(scores, self.df[col])

        icacols = []
        for i in list(range(1, len(scores[:, 0]) + 1)):
            if np.abs(np.max(loadings[i - 1, :])) < np.abs(
                    np.min(loadings[i - 1, :])):  # flip the sign if necessary to look nicer
                loadings[i - 1, :] = loadings[i - 1, :] * -1
                scores[i - 1, :] = scores[i - 1, :] * -1
            icacols.append(('ICA-JADE', i))
            self.df[('ICA-JADE', i)] = scores[i - 1, :].T
        self.ica_jade_loadings = loadings

        if corrcols:
            combined_cols = corrcols + icacols
            corrdf = self.df[combined_cols].corr().drop(icacols, 1).drop(corrcols, 0)
            ica_jade_ids = []
            for i in corrdf.loc['ICA-JADE'].index:
                tmp = corrdf.loc[('ICA-JADE', i)]
                match = tmp.values == np.max(tmp)
                ica_jade_ids.append(corrcols[np.where(match)[0]][1] + ' (r=' + str(np.round(np.max(tmp), 1)) + ')')
                pass
            self.ica_jade_corr = corrdf
            self.ica_jade_ids = ica_jade_ids

    def col_within_range(self, rangevals, col):
        mask = (self.df[('meta', col)] > rangevals[0]) & (self.df[('meta', col)] < rangevals[1])
        return self.df.loc[mask]

    def enumerate_duplicates(self, col):
        rows = self.df[('meta', col)]
        rows = rows.fillna('-')
        rows = [str(x) for x in rows]
        unique_rows = np.unique(rows)
        rows=np.array(rows)
        rows_list=list(rows)
        for i in unique_rows:
            if i is not '-':
                matchindex = np.where(rows == i)[0]

                if len(matchindex) > 1:
                    for n, name in enumerate(rows[matchindex]):
                        rows_list[matchindex[n]] = i+ ' - ' + str(n + 1)

        self.df[('meta', col)] = rows_list
