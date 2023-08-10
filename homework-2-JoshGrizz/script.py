"""
use this file to script the creation of plots, run experiments, print information etc.

Please put in comments and docstrings in to make your code readable
"""
import numpy as np
import scipy as sp
import scipy.linalg as la
import matplotlib.pyplot as plt
import time
from scipy.linalg import blas
from matlib import *

# Add-on: make labeling more flexible

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# Problem 0

# part B

# Compare LU and Cholesky

ValSpace = np.round(np.logspace(1, np.round(np.log10(4000), decimals = 5), num=10)).astype(int)
Chol_ns = ValSpace
Chol_ts = []
LU_ns = ValSpace
LU_ts = []
for n in ValSpace:
    A = np.random.randn(n,n)
    A = A @ A.T
    
    # Timing: Cholesky
    
    start = time.time()
    Chol_F = la.cholesky(A, lower = True)
    end = time.time()
    Chol_ts.append(end - start)
    
    # Timing: LU
    
    start = time.time()
    P, L, U = la.lu(A)
    end = time.time()
    LU_ts.append(end - start)
    
# Create log-log plot    
    
plt.loglog(Chol_ns, Chol_ts, label = f"Cholesky")
plt.loglog(LU_ns, LU_ts, label = f"LU")
plt.xlabel('n')
plt.ylabel('time (sec.)')
plt.title('time to get the factorizations')
plt.legend()
plt.show(block=False)
plt.pause(3)
plt.close()

# Problem 1

# PartA

# Compare the eight algorithms and plot

m = np.log10(1000)
ValSpace2 = np.round(np.logspace(2, np.round(m, decimals = 5), num=10)).astype(int)
mulIJK = mulIKJ = mulJIK = mulJKI = mulKIJ = mulKJI = dgemm_BLAS = np_mat_mul = ValSpace2
IJK_ts = []
IKJ_ts = []
JIK_ts = []
JKI_ts = []
KIJ_ts = []
KJI_ts = []
dgemm_BLAS_ts = []
np_mat_mul_ts = []

n1 = 100

b = np.array(np.random.randn(n1,n1), order='C')
c = np.array(np.random.randn(n1,n1), order='C')

# Precompile: for numba

p1 = matmul_ijk(b, c)
p2 = matmul_ikj(b, c)
p3 = matmul_jik(b, c)
p4 = matmul_jki(b, c)
p5 = matmul_kij(b, c)
p6 = matmul_kji(b, c)

for n in ValSpace2:
    # Generate: row-major
    B = np.array(np.random.randn(n,n), order='C')
    C = np.array(np.random.randn(n,n), order='C')
    
    start = time.time()
    y1 = matmul_ijk(B, C)
    end = time.time()
    IJK_ts.append(end-start)
    
    start = time.time()
    y2 = matmul_ikj(B, C)
    end = time.time()
    IKJ_ts.append(end-start)
    
    start = time.time()
    y3 = matmul_jik(B, C)
    end = time.time()
    JIK_ts.append(end-start)
    
    start = time.time()
    y4 = matmul_jki(B, C)
    end = time.time()
    JKI_ts.append(end-start)
    
    start = time.time()
    y5 = matmul_kij(B, C)
    end = time.time()
    KIJ_ts.append(end-start)
    
    start = time.time()
    y6 = matmul_kji(B, C)
    end = time.time()
    KJI_ts.append(end-start)
    
    start = time.time()
    y7 = blas.dgemm(1.0, B, C)
    end = time.time()
    dgemm_BLAS_ts.append(end-start)
    
    start = time.time()
    y8 = np.matmul(B,C)
    end = time.time()
    np_mat_mul_ts.append(end-start)
    
    # A mileage indicator
    
    print("current loop: " + str(n))

list1 = [mulIJK, mulIKJ, mulJIK, mulJKI, mulKIJ, mulKJI, dgemm_BLAS, np_mat_mul]
list2 = [IJK_ts, IKJ_ts, JIK_ts, JKI_ts, KIJ_ts, KJI_ts, dgemm_BLAS_ts, np_mat_mul_ts]
list3 = ["order ijk", "order ikj", "order jik", "order jki", "order kij", "order kji", "Blas_dgemm", "np.matmul()"]
for i in range(8):
    plt.loglog(list1[i], list2[i], label = list3[i])

plt.xlabel('n')
plt.ylabel('time (sec.)')
plt.title('time to calculate the product')
plt.legend()
plt.show(block=False)
plt.pause(3)
plt.close()

# Part B
# Compare IKJ and blocked

# Precompile

n2 = 64

b = np.array(np.random.randn(n2,n2), order='C')
c = np.array(np.random.randn(n2,n2), order='C')
p1 = matmul_ikj(b, c)
p2 = matmul_blocked(b, c)

ikj_ts = []
block_ts = []
ikj_ns = block_ns = [2**k for k in range(6,13)]
for i in range (6,13):
    B = np.array(np.random.randn(2**i, 2**i), order='C')
    C = np.array(np.random.randn(2**i, 2**i), order='C')
    
    start = time.time()
    z1 = matmul_ikj(B, C)
    end = time.time()
    ikj_ts.append(end - start)
    
    start = time.time()
    z2 = matmul_blocked(B, C)
    end = time.time()
    block_ts.append(end - start)
    print("current loop: " + str(i))

list21 = [ikj_ns, block_ns]
list22 = [ikj_ts, block_ts]
list23 = ["order ikj", "matmul_blocked"]

for i in range(2):
    plt.loglog(list21[i], list22[i], basex = 2, label = list23[i])

plt.xlabel('n')
plt.ylabel('time (sec.)')
plt.title('time to calculate the product')
plt.legend()
plt.show(block=False)
plt.pause(3)
plt.close()

# Part C
# Compare Strassen and blocked

strassen_ts = []
blk_ts = []
blk_ns = strassen_ns = [2**k for k in range(6,13)]
n3 = 64
b = np.array(np.random.randn(n3,n3), order='C')
c = np.array(np.random.randn(n3,n3), order='C')
p21 = matmul_strassen(b, c)
p22 = matmul_blocked(b, c)

for i in range (6,13):
    B = np.array(np.random.randn(2**i, 2**i), order='C')
    C = np.array(np.random.randn(2**i, 2**i), order='C')
    
    start = time.time()
    z21 = matmul_strassen(B, C)
    end = time.time()
    strassen_ts.append(end - start)
    
    start = time.time()
    z22 = matmul_blocked(B, C)
    end = time.time()
    blk_ts.append(end - start)
    print("current loop: " + str(i))
    
list31 = [strassen_ns, blk_ns]
list32 = [strassen_ts, blk_ts]
list33 = ["Strassen", "matmul_blocked"]

for i in range(2):
    plt.loglog(list31[i], list32[i], basex = 2, label = list33[i])

plt.xlabel('n')
plt.ylabel('time (sec.)')
plt.title('time to calculate the product')
plt.legend()
plt.show(block=False)
plt.pause(3)
plt.close()

# Problem 2
# Markov chain starting at p0

# 2.2
p = np.zeros(50)
p[0] = 1
p_list = []
Init_Dis = p
Trans_Matrix = markov_matrix(50)

for t in (10, 100, 1000):
    p = Init_Dis
    for k in range(t):
        p = Trans_Matrix.dot(p)
    p_list.append(p)

p_state = [k for k in range(50)]
list43 = ["t = 10", "t = 100", "t = 1000"]
for i in range(3):
    plt.plot(p_state, p_list[i], label = list43[i])
    
plt.xlabel('State spaces')
plt.ylabel('probability')
plt.title('Random walk')
plt.legend()
plt.show(block=False)
plt.pause(3)
plt.close()

# 2.3

# Get eigenvector corresponding to the eigenvalue

eValue, eV = la.eig(Trans_Matrix)
position = np.argmax(eValue)
eVector1 = eV[:,position]

# normalize
eVector1 = eVector1 / np.sum(eVector1)

# Output results
print("Distance at t = 1000: " + str(la.norm(eVector1-p_list[2])))
p = Init_Dis
for k in range(2000):
        p = Trans_Matrix.dot(p)
print("Distance at t = 2000: " + str(la.norm(eVector1-p)))

