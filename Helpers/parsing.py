# Roxane Morin, 40191881
# Hong Nhat Ai Nguyen, 40192995
# COMP 354

# method to parse multiple values for MAD and SD
def parse_string_multi_values(data_points):
    values = []
    # return None if there's 1 value or less
    if (len(data_points) <= 1):
        return None
    # try to convert values from string to floats
    try:
        values = [float(value) for value in data_points]
    # return None if any value is not a real number 
    except ValueError:
        return None
        
    return values

# Parentheses matching function
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
    
# convert a string to int or float
def convert_str_to_num(s):
    try:
        # convert string to int if appropriate, else float
        f = float(s)
        i = int(f)
        return i if i == f else f
    # return None if value is not a real number 
    except ValueError:
        return None
    
# method to check if passed string(s) can be converted to a number
def is_numerical(string_inputs):
    if len(string_inputs) == 0:
        return False
    else:
        # go through strings in the list
        for s in string_inputs:
            # return False if any string passed CANNOT be converted to a number
            if (convert_str_to_num(s) is None):
                return False
        # return True if all strings passed can be converted to a number
        return True
