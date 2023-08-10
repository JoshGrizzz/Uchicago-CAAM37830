import math
import random
import numpy as np
class Person_spatial():
    """
    A person can be either susceptible, infected or removed (recovered or deceased)
    Susceptible, infected and removed have been set as booleans.
    
    We also consider the factor of masks, the effectiveness of masks and quarantine.
    
    New Features: 2-d spatial component, b in the model will no longer necessary
    """
    
#    def __init__(self, p, orig_b_exposed, N):
    def __init__(self, orig_b_exposed, N):
        self.susceptible = True # By default
        self.infected = False
        self.removed = False
        self.masked = False
        self.transition_time = 0
        
        # spatial component information
        self.N = N
        self.pos_x = random.uniform(0, 1)
        self.pos_y = random.uniform(0, 1)
        self.pos = np.array([self.pos_x,self.pos_y]) # Position of the agent, will be assigned at the start of simulations
#        self.p = p # step length in random direction, will be generated for each simulation
        self.q = math.sqrt((orig_b_exposed/self.N)/np.pi) # interaction radius, determined by the original b
#        self.dpos = np.array([0,0])
#        self.temp_pos = np.array([0,0])
    
    def is_susceptible(self):
        return self.susceptible
    
    def is_infected(self):
        return self.infected
    
    def is_removed(self):
        return self.removed
    
    def is_masked(self):
        return self.masked
    
    def WearMask(self):
        self.masked = True
        
    def got_infected(self):
        self.infected = True
        self.susceptible = False
        
    def got_removed(self):
        self.infected = False
        self.removed = True
        self.q = 0
        
    def renew(self):
        self.susceptible = True 
        self.infected = False
        self.removed = False
        self.masked = False
        self.transition_time = 0
        
    def transiton_to_removed(self):
        self.transition_time += 1
    
    def quarantine(self, b_quarantine):
        # b_quarantine: expected contacts after quarantine
        self.q = math.sqrt((b_quarantine/self.N)/np.pi)
    
#    def move(self):
#        self.dpos = np.random.randn(2)
#        self.dpos = self.dpos / np.linalg.norm(self.dpos)
        
        # If move out of bound, the position stays unchanged
    
#        self.temp_pos = self.pos + self.dpos
#        if np.amax(self.temp_pos) <=1 and np.amin(self.temp_pos) >=0:
#            self.pos = self.temp_pos
