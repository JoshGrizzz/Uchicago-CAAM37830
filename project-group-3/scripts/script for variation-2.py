import numpy as np
import random
from numpy.random import randint, rand
import matplotlib.pyplot as plt
from SIR import *

N = 5000 # population size that we are considering
p_infectivity =[0.04 , 0.08 , 0.16, 0.32] # probability that a close contact is infected
prob_masked_effective = 0.6 #probability of not be infected wearing mask
prob_quarantined = 0.5 # probability a person is quarantined after being infected

k = 0.05
b_exposed = 30
b_quaratined = 5

T = 80

for p in p_infectivity:
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
                    b = b_exposed
                
                contacts = randint(N, size=b)# the randomness of the number of interactions
            
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
    
        n_recover = np.int(k*count_infected(population))# number of recovered today
        for i in random.sample(infected_list,n_recover):
            population[i].got_removed() # recovered
       
        #counts_s.append(count_susceptible(population))
        counts_i.append(count_infected(population))
        #counts_r.append(count_removed(population))
            
    #plt.plot(counts_s, color = 'green', label='susceptible')
    plt.plot(counts_i, label='p_infectivity={}'.format(p))
    #plt.plot(counts_r, color = 'blue', label='removed')
plt.xlabel('T (days)')
plt.ylabel('number of people')
plt.legend()
plt.title('Different infectivity of diseases')
plt.show()


