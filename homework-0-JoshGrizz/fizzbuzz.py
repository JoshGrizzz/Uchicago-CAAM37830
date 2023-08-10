"""
fizzbuzz

Write a python script which prints the numbers from 1 to 100,
but for multiples of 3 print "fizz" instead of the number,
for multiples of 5 print "buzz" instead of the number,
and for multiples of both 3 and 5 print "fizzbuzz" instead of the number.
"""

# Print "fizz" for multiples of 3, print buzz for multiples of 5, print "fizzbuzz" for multiples of both 3 and 5
def fizzbuzzPrinter(x):
    """
    Print "fizz" for multiples of 3
    print buzz for multiples of 5
    print "fizzbuzz" for multiples of both 3 and 5
    nothing to return, only serves to print
    """
    for i in range(1, x+1):
        if i%3 == 0 and i%5 != 0: # divisible by 3 only, print fizz
            print("fizz")
        elif i%5 == 0 and i%3 != 0: # divisible by 5 only, print buzz
            print("buzz")
        elif i%3 == 0 and i%5 == 0: # divisible by both 3 and 5, print fizzbuzz
            print("fizzbuzz")
        else: # else, print number
            print(i)

fizzbuzzPrinter(100)
            
            
        