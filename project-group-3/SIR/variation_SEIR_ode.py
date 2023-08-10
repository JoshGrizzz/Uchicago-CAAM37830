import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

"""
SEIR model implementation: E refers to Exposed, further details will be discussed in the next part

I. Some explanations and head-ups:

I. About the parameters
p: mask effectiveness, default is 0
q: proportion of people who wear masks, default is 0
g: quarantine level, default is 1, which refers to no quarantine. 0 refers to perferct quarantine.
k: fixed fraction k of the infected group will recover during any given day
d: fixed fraction d of the infected group will die during any given day
b: infected individual has a fixed number b of contacts per day
v: environmental factor of virus transmission, which is designed to be relatively small
w: transmission rate from "Exposed" to infectious

II. About the variables

SEIR model has some differences with the basic SIR model: let N be total number of people (population), S refers to the number of susceptible people; E refers to the number of "exposed", which means infected but not yet infectious; I, here, refers to the number of infectious people (note the difference between the basic SIR model; R refers to the number of recovered people and D refers to the number of deaths.

Thus:

s(t) = S(t)/N
e(t) = E(t)/N
i(t) = I(t)/N
r(t) = R(t)/N
d(t) = D(t)/N

Note that there are two equalities that always hold, for any choice of valid t:
a. S + E + I + R + D = N
b  s + e + i + r + d = 1

III. Implementations

Before we do the implementations, we need to notice one really important thing for this model: when a susceptible person "catches" the virus, no matter from infected people or from environment, he/she becomes an "exposed" person. This is the core of this model: a person does not get infectious once get infected; instead, there is an incubation period.

Note we may let y = transpose[s, e, i, r, d]. Then our equations turn into:
ds/dt = y0'(t) = -b*g*(1-p*q)*s(t)*i(t) - v*(1-p*q)*s(t)= -b*g*(1-p*q)*y0*y2 - v*(1-p*q)*y0
de/dt = y1'(t) = b*g*(1-p*q)*s(t)*i(t) + v*(1-p*q)*s(t) - w*e(t) = b*g*(1-p*q)*y0*y2 + v*(1-p*q)*y0 - w * y1
di/dt = y2'(t) = w*e(t)-k*i(t)-d*i(t) = w*y1 - k*y2 - d*y2
dr/dt = y3'(t) = k*i(t) = k*y2
dd/dt = y4'(t) = d*i(t) = d*y2

The we may start implementing this with larger initial value of N = 1000000, k = 0.05, d = 0.0025 and b = 2. 
Also assume we have 0.1% of infectious(I) people at time 0.

IV. Case that we are considering

Case A: no protections
Case B: only protection is mask, while not all people are wearing masks
Case C: masks with patients quarantined
Case D: High Pressure: lockdown (more strict quarantine) and mandatory masks

"""   

def Variation_SEIR_Simulation_plot(N=1000000, b=2, p=0, q=0, g=1, k=0.05, d=0.0025, v=0.25, w=0.15, s0=0.999, e0=0, i0=0.001, r0=0, d0=0, t=200, s="", events_indicator = False):
    """
    Use this method to plot the simulations for Covid_19: some coefficients are default but changeable
    p: mask effectiveness, default is 0
    q: proportion of people who wear masks, default is 0
    r: quarantine level, default is 1, which refers to no quarantine. 0 refers to perferct quarantine.
    k: fixed fraction k of the infected group will recover during any given day
    d: fixed fraction d of the infected group will die during any given day
    b: infected individual has a fixed number b of contacts per day, default is 2
    v: environmental factor of virus transmission, which is designed to be relatively small
    w: transmission rate from "Exposed" to infectious
    events_indicator: Consider the given events or not
    """
    
    # Event: Susceptible reach almost 0, i.e, all infected or removed
    def Susceptible_al1(t, y): 
        return y[0] - 1e-2
    Susceptible_al1.terminal = True
    direction = -1
    y0 = np.array([s0, e0, i0, r0, d0])
    f = lambda t, y : np.array([-b*g*(1-p*q)*y[0]*y[2]-v*(1-p*q)*y[0]
                                ,b*g*(1-p*q)*y[0]*y[2] + v*(1-p*q)*y[0] - w * y[1],
                                w*y[1] - k*y[2] - d*y[2], k*y[2], d*y[2]])
    t_span = (0, t)
    t_eval = np.linspace(0, t, 2*t)
    
    if events_indicator == True:
        sol = solve_ivp(f, t_span, y0, t_eval=t_eval, events=Susceptible_al1)
    else:
        sol = solve_ivp(f, t_span, y0, t_eval=t_eval)
    
    plt.figure()
    plt.plot(sol.t, sol.y[0], label="Susceptibles", c='b')
    plt.plot(sol.t, sol.y[1], label="Exposed", c='r')
    plt.plot(sol.t, sol.y[2], label="Infectious", c='g')
    plt.plot(sol.t, sol.y[3], label="Recovered", c='k')
    plt.plot(sol.t, sol.y[4], label="Dead", c='y')
    plt.plot(sol.t, sol.y[3] + sol.y[4], label="Removed", c='purple')

    plt.title(s)
    plt.xlabel("time span/days")
    plt.ylabel("population")
    plt.legend()
    plt.show()
    return sol

Variation_SEIR_Simulation_plot(s = "SEIR") # The most plain SEIR model
Variation_SEIR_Simulation_plot(s = "SEIR", events_indicator = True) # Find the time that Susceptible drops down to almost 0
Variation_SEIR_Simulation_plot(p = 0.8, q = 0.76, s = "SEIR with masks") # Only consider masks
Variation_SEIR_Simulation_plot(p = 0.8, q = 0.76, s = "SEIR with masks", events_indicator = True)
Variation_SEIR_Simulation_plot(p = 0.8, q = 0.76, g = 0.5, s = "SEIR with masks and quarantine") # Consider masks and quarantine for patients
Variation_SEIR_Simulation_plot(p = 0.8, q = 0.76, g = 0.5, t = 150, s = "SEIR with masks and quarantine", events_indicator = True)
Variation_SEIR_Simulation_plot(p = 0.8, q = 0.95, g = 0.2, t = 150, s = "SEIR with high-pressure in 150 days") # High-Pressure rule 150 days: lockdown and mandatory masks
Variation_SEIR_Simulation_plot(p = 0.8, q = 0.95, g = 0.2, t = 300, s = "SEIR with high-pressure in 300 days") # High-Pressure rule 300 days: lockdown and mandatory masks
