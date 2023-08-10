import numpy as np
import random
from numpy.random import randint, rand
import matplotlib.pyplot as plt
from SIR import *

N = 5000 # population size that we are considering
p = 0.037 # probability that a close contact is infected
prob_masked_effective = 0.6 #probability of not be infected wearing mask
prob_quarantined = 0.5 # probability a person is quarantined after being infected

k = [0.01, 0.05, 0.1] # the fraction of the infectious population which recovers each day
b_exposed = [30, 45, 60] # the number of interactions each day that could spread the disease (per infectious individual if not quaratined)
b_quaratined = 5 # the number of interactions each day that could spread the disease (per infectious individual if quaratined)

population = [Person() for i in range(N)]

for i in range(5): # 5 infected people at T=0
    population[i].got_infected()

def count_infected(pop): #number of infected
    return sum(p.is_infected() for p in pop)

def count_susceptible(pop): #number of susceptible
    return sum(p.is_susceptible() for p in pop)

def count_removed(pop): #number of removed
    return sum(p.is_removed() for p in pop)

def count_total(pop): #total_ever_infected
    return sum(p.is_infected() + p.is_removed() for p in pop)

'''
Question:
how s, i, and r change over the length of
the simulation for a couple different choices of k and b.
'''

#simulation

T = 80
counts_s = [count_susceptible(population)]
counts_i = [count_infected(population)]
counts_r = [count_removed(population)]

for ki in k:
    for bi in b_exposed:
        # initialization for every couple of bi and ki
        population = [Person() for i in range(N)] 

        for i in range(5): # 5 infected people at T=0
            population[i].got_infected()
            
        counts_s = [count_susceptible(population)]
        counts_i = [count_infected(population)]
        counts_r = [count_removed(population)]
        for t in range(T):
            infected_list = []# the list of infectious each day
            for i in range(N):
                if population[i].is_infected():
                    infected_list.append(i)
                    if rand() < prob_quarantined:#if an infected person is quarantined
                        b = b_quaratined
                    else:
                        b = bi
                
                    contacts = randint(N, size=b)
            
                    for j in contacts:
                        if population[j].is_removed() == False:
                            # Suppose masks not effective, then person is exposed
                            if rand() >= prob_masked_effective: 
                                if rand() < p: 
                                    population[j].got_infected()
                    population[i].transiton_to_removed()
                    # if a person is infected more than 14 days, he/she dies
                    if population[i].transition_time >= 14:
                        population[i].got_removed()
    
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
        plt.legend()
        plt.title('k={k}, b_exposed={b}, b_quarantined=5'.format(k=ki,b=bi))
        plt.show()

'''
Question:
how does the total percentage of
the population infected at some point 
in the simulation depend on these parameters? 
'''

def run_simulation(k, b_exposed, T, b_quaratined=5, N=5000, n=5):
    '''
    return number of s, i, r in day T and population that ever infected i_total
    parameters:
    k -- the fraction of the infectious population which recovers each day
    b_exposed -- the number of interactions each day(per infectious individual if not quaratined)
    b_quaratined -- the number of interactions each day(per infectious individual if quaratined)
    N -- population in total
    n -- initial number of infected
    T -- days
    '''
    
    # initialization for every couple of bi and ki
    population = [Person() for i in range(N)] 

    for i in range(n): # n infected people at T=0
        population[i].got_infected()
            
    for t in range(T):
        infected_list = []# the list of infectious each day
        for i in range(N):
            if population[i].is_infected():
                infected_list.append(i)
                if rand() < prob_quarantined:#if an infected person is quarantined
                    b = b_quaratined
                else:
                    b = b_exposed
                
                contacts = randint(N, size=b)
            
                for j in contacts:
                    if population[j].is_removed() == False:
                        # Suppose masks not effective, then person is exposed
                        if rand() >= prob_masked_effective: 
                            if rand() < p: 
                                population[j].got_infected()
                population[i].transiton_to_removed()
            
                if population[i].transition_time >= 14:
                    population[i].got_removed()# if a person is infected more than 14 days, he/she dies
    
        n_recover = np.int(ki*count_infected(population))# number of recovered today
        for i in random.sample(infected_list,n_recover):
            population[i].got_removed() # recovered
        
    s = count_susceptible(population)
    i = count_infected(population)
    r = count_removed(population)
    i_total = count_total(population)
        
    return s, i, r, i_total

#simulations; Take T=20 as an example
N=5000
ks = np.logspace(-2,0, 10)
bs = np.arange(30, 60, dtype=np.int64)

cts = np.zeros((len(ks), len(bs)))
for i, k in enumerate(ks):
    for j, b in enumerate(bs):
        s,infected,r,i_total = run_simulation(k, b, T=20, b_quaratined=5, N=N, n=5)
        cts[i,j]=i_total/N

plt.figure(figsize=(10,5))
plt.imshow(cts, extent=[np.min(bs), np.max(bs), np.max(ks), np.min(ks)])
plt.colorbar()
plt.yscale('log')
plt.xlabel('b_exposed')
plt.ylabel('k')
plt.title('Total percentage of the population infected at T=20')

plt.show()
