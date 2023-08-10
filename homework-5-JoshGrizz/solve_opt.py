import numpy as np
import scipy.linalg as la
import scipy.optimize as opt

n = 5
A = np.random.randn(n,n)
x0 = np.random.randn(n) # ground truth x
b = A @ x0

sol1 = opt.minimize(lambda x : la.norm(b - A @ x), np.random.randn(n))
sol2 = opt.minimize(lambda x : la.norm(b - A @ x, 1), np.random.randn(n))

print(sol1.x - x0)
print(sol2.x - x0)