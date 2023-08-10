"""
A library of functions
"""

"""
Homework1
Team3: Van Anh Le, Xinyu Shi, Haochun Wang
"""

import numpy as np
import matplotlib.pyplot as plt
import numbers
import math

class AbstractFunction:
    """
    An abstract function class
    """

    def derivative(self):
        """
        returns another function f' which is the derivative of x
        """
        raise NotImplementedError("derivative")


    def __str__(self):
        return "AbstractFunction"


    def __repr__(self):
        return "AbstractFunction"


    def evaluate(self, x):
        """
        evaluate at x

        assumes x is a numeric value, or numpy array of values
        """
        raise NotImplementedError("evaluate")


    def __call__(self, x):
        """
        if x is another AbstractFunction, return the composition of functions

        if x is a string return a string that uses x as the indeterminate

        otherwise, evaluate function at a point x using evaluate
        """
        if isinstance(x, AbstractFunction):
            return Compose(self, x)
        elif isinstance(x, str):
            return self.__str__().format(x)
        else:
            return self.evaluate(x)


    # the rest of these methods will be implemented when we write the appropriate functions
    def __add__(self, other):
        """
        returns a new function expressing the sum of two functions
        """
        return Sum(self, other)


    def __mul__(self, other):
        """
        returns a new function expressing the product of two functions
        """
        return Product(self, other)


    def __neg__(self):
        return Scale(-1)(self)


    def __truediv__(self, other):
        return self * other**-1


    def __pow__(self, n):
        return Power(n)(self)


    def plot(self, vals=np.linspace(-1, 1, 100), **kwargs):
        """
        plots function on values
        pass kwargs to plotting function
        """
        y = self.evaluate(vals)
        return plt.plot(vals, y, **kwargs)
        raise NotImplementedError("plot")
        
    # Taylor Series Implementation
    def taylor_series(self, x0, deg=5):
        """
        Taylor expansion, center could be chosen by yourself
        """
        Tf = Constant(self.evaluate(x0))
        fderived = self.derivative()
        for i in range(1, deg + 1):
            termToAdd = Product(Constant(fderived.evaluate(x0)/math.factorial(i)), Compose(Power(i),(Affine(1, -x0))))
            Tf = Sum(Tf, termToAdd)
            fderived = fderived.derivative()
        
        return Tf


class Polynomial(AbstractFunction):
    """
    polynomial c_n x^n + ... + c_1 x + c_0
    """

    def __init__(self, *args):
        """
        Polynomial(c_n ... c_0)

        Creates a polynomial
        c_n x^n + c_{n-1} x^{n-1} + ... + c_0
        """
        self.coeff = np.array(list(args))


    def __repr__(self):
        return "Polynomial{}".format(tuple(self.coeff))


    def __str__(self):
        """
        We'll create a string starting with leading term first

        there are a lot of branch conditions to make everything look pretty
        """
        s = ""
        deg = self.degree()
        for i, c in enumerate(self.coeff):
            if i < deg-1:
                if c == 0:
                    # don't print term at all
                    continue
                elif c == 1:
                    # supress coefficient
                    s = s + "({{0}})^{} + ".format(deg - i)
                else:
                    # print coefficient
                    s = s + "{}({{0}})^{} + ".format(c, deg - i)
            elif i == deg-1:
                # linear term
                if c == 0:
                    continue
                elif c == 1:
                    # suppress coefficient
                    s = s + "{0} + "
                else:
                    s = s + "{}({{0}}) + ".format(c)
            else:
                if c == 0 and len(s) > 0:
                    continue
                else:
                    # constant term
                    s = s + "{}".format(c)

        # handle possible trailing +
        if s[-3:] == " + ":
            s = s[:-3]

        return s


    def evaluate(self, x):
        """
        evaluate polynomial at x
        """
        if isinstance(x, numbers.Number):
            ret = 0
            for k, c in enumerate(reversed(self.coeff)):
                ret = ret + c * x**k
            return ret
        elif isinstance(x, np.ndarray):
            x = np.array(x)
            # use vandermonde matrix
            return np.vander(x, len(self.coeff)).dot(self.coeff)


    def derivative(self):
        if len(self.coeff) == 1:
            return Polynomial(0)
        return Polynomial(*(self.coeff[:-1] * np.array([n+1 for n in reversed(range(self.degree()))])))


    def degree(self):
        return len(self.coeff) - 1


    def __add__(self, other):
        """
        Polynomials are closed under addition - implement special rule
        """
        if isinstance(other, Polynomial):
            # add
            if self.degree() > other.degree():
                coeff = self.coeff
                coeff[-(other.degree() + 1):] += other.coeff
                return Polynomial(*coeff)
            else:
                coeff = other.coeff
                coeff[-(self.degree() + 1):] += self.coeff
                return Polynomial(*coeff)

        else:
            # do default add
            return super().__add__(other)


    def __mul__(self, other):
        """
        Polynomials are clused under multiplication - implement special rule
        """
        if isinstance(other, Polynomial):
            return Polynomial(*np.polymul(self.coeff, other.coeff))
        else:
            return super().__mul__(other)


class Affine(Polynomial):
    """
    affine function a * x + b
    """
    def __init__(self, a, b):
        super().__init__(a, b)

# Constant Function
class Constant(Polynomial):
    """
    Constant function: just input a number
    """
    def __init__(self, c):
        super().__init__(0, c)

# Scale Function
class Scale(Polynomial):
    """
    Scale function: ax + 0
    """
    def __init__(self, a):
        super().__init__(a, 0)

# Compose two functions
class Compose(AbstractFunction):
    """
    Five parts included
    Functions as f(g(x))
    """
    def __init__(self, A, B): # A and B are general functions
        self.A = A
        self.B = B
        
    def __repr__(self):
        return f"Compose({self.A}, {self.B})"
    
    def __str__(self): # for output
        return str(self.A).format(str(self.B))
    
    def evaluate(self, x): # evaluate value
        p = self.B.evaluate(x)
        return self.A.evaluate(p)
    
    def derivative(self): # derivative, returns an object
        return Product(self.B.derivative(), Compose(self.A.derivative(), self.B))

# Take Product of two functions
class Product(AbstractFunction):
    """
    Functions as f(x) * g(x)
    """
    def __init__(self, A, B): # A and B are general functions
        self.A = A
        self.B = B
        
    def __repr__(self):
        return f"Product({self.A}, {self.B})"
        
    def __str__(self):
        s = "{} * {}".format(str(self.A), str(self.B))
        return s
    
    def evaluate(self, x):
        return self.A.evaluate(x) * self.B.evaluate(x)
    
    def derivative(self):
        return self.A.derivative() * self.B + self.B.derivative() * self.A

# Sum of two functions
class Sum(AbstractFunction):
    def __init__(self, A, B): # A and B are general functions
        self.A = A
        self.B = B
        
    def __repr__(self):
        return f"Sum({self.A}, {self.B})"
        
    def __str__(self):
        return "{} + {}".format(str(self.A), str(self.B))
    
    def evaluate(self, x):
        return self.A.evaluate(x) + self.B.evaluate(x)
    
    def derivative(self):
        return self.A.derivative() + self.B.derivative()
    
# Power function, one input needed
class Power(AbstractFunction):
    """
    Power function, one input needed
    """
    def __init__(self, n, coefficient = 1):
        self.power = n
        self.coefficient = coefficient
        
    def __repr__(self):
        return "power"
    
    def __str__(self):
        
        if self.coefficient != 1:
            return str(self.coefficient) + " * {0} ^ " + str(self.power)
        else:
            return "{0} ^ " + str(self.power)
    
    def evaluate (self, x):
        return self.coefficient * (x ** self.power)
    
    def derivative (self): # derivative rule of power function
        return Power(self.power-1, coefficient = self.power)

# Log function, natural log by default
class Log(AbstractFunction):
    """
    Natural Log
    """
    def __init__(self):
        pass
        
    def __repr__(self):
        return "Natural Log"
    
    def __str__(self):
        return "Log{0}"
    
    def evaluate (self, x):
        return np.log(x)
    
    def derivative (self):
        return Power(-1)

# Exponential Function
class Exponential(AbstractFunction):
    """
    Exponential Function
    """
    def __init__(self):
        pass
        
    def __repr__(self):
        return "exponential"
    
    def __str__(self):
        return "exp({0})"
    
    def evaluate (self, x):
        return np.exp(x)
    
    def derivative (self):
        return Exponential()

# Sine Function
class Sin(AbstractFunction):
    """
    Sine function
    """
    def __init__(self):
        pass
    def __repr__(self):
        return "Sine"
    
    def __str__(self):
        return "sin({0})"
    
    def evaluate (self, x):
        return np.sin(x)
    
    def derivative (self):
        return Cos()

# Cosine Function
class Cos(AbstractFunction):
    """
    Cosine Function
    """
    def __init__(self):
        pass
    def __repr__(self):
        return "Cosine"
    
    def __str__(self):
        return "cos({0})"
    
    def evaluate (self, x):
        return np.cos(x)
    
    def derivative (self):
        return Product(Constant(-1),Sin())

# Symblolic Functions
class Symbolic(AbstractFunction):
    def __init__(self, functionName = 'f'):
        self.functionName = functionName
    def __repr__(self):
        return "Symbolic"
    def __str__(self):
        return self.functionName + "({0})"
    def __call__(self, InputVal):
        return "{}({})".format(self.functionName, InputVal)
    def derivative (self):
        return Symbolic("{}'".format(self.functionName))

# Problem1 PartA
    
# Newton Root algorithm
def newton_root(f, x0, tol=1e-8):
    """
    find a point x so that f(x) is close to 0,
    measured by abs(f(x)) < tol

    Use Newton's method starting at point x0
    """
    
    # The following three if/else statement is checking floating and AbstractFunction
    if not isinstance(f, AbstractFunction):
        raise ValueError('f should be inside the AbstractFunction Class')
        
    elif isinstance(f, Symbolic):
        raise ValueError('f should not be a Symbolic function')
        
    if not isinstance(x0, float):
        raise ValueError('x should be a floating number')
        
    else:
        x = x0
        fvalue = f.evaluate(x)
        iterationsList = []
        fvaluesList = []
        while (abs(fvalue) > tol):
            x = x - fvalue / (f.derivative().evaluate(x))
            fvalue = f.evaluate(x)
            iterationsList.append(x)
            fvaluesList.append(fvalue)
      
    return x

# Problem1 PartB

# Newton Root algorithm
def newton_extremum(f, x0, tol=1e-8):
    """
    Newton Extremum algorithm, starting point needed to be input, tolerance threshold could be changed
    """
    
    # The following three if/else statement is checking floating and AbstractFunction
    if not isinstance(f, AbstractFunction):
        raise ValueError('f should be inside the AbstractFunction Class')
        
    elif isinstance(f, Symbolic):
        raise ValueError('f should not be a Symbolic function')
        
    if not isinstance(x0, float):
        raise ValueError('x should be a floating number')
        
    else:
        fderiv = f.derivative()
        x = x0
        fderivValue = fderiv.evaluate(x)
        iterationsList = []
        fderivValuesList = []
        while (abs(fderivValue) > tol):
            x = x - fderivValue / (fderiv.derivative().evaluate(x))
            fderivValue = fderiv.evaluate(x)
            iterationsList.append(x)
            fderivValuesList.append(fderivValue)
        
        return x