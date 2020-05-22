

'''
This file is for creating a test to obtain the optimum epsilon and scaling
coefficient for mechanical analysis in finding the linear regions of the data

optimization function:
                adjusted r-square:
                    R_adjusted = 1 - ( 1-r_squared * (N-1) ) / (N - K - 1)

                    where N is number of data points, K is number of lines
'''


# import data

# function to get the adjusted r-squared value
def _computeAdjustedRsquared(data):
    pass

# for number of data sets obtain optimization parameters
