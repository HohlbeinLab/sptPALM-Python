#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import pandas as pd
import numpy as np
import trackpy as tp
import matplotlib.pyplot as plt
import warnings as warn
import time
import os


def diffusion_analysis(para):
    # Extract track data
    track_data_tracks = para['tracks_all'].to_numpy()
    track_id_column = para['tracks_all'].columns.get_loc('"track_id"')

    # Making a save name (.csv file)
    para['filename_DiffList'] = para['filename_analysis_csv'][:-4] + '_DiffCoeffsList.csv'
    save_file = para['dataPathName'] + para['filename_DiffList']

    # Find unique elements in the track_id column
    track_ids, ic = np.unique(track_data_tracks[:, track_id_column], return_inverse=True)
    track_length = np.bincount(ic)
    track_count_temp = np.column_stack((track_ids, track_length, np.cumsum(track_length)))

    # Filter tracks that are longer than DiffHistSteps_min and shorter than DiffHistSteps_max
    filter_vec = (track_length > para['DiffHistSteps_min']) & (track_length < para['DiffHistSteps_max'])
    track_count = track_count_temp[filter_vec, :]

    # Create empty vector for MSDs
    msd = np.zeros(len(track_count))

    # For each track (which can have many localizations/positions)
    for ii in range(len(track_count)):
        start_pos = int(track_count[ii, 2] - track_count[ii, 1] + 1)
        
        # Calculate averaged MSD for DiffHistSteps_min + 1 steps
        for jj in range(para['DiffHistSteps_min']):
            con = track_data_tracks[start_pos + jj, 2] - track_data_tracks[start_pos + jj - 1, 2]
            
            # Account for 1-frame memories
            if con <= para['trackMemory'] + 1 and con != 0:
                # Calculate MSD (single frame MSD!)
                msd[ii] += (((track_data_tracks[start_pos + jj, 0] - track_data_tracks[start_pos + jj - 1, 0]) ** 2 + 
                             (track_data_tracks[start_pos + jj, 1] - track_data_tracks[start_pos + jj - 1, 1]) ** 2) / con)
            else:
                msd[ii] += ((track_data_tracks[start_pos + jj, 0] - track_data_tracks[start_pos + jj - 1, 0]) ** 2 + 
                            (track_data_tracks[start_pos + jj, 1] - track_data_tracks[start_pos + jj - 1, 1]) ** 2)

        # Divide by total number of steps
        msd[ii] /= (jj + 1)  # Mean square displacement

    # Calculate D from MSD and correct for localization noise
    dmle = msd / (4 * para['frametime']) - (para['sigmaNoise'] ** 2) / para['frametime']

    # Save data
    output = pd.DataFrame({
        '"DiffCoeffsFiltered"': dmle,
        '"#localisations"': track_count[:, 1],
        '"track_id"': track_count[:, 0]
    })

    if not output.empty:  # Check if output is not empty
        output.to_csv(save_file, index=False, quoting=3)  # quoting=3 corresponds to 'QUOTE_NONE'
        print('\nDiffusion analysis done and diffusion coefficients saved!\n')
    else:
        print('\nEmpty list of diffusion coefficients!\n')

    para1['DiffCoeffsList'] = output
    return para



