import scipy.sparse as sparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# First we create the Laplacian (with weighting) under this setting
def forward_diff_matrix(n):
    data = []
    i = []
    j = []
    for k in range(n - 1):
        i.append(k)
        j.append(k)
        data.append(-1)

        i.append(k)
        j.append(k+1)
        data.append(1)
        
    return sparse.coo_matrix((data, (i,j)), shape=(n, n)).tocsr()

def backward_diff_matrix(n):
    data = []
    i = []
    j = []
    for k in range(1,n):
        i.append(k)
        j.append(k)
        data.append(1)

        i.append(k)
        j.append(k-1)
        data.append(-1)
        
    return sparse.coo_matrix((data, (i,j)), shape=(n, n)).tocsr()

def Laplacian_mtx(M):
    D = forward_diff_matrix(M) @ backward_diff_matrix(M)
    D[0,0] = -2
    D[M-1, M-2] = 1
    D[M-1, M-1] = -2
    Dx = sparse.kron(sparse.eye(M), D).tocsr()
    Dy = sparse.kron(D, sparse.eye(M)).tocsr()
    Lap = Dx + Dy
    Lap = Lap / (M**2)
    return Lap

# Then consider the M*M grid, our goal is to turn the pde problem into a system of odes

"""
The PDE system:
1. \partial s(x, t)/ \partial t = -b * s(x, t) * i(x, t) + p * L s(x, t)
2. \partial r(x, t)/ \partial t = k * i(x, t) + p * L r(x, t)
3. \partial i(x, t)/ \partial t = b * s(x, t) * i(x, t) - k * i(x, t) + p * L i(x, t)

b: same as before, infected individual has a fixed number b of contacts per day
p: use the parameter p to weight the diffusion term

What to solve: a system consisting of 3(M^2) ODEs.
How to achieve this goal: using np.flatten() and np.append()
"""

# Input I: initial infected on the grid setting

def Covid_SIR_Spatial(I, b=10, p=20, M=200, k = 0.05, time = 80):
    # N: initial un-infected population, M: grid size, I: initial infected M*M array, k: recovery rate
    # By hint from Dr. Nelson and Yian, each grid has entry value range from 0 to 1, which refers
    # to a probability referring to the current type
    R = np.zeros((M,M))
    S = np.ones((M,M))
    S = S-I
        
    # flatten, M*M -> 1*(M^2)   
    L = Laplacian_mtx(M)
    #L = laplace(M)
    
    S0 = S.flatten()
    I0 = I.flatten()
    R0 = R.flatten()
    
    # Now we set up the initial state by combining those up using np.append
    y0 = np.append(S0, I0)
    y0 = np.append(y0, R0)
    
    # \partial s(x, t)/ \partial t = -b * s(x, t) * i(x, t) + p * L s(x, t)
    # \partial r(x, t)/ \partial t = k * i(x, t) + p * L r(x, t)
    # \partial i(x, t)/ \partial t = b * s(x, t) * i(x, t) - k * i(x, t) + p * L i(x, t)
    
    # The set up the equations, note: S: 0~M^2, I: M^2~(2M^2-1), R: 2M^2~(3M^2-1), still we use lambda function
    f = lambda t, y : np.append(np.append(-b*y[:M**2]*y[M**2:2*M**2]+p*L@y[:M**2], b*y[:M**2]*y[M**2:2*M**2]-k*y[M**2:2*M**2]+p*L@y[M**2:2*M**2]), 
                                k*y[M**2:2*M**2]+p*L@y[2*M**2:3*M**2])
    
    t_span = [0, time]
    t_eval = np.linspace(0, time, time+1)
    
    sol = solve_ivp(f, t_span, y0, t_eval=t_eval)

    return sol

