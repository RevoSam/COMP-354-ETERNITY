# Subordinate functions for Eternity

EULER = 2.71828182845904523536
PI = 3.14159265358979323846
EPSILON = 1e-07

def abs(z):
   return z if (z >= 0) else -z

def factorial(z):
   # check invalid input
   if (z<0 or not isinstance(z, int)):
      return None
   if (z == 1):
      return z
   else:
      return z*factorial(z-1)

def deg(z):
   return z * PI/180

def sqrt(z):
   # check invalid input
   if (z < 0):
      return None
   return z ** 0.5

# Taylor series approximation
def sin(z):
   z = deg(z)
   n = 75  #precision
   y = 0
   for i in range(0,n,1):
      y = y + ((-1)**i) * (z**(2*i+1)) / factorial(2*i+1)
   return y

def exp(z):
   return EULER ** z