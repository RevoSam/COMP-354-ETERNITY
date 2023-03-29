# Written by Christopher Lopez, 40199547
# COMP 354

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def cosine(x, epsilon=1e-10):
    result = 0
    n = 0
    while True:
        term = ((-1) * n) * (x * (2 * n)) / factorial(2 * n)
        result += term
        if abs(term) <= epsilon:
            break
        n += 1
    return result
    
def arccos(x, epsilon=1e-10):
    if x == 1:
        return 0
    elif x == -1:
        return 3.141592653589793
    elif x < -1 or x > 1:
        raise ValueError("x must be between -1 and 1")
    lower = 0
    upper = 3.141592653589793
    while True:
        mid = (lower + upper) / 2
        if abs(cosine(mid) - x) <= epsilon:
            return mid
        elif cosine(mid) > x:
            lower = mid
        else:
            upper = mid

