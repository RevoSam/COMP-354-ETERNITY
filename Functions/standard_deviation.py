# Written by Roxane Morin, 40191881
# COMP 354

from Functions.subordinate_fn import sqrt, power, sum


def standard_deviation(data_points, sample_sd):
    
    ## Should we convert the data_points list to an array just to be safe?
    ## Might need to change len vs size depending on the format they'll come in.
    
    sum_data = sum(data_points)
    mean = sum_data / len(data_points)
    
    N = len(data_points)
    sd_type = "Population"
    if (sample_sd == True):
        N -= 1
        sd_type = "Sample"
    
    sum_diff = 0
    for point in data_points:
        sum_diff += power(point - mean, 2)
    sd = sqrt(sum_diff / N)
    
    # Here for testing purposes. Comment out during implementation.
    print("{0} standard deviation: {1}.".format(sd_type, sd))
    
    return sd


def standard_deviation_tests():
    
    # Integer values.
    print("\nStandard deviation of the integer values [12, 11, 17, 15, 13, 12, 14, 15].")
    print("Expected values:\nPopulation standard deviation: 1.8666480653835.\nSample standard deviation: 1.9955307206713.\nActual values:")
    test_points = [12, 11, 17, 15, 13, 12, 14, 15]
    standard_deviation(test_points, False)
    standard_deviation(test_points, True)
    
    # Floating point values.
    print("\nStandard deviation of the floating point values [2.5, 3.4, 2.1, 3.1, 3.2, 2.9] :")
    print("Expected values:\nPopulation standard deviation: 0.44221663871405.\nSample standard deviation: 0.4844240566556.\nActual values:")
    test_points = [2.5, 3.4, 2.1, 3.1, 3.2, 2.9]
    standard_deviation(test_points, False)
    standard_deviation(test_points, True)
    
    # Mixed values.
    print("\nStandard deviation of the mixed values [7, 6.5, 7.5, 6, 3, 5.6] :")
    print("Expected values:\nPopulation standard deviation: 1.4510532573119.\nSample standard deviation: 1.5895492023422.\nActual values:")
    test_points = [7, 6.5, 7.5, 6, 3, 5.6]
    standard_deviation(test_points, False)
    standard_deviation(test_points, True)


#standard_deviation_tests()