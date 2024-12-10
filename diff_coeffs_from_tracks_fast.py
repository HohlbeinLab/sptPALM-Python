#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This work is licensed under the CC BY 4.0 License.
You are free to share and adapt this work, even for commercial purposes,
as long as you provide appropriate credit to the original creator.

Original Creator: Johannes Hohlbein (Wageningen University & Research)
Date of Creation: September, 2024

Full license details can be found at https://creativecommons.org/licenses/by/4.0/
"""

import numpy as np
import pandas as pd
import time



def diff_coeffs_from_tracks_fast(tracks, para):

# from typing import List, Tuple, Dict
# def diff_coeffs_from_tracks_fast(tracks: List[List], para: [Dict|none]) -> Tuple(int, np.ndarray()):

    """
    some description
    
    @params:
        tracks: a list of tracks
    """
    
    print("\nRun 'diff_coeffs_from_tracks_fast.py'")

    # Initialize
    tracks_data = tracks.copy()
    # Count occurrences of each unique track_ids
    tracklength_counts = tracks_data['track_id'].value_counts()    
    
    # Map these counts back to the DataFrame as a new column '#_loc'
    tracks_data['#_locs'] = tracks_data['track_id'].map(tracklength_counts)
    # Some more additions
    tracks_data['MSD'] = np.nan
    tracks_data['D_coeff'] = np.nan
    tracks_data['frametime'] = para['frametime']
    
    start = time.time() 

    # For each tracklength in para
    for i, track_len in enumerate(para['tracklengths_steps']):
        # Find all tracks with a certain number of localisations per track
        idx = tracks_data.index[tracks_data['#_locs'] == track_len + 1].tolist()
        # If idx is not empty/false
        if idx: # implicit booleanness
            tracks_data.loc[idx,'MSD'] = calculate_MSD(tracks_data.loc[idx,:],
                                                       'x [µm]', 'y [µm]', track_len + 1)
    
    # How long did the MSD calculation take?
    end = time.time()
    rounded_time = round(end-start, 2)
    print(f"  Time for MSD calculation: {rounded_time} seconds")


    # # Correct for localization error if specified (option in anaDDA does require to switch that off)
    # # what is the best correction here? Michelet 2010 reduced localization error? 
    # if 'correct_diff_calc_loc_error' in para: 
    #     if para['correct_diff_calc_loc_error']:
    #         loc_error_correction = np.random.normal(0, para['loc_error'], 
    #                                             len(tracks_data.loc[:, 'D_coeff']))**2 / para['frametime']
    # else:
    #     print('log error connection = 0')
    #     loc_error_correction = 0

    loc_error_correction =  (para['loc_error'] ** 2)/para['frametime']
    tracks_data['D_coeff'] = tracks_data['MSD'] / (4 * para['frametime']) - loc_error_correction

    D = tracks_data.copy()

    # Create the histogram of diffusion coefficients as a function of track lengths
    if para['plot_option'] == 'logarithmic':
        edges = np.arange(np.log10(para['plot_diff_hist_min']),
                      np.log10(para['plot_diff_hist_max']) + para['binwidth'],
                      para['binwidth'])
    else:
        edges = np.arange(0, para['plot_diff_hist_max'] + para['binwidth'],
                      para['binwidth'])      

    D_track_length_matrix = pd.DataFrame(np.zeros((len(edges),
                                                   len(para['tracklengths_steps']) + 1)),
                                         columns=['Bins'] + list(para['tracklengths_steps']))  
 
    if para['plot_option'] == 'logarithmic':
        D_track_length_matrix.loc[:, 'Bins'] = 10 ** edges
    else:
        D_track_length_matrix.loc[:, 'Bins'] = edges
    
    for i, track_len in enumerate(para['tracklengths_steps']):
        # Use idx_track_ids to prevent counting diffusion coefficients several times
        idx = tracklength_counts.index[tracklength_counts[:] == track_len + 1].tolist()
        if idx:
            hist, _ = np.histogram(D.loc[idx, 'D_coeff'], D_track_length_matrix.loc[:, 'Bins'])
            D_track_length_matrix.loc[D_track_length_matrix.index[:-1], track_len] = hist

    return D, D_track_length_matrix


# Generalized function to calculate differences between two columns in groups of rows
def calculate_MSD(df, col_name1, col_name2, group_size):
    
    """
    Calculates the differences between two columns within non-overlapping groups of rows.
    
    Parameters:
    df (DataFrame): The DataFrame containing the data.
    col_name1 (str): The first column name.
    col_name2 (str): The second column name.
    group_size (int): The number of rows per group to calculate differences for.
    
    Returns:
    MSD (array): A 2D array where each row contains the differences for one group.
    """
    # Extract the two columns as NumPy arrays
    x_positions = df[col_name1].values
    y_positions = df[col_name2].values
    
    # Determine the number of complete groups
    num_groups = len(x_positions) // group_size
    
    # Reshape the values into a matrix of shape (num_groups, group_size)
    reshaped_x_positions = x_positions[:num_groups * group_size].reshape(num_groups, group_size)
    reshaped_y_positions = y_positions[:num_groups * group_size].reshape(num_groups, group_size)
    
    squared_displacements = np.diff(reshaped_x_positions)**2 + np.diff(reshaped_y_positions)**2
    # breakpoint()
# Careful some checks missing!
# Adjust based on frame differences
#     D_coeff_contribution = np.where(frame_diff == 2, squared_displacements / 2, squared_displacements)
    MSD = squared_displacements.mean(axis = 1)
    
    #Ensure that D_coff is showing up behind each localisation later
    MSD = np.repeat(MSD, group_size, axis = None)
    
    
    return MSD

