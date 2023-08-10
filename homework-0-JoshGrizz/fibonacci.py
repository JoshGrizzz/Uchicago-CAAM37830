"""
fibonacci

functions to compute fibonacci numbers

Complete problems 2 and 3 in this file.
"""

import time # to compute runtimes
from tqdm import tqdm # progress bar

# Question 2
# Recursive method to calculate nth term in Fibonacci Sequence
def fibonacci_recursive(n):
    """
    Fibonacci Recursive Method with base cases handled properly
    Input should be an integer larger or equal to 0
    """
    
    # Base cases: 0 and 1
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # Recursive step
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)
    pass


# Question 2
#Iterative Method for Fibonacci
def fibonacci_iter(n):
    """
    Fibonacci iterative method, given first two terms
    """
    a = 0
    b = 1
    if n == 0:
        return 0
    
    elif n == 1:
        return 1
    
    else:
        for i in range(2, n+1):
            a, b = b, a+b
        return b
    pass

# Print first 30 entries for both methods. The results should be same.
print("Recursive: ")
for i in range(30):
    print("F_{} = {}".format(i, fibonacci_recursive(i)))
    
print("Iterative: ")
for j in range(30):
    print("F_{} = {}".format(j, fibonacci_iter(j)))
    



# Question 3
import numpy as np

#Matrix Power method for Fibonacci
def fibonacci_power(n):
    """
    Using matrix power to get nth entry in Fibonacci sequence
    """
    A = np.array([[1,1], [1,0]])
    def isodd(n):
        """
        returns True if n is odd
        """
        return n & 0x1 == 1
    
    def power(A, n):
        """
        Egyptian idea to calculate matrix power
        """
        # Special cases: 0 and 1
        if n == 1:
            return A
        if n == 0:
            return 0
        
        # Odd case
        if isodd(n):
            return power(A @ A, n // 2) @ A
        # Even case
        else:
            return power(A @ A, n // 2)
    
    # Special cases: 0 and 1
    if n == 0:
        return 0
    
    elif n == 1:
        return 1
    
    # General case
    else:
        return (power(A, n-1) @ ([1,0]))[0]
    pass

# Print the results. Should be same as previous methods 
print("Using power of matrix: ")
for k in range(30):
    print("F_{} = {}".format(k, fibonacci_power(k)))

if __name__ == '__main__':
    """
    this section of the code only executes when
    this file is run as a script.
    """
    def get_runtimes(ns, f):
        """
        get runtimes for fibonacci(n)

        e.g.
        trecursive = get_runtimes(range(30), fibonacci_recusive)
        will get the time to compute each fibonacci number up to 29
        using fibonacci_recursive
        """
        ts = []
        for n in tqdm(ns):
            t0 = time.time()
            fn = f(n)
            t1 = time.time()
            ts.append(t1 - t0)

        return ts


    nrecursive = range(35)
    trecursive = get_runtimes(nrecursive, fibonacci_recursive)

    niter = range(10000)
    titer = get_runtimes(niter, fibonacci_iter)

    npower = range(10000)
    tpower = get_runtimes(npower, fibonacci_power)

    ## write your code for problem 4 below...
    
    import matplotlib.pyplot as plt
    x = [nrecursive, niter, npower]
    y = [trecursive, titer, tpower]
    names = ["Recursive", "Iterative", "Power of Matrix"]
    for n in range(3):
        # Use plt.loglog to generate the log-base
        plt.loglog(x[n],y[n], basex=10, basey=10, label=names[n])
        
    # Add important features to the plot
    plt.legend()
    plt.xlabel("n")
    plt.ylabel("time (sec.)")
    plt.title("Time to compute Fibonacci(n)")
    plt.show()
    
