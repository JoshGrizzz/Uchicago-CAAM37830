import numpy as np
import random
from numpy.random import randint, rand
import matplotlib.pyplot as plt
import scipy as sp
import scipy.spatial
import scipy.spatial.distance as distance
from scipy.spatial import KDTree, cKDTree
from Person_spatial import *

N = 5000 # population size that we are considering
prob_contact_infected = 0.037 # probability that a close contact is infected
prob_masked_effective = 0.6 #probability of not be infected wearing mask
prob_quarantined = 0.5 # probability a person is quarantined after being infected
T = 80
ki = 0.05 #recovery

b_quarantined = 10 # the number of interactions each day that could spread the disease (per infectious individual if quaratined)

def count_infected(pop): #number of infected
    return sum(p.is_infected() for p in pop)

def count_susceptible(pop): #number of susceptible
    return sum(p.is_susceptible() for p in pop)

def count_removed(pop): #number of removed
    return sum(p.is_removed() for p in pop)

def count_total(pop): #total_ever_infected
    return sum(p.is_infected() + p.is_removed() for p in pop)

"""
Q1. If infected individuals start at the center of the square, how does the total number of individuals infected throughout the simulation change with the parameter p?
"""
"""
Set p = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1]
b_exposed = 30 (when q is approximately 0.44)
"""

step_lengths = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1]
b_exposed = 30

X = np.zeros((N, 2))
population = [Person_spatial(b_exposed, N) for i in range(N)]
for i in range(N):
    X[i,0] = population[i].pos[0]
    X[i,1] = population[i].pos[1]
for i in range(5): # 5 infected people at T=0
    population[i].got_infected()
    population[i].pos = np.array([0.5,0.5])  
    
X_initial = X # save the initial position

for p in step_lengths:
    #for b in b_exposed:
    for i in range(N): # To make variables be better controlled, we have to let the status of population back to the beginning
        population[i].renew()
        X = X_initial
        for i in range(N):
            population[i].pos[0] = X[i,0]
            population[i].pos[1] = X[i,1]
        for i in range(5): # the same 5 initial infected people
            population[i].got_infected()
            population[i].pos = np.array([0.5,0.5])  
        
    print("Step length: " + str(p) + ", b_exposed: " + str(b_exposed)) 
        
    counts_i = [count_infected(population)]
    counts_total = [count_total(population)]
        
    # Let every agent move (or stay), then spread the virus
    for t in range(T):
        infected_list = []# the list of infectious each day
        
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
       
        counts_i.append(count_infected(population))
        counts_total.append(count_total(population))
        
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
        
    plt.plot(counts_i, color = 'red', label='current infected')
    plt.plot(counts_total, color = 'blue', label='total infected')
    plt.text(80, counts_total[-1],(80, counts_total[-1]) )
    plt.xlabel('T (days)')
    plt.ylabel('number of people')
    plt.title('Spatial Component Introduced with p={} q={}'.format(p,math.sqrt((b_exposed/N)/np.pi)))
    plt.legend()
    plt.show()
    
"""
limit the range of p to [0.01,0.1] and plot lines in one graph with labels
take b_exposed = 60 (when q is approximately 0.6)
"""

step_lengths = np.linspace(0.01,0.1,10)
b_exposed = 60

X = np.zeros((N, 2))
population = [Person_spatial(b_exposed, N) for i in range(N)]
for i in range(N):
    X[i,0] = population[i].pos[0]
    X[i,1] = population[i].pos[1]
for i in range(5): # 5 infected people at T=0
    population[i].got_infected()
    population[i].pos = np.array([0.5,0.5])  
    
X_initial = X # save the initial position

for p in step_lengths:
    #for b in b_exposed:
    for i in range(N): # To make variables be better controlled, we have to let the status of population back to the beginning
        population[i].renew()
        X = X_initial
        for i in range(N):
            population[i].pos[0] = X[i,0]
            population[i].pos[1] = X[i,1]
        for i in range(5): # the same 5 initial infected people
            population[i].got_infected()
            population[i].pos = np.array([0.5,0.5])  
        
    #print("Step length: " + str(p) + ", b_exposed: " + str(b_exposed)) 
        
    #counts_i = [count_infected(population)]
    counts_total = [count_total(population)]
        
    # Let every agent move (or stay), then spread the virus
    for t in range(T):
        infected_list = []# the list of infectious each day

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
       
        #counts_i.append(count_infected(population))
        counts_total.append(count_total(population))
        
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
    #plt.plot(counts_i, color = 'red', label='current infected')
    plt.plot(counts_total, label = 'p={}'.format('%.2f' % p))
        
plt.xlabel('T (days)')
plt.ylabel('number of people')
plt.title('Spatial Component Introduced with q={}'.format(math.sqrt((b_exposed/N)/np.pi)))
plt.legend()
plt.show()

"""
Q2.Choose an interesting parameter of p using question 1. How does the simulation qualitatively differ when the initial infected individuals start in a single corner of the square vs. the center of the square vs. being randomly spread out? PDE model
"""

p = 0.05
b_exposed = 30
pos_list = ['center','corner','random']
X = np.zeros((N, 2))

population = [Person_spatial(b_exposed, N) for i in range(N)] # initialization
for i in range(N):
    X[i,0] = population[i].pos[0]
    X[i,1] = population[i].pos[1]
    
X_initial = X # save the initial position



#for p in step_lengths:
for m in range(3): # switch the position of initial infected individuals
    #for b in b_exposed:
    X = np.zeros((N, 2))
    population = [Person_spatial(b_exposed, N) for i in range(N)]
    
    for i in range(N): # To make variables be better controlled, we have to let the status of population back to the beginning
        population[i].renew()
        X = X_initial
        for i in range(N):
            population[i].pos[0] = X[i,0]
            population[i].pos[1] = X[i,1]
       
    for i in range(5): # 5 infected people at T=0
        population[i].got_infected()
        if m == 0: # start in a center of the square 
            population[i].pos = np.array([0.5,0.5]) 
        if m == 1: # start in a single corner of the square
            population[i].pos = np.array([0,0]) 
        #if m == 2:  randomly spread out
            
    #print("Step length: " + str(p) + ", b_exposed: " + str(b_exposed)) 
        
    #counts_i = [count_infected(population)]
    counts_total = [count_total(population)]
        
    # Let every agent move (or stay), then spread the virus
    for t in range(T):
        infected_list = []# the list of infectious each day
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
       
        #counts_i.append(count_infected(population))
        counts_total.append(count_total(population))
        
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
    #plt.plot(counts_i, color = 'red', label='current infected')
    plt.plot(counts_total, label = pos_list[m])
    #plt.text(40+5*m, counts_total[40+5*m],'p={}'.format(p) )
        
plt.xlabel('T (days)')
plt.ylabel('number of people')
plt.title('Spatial Component Introduced with different initial infected position')
plt.legend()
plt.show()
