"""Low Rank Alignment algorithm by T. Boucher and C.J. Carey from https://github.com/all-umass/low_rank_alignment
This method has been demonstrated to be effective for calibration transfer on LIBS spectra:
http://www.aaai.org/ocs/index.php/AAAI/AAAI15/paper/download/9972/9880
"""

from scipy.linalg import block_diag, eigh, svd
from scipy.sparse.csgraph import laplacian
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
import numpy as np


def low_rank_align(X, Y, Cxy, d=None, mu=0.8):
    """Input: data matrices X,Y,  correspondence matrix Cxy,
              embedding dimension d, and correspondence weight mu
       Output: embedded X and embedded Y
    """
    nx, dx = X.shape
    ny, dy = Y.shape
    assert Cxy.shape==(nx,ny), \
        'Correspondence matrix must be shape num_X_samples X num_Y_samples.'
    C = np.fliplr(block_diag(np.fliplr(Cxy),np.fliplr(Cxy.T)))
    if d is None:
        d = min(dx,dy)
    Rx = low_rank_repr(X,d)
    Ry = low_rank_repr(Y,d)
    R = block_diag(Rx,Ry)
    tmp = np.eye(R.shape[0]) - R
    M = tmp.T.dot(tmp)
    L = laplacian(C)
    eigen_prob = (1-mu)*M + 2*mu*L
    _,F = eigh(eigen_prob,eigvals=(1,d),overwrite_a=True)
    Xembed = F[:nx]
    Yembed = F[nx:]
    return Xembed, Yembed


def low_rank_repr(X, n_dim):
    U, S, V = svd(X.T,full_matrices=False)
    mask = S > 1
    V = V[mask]
    S = S[mask]
    R = (V.T * (1 - S**-2)).dot(V)
    return R


def demo():
    ''' 3-D noisy dollar example '''
    n_sline = 50
    n_lline = 20
    noise_std = .05

    X,_ = dollar_sign(n_sline,n_lline)
    X += np.random.normal(scale=noise_std, size=X.shape)
    Y = X + np.random.normal(scale=noise_std, size=X.shape)
    Y = np.rot90(Y).T[:,(0,2,1)]

    Xembed, Yembed = low_rank_align(X,Y,np.eye(n_sline+n_lline),d=2)

    fig = plt.figure()
    ax1 = fig.add_subplot(1,3,1,projection='3d')
    ax1.set_title('Noisy Dollar')
    ax1.scatter(X[:n_sline,0],X[:n_sline,1],X[:n_sline,2],c='b',s=50)
    ax1.scatter(X[n_sline:,0],X[n_sline:,1],X[n_sline:,2],c='b',marker='*',s=60)
    ax2 = fig.add_subplot(1,3,2,projection='3d')
    ax2.set_title('Rotated Noisier Dollar')
    ax2.scatter(Y[:n_sline,0],Y[:n_sline,1],Y[:n_sline,2],c='r',s=50)
    ax2.scatter(Y[n_sline:,0],Y[n_sline:,1],Y[n_sline:,2],c='r',marker='*',s=60)
    ax3 = fig.add_subplot(1,3,3)
    ax3.set_title('Aligned 2-D Dollars')
    ax3.scatter(Xembed[:n_sline,0],Xembed[:n_sline,1],c='b',edgecolor='b',s=150)
    ax3.scatter(Xembed[n_sline:,0],Xembed[n_sline:,1],c='b',edgecolor='b',s=165,
                marker='*')
    ax3.scatter(Yembed[:n_sline,0],Yembed[:n_sline,1],c='r',edgecolor='r',s=50)
    ax3.scatter(Yembed[n_sline:,0],Yembed[n_sline:,1],c='r',edgecolor='r',s=60,
                marker='*')
    ax3.xaxis.set_visible(False)
    ax3.yaxis.set_visible(False)
    plt.show()


def dollar_sign(num_s_points, num_bar_points):
    '''returns a tuple of (3d points, 1d labels)'''
    s = s_curve(num_s_points)
    bar_width = np.random.uniform(-1, 1, size=num_bar_points)
    bar_length = np.linspace(s[:,2].min()-1, s[:,2].max()+1, num_bar_points)
    bar = np.column_stack((np.zeros(num_bar_points), bar_width, bar_length))
    dollar = np.vstack((s,bar))
    labels = np.ones(dollar.shape[0])
    labels[num_s_points:] = 2
    return dollar, labels


def s_curve(n_pts):
    theta = np.linspace(-np.pi-1, np.pi+1, n_pts)
    width = np.random.uniform(-1, 1, size=n_pts)
    X = np.column_stack((np.sin(theta), width, np.cos(theta)))
    mid = n_pts // 2
    X[:mid,2] = 2 + -X[:mid,2]
    return X


if __name__ == '__main__':
    demo()