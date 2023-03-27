import math

# power function x^y
def power(x,y):
    if y == 0:
        return 1
    else:
        result = 1
        for i in range(y):
            result = result * x
    return result

# hyperbolic sine function
def sinh(x):
    e = math.e
    return (pow(e,x) - pow(e,-x)) / 2

# parentheses matching function
def parenthesesMatching(s):
    stack = []
    for i in range(len(s)):
        if s[i] == '(':
            stack.append(s[i])
        elif s[i] == ')':
            if len(stack) == 0:
                return False
            else:
                stack.pop()
    if len(stack) == 0:
        return True
    else:
        return False

# print(power(2,10))
# print(sinh(1.0))
# print(parenthesesMatching('((a+b)*(c+d)))'))