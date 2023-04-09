
import Functions.subordinate_fn as subordinateFunctions

"""------------------------------
STANDARD DEVIATION
Roxane Morin, 40191881
------------------------------"""

def standard_deviation(data_points, sample_sd):
    
    ## Should we convert the data_points list to an array just to be safe?
    ## Might need to change len vs size depending on the format they'll come in.
    
    sum_data = subordinateFunctions.sum(data_points)
    mean = sum_data / len(data_points)
    
    N = len(data_points)
    sd_type = "Population"
    if (sample_sd == True):
        N -= 1
        sd_type = "Sample"
    
    sum_diff = 0
    for point in data_points:
        sum_diff += (point - mean)**2
    sd = subordinateFunctions.sqrt(sum_diff / N)
    
    # Here for testing purposes. Comment out during implementation.
    # print("{0} standard deviation: {1}.".format(sd_type, sd))
    
    return sd

"""------------------------------
Mean Absolute Deviation
Sami NAJIM, 21289640
------------------------------"""

def mad(data_points):
    
    sum_data = subordinateFunctions.sum(data_points)
    mean = sum_data / len(data_points)
    
    N = len(data_points)
    
    sum_abs = 0
    for point in data_points:
        sum_abs += subordinateFunctions.abs(point - mean)
    mad = sum_abs / N
    
    # Here for testing purposes. Comment out during implementation.
    # print("Sample size {0}, Avg: {1}, MAD: {2}", N, mean, mad)
    
    return mad

"""------------------------------
AB^X
Yirun Liu 40067857
------------------------------"""

def natural_exp(a, b, x):
    return a * pow(b,x)

"""------------------------------
SINH(X) & X^Y
Chuanqi Mo
------------------------------"""

# hyperbolic sine function
def sinh(x):
    return (subordinateFunctions.exp(x) - subordinateFunctions.exp(-x)) / 2

# power function x^y
def power(x,y):
    return x**y

"""------------------------------
GAMMA
Hong Nhat Ai Nguyen 40192995
------------------------------"""

# lanczos approximation of gamma
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
    y = subordinateFunctions.PI/(subordinateFunctions.sin(subordinateFunctions.PI*z)*gamma(1.0 - z))
  else:
    z = z - 1.0
    base = z + g + 0.5
    sum = 0
    i = n
    while (i>=1):
        sum += p[int(i)]/ (z + i)
        i -= 1
    sum += p[0]
    y = subordinateFunctions.sqrt(2.0*subordinateFunctions.PI)*sum*base**(z + 0.5)*subordinateFunctions.exp(-base)

  return y

"""------------------------------
ARCCOS
Christopher Lopez, 40199547
------------------------------"""
    
def arccos(x):
    if x == 1:
        return 0
    elif x == -1:
        return subordinateFunctions.PI
    elif x < -1 or x > 1:
        return None
    lower = 0
    upper = subordinateFunctions.PI
    while True:
        mid = (lower + upper) / 2
        if abs(subordinateFunctions.cosine(mid) - x) <= subordinateFunctions.EPSILON:
            return mid
        elif subordinateFunctions.cosine(mid) > x:
            lower = mid
        else:
            upper = mid
