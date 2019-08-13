from bin.jade import JADE
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold.t_sne import TSNE
from sklearn.manifold.locally_linear import LocallyLinearEmbedding

#This function does dimensionality reduction on a data frame full of spectra. A number of different methos can be chosen

def dim_red(df, col, method, params, kws, load_fit=None):
    if method == 'PCA':
        do_dim_red = PCA(*params, **kws)
    if method == 'FastICA':
        do_dim_red = FastICA(*params, **kws)
    if method == 't-SNE':
        do_dim_red = TSNE(*params, **kws)
    if method == 'LLE':
        do_dim_red = LocallyLinearEmbedding(*params, **kws)
    if method == 'JADE-ICA':
        do_dim_red = JADE(*params, **kws)
    if load_fit:
        do_dim_red = load_fit
    else:
        if method != 't-SNE':
            do_dim_red.fit(df[col])
            dim_red_result = do_dim_red.transform(df[col])
        else:
            dim_red_result = do_dim_red.fit_transform(df[col])

    for i in list(range(1, dim_red_result.shape[
                               1] + 1)):  # will need to revisit this for other methods that don't use n_components to make sure column names still mamke sense
        df[(method, method+'-'+str(i))] = dim_red_result[:, i - 1]

    return df, do_dim_red
