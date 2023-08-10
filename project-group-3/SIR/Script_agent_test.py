from numpy.random import randint, rand
import matplotlib.pyplot as plt
from Person import *

N = 5000 # population size that we are considering
p = 0.037 # probability that a close contact is infected
prob_masked_effective = 0.6
prob_quarantined = 0.5 # quarantine

population = [Person() for i in range(N)]

for i in range(5):
    population[i].got_infected()

def count_infected(pop):
    return sum(p.is_infected() for p in pop)

def count_total(pop):
    return sum(p.is_infected() + p.is_removed() for p in pop)

T = 120
counts = [count_infected(population)]
Total_ever_infected = [count_total(population)]

for t in range(T):
    for i in range(N):
        if population[i].is_infected():
            if rand() < prob_quarantined:
                k = randint(5)
            else:
                k = randint(30) # limit: assume a person can meet at most 30 people a day
                
            contacts = randint(N, size=k)
            for j in contacts:
                if population[j].is_removed() == False:
                    if rand() >= prob_masked_effective: # Suppose masks not effective, then person is exposed
                        if rand() < p: 
                            population[j].got_infected()
            population[i].transiton_to_removed()
            if population[i].transition_time >= 14:
                population[i].got_removed()
    counts.append(count_infected(population))
    Total_ever_infected.append(count_total(population))

plt.plot(counts)
plt.plot(Total_ever_infected, color = 'red')
plt.show()
