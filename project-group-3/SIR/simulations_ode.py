# This file are some simulations
from ODE_SIR import *
Covid_SIR_Simulation_plot(s = "SIR") # The most plain SIR model
Covid_SIR_Simulation_plot(s = "SIR", events_indicator = True) # Find the time that Susceptible drops down to almost 0
Covid_SIR_Simulation_plot(p = 0.8, q = 0.76, s = "SIR with masks") # Only consider masks
Covid_SIR_Simulation_plot(p = 0.8, q = 0.76, s = "SIR with masks", events_indicator = True)
Covid_SIR_Simulation_plot(p = 0.8, q = 0.76, g = 0.5, s = "SIR with masks and quarantine") # Consider masks and quarantine for patients
Covid_SIR_Simulation_plot(p = 0.8, q = 0.76, g = 0.5, t = 150, s = "SIR with masks and quarantine", events_indicator = True)
Covid_SIR_Simulation_plot(p = 0.8, q = 0.95, g = 0.2, t = 150, s = "SIR with high-pressure in 150 days") # High-Pressure rule 150 days: lockdown and mandatory masks
Covid_SIR_Simulation_plot(p = 0.8, q = 0.95, g = 0.2, t = 300, s = "SIR with high-pressure in 300 days") # High-Pressure rule 300 days: lockdown and mandatory masks