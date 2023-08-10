# Answers

Put any answers to questions in the assignment in this file, or any commentary you don't include in the code.

This is a markdown file (the `.md` extension gives it away). If you have never used markdown before, check out [this short guide](https://guides.github.com/features/mastering-markdown/).

## Problem 0
You don't need to say anything here.  Just complete [`fizzbuzz.py`](fizzbuzz.py).

## Problem 1

How many additions are done in the Egyptian multiplication algorithm?

If we convert a base-10 decimal to binary form, the number of digits will be (floor(log2(n)) + 1), where "floor" refers to floor function. By definition given out in the question, the number of non-zero digits is #n, so the number of 0's will be (floor(log2(n)) - #n + 1). By the algorithm of converting base-10 decimals to binart form, when we apply the Egyptian multiplication algorithm, we will encounter even numbers for (floor(log2(n)) - #n + 1) times and odd numbers for #n times. Note that when we encounter even numbers, one addition operation is needed and when we encounter odd numbers except 1, two additions are needed, so we finally need (floor(log2(n)) + #n - 1) additions in total.

## Problem 2

Which of these algorithms do you expect to be asymptotically faster? Why?

Computing iteratively is faster. It is really obvious that computing iteratively has time complexity of O(n). For the recursive approach, Time(n) approximately equals to Time(n-1) + Time(n-2). So, its time complexity is (roughly) O(2^n). So, the iterative method is faster.

## Problem 3

(a): What is the asymptotic number of operations done in this algorithm? How does this compare to the algorithms in problem 2?

Since we are applying the similar idea as problem1, the structure of analysis is also quite similar: there are #n non-zero digits and (floor(log2(n-1)) - #n + 1))'s. Since the size of the matrix is 2 * 2, the multiplication process takes constant number of operations. Let us say it takes c' times (value of c' depends on the matrix-matrix multiplication method that is used) of operations to finish the process of multiplication of two 2 * 2 matrices. When we encounter odd numbers except 1, 2c' operations are done; when we encounter even numbers, c' operations are done. So, the time complexity of calculating A^(n-1) using Egyptian idea is O(c' * (floor(log2(n-1)) - #n + 1) + 2c' * #n) = O(c' * (floor(log2(n-1)) + #n + 1)). Since #n is bounded by (floor(log2(n-1)) + 1, O(c' * (floor(log2(n-1)) + #n + 1)) is exactly same as O(log(n)). Note that the algorithm has an extra step of taking the product of A^(n-1) and vector [1,0], but since that also could be done in constant number of operations, the asymptotic number of operations done in this algorithm is O(log(n)).

Comparing to the algorithms in problem2, no matter comparing with the iterative or the recursive method, this algorithm has much better performance.

(b): What are potential issues you might run into with large values of n in this algorithm? Do you think it would be better to use np.float64 or np.int64 in your arrays for large values of n?

The potential issue that we might run into is overflow, since numpy package is used here. 

I think it might be better to use np.float64 or np.int64, since the algorithm could hold for larger n's. However, when n is sufficiently large, overflow problems will happen again. Here, we should also notice that using the default python setup might help us avoid this problem.

## Problem 4

![](/images/fibonacci_runtime.png)

Give a short interpretation of what you see:

From the plot, we see that the recursive method's runtime has a really steep curve of increasing, which coincides with the results that it has the highest time complexity. The iterative method is faster than the matrix-power method as n is relatively small and is slower as n becomes larger. 

One funny fact about the plot is that both the iterative method's curve and the matrix-power method's curve have some "oscillation" as n increases.

## Feedback
