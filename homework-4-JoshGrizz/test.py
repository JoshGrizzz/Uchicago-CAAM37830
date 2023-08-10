"""
Implement tests for Problem 0 Part C
"""
import unittest
from scipy.integrate import solve_ivp
from euler import*
import numpy as np

# Key condition: |dy_hat(t) - y(t)| < y(t) * h

class Test_Solve_Ivp(unittest.TestCase):
    
    def setUp(self):
            pass

    # Test for Euler Forward Method   
        
    def test_Euler(self):
        # Key condition: |dy_hat(t) - y(t)| < y(t) * h
        # Using forward_difference(g, x, h): (g(x + h) - g(x)) / h
        
        v0 = np.array([1])
        f = lambda t, v: v
        # Test for h = 0.01
        t_span = (0,5)
        sol1 = solve_ivp(f, t_span, v0, method = ForwardEuler, h=0.01)
        sol2 = solve_ivp(f, t_span, v0, method = ForwardEuler, h=0.0001) # step size smaller than h
        Sol1 = sol1.y[0]
        Sol2 = sol2.y[0]
        
        # Implement test for three points
        self.assertTrue(np.abs((Sol2[1001] - Sol2[1000])/0.0001 - Sol1[10]) < Sol1[10]*0.01)
        self.assertTrue(np.abs((Sol2[10001] - Sol2[10000])/0.0001 - Sol1[100]) < Sol1[100]*0.01)
        self.assertTrue(np.abs((Sol2[15001] - Sol2[15000])/0.0001 - Sol1[150]) < Sol1[150]*0.01)
        self.assertTrue(np.abs((Sol2[20001] - Sol2[20000])/0.0001 - Sol1[200]) < Sol1[200]*0.01)
        
        # Using center_difference(g, x, h): (g(x + h) - g(x-h)) / 2h
        
        self.assertTrue(np.abs((Sol2[1001] - Sol2[999])/0.0002 - Sol1[10]) < Sol1[10]*0.01)
        self.assertTrue(np.abs((Sol2[10001] - Sol2[9999])/0.0002 - Sol1[100]) < Sol1[100]*0.01)
        self.assertTrue(np.abs((Sol2[15001] - Sol2[14999])/0.0002 - Sol1[150]) < Sol1[150]*0.01)
        self.assertTrue(np.abs((Sol2[20001] - Sol2[19999])/0.0002 - Sol1[200]) < Sol1[200]*0.01)
        
    # Test for Default IVP Method: compare with a reasonable tolerance      
        
    def test_default(self):
        tol = 5e-2
        v0 = np.array([1])
        f = lambda t, v: v
        # Test for h = 0.01
        t_span = (0,5)
        t_eval = np.linspace(0, 5, 5001)
        sol1 = solve_ivp(f, t_span, v0, t_eval=t_eval)
        Sol1 = sol1.y[0]
        self.assertTrue(np.abs((Sol1[101] - Sol1[99])/0.002 - Sol1[100]) < tol)
        self.assertTrue(np.abs((Sol1[1001] - Sol1[999])/0.002 - Sol1[1000]) < tol)
        self.assertTrue(np.abs((Sol1[1501] - Sol1[1499])/0.002 - Sol1[1500]) < tol)
        self.assertTrue(np.abs((Sol1[2001] - Sol1[1999])/0.002 - Sol1[2000]) < tol)
        