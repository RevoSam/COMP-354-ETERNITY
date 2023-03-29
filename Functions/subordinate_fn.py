# Written by (add your name if you contributed pls)
# Roxane Morin, 40191881
# COMP 354

# Subordinate functions for Eternity

## Constants
EULER = 2.71828182845904523536
PI = 3.14159265358979323846
EPSILON = 1e-07


## Functions

## Conversions

# Convert z to degrees.
def deg(z):
   return z * PI/180


## General maths.

# Return the absolute value of z.
def abs(z):
   return z if (z >= 0) else -z

# Return z!
def factorial(z):
   # check invalid input
   if (z<0 or not isinstance(z, int)):
      return None
   if (z == 1):
      return z
   else:
      return z*factorial(z-1)

# Return the square root of z.
def sqrt(z):
   # check invalid input
   if (z < 0):
      return None
   return z ** 0.5

# Return x^y.
def power(x,y):
    if y == 0:
        return 1
    else:
        result = 1
        for i in range(y):
            result = result * x
    return result


## Trigonometry

# Taylor series approximation of sin(z)
# formula @ https://web.ma.utexas.edu/users/m408s/m408d/CurrentWeb/LM11-10-4.php
def sin(z):
   n = 75  #precision
   y = 0
   for i in range(0,n,1):
      y = y + ((-1)**i) * (z**(2*i+1)) / factorial(2*i+1)
   return y


## Array operations

# Return the sum of an arraylike's numerical elements.
def sum(arraylike):
    sum = 0
    for item in arraylike:
        sum += item
    return sum




## Misc 
    

