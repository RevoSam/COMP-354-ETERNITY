# Hong Nhat Ai Nguyen

# lanczos approximation

from subordinate_fn import PI, sin, sqrt, exp

def gamma(z):
  
  # check invalid input
  if (z <= 0):
     return None
  
  # table of coefficients derived by Paul Godfrey @ http://www.numericana.com/answer/info/godfrey.htm
  # relative error less than 10^-13
  g = 9
  n = 10
  p = [
    1.000000000000000174663,
 	  5716.400188274341379136,
 	  -14815.30426768413909044,
 	  14291.49277657478554025,
 	  -6348.160217641458813289,
 	  1301.608286058321874105,
 	  -108.1767053514369634679,
 	  2.605696505611755827729,
 	  -0.7423452510201416151527e-2,
 	  0.5384136432509564062961e-7,
 	  -0.4023533141268236372067e-8
  ]

  if (z < 0.5):
    # Euler's reflection formula
    y = PI/(sin(PI*z)*gamma(1.0 - z))
  else:
    z = z - 1.0
    base = z + g + 0.5
    sum = 0
    i = n
    while (i>=1):
        sum += p[int(i)]/ (z + i)
        i -= 1
    sum += p[0]
    y = sqrt(2.0*PI)*sum*base**(z + 0.5)*exp(-base)

  return y