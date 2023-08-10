## Problem0

## Part A: Memory

### i) How much memory does a dense array of N double-precision floating point numbers require for:

N = 1,000 (1 thousand)
N = 1,000,000 (1 million)
N = 1,000,000,000 (1 billion)
N = 1,000,000,000,000 (1 trillion)

### Answer

First notice that each double-precision floating point number is taking 8 Bytes (64 Bits) of memory.

For N = 1,000: 8 * 1,000 = 8,000 Bytes, which is approximately 7.8125 KB.

For N = 1,000,000: 7.8125 KB * 1000 = 7812.5 KB, which is approximately 7.6294 MB.

For N = 1,000,000,000: 7629.4 MB, which is approximately 7.4506 GB

For N = 1,000,000,000,000, 7450.6 GB, which is approximately 7.2760 TB

### ii) How much memory does a dense N x N array of double precision floating point numbers require for:

N = 1,000

N = 1,000,000

### Answer

For N = 1,000: we have 1,000,000 entries in total, thus is approximately 7.6294 MB.

For N = 1,000,000: we have 1,000,000,000,000 entries in total, thus is approximately 7.2760 TB.

### iii) Let's say you have 8 GB of RAM available. What is the largest value of N for which you can fit a dense N x N matrix of double precision numbers in available memory?

### Answer

8 * (1024^3) / 8 = 1024^3. Then we take square root of it, we get N to be 32768.

### iv) Let's say you have 8 GB of RAM available. Give tight upper and lower bounds on the number of non-zeros you can store in a CSR matrix and fit in available memory (assume 64-bit data types, and don't worry about the two integers that specify the number of rows and number of columns, or other constant memory overhead).

### Answer

Recall that CSR is the way to represent an m * n matrix using three 1-dimensional arrays. The memory it takes could be measured by (2 * nnz + m + 1) times the unit size depending on the data type, where nnz refers to the number of nonzeros.

Tight Upper bound: when m is as small as possible, which is 1. Then, the memory for now is (2 * nnz + 2), which takes 8 GB. Thus, we have (2 * nnz + 2) * 8 = 8 * (1024^3). In this case, the tight upper bound of nnz is (2^30-2)/2, which equals to 2^29 - 1.

Tight lower bound: when m is as large as possible, which is nnz. In this case , we have (3 * nnz + 1) * 8 = 8 * (1024^3). Thus the tight lower bound for nnz is (1024^3-1)/3, which is approximately 357913941.

## Part B: Run times

### i) You use a sorting algorithm which runs in Omega(n log(n)) time. On an array with n=1,000 elements, this algorithm takes 1 ms to execute. Estimate how long the sorting algorithm will take on an array with n=1,000,000 elements.

### Answer:

The expected run time for n = 1,000,000: 1 * (1,000,000 * log(1,000,000) / (1,000 * log(1000))) = 1 * 1000 * 2 = 2000 ms.

### ii) Your implementation of matrix-matrix multiplication takes 150ms to execute when forming the product of two 2000 x 2000 matrices. How long do you expect this implementation to take on two 4000 x 4000 matrices? What about 8000 x 8000 matrices?

### Answer:

Since The time complexity for matrix-matrix multiplication is O(n^3), we know 4000 * 4000 takes 8 times more run time than the 2000 * 2000 case, which will take 1200ms. Samely, 8000 * 8000 will take 64 times more run time than the 2000 * 2000 case, which will take 9600 ms.

### iii) You have an agent-based model simulation which has a run time that scales as n ** 2 in the number of agents. If your simulation takes 1 sec. for n=1000, how long do you expect it to take for n=10,000? If you are willing to wait for up to an hour for your simulation to run, how large can n be?

### Answer:

Case for n = 10000: (10^2) * 1 = 100 sec.

Value for n that runs for an hour: an hour is 3600 seconds. Thus, the max n will the 10000 times square root of 36, which is 60000. 

### iv) If you optimize your agent-based model simulation to have a run time that scales as n*sqrt(n), with the same constant as before, how large can you make n now, while still keeping your simulation run time less than 1 hour?

### Answer: 

The case n = 1000 takes 1 second to run. The, for the case in this problem, the largest n that could runs less than an hour is 1000 * (3600^(2/3)), which is approximately 234892.
