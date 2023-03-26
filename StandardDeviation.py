# Written by Roxane Morin, 40191881
# COMP 354

import numpy as np

def standard_deviation(data_points, sample_sd):
    
    ## Should we convert the data_points list to an array just to be safe?
    ## Might need to change len vs size depending on the format they'll come in.
    
    sum_data = np.sum(data_points)
    mean = sum_data / len(data_points)
    
    N = len(data_points)
    if (sample_sd == True):
        N -= 1
    
    sum_diff = 0
    for point in data_points:
        sum_diff += np.power(point - mean, 2)
    sd = np.sqrt(sum_diff / N)
    
    print(sd)
    return sd


#test_points = [12, 11, 17, 15, 13, 12, 14]

#standard_deviation(test_points, False)
#standard_deviation(test_points, True)