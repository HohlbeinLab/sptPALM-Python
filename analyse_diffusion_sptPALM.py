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


import pandas as pd
import numpy as np
import os


def analyse_diffusion_sptPALM(para):
    print('\nRun analyse_diffusion_sptPALM.py')

    # Find unique elements in the track_id column
    track_ids, ic = np.unique(para['tracks']['track_id'], return_inverse=True)
    track_length_steps = np.bincount(ic) #steps or locs? Think these are steps (= locs + 1)
    track_ids_length = np.column_stack((track_ids, track_length_steps))
    # Select tracks that are longer than diff_hist_steps_min and shorter than diff_hist_steps_max
    filter_vec = (track_length_steps > para['diff_hist_steps_min']) & (track_length_steps < para['diff_hist_steps_max'])
    track_ids_length_filtered = track_ids_length[filter_vec, :]

    # Create empty vector for MSDs
    msd = np.zeros(len(track_ids_length_filtered))
   
    diffs_df = pd.DataFrame()
    # For each track (which can have many localizations)
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
                msd[ii] += (((temp_array.iloc[jj+1]['x [µm]'] - temp_array.iloc[jj]['x [µm]']) ** 2 + 
                              (temp_array.iloc[jj+1]['y [µm]'] - temp_array.iloc[jj]['y [µm]']) ** 2) / con)
            else:
                msd[ii] += ((temp_array.iloc[jj+1]['x [µm]'] - temp_array.iloc[jj]['x [µm]']) ** 2 + 
                            (temp_array.iloc[jj+1]['y [µm]'] - temp_array.iloc[jj]['y [µm]']) ** 2)

        # Divide by total number of steps
        msd[ii] /= para['diff_hist_steps_min']  # Mean square displacement

    print(f"   ...track {ii+1} out of {len(track_ids_length_filtered)} valid tracks.")

    # Calculate diffusion coefficient from MSD and correct for localization error
    diffquot = msd/(4 * para['frametime']) - (para['loc_error'] ** 2)/para['frametime']

    # Save data
    diffs_df = pd.DataFrame({
        'diff_coeffs_filtered': diffquot,
        'track_length_filtered': track_ids_length_filtered[:, 1],
        'track_id': track_ids_length_filtered[:, 0]
        })

    if not diffs_df.empty:  # Check if diffs_df is not empty
        # # Save data into a new *.csv file
        # temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
        # diffs_df.to_csv(temp_path + para['fn_locs'][:-4] + para['fn_diffs_handle'], index=False, quoting=3)  # quoting=3 corresponds to 'QUOTE_NONE'
        print('  Diffusion analysis done and diffusion coefficients saved!')
    else:
        print('  Careful, empty list of diffusion coefficients returned!')

    para['diff_coeffs_filtered_list'] = diffs_df
    
    return para



