"""
use this file to script the creation of plots, run experiments, print information etc.

Please put in comments and docstrings in to make your code readable
"""

import numpy as np
import scipy as sp
import scipy.sparse as sparse
import scipy.sparse.linalg as sla
from life import *
import time
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# Problem 0

# part A

"""
Converts a tuple of index arrays into an array of flat
indices, applying boundary modes to the multi-index.
"""

print("Part A: some examples to illustrate ravel and unravel: ")
S = np.random.randint(100, size = (5, 8))
print(S[4,7])
k = np.ravel_multi_index(np.array([[4],[7]]), (5,8))
s = S.flatten()
print("The k we are looking for: " + str(k[0]))
print(s[k[0]])

[i,j] = np.unravel_index([31], (5,8))
print("The i,j pair we are looking for: " + str(i[0]) + " " + str(j[0]))
print(S[i[0], j[0]])
print(s[31])

Sr = np.reshape(s, (5, 8))
print(Sr)
print(S)

# Part C

# Code for count_alive_neighbors
def neighbors(i, j, m, n):
    inbrs = [-1, 0, 1]
    if i == 0:
        inbrs = [0, 1]
    if i == m-1:
        inbrs = [-1, 0]
    jnbrs = [-1, 0, 1]
    if j == 0:
        jnbrs = [0, 1]
    if j == n-1:
        jnbrs = [-1, 0]

    for delta_i in inbrs:
        for delta_j in jnbrs:
            if delta_i == delta_j == 0:
                continue
            yield i + delta_i, j + delta_j

def count_alive_neighbors(S):
    m, n = S.shape
    cts = np.zeros(S.shape, dtype=np.int64)
    for i in range(m):
        for j in range(n):
            for i2, j2 in neighbors(i, j, m, n):
                cts[i,j] = cts[i,j] + S[i2, j2]

    return cts

print("Part C: ")
# We set a seed here:
np.random.seed(0)

# Generate random 100*100 and 1000*1000 grids referring to the given seed
S1 = np.random.rand(100, 100) < 0.3
S2 = np.random.rand(1000, 1000) < 0.3
A1 = grid_adjacency(100,100)
print("100*100 grid have finished generating its adjacency matrix.")
A2 = grid_adjacency(1000,1000)
print("1000*1000 grid have finished generating its adjacency matrix.")

# For 100 * 100, do the sparse matrix type conversion
A11 = A1.tocsc()
A12 = A1.tocsr()
A13 = A1.todia()

# For 1000 * 1000, do the sparse matrix type conversion
A21 = A2.tocsc()
A22 = A2.tocsr()
A23 = A2.todia()

# First Compare matrix multiplication performances:

start = time.time()
result1 = A11 @ S1.flatten()
end = time.time()
time1 = end - start
print("100*100, csc multiply takes: " + str(time1) + " sec")

start = time.time()
result2 = A12 @ S1.flatten()
end = time.time()
time1 = end - start
print("100*100, csr multiply takes: " + str(time1) + " sec")

start = time.time()
result1 = A13 @ S1.flatten()
end = time.time()
time1 = end - start
print("100*100, dia multiply takes: " + str(time1) + " sec")

start = time.time()
result1 = A21 @ S2.flatten()
end = time.time()
time1 = end - start
print("1000*1000, csc multiply takes: " + str(time1) + " sec")

start = time.time()
result2 = A22 @ S2.flatten()
end = time.time()
time1 = end - start
print("1000*1000, csr multiply takes: " + str(time1) + " sec")

start = time.time()
result1 = A23 @ S2.flatten()
end = time.time()
time1 = end - start
print("1000*1000, dia multiply takes: " + str(time1) + " sec")

# Then compare count_alive_neighbors and count_alive_neighbors_matmul
# Note: adding in a part of comparison for different type of matrices in the function count_alive_neighbors_matmul

start = time.time()
cts1 = count_alive_neighbors(S1)
end = time.time()
time1 = end - start
print("100*100, count_alive_neighbors method takes: " + str(time1) + " sec")

start = time.time()
cts2 = count_alive_neighbors_matmul(S1, A11)
end = time.time()
time2 = end - start
print("100*100, with csc_matrix takes: " + str(time2) + " sec")

start = time.time()
cts3 = count_alive_neighbors_matmul(S1, A12)
end = time.time()
time3 = end - start
print("100*100, with csr_matrix takes: " + str(time3) + " sec")

start = time.time()
cts4 = count_alive_neighbors_matmul(S1, A13)
end = time.time()
time4 = end - start
print("100*100, with dia_matrix takes: " + str(time4) + " sec")

start = time.time()
cts5 = count_alive_neighbors(S2)
end = time.time()
time5 = end - start
print("1000*1000, count_alive_neighbors method takes: " + str(time5) + " sec")

start = time.time()
cts6 = count_alive_neighbors_matmul(S2, A21)
end = time.time()
time6 = end - start
print("1000*1000, with csc_matrix takes: " + str(time6) + " sec")

start = time.time()
cts7 = count_alive_neighbors_matmul(S2, A22)
end = time.time()
time7 = end - start
print("1000*1000, with csr_matrix takes: " + str(time7) + " sec")

start = time.time()
cts8 = count_alive_neighbors_matmul(S2, A23)
end = time.time()
time8 = end - start
print("1000*1000, with dia_matrix takes: " + str(time8) + " sec")

# Part D
# Comparing slicing and original algorithm
print("Part D: ")
start = time.time()
cts9 = count_alive_neighbors(S2)
end = time.time()
time9 = end - start
print("For 1000*1000 grid, count_alive_neighbors method takes: " + str(time9) + " sec")

start = time.time()
cts10 = count_alive_neighbors_slice(S2)
end = time.time()
time10 = end - start
print("For 1000*1000 grid, count_alive_neighbors_slice method takes: " + str(time10) + " sec")

# Part E
# Generating GIF using the code given on class

fig = plt.figure(figsize=(5,5))
fig.set_tight_layout(True)

# Plot an image that persists
im = plt.imshow(S1, animated=True)
plt.axis('off') # turn off ticks

def update(*args):

    global S1
    
    # Update image to display next step
    cts = count_alive_neighbors_slice(S1)
    # Game of life update
    S1 = np.logical_or(
        np.logical_and(cts == 2, S1),
        cts == 3
    )
    im.set_array(S1)
    return im,

anim = FuncAnimation(fig, update, frames=50, interval=200, blit=True) # setting frames to 50
anim.save('fav.gif', dpi=80, writer='pillow') # Set writer to pillow to make it compile successfully