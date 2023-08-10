# Homework 5

This is a short homework with almost no code, and mostly review.  The intent is to give you extra time for your midterm checkpoint.  Because of the midterm checkpoint, the due date is extended to Monday, November 16.  However you may find working through this assignment is complementary to the midterm checkpoint.

Put your written answers for Problem 0 in a file `answers.md`.  You don't need to write or submit any code for Problem 0.  You don't need to include a written answer for Problem 1 (just the requested files).

## Important Information

### Due Date
This assignment is due Monday, November 16 at 12pm (noon) Chicago time.

### Grading

There is no autograder and little code.  Points will be based on providing the requested files, correctness, and showing your work. 

## Problem 0 - Some computations (40 points)

When you submit jobs to a cluster (or run them on your computer), it is useful to be able to do some back-of-the-envelope calculations on memory and time requirements to run an algorithm.

In this problem, include a brief explanation of your answers (show your work).

### Part A - Memory (20 points)

Use B (bytes), KB, MB, GB, TB, etc. when answering the following questions

**i)** How much memory does a dense array of N double-precision floating point numbers require for:
* N = 1,000 (1 thousand)
* N = 1,000,000 (1 million)
* N = 1,000,000,000 (1 billion)
* N = 1,000,000,000,000 (1 trillion)

**ii)** How much memory does a dense N x N array of double precision floating point numbers require for:
* N = 1,000
* N = 1,000,000

**iii)** Let's say you have 8 GB of RAM available.  What is the largest value of N for which you can fit a dense N x N matrix of double precision numbers in available memory?

**iv)** Let's say you have 8 GB of RAM available.  Give tight upper and lower bounds on the number of non-zeros you can store in a CSR matrix and fit in available memory (assume 64-bit data types, and don't worry about the two integers that specify the number of rows and number of columns, or other constant memory overhead).

### Part B - Run Times (20 points)

Assume the following run times are for sequential (not parallel) algorithms.

**i)** You use a sorting algorithm which runs in Omega(n log(n)) time.  On an array with n=1,000 elements, this algorithm takes 1 ms to execute.  Estimate how long the sorting algorithm will take on an array with n=1,000,000 elements.

**ii)** Your implementation of matrix-matrix multiplication takes 150ms to execute when forming the product of two 2000 x 2000 matrices.  How long do you expect this implementation to take on two 4000 x 4000 matrices?  What about 8000 x 8000 matrices?

**iii)** You have an agent-based model simulation which has a run time that scales as `n**2` in the number of agents.  If your simulation takes 1 sec. for n=1000, how long do you expect it to take for n=10,000?  If you are willing to wait for up to an hour for your simulation to run, how large can `n` be?

**iv)** If you optimize your agent-based model simulation to have a run time that scales as `n*sqrt(n)`, with the same constant as before, how large can you make `n` now, while still keeping your simulation run time less than 1 hour?


## Problem 1 - A Simple SLURM script (10 points)

You are supposed to set up some scripts for your midterm checkpoint - this problem is primarily intended to make sure everyone tries running a script on Midway.

Write a simple Python script `solve_opt.py` which minimizes `la.norm(b - A @ x)`, using both the 1-norm and 2-norm.  See this [exercise in the class notes](https://caam37830.github.io/book/03_optimization/scipy_opt.html#exercises) for context.

Run the minimization problem on a random `5 x 5` linear system.  Print the residual `b - A @ x` where `x` is the computed solution.  Do this for both the 1-norm and 2-norm minimization variations (so you will print 2 residuals, which are each vectors of length 5).

Write a file `solve_opt.sbatch` which you can use to submit your script to the Midway cluster on RCC.  Send your output to `solve_opt.out` (you should see the two residuals printed), and your errors to `solve_opt.err`.  Include these files in your submission.
