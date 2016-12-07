import numpy as np
from numpy.polynomial.hermite import hermvander
from pysat.spectral.baseline_code.common import Baseline
try:
  from cvxopt import matrix as cvx_matrix, solvers
  HAS_CVXOPT = True
except ImportError:
  cvx_matrix, solvers = None, None
  HAS_CVXOPT = False
  try:
    from scipy.optimize import linprog
  except ImportError:
    print('\nError: Use scipy >= 0.15 or install cvxopt\n')
    raise

np.set_printoptions(precision=4, suppress=True)
_callback_state = {'last_nit':0, 'last_phase':0}


def mario_baseline(bands, intensities, poly_order=10, max_iters=None,
                   verbose=False, tol=1e-2):
  '''Solves a linear program: min_u f'u s.t. -P'u <= -s
  Where u are coefficients of a Hermite polynomial.'''
  bands = bands.astype(float)
  intensities = intensities.astype(float)
  if max_iters is None:
    max_iters = len(bands) * 10
  opts = dict(maxiter=max_iters, disp=verbose, tol=tol)
  callback = _linprog_callback if verbose else None
  # Flip intensities upside down.
  maxval = intensities.max() + 500
  s = maxval - intensities
  # Keep trying to solve until we succeed.
  for order in range(poly_order, 0, -1):
    result, P = _mario_helper(bands, s, order, opts, callback)
    print('With order %d:' % order, result['status'])
    if result['x'] is not None:
      break
  else:
    print('mario_baseline didnt find a fit at any order')
    return np.zeros_like(s)
  baseline = P.dot(np.array(result['x']).ravel())
  # Flip it back over.
  return maxval - baseline


def _mario_helper(bands, s, poly_order, opts, callback):
  # Build the polynomial basis over the bands.
  P = hermvander(bands, poly_order-1)
  f = P.sum(axis=0)

  if HAS_CVXOPT:
    solvers.options['show_progress'] = opts['disp']
    solvers.options['maxiters'] = opts['maxiter']
    solvers.options['abstol'] = opts['tol']
    solvers.options['reltol'] = opts['tol']
    solvers.options['feastol'] = 1e-100  # For some reason this helps.
    try:
      res = solvers.lp(cvx_matrix(f), cvx_matrix(-P), cvx_matrix(-s))
    except ValueError as e:
      # This can be thrown when poly_order is too large for the data size.
      res = {'status': e.message, 'x': None}
    return res, P

  res = linprog(f, A_ub=-P, b_ub=-s, bounds=(-np.inf,np.inf), options=opts,
                callback=callback)
  res = {'status': res.message, 'x': res.x if res.success else None}
  return res, P


def _linprog_callback(xk, nit=0, phase=0, tableau=None, **kwargs):
  obj = -tableau[-1, -1]
  new_state = False
  if _callback_state['last_phase'] != phase:
    new_state = True
    _callback_state['last_phase'] = phase
  if phase == 1:
    if new_state:
      print('--- Phase 1: Find a feasible point. ---')
      print('Iter\tObjective')
    _callback_state['last_nit'] = nit
    print('%d\t%g' % (nit, obj))
  else:
    if new_state:
      print('--- Phase 2: Minimize using simplex. ---')
      print('Iter\tObjective')
    print('%d\t%g' % (nit - _callback_state['last_nit'], obj))


class Mario(Baseline):
  def __init__(self, poly_order=10, max_iters=None, verbose=False, tol=1e-2):
    self.poly_order_ = poly_order
    self.max_iters_ = max_iters
    self.verbose_ = verbose
    self.tol_ = tol

  def _fit_one(self, bands, intensities):
    return mario_baseline(bands, intensities, self.poly_order_,
                          self.max_iters_, self.verbose_, self.tol_)

  def param_ranges(self):
    return {'poly_order_': (1, 12, 'integer')}
