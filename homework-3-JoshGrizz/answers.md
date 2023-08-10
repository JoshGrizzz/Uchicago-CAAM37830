# Answers

Put any answers to questions in the assignment in this file, or any commentary you don't include in the code.

This is a markdown file (the `.md` extension gives it away). If you have never used markdown before, check out [this short guide](https://guides.github.com/features/mastering-markdown/).

## Problem 0

## PartA:

## Sub-question1: Read the documentation for np.ravel_multi_index. How can you compute k so that s[k] is the same entry as S[i,j]?

By the description of the function np.ravel_multi_index, we know that this function converts a tuple of index arrays into an array of flat indices, applying boundary modes to the multi-index. It might be useful to illustrate with an example given in the documentation: (Note: we use the simplest example. In the actual operations, matrix memory format matters.)

Example:
arr = np.array([[3,6,6],[4,5,1]])
np.ravel_multi_index(arr, (7,6))
array([22, 41, 37])

Here, it gives us a case of flattening a 7*6 array and get the position of the original entry on positions [3, 4], [6, 5] and [6, 1]. Thus, we get 3 * 6 + 4 = 22 as the first entry of our output, 6 * 6 + 5 = 41 as the second entry and 6 * 6 + 1 = 37 as the third entry. Generally, for [i, j], we get i * n + j, for the default setups. The result will change if we change the format.

So, to compute k so that s[k] is the same entry as S[i,j], we can use np.ravel_multi_index(np.array([[i],[j]]), (m,n)) to get the result, where m, n refers to the size of S. 

## Sub-question2: How can you compute i,j so that S[i,j] is the same entry as s[k]?

Still we look at the documentation and illustrate using an example: 

Example:
np.unravel_index([22, 41, 37], (7,6))
(array([3, 6, 6]), array([4, 5, 1]))

We notice that this is simply the reversal process of np.ravel_multi_index. Thus, to compute i,j so that S[i,j] is the same entry as s[k], we can just use np.unravel_index([k], (m,n)), where m, n refers to the size of S. 

## Sub-question3: Read the documentation for np.reshape. How can you turn the array s back into the 2-dimensional array S?

Without given constraints of the reshaping (for example, memory format of matrices), we may simply use np.reshape(s, (m, n)), where s refers to S.flatten() and m,n refers to the size that we want to reshape into.

## PartB: 

## Give a brief explanation of why you chose the matrix type that you did.

In partB, I chose row-based list of lists sparse matrix (sparse.lil_matrix). I chose this because from the documentations of list of lists matrix, it is a convenient format of constructing sparse matrices and it can change to the matrix sparsity structure efficiently. (By the documentation, it says that we might consider using list of lists format when constructing large matrices.) Although it has relatively weak performance in matrix-vector multiplications, changing that to CSR or CSC matrices can resolve the problem easily.

## PartC:

## Among the three matrix formats,for matrix multiplication c = A @ s, which is fastest on a 100 x 100 grid? Which is fastest on a 1000 x 1000 grid?

According to my result, dia_matrix is the fastest for both cases, which is a little bit out of my expectation. 

## Is the function count_alive_neighbors_matmul faster or slower than count_alive_neighbors? Does it depend on the sparse matrix type?

It is much faster than the function count_alive_neighbors, no matter we pick csc_matrix, csr_matrix or dia_matrix. I also did a comparison between those three matrix types and found out that using dia_matrix in the input of function count_alive_neighbors_matmul is again the fastest.

## PartD:

## Is the function count_alive_neighbors_slice faster or slower than count_alive_neighbors?

It is much faster than count_alive_neighbors. Actually, it is even faster than the function count_alive_neighbors_matmul.

## In terms of memory access of A and cts, which of the three matrix types in part C would do matrix-vector multiplication in a way most similar to count_alive_neighbors_slice?

Let us discuss by cases: if S has m = n, then it is kind of equivalently similar to csc_matrix and csr_matrix. If m > n , it is more similar to csr_matrix; if m < n, it is more similar to csc_matrix.

## PartE:

The method count_alive_neighbors_slice is chosen here.

## Feedback
