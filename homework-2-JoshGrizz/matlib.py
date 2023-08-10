"""
matlib.py

Put any requested function or class definitions in this file.  You can use these in your script.

Please use comments and docstrings to make the file readable.
"""
import numpy as np
import scipy as sp
import scipy.linalg as la
import time
from numba import njit

# Problem 0
    
# Part A

def solve_chol(A, b):
    """
    Cholesky: A = L * (L^T), then Ax = b is changed to L * (L^T) * x = b
    Solve: First get the Cholesky factorization, then get c such that L * c = b. 
    Nextly get the solution for (L^T) * x = c
    """
    L = la.cholesky(A, lower = True)
    c = la.solve(L, b)
    sol = la.solve(L.T, c)
    return sol

# Part C

def matrix_pow(A, n):
    """
    Here suppose A is symmetric: we use eigen-decompostion to facilatate the calculation of A^n
    """
    Lam, X = la.eig(A)
    m = Lam.shape[0]
    for i in range (m):
        Lam[i] = np.power(Lam[i], n)
    return X @ np.diag(Lam) @ X.T
    
# Part D

def abs_det(A):
    """
    Use LU factorization, i.e, PLU = A. 
    Then to get the abs. determinant of A, we just need to get determinants of L and U
    for the determinants: for upper/lower triangular matrices, we only need to multiply the diagonal entries together
    """
    
    P, L, U = la.lu(A)
    n = A.shape[0]
    detL = detU = 1;
    for i in range (n):
        detU = detU * abs(U[i,i])
    return detL * detU
    
    
# Problem 1

# PartA: Six multiplication algorithms:

# ijk matrix multiplication of B and C: equivalent to B @ C
@njit
def matmul_ijk(B, C):
    """
    ijk-order matrix multiplication of B and C
    """
    p = B.shape[0]
    q = C.shape[1]
    r = B.shape[1]
    A = np.zeros((p, q))
    for i in range(p):
        for j in range(q):
            for k in range(r):
                A[i,j] = A[i,j] + B[i,k] * C[k,j]
    return A

# ikj
@njit
def matmul_ikj(B, C):
    """
    ikj-order matrix multiplication of B and C
    """
    p = B.shape[0]
    q = C.shape[1]
    r = B.shape[1]
    A = np.zeros((p, q))
    for i in range(p):
        for k in range(r):
            for j in range(q):
                A[i,j] = A[i,j] + B[i,k] * C[k,j]
    return A

# jik
@njit
def matmul_jik(B, C):
    """
    jik-order matrix multiplication of B and C
    """
    p = B.shape[0]
    q = C.shape[1]
    r = B.shape[1]
    A = np.zeros((p, q))
    for j in range(q):
        for i in range(p):
            for k in range(r):
                A[i,j] = A[i,j] + B[i,k] * C[k,j]
    return A

# jki
@njit
def matmul_jki(B, C):
    """
    jki-order matrix multiplication of B and C
    """
    p = B.shape[0]
    q = C.shape[1]
    r = B.shape[1]
    A = np.zeros((p, q))
    for j in range(q):
        for k in range(r):
            for i in range(p):
                A[i,j] = A[i,j] + B[i,k] * C[k,j]
    return A

# kij
@njit
def matmul_kij(B, C):
    """
    kij-order matrix multiplication of B and C
    """
    p = B.shape[0]
    q = C.shape[1]
    r = B.shape[1]
    A = np.zeros((p, q))
    for k in range(r):
        for i in range(p):
            for j in range(q):
                A[i,j] = A[i,j] + B[i,k] * C[k,j]
    return A

# kji
@njit
def matmul_kji(B, C):
    """
    kji-order matrix multiplication of B and C
    """
    p = B.shape[0]
    q = C.shape[1]
    r = B.shape[1]
    A = np.zeros((p, q))
    for k in range(r):
        for j in range(q):
            for i in range(p):
                A[i,j] = A[i,j] + B[i,k] * C[k,j]
    return A


# Part B: Blocked matrix multiplication

@njit
def matmul_blocked(B, C):
    """
    A[I, J] = A[I, J] + B[I, K] @ C[K, J]
    """
    n = B.shape[0]
    A = np.zeros((n, n))
    slices = (slice(0, n//2), slice(n//2, n))
    if n <= 64:
        A = matmul_ikj(B,C)
    
    else:
        for I in slices:
            for J in slices:
                for K in slices:
                    A[I,J] = A[I, J] + matmul_blocked(B[I, K], C[K, J])
    return A

# Part C

@njit
def matmul_strassen(B, C):
    """
    Strassen implementation of Matrix Multiplication
    """
    n = B.shape[0]
    A = np.zeros((n, n))
    s1 = slice(0, n//2)
    s2 = slice(n//2, n)

    B11, B12, B21, B22 = B[s1,s1], B[s1,s2], B[s2, s1], B[s2, s2]
    C11, C12, C21, C22 = C[s1,s1], C[s1,s2], C[s2, s1], C[s2, s2]

    M1 = matmul_kij((B11 + B22),(C11 + C22))
    M2 = matmul_kij((B21 + B22), C11)
    M3 = matmul_kij(B11, (C12 - C22))
    M4 = matmul_kij(B22, (C21 - C11))
    M5 = matmul_kij((B11 + B12), C22)
    M6 = matmul_kij((B21 - B11), (C11 + C12))
    M7 = matmul_kij((B12 - B22), (C21 + C22))

    A[s1, s1] = M1 + M4 - M5 + M7
    A[s1, s2] = M3 + M5
    A[s2, s1] = M2 + M4
    A[s2, s2] = M1 - M2 + M3 + M6
    
    return A
    
# Problem 2

def markov_matrix(n):
    """
    Create transition matrix for the random walk
    """
    A = np.zeros((n, n))
    for i in range(n):
        if i == 0:
            A[0, 0] = 0.5
            A[1, 0] = 0.5
            
        elif i == n-1:
            A[n-2, n-1] = 0.5
            A[n-1, n-1] = 0.5
            
        else:
            A[i-1, i] = 0.5
            A[i+1, i] = 0.5
    return A
