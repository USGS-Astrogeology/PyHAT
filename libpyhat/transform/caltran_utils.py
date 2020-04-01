from itertools import chain

import glob
import numpy as np
import os
import functools

try:
  from np.linalg import multi_dot
except ImportError:
  def multi_dot(arrays):
    return functools.reduce(np.dot, arrays)


def svt_thresh(X, thresh):
    '''Solves argmin_X 1/2 ||X-Y||_F^2 + thresh ||X||_*
       proximal operator for spectral norm (rank reducer)
       See: http://www-stat.stanford.edu/~candes/papers/SVT.pdf
    '''
    U, s, V = np.linalg.svd(X, full_matrices=False)
    s = np.maximum(0, s - thresh)
    return (U * s).dot(V)


def soft_thresh(X, thresh):
    '''Solves argmin_X 1/2 ||X-Y||_F^2 + thresh ||X||_1
       proximal operator for l1-norm (sparsifier)
       See: http://www.simonlucey.com/soft-thresholding/
    '''
    return np.sign(X) * np.maximum(0, np.abs(X)-thresh)


def norm1(shots,copy=True):
  from sklearn.preprocessing import normalize
  return normalize(shots,norm='l1',copy=copy)


def norm3(shots,copy=True):
  if copy:
    n3shots = np.copy(shots)
  else:
    n3shots = shots
  num_chan = shots.shape[1]
  if num_chan == 6143:
    return np.hstack((norm1(n3shots[:,:2047]),
                      norm1(n3shots[:,2047:4097]),
                      norm1(n3shots[:,4097:])))
  if num_chan == 6144:
    return np.hstack((norm1(n3shots[:,:2048]),
                      norm1(n3shots[:,2048:4098]),
                      norm1(n3shots[:,4098:])))
  if num_chan == 5485:
    return np.hstack((norm1(n3shots[:,:1884]),
                      norm1(n3shots[:,1884:3811]),
                      norm1(n3shots[:,3811:])))
  assert False, 'num_chan must be either 6143, 6144 or 5485'


ALAMOS_MASK = list(chain(range(0,110),range(1994,2169),
                         range(4096,4182),range(5856,6144)))

def load_caltargets(base_dir='~/Mars/Data/Transfer/caltargets/',normz=None):
    base_dir = os.path.expanduser(base_dir)
    mars = []
    for i in range(1,8):
        mars.append(np.mean(np.genfromtxt(base_dir+'Mars%d.csv'%i,delimiter=',',dtype=None)[:,1:],1))
    mars = np.delete(np.array(mars),ALAMOS_MASK,1)
    lab = np.genfromtxt(base_dir+'lab_targets.csv',delimiter=',',dtype=None)

    labels = np.genfromtxt(base_dir+'target_comps.csv',delimiter=',',dtype=None)
    names = np.genfromtxt(base_dir+'target_names.csv',delimiter=',',dtype=None)
    if normz is None:
        return [lab,mars],labels,names
    else:
        return [normz(lab),normz(mars)],labels,names

#
# def load_data(masked=True,norm=1):
#     ALAMOS_PATH = os.path.expanduser('~/Mars/Data/LA400/preprocessed')
#     samples = []
#     comps = np.genfromtxt(os.path.expanduser('~/Mars/Data/LA400/folds_n_comps.csv'),names=True,delimiter=',',dtype=None)
#     if masked:
#        mask = ALAMOS_MASK
#     else:
#         mask = [0]
#     for sname in comps['Name']:
#         print(sname)
#         fullpath = os.path.abspath(os.path.join(ALAMOS_PATH, sname))
#         shots = []
#         for spot in read_shots(data_dir=fullpath,min_shot_length=50,mask=mask):
#             shots.extend(spot)
#         shots = np.array(shots)
#         samples.append(shots.mean(0))
#     samples = np.array(samples)
#     if norm == 1:
#         samples = norm1(samples)
#     elif norm == 3:
#         samples = norm3(samples)
#     return samples,comps

#
# def read_shots(data_dir,min_shot_length=30,parse_distance=False,return_names=False,mask=None):
#     file_pattern = os.path.join(data_dir, '*.csv')
#     files = glob.glob(file_pattern)
#     assert files, 'No files match ' + file_pattern
#     for data_file in files:
#         shots = np.loadtxt(data_file, delimiter=',').T[1:-2]
#     if mask is not None:
#         shots = np.delete(shots,mask,1)
#     if shots.shape[0] >= min_shot_length:
#         if parse_distance:
#             dist = _shot_distance(data_file)
#             # TODO fix this gahbage
#             if not dist:
#                 print("Couldn't find dist for file:", data_file)
#             if return_names:
#                 yield shots, dist, data_file
#             else:
#                 yield shots, dist
#         else:
#             if return_names:
#                 yield shots, data_file
#             else:
#                 yield shots
