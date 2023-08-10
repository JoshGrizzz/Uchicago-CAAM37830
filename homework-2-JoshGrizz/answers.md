# Answers

Put any answers to questions in the assignment in this file, or any commentary you don't include in the code.

This is a markdown file (the `.md` extension gives it away). If you have never used markdown before, check out [this short guide](https://guides.github.com/features/mastering-markdown/).

## Problem 0

PartB: Both factorizations take O(n^3) time to compute - which is faster in practice?

![](/images/Figure_1.png)

Answer: 
By the plot, we notice that the Cholesky factoraization is faster than the LU factorization.

PartC: Do you expect this function to be asymptotically faster or slower than the approach you used in Homework 0? Considering that the Fibonacci numbers are integers, what issues might you need to consider if using this function to compute Fibonacci numbers?

Answer: 
I expect this algorithm to be asymptotically faster than the approach that I used in homework 0. For a given symmetric A with specified size d, the time complexity to perform eigen-decomposition is O(1). After performing the eigen-decomposition, the time complexity of performing np.power(n) on each diagonal entry is O(1). Thus, the whole process of calculating the nth power of the diagonal matrix is also O(1). Finally, for the step of calculating the prodect of three matrices together, the time complexity is also O(1) for given matrix size. So, this algorithm is asymptotically faster. 

The biggest issue that I can think about is the rounding-off error issue. For the matrix that we use to compute nth element in Fibonacci sequence, we have two eigen-values: (1+sqrt(5))/2 and (1-sqrt(5))/2. For large n, calculating the nth power of those two might producing relatively higher rounding-off error. Also, since Fibonacci numbers are integers, in the final step we need to round off our result off to a decimal, which possibly can produce large error between the actual result. 


## Problem 1

PartA: All of these implementations have an O(n^3) asymptotic run time, and perform an identical number of floating point operations. Give an explanation for why some loop orders are faster than others - why is the fastest version fastest? Why is the slowest version slowest?

![](/images/Figure_2.png)

Answer: Even though all these implementations have an O(n^3) asymptotic run time and perform an identical number of floating point operations, the actual performance of them are actually not the same, because of the memory structures of the matrices, specifically, row-major versus column-major. The different memory structures directly influence the performances of traversion and loops.

For our case: 

The order ikj is the fastest because the most inside inner loop j is executed and "traversed" first, which takes advantage of the contiguous nature of the memory of rows of matrix C. After loop of j is executed to the end for the corresponding i and k, loop of k starts to execute, which again takes advantage of the contiguous nature of the memory of rows of matrix B. 

The order jki is the slowest because the most inner loop i is executed first, which fails to take advantage of the contiguous row memory of matrix B. After loop i is executed to the end, loop of k starts to execute, which again, fails to take advantage of the contiguous row memory of C.

PartB: 

![](/images/Figure_3.png)

PartC: Does Strassen's algorithm actually beat blocked matrix multiplication for the values of n that you tested?

![](/images/Figure_4.png)

Answer: Yes, Strassen's algorithm actually beats blocked matrix multiplication for the values of n that I tested.


## Problem 2

2.
![](/images/Markov.png)

3.
How close is this to p at t=1000 in part 2?
Answer: 0.02774622469939288

How close is this to p at t=2000?
Answer: 0.0038492383304019368

## Feedback
