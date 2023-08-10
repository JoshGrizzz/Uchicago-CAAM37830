import unittest
import numpy as np
from SIR import *
import math
"""
Tests operate by checking that functions evaluate to the correct answer
"""

class Test_agent(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_gotinfected(self):
        p = Person()
        
        self.assertTrue(p.infected == False)
        self.assertTrue(p.susceptible == True)
        
        p.got_infected()
        self.assertTrue(p.infected == True)
        self.assertTrue(p.susceptible == False)
        
    def test_gotremoved(self):
        p = Person()
        
        self.assertTrue(p.removed == False)
        p.got_infected()
        p.got_removed()
        self.assertTrue(p.infected == False)
        self.assertTrue(p.removed == True)
        
    def test_transition(self):
        p = Person()
        
        self.assertTrue(p.transition_time == 0)
        
        for i in range(5):
            p.transiton_to_removed()
            self.assertTrue(p.transition_time == i+1)
            
    def test_wearmask(self):
        p = Person()
        
        self.assertTrue(p.masked == False)
        p.WearMask()
        self.assertTrue(p.masked == True)
        
class Test_ODE(unittest.TestCase):
    def setUp(self):
        pass
    def test_sum_1(self):
        tol = 1e-4
        sol = Covid_SIR_Simulation_plot()
        Sol0 = sol.y[0]+sol.y[1]+sol.y[2]+sol.y[3]
        self.assertTrue(np.all(np.abs(Sol0-1)) < tol)

class Test_agent_spatial(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_gotinfected(self):
        p = Person_spatial(30,5000)
        
        self.assertTrue(p.infected == False)
        self.assertTrue(p.susceptible == True)
        self.assertTrue(p.N == 5000)# test initialization
        self.assertTrue(p.q == math.sqrt((3/500)/np.pi))
        
        p.got_infected()
        self.assertTrue(p.infected == True)
        self.assertTrue(p.susceptible == False)
        
    def test_gotremoved(self):
        p = Person_spatial(30,5000)
        
        self.assertTrue(p.removed == False)
        p.got_infected()
        p.got_removed()
        self.assertTrue(p.infected == False)
        self.assertTrue(p.removed == True)
        self.assertTrue(p.q == 0)
        
    def test_transition(self):
        p = Person_spatial(30,5000)
        
        self.assertTrue(p.transition_time == 0)
        
        for i in range(5):
            p.transiton_to_removed()
            self.assertTrue(p.transition_time == i+1)
            
    def test_wearmask(self):
        p = Person_spatial(30,5000)
        
        self.assertTrue(p.masked == False)
        p.WearMask()
        self.assertTrue(p.masked == True)
    
    def test_renew(self):
        p = Person_spatial(30,5000)
        
        p.got_infected()        
        p.renew()
        self.assertTrue(p.infected == False)
        self.assertTrue(p.susceptible == True)
        self.assertTrue(p.transition_time == 0)
        
        p.got_removed()
        p.transiton_to_removed()
        p.renew()
        self.assertTrue(p.infected == False)
        self.assertTrue(p.susceptible == True)
        self.assertTrue(p.transition_time == 0)
        
    def test_quarantine(self):
        p = Person_spatial(30,5000)
        
        p.quarantine(10)
        self.assertTrue(p.q == math.sqrt((1/500)/np.pi))
        
        
class Test_PDE(unittest.TestCase):
    def setUp(self):
        pass
    def test_sum(self):
        M = 200
        tol = 1e-3
        I = np.zeros((M,M))
        for i in range(5):
            for j in range(5):
                I[i+98, j+98] = 1
        sol = Covid_SIR_Spatial(I)
        s = np.mean(sol.y[:M**2], axis=0)
        i = np.mean(sol.y[M**2:2*M**2], axis=0)
        r = np.mean(sol.y[2*M**2:3*M**2], axis=0)
        sol0 = s+i+r
        self.assertTrue(np.all(np.abs(sol0-1)) < tol)
