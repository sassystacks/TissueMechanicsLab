# -*- coding: utf-8 -*-
r"""
Created on Tue Jun 23 17:34:18 2020

@author: tongtuanthinh@gmail.com
Data in this code is arranged in the following order:
    1 folder containing sub-folder, each sub-folder is one patient's data
    In each sub-folder, all of the binned data was located without any other sub-folders under these
    sub-folders
"""

import pandas as pd; 
import numpy as np;
import matplotlib.pyplot as plt;
import math;

r""" This function is to count number of data points in both directions after data is processed by the
binning program of Richard; 
The funtion requires patient_ID and protocol as well as file_type to process; 
At the same time, one may want to change the folder_path to get the code work properly 
"""
def data_points_count(df):    
    number_data_points_11 = 0;
    number_data_points_22 = 0;
    minus_11 = 0;
    minus_22 = 0; 
    for m in range(len(df[['S11']])):
        if math.isnan(df.S11[m]):
            minus_11 = minus_11 + 1;
    for n in range(len(df[['S22']])):
        if math.isnan(df.S22[n]):
            minus_22 = minus_22 + 1; 
    number_data_points_11 = len(df[['S11']]) - minus_11;
    number_data_points_22 = len(df[['S22']]) - minus_22;
    return(number_data_points_11, number_data_points_22);


r""" This function is to count number of data points in each "bin"; "bin" here is calculated by the range of 
min-max stretch divided by number of bins that we want; 
number of bins is the same as number of data points that we want to target it out; ideally, we want in each bin there is one data point only
BOTH DIRECTION AT A TIME!; equal bin size!
max_data_points is to get rid of the NaN values in the series 

This function also takes average of all of the data points in the same bin so that all of the count in
one bin is equal to 1 or 0; this helps to ease the interpolation step laters;
This function accepts the input of a data frame and gives out a data frame with average values for those bin that
has more than 2 data points
"""
def average(df, number_of_bins, max_data_points_11, max_data_points_22):
    
    # create arrays to store number of data points in each bin: from 0 to (number_of_bins - 1)
    dt_point_bin_11 = [0] * number_of_bins;
    dt_point_bin_22 = [0] * number_of_bins;
    
    #create a list to fill in values 
    E11_dots = [0] * number_of_bins;
    E22_dots = [0] * number_of_bins;
    S11 = [0] * number_of_bins;
    S22 = [0] * number_of_bins;
    
    #extract values from df
    stretch_11 = df['E11(dots)'];
    Cauchy_11 = df['S11'];
    stretch_22 = df['E22(dots)'];
    Cauchy_22 = df['S22']
    
    # 11-direction
    min_stretch11 = min(df['E11(dots)']);
    max_stretch11 = max(df['E11(dots)']);
    bin_size11 = (max_stretch11 - min_stretch11)/number_of_bins;
    for i in range(number_of_bins):
        count = 0;
        for j in range(max_data_points_11):
            lower_limit = min_stretch11 + i * bin_size11;
            upper_limit = min_stretch11 + (i + 1) * bin_size11; 
            if (stretch_11[j] >= lower_limit) and (stretch_11[j] <= upper_limit):
                count = count + 1;
                if (count == 1):
                    E11_dots[i] = stretch_11[j];
                    S11[i] = Cauchy_11[j];
                if (count > 1):
                    E11_dots[i] = np.average(stretch_11[(j-count+1):(j+1)]);
                    S11[i] = np.average(Cauchy_11[(j-count+1):(j+1)]);
        dt_point_bin_11[i] = count;
    # 22-direction
    min_stretch22 = min(df['E22(dots)']);
    max_stretch22 = max(df['E22(dots)']);
    bin_size22 = (max_stretch22 - min_stretch22)/number_of_bins;
    for i in range(number_of_bins):
        count = 0;
        for j in range(max_data_points_22):
            lower_limit = min_stretch22 + i * bin_size22;
            upper_limit = min_stretch22 + (i + 1) * bin_size22; 
            if (stretch_22[j] >= lower_limit) and (stretch_22[j] <= upper_limit):
                count = count + 1;
                if (count == 1):
                    E22_dots[i] = stretch_22[j];
                    S22[i] = Cauchy_22[j];
                if (count > 1):
                    E22_dots[i] = np.average(stretch_22[(j-count+1):(j+1)]);
                    S22[i] = np.average(Cauchy_22[(j-count+1):(j+1)]);
        dt_point_bin_22[i] = count;
    Update_df = pd.DataFrame({'E11(dots)': E11_dots, 'E22(dots)': E22_dots, 'S11':S11, 'S22': S22},
                             columns = ['E11(dots)', 'E22(dots)', 'S11', 'S22']);
    return(dt_point_bin_11, dt_point_bin_22, Update_df);


r""" Based on number of data points input, the function creates 
the extra number of data points (which is the n parameters) required to be added between the lower and upper values;
Please note that this is linear interpolation; The data points added are equally spaced in the x-direction
"""

def interpolate_number_of_points_added(lower_x, upper_x, lower_y, upper_y, n):
    number_of_gaps = n + 1;
    x_array = [0] * n;
    y_array = [0] * n;
    gap_value = (upper_x - lower_x)/number_of_gaps;
    for i in range(n):
        x_array[i] = lower_x + i * gap_value;
    for j in range(n):
        y_array[j] = lower_y + (upper_y - lower_y)/(upper_x - lower_x) * (x_array[j] - lower_x);
    return(x_array, y_array);

r""" This function is to added to the number of interpolating points towards those bins with 0 points in it;
see interpolate_number_of_points_added as a function to be used extensively in this function;
The function first identifies index of those bins with at least 1 data point in that bin; then from these, calculate the bins without any points in it and based on it to do interpolation;  
"""

def interpolate_step(dt_point_bin_11, dt_point_bin_22, update_df, folder_path, patient, protocol, number_of_bins):
    # count number of bins that have at least 1 data point
    bins_in_string = str(number_of_bins);
    count_11_direction = 0;
    for i in range(len(dt_point_bin_11)):
        if (dt_point_bin_11[i] > 0):
            count_11_direction = count_11_direction + 1;

    count_22_direction = 0;
    for i in range(len(dt_point_bin_22)):
        if (dt_point_bin_22[i] > 0):
            count_22_direction = count_22_direction + 1;
    
    #store index values of bins with at least more than 1 data point
    index_of_1_11_direction = [0] * count_11_direction;
    index_of_1_22_direction = [0] * count_22_direction;
    #11 direction
    i = 0;
    for m in range(len(dt_point_bin_11)):
        if (dt_point_bin_11[m] > 0):
            index_of_1_11_direction[i] = m;
            i = i + 1;
    #22 direction
    j = 0;
    for m in range(len(dt_point_bin_22)):
        if (dt_point_bin_22[m] > 0):
            index_of_1_22_direction[j] = m;
            j = j + 1;
    #interpolate, added in values now
    #extract values from df
    stretch_11 = update_df['E11(dots)'];
    Cauchy_11 = update_df['S11'];
    stretch_22 = update_df['E22(dots)'];
    Cauchy_22 = update_df['S22']
    #11 direction 
    for i in range(len(index_of_1_11_direction)-1):
        count = index_of_1_11_direction[i+1] - index_of_1_11_direction[i];
        [x_array_11, y_array_11] = interpolate_number_of_points_added(stretch_11[index_of_1_11_direction[i]],
                                             stretch_11[index_of_1_11_direction[i+1]],
                                             Cauchy_11[index_of_1_11_direction[i]],
                                             Cauchy_11[index_of_1_11_direction[i+1]],
                                             count);
        stretch_11[(index_of_1_11_direction[i]):(index_of_1_11_direction[i]+count)] = x_array_11;
        Cauchy_11[(index_of_1_11_direction[i]):(index_of_1_11_direction[i]+count)] = y_array_11;
    for i in range(len(index_of_1_22_direction)-1):
        count = index_of_1_22_direction[i+1] - index_of_1_22_direction[i];
        [x_array_22, y_array_22] = interpolate_number_of_points_added(stretch_22[index_of_1_22_direction[i]],
                                             stretch_22[index_of_1_22_direction[i+1]],
                                             Cauchy_22[index_of_1_22_direction[i]],
                                             Cauchy_22[index_of_1_22_direction[i+1]],
                                             count);
        stretch_22[(index_of_1_22_direction[i]):(index_of_1_22_direction[i]+count)] = x_array_22;
        Cauchy_22[(index_of_1_22_direction[i]):(index_of_1_22_direction[i]+count)] = y_array_22;
    final_df = pd.DataFrame({'E11(dots)': stretch_11, 'E22(dots)': stretch_22, 'S11':Cauchy_11, 'S22': Cauchy_22},
                             columns = ['E11(dots)', 'E22(dots)', 'S11', 'S22']);
    File_final_name = folder_path + "\\" + patient + '\\Interpolated_4Dots_Stretch_Cauchy_' + protocol + "bin_" + bins_in_string + '.txt';
    final_df.to_csv(File_final_name);
    return (final_df);

#This function is to compared raw binned data vs interpolated data in a graph form

def plot_comparison(binned_df, final_df, folder_path, protocol, number_of_bins):
    
    binned_stretch_11 = binned_df['E11(dots)'];
    binned_Cauchy_11 = binned_df['S11'];
    binned_stretch_22 = binned_df['E22(dots)'];
    binned_Cauchy_22 = binned_df['S22'];

    final_stretch_11 = final_df['E11(dots)'];
    final_Cauchy_11 = final_df['S11'];
    final_stretch_22 = final_df['E22(dots)'];
    final_Cauchy_22 = final_df['S22'];
    
    #11_directions
    fig = plt.figure();
    ax1 = fig.add_subplot(111);
    ax1.scatter(final_stretch_11, final_Cauchy_11, s=10, c='r', marker="o", label='Final' );
    ax1.scatter(binned_stretch_11, binned_Cauchy_11, s=10, c='b', marker="s", label='Binned');
    plt.legend(loc = 'upper left');
    plt.show();
  
    #22_direction
    fig = plt.figure();
    ax2 = fig.add_subplot(111);
    ax2.scatter(final_stretch_22, final_Cauchy_22, s=10, c='r', marker="o", label='Final' );
    ax2.scatter(binned_stretch_22, binned_Cauchy_22, s=10, c='b', marker="s", label='Binned');
    plt.legend(loc = 'upper left');
    plt.show();

#declare patient ID and protocol interests (which will be put into a loop in the future)
# declare glocal variables such as folder_path and file_type as well as loops in patients and protocols
folder_path = r'Z:\NIH_BAV_Project\Undergrad_Research\2_Code\Richard_Binning_Data\Binned_Data';
patients = ['1GC4', '13GC6', '13P2', '14P2', '18GC3', '20A3', '21A3', '21GC3', '23GC6', '25A13'];
file_type = '4Dots_Stretch_Cauchy_'; 
protocols = ['1_1', '1_05', '1_02', '05_1', '02_1'];
number_of_bins = [20, 50, 100, 200];
#for loops to loop through patients under the same folder of binning data::
for i in patients:
    for j in protocols:
        for n in number_of_bins:
            file_name = folder_path +"\\" + i + "\\4Dots_Stretch_Cauchy_"  + j + ".txt";
            df = pd.read_csv(file_name);
            [points_max_11, points_max_22] = data_points_count(df);
            [bin_11, bin_22, update_df] = average(df, n, points_max_11, points_max_22);
            final_df = interpolate_step(bin_11, bin_22, update_df, folder_path, i, j, n);
            plot_comparison(df, final_df, folder_path, j, n);