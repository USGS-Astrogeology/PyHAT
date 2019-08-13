from libpyhat.transform.lra import low_rank_align as LRA
import numpy as np
from sklearn.cross_decomposition import CCA, PLSRegression
from sklearn.preprocessing import normalize
from scipy.linalg import cho_factor, cho_solve, svdvals
from numpy.linalg import norm
import libpyhat.transform.caltran_utils as ct

#apply calibration transfer to a data set to transform it to match a different data set.

class cal_tran:
    def __init__(self, params):

        self.algorithm_list = ['None',
                               'PDS - Piecewise DS',
                               'DS - Direct Standardization',
                               'LASSO DS',
                               'Ratio',
                               'Ridge DS',
                               'Sparse Low Rank DS',
                               'CCA - Canonical Correlation Analysis',
                               'New CCA',
                               'Incremental Proximal Descent DS',
                               'Forward Backward DS']
        self.method = params.pop('method')

        self.ct_obj = None

        if self.method == 'PDS - Piecewise DS':
            self.ct_obj = piecewise_ds(**params)
        if self.method == 'None':
            self.ct_obj = no_transform()
        if self.method == 'DS - Direct Standardization':
            self.ct_obj = ds(**params)
        if self.method == 'LASSO DS':
            self.ct_obj = admm_ds(**params)
        if self.method == 'Ridge DS':
            self.ct_obj = admm_ds(**params)
        if self.method == 'Sparse Low Rank DS':
            self.ct_obj = admm_ds(**params)
        if self.method == 'CCA - Canonical Correlation Analysis':
            self.ct_obj = cca(**params)
        if self.method == 'New CCA':
            self.ct_obj = cca(**params)
        if self.method == 'Incremental Proximal Descent DS':
            self.ct_obj = ipd_ds(**params)
        if self.method == 'Forward Backward DS':
            self.ct_obj = forward_backward_ds(**params)
        if self.method == 'Ratio':
            self.ct_obj = ratio()
        if self.method == 'PDS-PLS - PDS using Partial Least Squares':
            self.ct_obj = piecewise_ds(**params)


        if self.ct_obj==None:
            print('Method '+self.method+' not recognized!')

    def derive_transform(self,A,B):
        self.ct_obj.derive_transform(A,B)

    def apply_transform(self,C):
        return self.ct_obj.apply_transform(C)

class no_transform:
    def derive_transform(self,A,B):
        return
    def apply_transform(self,C):
        return C

class ratio:
    def __init__(self):

        def derive_transform(self, A, B):
            A_mean = np.mean(A, axis=0)
            B_mean = np.mean(B, axis=0)
            self.ratio_vect = B_mean / A_mean

        def apply_transform(self, C):
            C_transformed = C.multiply(self.ratio_vect, axis=1)
            return C_transformed

class piecewise_ds:
    def __init__(self, win_size=5, pls=False, nc=5):
        self.pls = pls
        self.win_size = win_size
        self.pls_nc = nc
        assert win_size % 2 == 1, "Window size must be odd."
        self.padding = (win_size - 1) / 2

    def derive_transform(self, A, B):
        A = np.array(A, dtype='float')
        B = np.array(B, dtype='float')
        assert A.shape == B.shape, "Input matrices must be the same shape."
        self.B_shape = B.shape
        n_feats = B.shape[1]
        coefs = []
        for i in range(n_feats):
            row = np.zeros(n_feats)
            start = int(max(i - self.padding, 0))
            end = int(min(i + self.padding, n_feats - 1) + 1)
            if self.pls:
                model = PLSRegression(n_components=self.pls_nc, scale=False)
                try:
                    model.fit(A[:, start:end], B[:, i])
                    row[start:end] = model.coef_.ravel()
                except:
                    pass
            else:
                row[start:end] = np.dot(np.linalg.pinv(A[:, start:end]), B[:, i])

            coefs.append(row)

        self.proj_to_B = np.array(coefs).T

    def apply_transform(self, C):
        C_transformed = np.dot(C, self.proj_to_B)
        return C_transformed

class ds:
    def __init__(self, fit_intercept=False):
        self.fit_intercept = fit_intercept

    def get_working_data(self, data):
        if self.fit_intercept:
            if len(data.shape) == 1:
                data = np.reshape(data, (1, data.shape[0]))
            working = np.hstack((data, np.ones((data.shape[0], 1))))
        else:
            working = np.copy(data)
        return working

    def derive_transform(self, A, B):
        assert A.shape[0] == B.shape[0], (
            'Input matrices must have the same number of rows (i.e. samples).')
        working_A = self.get_working_data(A)
        self.proj_to_B = np.dot(np.linalg.pinv(working_A), B)

    def apply_transform(self, C):
        working_C = self.get_working_data(C)
        C_transformed = np.dot(working_C, self.proj_to_B)
        return C_transformed

class admm_ds:
    def __init__(self, rho=1, beta=0.2, epsilon=1e-5, max_iter=100, verbose=True, reg='lasso'):
        self.rho = rho
        self.beta = beta
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.verbose = verbose
        self.reg = reg

    def L2_norm(self, data):
        if len(data.shape) > 1:
            w = np.sqrt(np.sum(np.square(data), axis=1))
            data_normed = data / w[:, None]
        else:
            w = np.sqrt(np.sum(np.square(data), axis=0))
            data_normed = data / w
        return data_normed, w

    def undo_L2_norm(self, data_normed, w):

        if len(data_normed.shape) > 1:
            data = data_normed * w[:, None]
        else:
            data = data_normed * w
        return data

    def derive_transform(self, A, B):
        n = A.shape[1]
        P = np.zeros((n, n))
        Z = P.copy()
        Y = P.copy()

        A, Aw = self.L2_norm(A)
        B, Bw = self.L2_norm(B)

        AtA = np.dot(A.T, A)
        AtB = np.dot(A.T, B)
        if self.reg is 'fused':
            I = np.identity(n - 1)
            pos = np.hstack((I, np.zeros((len(I), 1))))
            neg = -1 * np.roll(pos, 1, 1)
            D = np.vstack(((pos + neg), np.zeros((1, len(I) + 1))))
            P_fact = cho_factor(AtA + self.rho * np.dot(D.T, D))
        else:
            P_fact = cho_factor(AtA + self.rho * np.eye(n))
        if self.reg is 'ridge':
            Z_fact = cho_factor(2 * np.eye(n) + self.rho * np.eye(n))

        for it in range(self.max_iter):
            last_P = P
            last_Z = Z
            if self.reg is 'fused':
                Z = ct.soft_thresh(np.dot(D, P) + (Y / self.rho), self.beta / self.rho)
            elif self.reg is 'rank':
                Z = ct.svt_thresh(P + (Y / self.rho), self.beta / self.rho)
            elif self.reg is 'ridge':
                Z = cho_solve(Z_fact, self.rho * P + Y)
            elif self.reg is 'sp_lr':
                Z = (ct.soft_thresh(P + (Y / self.rho), self.beta / self.rho) +
                     ct.svt_thresh(P + (Y / self.rho), self.beta / self.rho)) / 2.0
            elif self.reg is 'lasso':
                Z = ct.soft_thresh(P + (Y / self.rho), self.beta / self.rho)
            else:
                return 'ERROR: Regularizer not programmed.'
            if self.reg is 'fused':
                P = cho_solve(P_fact, AtB + self.rho * np.dot(D.T, Z) - np.dot(D.T, Y))
                Y += self.rho * (np.dot(D, P) - Z)
            else:
                P = cho_solve(P_fact, AtB + self.rho * Z - Y)
                Y += self.rho * (P - Z)
            P_conv = norm(P - last_P) / norm(P)
            Z_conv = norm(Z - last_Z) / norm(Z)
            if self.verbose:
                # num_zero = np.count_nonzero(P<=1e-9)
                if self.reg is 'fused':
                    print(it, P_conv, Z_conv, norm(np.dot(D, P) - Z), np.count_nonzero(Z), sum(svdvals(Z)))
                    print("score: %.4f" % (norm(np.dot(D, P) - Z) + norm(A - B.dot(Z))))
                else:
                    print(it, P_conv, Z_conv, norm(P - Z), np.count_nonzero(Z),
                          norm(Z, 1))  # ,sum(sp.linalg.svdvals(Z)))
                    print("score: %.4f" % (norm(P - Z) + norm(A - B.dot(Z))))
            if P_conv <= self.epsilon and Z_conv <= self.epsilon:
                break
        else:
            print("Didn't converge in %d steps" % self.max_iter)

        self.proj_to_B = P

    def apply_transform(self, C):
        C, Cw = self.L2_norm(C)
        C_proj_to_B = np.dot(C, self.proj_to_B)
        C_proj_to_B = self.undo_L2_norm(C_proj_to_B, Cw)

        return C_proj_to_B

class cca:
    def __init__(self, n_components=1, ccatype='new'):
        self.n_components = n_components
        self.ccatype = ccatype

    def derive_transform(self, A, B):
        self.model = CCA(n_components=self.n_components, scale=False).fit(A, B)
        if self.ccatype == 'new':
            # http://onlinelibrary.wiley.com/doi/10.1002/cem.2637/abstract
            F1 = np.linalg.pinv(self.model.x_scores_).dot(self.model.y_scores_)
            F2 = np.linalg.pinv(self.model.y_scores_).dot(B)
            P = ct.multi_dot((self.model.x_weights_, F1, F2))
            self.proj_to_B = P

        else:
            return self.model

    def apply_transform(self, C):
        if self.ccatype == 'new':
            return C.dot(self.proj_to_B)
        else:
            if len(C.shape) == 1:
                C = C.reshape(1, -1)
            return self.model.predict(C)

        return C

class ipd_ds:
    def __init__(self, t=.0002, svt=10, l1=10, epsilon=1e-5, max_iter=50, verbose=True):
        self.t = t
        self.svt = svt
        self.l1 = l1
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.verbose = verbose

    def derive_transform(self, A, B):
        # incremental proximal descent, Bertsekas 2010
        P = np.eye(A.shape[1])
        # P = np.zeros(B.shape[1])
        A = normalize(A, axis=1)
        B = normalize(B, axis=1)

        AtA = np.dot(A.T, A)
        AtB = np.dot(A.T, B)
        for it in range(self.max_iter):
            last_P = P.copy()
            P = P - self.t * (np.dot(AtA, P) - AtB)
            P = ct.svt_thresh(P, self.svt * self.t)
            P = ct.soft_thresh(P, self.l1 * self.t)
            P_conv = norm(P - last_P) / norm(P)
            if self.verbose:
                # svdsum = sum(sp.linalg.svdvals(P))
                # print(it, P_conv, norm(A-B.dot(P)), norm(P,1), svdsum)
                print(it, P_conv, norm(B - A.dot(P)), norm(P, 1))
                # print("score: %.4f" % (norm(A-B.dot(P))+norm(P,1)+svdsum))
            if P_conv <= self.epsilon:
                break
        else:
            print("Didn't converge in %d steps" % self.max_iter)

        self.proj_to_B = P

    def apply_transform(self, C):
        return np.dot(C, self.proj_to_B)

class forward_backward_ds:
    def __init__(self, t=0.001, svt=1, l1=1, epsilon=1e-5, max_iter=20, verbose=True):
        self.t = t
        self.svt = svt
        self.l1 = l1
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.verbose = verbose

    def derive_transform(self, A, B):
        P = np.zeros(B.shape[1])
        Z1 = P.copy()
        Z2 = P.copy()

        A = normalize(A, axis=1)
        B = normalize(B, axis=1)

        AtA = np.dot(A.T, A)
        AtB = np.dot(A.T, B)
        for it in range(self.max_iter):
            last_P = P.copy()
            G = np.dot(AtA, P) - AtB
            Z1 = ct.svt_thresh(2 * P - Z1 - self.t * G, 2 * self.svt * self.t)
            Z2 = ct.soft_thresh(2 * P - Z2 - self.t * G, 2 * self.l1 * self.t)
            P = (Z1 + Z2) / 2.0
            P_conv = norm(P - last_P) / norm(P)
            if self.verbose:
                print(it, P_conv)
            if P_conv <= self.epsilon:
                break
        else:
            print("Didn't converge in %d steps" % self.max_iter)
        self.proj_to_B = P

    def apply_transform(self,C):
        return np.dot(C,self.proj_to_B)
