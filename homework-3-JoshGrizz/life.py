"""
life.py

Put any requested function or class definitions in this file.  You can use these in your script.

Please use comments and docstrings to make the file readable.
"""

import numpy as np
import scipy as sp
import scipy.sparse as sparse
import scipy.sparse.linalg as sla

# Part B

# Generate the adjacentcy matrix for given m*n grid
def grid_adjacency(m,n):
    """
    returns the adjacency matrix for an m x n grid
    """
    mn = m*n
    
    # Construct using sparse.lil_matrix. Explanation has been given in script.py
    
    A = sparse.lil_matrix((mn,mn), dtype = np.int8) # np.int8 is enough for our case. Just to save some memory.
    for i in range(m):
        for j in range(n):
            iNeighbors = [-1, 0, 1]
            if i == 0:
                iNeighbors = [0, 1]
            if i == m-1:
                iNeighbors = [-1, 0]
        
            jNeighbors = [-1, 0, 1]
            if j == 0:
                jNeighbors = [0, 1]
            if j == n-1:
                jNeighbors = [-1, 0]
                
            # Avoid using ravel here, since it is super slow
            
            k1 = i * n + j

            for delta_i in iNeighbors:
                for delta_j in jNeighbors:
                    # if not having two zero's, go on and change
                    if delta_i != 0 or delta_j != 0:
                        k2 = (i + delta_i) * n + (j + delta_j)
                        A[k1,k2] = 1
    return A


# Part C

# Multiplication between a sparse matrix and flattened version of S
def count_alive_neighbors_matmul(S, A):
    """
    return counts of alive neighbors in the state array S.

    Uses matrix-vector multiplication on a flattened version of S
    """
    
    return np.reshape(A @ S.flatten(), S.shape)

# Considering all eight directions to directly get the results
def count_alive_neighbors_slice(S):
    """
    return counts of alive neighbors in the state array S.

    Uses matrix-vector multiplication on a flattened version of S
    """
    
    cts = np.zeros(S.shape)
    cts[1:, :] = cts[1:, :] + S[:-1, :]
    cts[:-1,:] = cts[:-1,:] + S[1:, :]
    cts[:,1:] = cts[:,1:] + S[:, :-1]
    cts[:,:-1] = cts[:,:-1] + S[:, 1:]
    cts[1:, 1:] = cts[1:, 1:] + S[:-1, :-1]
    cts[:-1, :-1] = cts[:-1, :-1] + S[1:, 1:]
    cts[1:, :-1] = cts[1:, :-1] + S[:-1, 1:]
    cts[:-1, 1:] = cts[:-1, 1:] + S[1:, :-1]
    
    
    return cts
            
