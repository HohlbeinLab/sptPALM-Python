#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import pandas as pd
import numpy as np
from warnings import warn

def tracking_fixed(xy_frame_data, max_disp, track_params):
    # This function should implement the tracking algorithm, such as the Crocker-Grier or similar.
    # It would be a placeholder function as the exact MATLAB function "track_fixed" is not defined.
    # For now, returning the input for illustrative purposes.
    return xy_frame_data

def tracking_analysis(para):
    # Load the CSV file
    if not para['use_segmentations']:
        print('\n Tracking without cell segmentations...\n')
        load_file = f"{para['data_pathname']}{para['filename_analysis_csv']}"
    elif para['use_segmentations']:
        print('\n Tracking with cell segmentations...\n')
        load_file = f"{para['data_pathname']}{para['filename_analysis_csv']}"
    else:
        raise ValueError(f"\n Problem! para['use_segmentations'] = {para['use_segmentations']}, should be True or False!\n")

    # Load data into a DataFrame
    print(f" loadFile [tracking]: {load_file}")
    csv_data = pd.read_csv(load_file)

    # Prepare filename for saving data
    save_file = f"{para['data_pathname']}{para['filename_analysis_csv']}"
    print(f" saveFile [tracking]: {save_file}")

    # Check for existing 'track_id' and warn if necessary
    if ('track_id' in csv_data.columns) and (csv_data['track_id'] != -1).any():
        warn('Previously assigned tracks in your analysis file will be overwritten!')

    # Set tracking parameters
    track_params = {
        'maxDisp': para['track_steplength_max'],
        'mem': para['track_memory'],
        'dim': 2,
        'good': 0,
        'quiet': 1
    }

    # Check for required columns in CSV file
    xpos_column = csv_data.columns.get_loc('x [nm]')
    ypos_column = csv_data.columns.get_loc('y [nm]')
    frame_id_column = csv_data.columns.get_loc('frame_id')
    cell_id_column = csv_data.columns.get_loc('cell_id') if 'cell_id' in csv_data.columns else None
    track_id_column = csv_data.columns.get_loc('track_id')

    # Tracking (cell by cell)
    if para['use_segmentations']:
        # Sort data by cell_id
        #full_track_array_sorted_for_cell_id = csv_data.sort_values(by = ['cell_id', 'frame_id'])

        csv_data_sort = csv_data.sort_values(by = ['cell_id', 'frame_id'])
  
        
        # breakpoint()

        # Find unique cell_ids
        cell_ids, ia, ic = np.unique(csv_data_sort['cell_id'], return_index=True, return_inverse=True)

        # Prepare cellTrackCount
        counts = np.bincount(ic)
        cell_track_count = np.column_stack((cell_ids, counts, np.cumsum(counts)))

        # Remove unsegmented localizations for tracking
        cell_track_count = cell_track_count[1:] if cell_track_count[0, 0] == -1 else cell_track_count 
            # start_pos = cell_track_count[0, 2] + 1
            # cell_track_count = cell_track_count[1:]  # Exclude localizations outside cells
        # else:
        #     start_pos = 0

        csv_data['tracks'] = {} #pd.DataFrame()
        # breakpoint() 
        
        
        # Perform tracking for each segmented cell
        for num_cell in range(len(cell_track_count)):
            if num_cell % 50 == 0 or num_cell == len(cell_track_count) - 1:
                print(f" Tracking for valid cell {num_cell+1} of {len(cell_track_count)+1}...")

            # track_id_shift = max(csv_data['tracks'][:, 3]) if num_cell > 0 else 0        
            # part_track_array_sorted_for_cells = full_track_array_sorted_for_cell_id.iloc[start_pos:cell_track_count[num_cell, 2], :]
            
            part_csv_data_sort = csv_data_sort[csv_data_sort['cell_id'] == num_cell+1]

            # # Extract required data for tracking
            xy_frame_temp = part_csv_data_sort[['x [nm]', 'y [nm]', 'frame_id']] #if num_cell > 0 else 0
            breakpoint()
            # Perform tracking
            if len(xy_frame_temp) > 0:
                # breakpoint()
                part_tracks_sorted_tracks = tracking_fixed(xy_frame_temp, track_params['maxDisp'], track_params)
            
            else:
                # track_id_shift += 1
                part_tracks_sorted_tracks = np.hstack((xy_frame_temp, np.zeros((xy_frame_temp.shape[0], 1))))
            
            # part_tracks_sorted_tracks[:, 3] += track_id_shift
            # tracks = pd.DataFrame(part_tracks_sorted_tracks, columns=['x (nm)', 'y (nm)', 'time (frame)', 'track_id'])
            # csv_data['tracks'] = pd.concat([csv_data['tracks'], tracks], ignore_index=True)

        # Update CSV file with track IDs
        csv_data.to_csv(save_file, index=False)
        print('\n Tracking analysis done!\n')
        print('track_ids have been set in *_analysis.csv!\n')

    else:
        # No segmentation scenario
        track_params['quiet'] = 0
        xy_frame_temp = csv_data.iloc[:, [xpos_column, ypos_column, frame_id_column]].to_numpy()
        csv_data['tracks'] = tracking_fixed(xy_frame_temp, track_params['maxDisp'], track_params)
        track_params['quiet'] = 1

    # Export track_id to '*_analysis.csv'
    csv_data.to_csv(save_file, index=False)
    print('\n Tracking analysis done!\n')
    print('track_ids have been set in *_analysis.csv!\n')

    para['tracks_all'] = csv_data['tracks']
    print('Tracks have been stored in the para structure!\n')

    return para
