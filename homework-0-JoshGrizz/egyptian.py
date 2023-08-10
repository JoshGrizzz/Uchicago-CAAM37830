"""
Egyptian algorithm
"""

def egyptian_multiplication(a, n):
    """
    returns the product a * n

    assume n is a nonegative integer
    """
    def isodd(n):
        """
        returns True if n is odd
        """
        return n & 0x1 == 1

    if n == 1:
        return a
    if n == 0:
        return 0

    if isodd(n):
        return egyptian_multiplication(a + a, n // 2) + a
    else:
        return egyptian_multiplication(a + a, n // 2)


if __name__ == '__main__':
    # this code runs when executed as a script
    for a in [1,2,3]:
        for n in [1,2,5,10]:
            print("{} * {} = {}".format(a, n, egyptian_multiplication(a,n)))

# Compute a^n using the Egyptian Algorithm
def power(a, n):
    """
    computes the power a ** n

    assume n is a nonegative integer
    """
    
    def isodd(n):
        """
        returns True if n is odd
        """
        return n & 0x1 == 1
    
    # Special cases: 0 and 1
    
    if n == 1:
        return a
    if n == 0:
        return 1

    if isodd(n): # odd case: need to multiply another a on the back
        return power(a * a, n // 2) * a
    else: # even case: go straightly to next recursion
        return power(a * a, n // 2)
    
    pass

# Sample outputs including the three required outputs

if __name__ == '__main__':
    for b in [3,4,5]:
        for c in [3,4,5]:
            print("{} ^ {} = {}".format(b, c, power(b,c)))
