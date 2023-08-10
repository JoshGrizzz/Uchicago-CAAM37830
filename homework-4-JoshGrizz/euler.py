"""
Defintions for problem 0
"""

import numpy as np
import scipy.integrate
from scipy.integrate import DenseOutput
from scipy.interpolate import interp1d

class ForwardEuler(scipy.integrate.OdeSolver):
    def __init__(self, fun, t0, y0, t_bound, vectorized=False, h = None):
        if h == None:
            h = (t_bound-t0)/100
        super(ForwardEuler, self).__init__(fun, t0, y0, t_bound, vectorized)
        self.h = h
        self.ts = []
        self.ys = []

    def _step_impl(self):
        self.ys.append(self.y)
        self.ts.append(self.t)
        h = self.h
        y = self.y
        t = self.t
        y_next = y + h * self.fun(t,y)
        t_next = t + h
        self.y = y_next
        self.t = t_next
        
        tol = 1e-5
        if np.abs(self.t-self.t_bound) < tol:
            self.t = self.t_bound
        
        return True, None
        
    def _dense_output_impl(self):
        return ForwardEulerOutput(ts, ys)

class ForwardEulerOutput(DenseOutput):
    """
    Interpolate ForwardEuler output
    """
    def __init__(self, ts, ys):

        """
        store ts and ys computed in forward Euler method

        These will be used for evaluation
        """
        super(ForwardEulerOutput, self).__init__(np.min(ts), np.max(ts))
        self.interp = interp1d(ts, ys, kind='linear', copy=True)


    def _call_impl(self, t):
        """
        Evaluate on a range of values
        """
        return self.interp(t)
