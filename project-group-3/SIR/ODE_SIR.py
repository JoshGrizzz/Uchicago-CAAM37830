import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Things and formulas that we need to consider

"""
Naive SIR model implementation

I. Some explanations and head-ups:

I. About the parameters
p: mask effectiveness, default is 0
q: proportion of people who wear masks, default is 0
g: quarantine level, default is 1, which refers to no quarantine. 0 refers to perferct quarantine.
k: fixed fraction k of the infected group will recover during any given day
d: fixed fraction d of the infected group will die during any given day
b: infected individual has a fixed number b of contacts per day

II. About the variables

Let N be total number of people
s(t) = S(t)/N
i(t) = I(t)/N
r(t) = R(t)/N
d(t) = D(t)/N

III. Implementations

Note we may let y = transpose[s, i, r, d]. Then our equations turn into:
y0'(t) = -b*g*(1-p*q)*s(t)*i(t) = -b*g*(1-p*q)*y0*y1
y1'(t) = b*g*(1-p*q)*s(t)*i(t)-k*i(t)-d*i(t) = b*g*(1-p*q)*y0*y1-k*y1-d*y1
y2'(t) = k*i(t) = k*y1
y3'(t) = d*i(t) = d*y1

The we may start implementing this with initial value of N = 5000, k = 0.05, d = 0.0025 and b = 2. 
Also assume we have 0.1% of affected people at time 0.

IV. Case that we are considering

Case A: no protections
Case B: only protection is mask, while not all people are wearing masks
Case C: masks with patients quarantined
Case D: High Pressure: lockdown (more strict quarantine) and mandatory masks

"""   

# Use this method to plot the simulations in a fixed time scope
def Covid_SIR_Simulation_plot(N=5000, b=2, p=0, q=0, g=1, k=0.05, d=0.0025, s0=0.999, i0=0.001, r0=0, d0=0, t=200, s="", events_indicator = False):
    """
    Use this method to plot the simulations for Covid_19: some coefficients are default but changeable
    p: mask effectiveness, default is 0
    q: proportion of people who wear masks, default is 0
    r: quarantine level, default is 1, which refers to no quarantine. 0 refers to perferct quarantine.
    k: fixed fraction k of the infected group will recover during any given day
    d: fixed fraction d of the infected group will die during any given day
    b: infected individual has a fixed number b of contacts per day, default is 2
    events_indicator: Consider the given events or not
    """
    
    # Event: Susceptible reach almost 0, i.e, all infected or removed
    def Susceptible_al1(t, y): 
        return y[0] - 1e-2
    Susceptible_al1.terminal = True
    direction = -1
    y0 = np.array([s0, i0, r0, d0])
    f = lambda t, y : np.array([-b*g*(1-p*q)*y[0]*y[1], b*g*(1-p*q)*y[0]*y[1]-k*y[1]-d*y[1], k*y[1], d*y[1]])
    t_span = (0, t)
    t_eval = np.linspace(0, t, 2*t)
    
    if events_indicator == True:
        sol = solve_ivp(f, t_span, y0, t_eval=t_eval, events=Susceptible_al1)
    else:
        sol = solve_ivp(f, t_span, y0, t_eval=t_eval)
    
    plt.figure()
    plt.plot(sol.t, sol.y[0], label="Susceptibles", c='b')
    plt.plot(sol.t, sol.y[1], label="Infected", c='r')
    plt.plot(sol.t, sol.y[2], label="Recovered", c='g')
    plt.plot(sol.t, sol.y[3], label="Dead", c='k')
    plt.plot(sol.t, sol.y[2] + sol.y[3], label="Removed", c='purple')

    plt.title(s)
    plt.xlabel("time span/days")
    plt.ylabel("population")
    plt.legend()
    plt.show()
    return sol


