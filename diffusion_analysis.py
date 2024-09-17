#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import pandas as pd
import numpy as np
import os


def diffusion_analysis(para):
    print('\nRun diffusion_analysis.py')

    # Find unique elements in the track_id column
    track_ids, ic = np.unique(para['tracks']['track_id'], return_inverse=True)
    track_length = np.bincount(ic)
    track_ids_length = np.column_stack((track_ids, track_length))
 
    # Filter tracks that are longer than DiffHistSteps_min and shorter than DiffHistSteps_max
    filter_vec = (track_length > para['diff_hist_steps_min']) & (track_length < para['diff_hist_steps_max'])
    track_ids_length_filtered = track_ids_length[filter_vec, :]

    # Create empty vector for MSDs
    msd = np.zeros(len(track_ids_length_filtered))
   
    diffs_df = pd.DataFrame()
    # For each track (which can have many localizations/positions)
    print("  MSD analysis...")
    for ii in range(len(track_ids_length_filtered)):
        if ii % 500 == 0 and ii > 0:
            print(f"   ...track {ii} out of {len(track_ids_length_filtered)} valid tracks,")
        temp_array = para['tracks'][para['tracks']['track_id'] == track_ids_length_filtered[ii,0]]
    
        # Calculate averaged MSD for DiffHistSteps_min + 1 steps
        for jj in range(para['diff_hist_steps_min']):
            con = temp_array.iloc[jj+1]['frame'] - temp_array.iloc[jj]['frame']
            
            # Account for 1-frame memories
            if con <= para['track_memory'] + 1 and con != 0:
                # Calculate MSD (single frame MSD!)
                msd[ii] += (((temp_array.iloc[jj+1]['x [um]'] - temp_array.iloc[jj]['x [um]']) ** 2 + 
                              (temp_array.iloc[jj+1]['y [um]'] - temp_array.iloc[jj]['y [um]']) ** 2) / con)
            else:
                msd[ii] += ((temp_array.iloc[jj+1]['x [um]'] - temp_array.iloc[jj]['x [um]']) ** 2 + 
                            (temp_array.iloc[jj+1]['y [um]'] - temp_array.iloc[jj]['y [um]']) ** 2)

        # Divide by total number of steps
        msd[ii] /= para['diff_hist_steps_min']  # Mean square displacement

    print(f"   ...track {ii+1} out of {len(track_ids_length_filtered)} valid tracks.")

    # Calculate diffusion coefficient from MSD and correct for localization noise
    diffquot = msd/(4 * para['frametime']) - (para['sigma_noise'] ** 2)/para['frametime']

    # Save data
    diffs_df = pd.DataFrame({
        'diff_coeffs_filtered': diffquot,
        'track_length_filtered': track_ids_length_filtered[:, 1],
        'track_id': track_ids_length_filtered[:, 0]
        })

    if not diffs_df.empty:  # Check if diffs_df is not empty
        # Save data into a new *.csv file
        temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
        diffs_df.to_csv(temp_path + para['fn_locs'][:-4] + para['fn_diffs_handle'], index=False, quoting=3)  # quoting=3 corresponds to 'QUOTE_NONE'
        print('  Diffusion analysis done and diffusion coefficients saved!')
    else:
        print('  Careful, empty list of diffusion coefficients returned!')

    para['diff_coeffs_filtered_list'] = diffs_df
    
    
    return para



