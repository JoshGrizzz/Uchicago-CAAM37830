class Person():
    """
    A person can be either susceptible, infected or removed (recovered or deceased)
    Susceptible, infected and removed have been set as booleans.
    
    We also consider the factor of masks, the effectiveness of masks and quarantine.
    """
    
    def __init__(self):
        self.susceptible = True # By default
        self.infected = False
        self.removed = False
        self.masked = False
        self.transition_time = 0
    
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
        
    def transiton_to_removed(self):
        self.transition_time += 1
    
        