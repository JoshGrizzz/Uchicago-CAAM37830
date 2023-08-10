import numpy as np
import random
from numpy.random import randint, rand
import matplotlib.pyplot as plt
import scipy as sp
import scipy.spatial
import scipy.spatial.distance as distance
from scipy.spatial import KDTree, cKDTree
#from Person_spatial import *

N = 5000 # population size that we are considering
prob_contact_infected = 0.037 # probability that a close contact is infected
prob_masked_effective = 0.6 #probability of not be infected wearing mask
prob_quarantined = 0.5 # probability a person is quarantined after being infected
T = 80
ki = 0.05 #recovery

step_lengths = [0.333, 0.667, 1]
b_exposed = [30, 45, 60]
b_quarantined = 10 # the number of interactions each day that could spread the disease (per infectious individual if quaratined)

def count_infected(pop): #number of infected
    return sum(p.is_infected() for p in pop)

def count_susceptible(pop): #number of susceptible
    return sum(p.is_susceptible() for p in pop)

def count_removed(pop): #number of removed
    return sum(p.is_removed() for p in pop)

def count_total(pop): #total_ever_infected
    return sum(p.is_infected() + p.is_removed() for p in pop)

for p in step_lengths:
    for b in b_exposed:
        print("Step length: " + str(p) + ", b_exposed" + str(b))
        X = np.zeros((N, 2))
        population = [Person_spatial(b, N) for i in range(N)]
        for i in range(N):
            X[i,0] = population[i].pos[0]
            X[i,1] = population[i].pos[1]
        for i in range(5): # 5 infected people at T=0
            population[i].got_infected()
            
        counts_s = [count_susceptible(population)]
        counts_i = [count_infected(population)]
        counts_r = [count_removed(population)]
        
        # Let every agent move (or stay), then spread the virus
        for t in range(T):
            infected_list = []# the list of infectious each day
            for i in range(N):
                # move, then update position
                #population[i].move()
                dpos = np.random.randn(2)
                dpos = p*dpos / np.linalg.norm(dpos)
        
        # If move out of bound, the position stays unchanged
    
                temp_pos = population[i].pos + dpos
        
                if np.amax(temp_pos) <=1 and np.amin(temp_pos) >=0:
                    population[i].pos = temp_pos
                   
                X[i,0] = population[i].pos[0]
                X[i,1] = population[i].pos[1]
            tree = KDTree(X)
            
            # detect infected and "let" them spread the disease
            for j in range(N):
                if population[j].is_infected():
                    infected_list.append(j)
                    # decide quarantine or not
                    if rand() < prob_quarantined:#if an infected person is quarantined
                        population[j].quarantine(b_quarantined)
                    # find the people within the radius
                    radius = population[j].q
                    x = [X[j, :]]
                    inds = tree.query_ball_point(x, radius) # finds neighbors in ball of radius
                    inds = inds[0]
                    for d in (inds):
                        if population[d].is_removed() == False:
                            # Suppose masks not effective, then person is exposed
                            if rand() >= prob_masked_effective: 
                                if rand() < prob_contact_infected: 
                                    population[d].got_infected()
                    population[d].transiton_to_removed()
                    # if a person is infected more than 14 days, he/she dies
                    if population[d].transition_time >= 14:
                        population[d].got_removed()
                        
            n_recover = np.int(ki*count_infected(population))# number of recovered today
            for i in random.sample(infected_list,n_recover):
                population[i].got_removed() # recovered
            counts_s.append(count_susceptible(population))
            counts_i.append(count_infected(population))
            counts_r.append(count_removed(population))
            
        plt.plot(counts_s, color = 'green', label='susceptible')
        plt.plot(counts_i, color = 'red', label='infected')
        plt.plot(counts_r, color = 'blue', label='removed')
        plt.xlabel('T (days)')
        plt.ylabel('number of people')
        plt.title('Spatial Component Introduced')
        plt.legend()
        plt.show()
