# Written by Roxane Morin, 40191881
# COMP 354

def parse_string_single_value(tk_string):
    value = None

    try:
        value = float(tk_string)
    except:
        print("Invalid input.\nThis function only accepts a single number.")
        # Reset the input window?
    
    return value


def parse_string_multi_values(tk_string):
    values = None
    
    try:
        values = [float(value) for value in tk_string.replace(";", ",").split(",")]
        # Should we also reject lone values?
    except:
        print("Invalid input.\nThis function only accepts numbers separated by commas.")
        # Reset the input window?
    
    return values
    

# Parse the context of a checkbox for boolean choices?
#


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



# TESTS

def parse_string_single_value_tests():
    
    print("\nAttempt at parsing the string \"1.12\" :")
    print(parse_string_single_value("1.12"))
    
    print("\nAttempt at parsing the string \"7\" :")
    print(parse_string_single_value("7"))
    
    print("\nAttempt at parsing the string \"Obi the java sparrow\" :")
    print(parse_string_single_value("Obi the java sparrow"))


def parse_string_multi_values_tests():
    
    print("\nAttempt at parsing the string \"1, 2.4, 3, 27, 10.11, 2\" :")
    print(parse_string_multi_values("1, 2.4, 3, 27, 10.11, 2"))
    
    print("\nAttempt at parsing the string \"1.2\" :")
    print(parse_string_multi_values("1.2"))

    print("\nAttempt at parsing the string \"I love to eat, 1, salad in the morning.\" :")
    print(parse_string_multi_values("I love to eat, 1, salad in the morning."))
    
# convert a strng to int or float
def convert_str_to_num(s):
    try:
        f = float(s)
        i = int(f)
        return i if i == f else f
    except ValueError:
        return None

def main():
    pass
    # Do the tests 
    parse_string_single_value_tests()
    parse_string_multi_values_tests()
if __name__ == "__main__":
    main()