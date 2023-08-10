import numpy as np
import random
from numpy.random import randint, rand
import matplotlib.pyplot as plt
from SIR import *

"""
Q1. If infected individuals start at the center of the square, how does the total number of individuals infected in the simulation change with the parameter p?
"""

M = 200
# Initialize at center
I1 = np.zeros((M,M))
for i in range(5):
    for j in range(5):
        I1[i+98, j+98] = 1
    
    
step_lengths = np.array([0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1])*200
b_exposed = 15

for P in step_lengths:
    
    sol = Covid_SIR_Spatial(I1, b = b_exposed, p=P)
    plt.figure()
    infected = np.mean(sol.y[M**2:2*M**2], axis=0)
    total_infected = np.mean(1-sol.y[:M**2], axis=0)
    plt.plot(sol.t, infected, label="Infected", c='r')
    plt.plot(sol.t, total_infected, label="Total Infected", c='g')
    plt.xlabel("T(days)")
    plt.ylabel("propotion")
    plt.title('Spatial Component Introduced with p={} b={}, center'.format(P, b_exposed))
    plt.legend()
    plt.show()


"""
Q2. Choose an interesting parameter of p using question 1. How does the simulation qualitatively differ when the initial infected individuals start in a single corner of the square vs. the center of the square vs. being randomly spread out? You can investigate this by choosing initial conditions for i(x,0) appropriately.
"""

P = 0.6*200
M = 200
pos_list = ['center','corner','random']

# Initialize at corner
I2 = np.zeros((M,M))
for i in range(5):
    for j in range(5):
        I2[i, j] = 1
# Initialize at random
I2 = np.zeros((M,M))
for i in range(5):
    for j in range(5):
        p_x = np.random.randint(200)
        p_y = np.random.randint(200)
        I3[p_x, p_y] = 1

for pos in pos_list:
    
    I = np.zeros((M,M))
    if pos == 'center':
        I = I1
    if pos == 'corner':
        I = I2
    if pos == 'random':
        I = I3
    
    sol = Covid_SIR_Spatial(I, b = b_exposed, p=P)
    
    total_infected = np.mean(1-sol.y[:M**2], axis=0)
    plt.plot(sol.t, total_infected ,label = pos)

    #plt.figure()
    #plt.plot(sol.t, counts_infected, label="current infected", c='r')
    
#plt.text(sol.t[-1], counts_total[-1],(80, '%.0f' % counts_total[-1]) )
plt.xlabel("T (days)")
plt.ylabel("number of people")
plt.title('Spatial Component Introduced with initial infected position at {}'.format(pos))
plt.legend()
plt.show()
