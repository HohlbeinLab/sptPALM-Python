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

def tracking_analysis(Para1):
    # Load the CSV file
    if not Para1['useSegmentations']:
        print('\n Tracking without cell segmentations...\n')
        load_file = f"{Para1['dataPathName']}{Para1['filename_analysis_csv']}"
    elif Para1['useSegmentations']:
        print('\n Tracking with cell segmentations...\n')
        load_file = f"{Para1['dataPathName']}{Para1['filename_analysis_csv']}"
    else:
        raise ValueError(f"\n Problem! Para1['useSegmentations'] = {Para1['useSegmentations']}, should be True or False!\n")

    # Load data into a DataFrame
    print(f" loadFile [tracking]: {load_file}")
    load_data = pd.read_csv(load_file)

    # Prepare filename for saving data
    save_file = f"{Para1['dataPathName']}{Para1['filename_analysis_csv']}"
    print(f" saveFile [tracking]: {save_file}")

    # Check for existing 'track_id' and warn if necessary
    if ('track_id' in load_data.columns) and (load_data['track_id'] != -1).any():
        warn('Previously assigned tracks in your analysis file will be overwritten!')

    # Set tracking parameters
    track_params = {
        'maxDisp': Para1['trackStepLength_max'],
        'mem': Para1['trackMemory'],
        'dim': 2,
        'good': 0,
        'quiet': 1
    }

    # Check for required columns in CSV file
    xpos_column = load_data.columns.get_loc('x [nm]')
    ypos_column = load_data.columns.get_loc('y [nm]')
    frame_id_column = load_data.columns.get_loc('frame_id')
    cell_id_column = load_data.columns.get_loc('cell_id') if 'cell_id' in load_data.columns else None
    #Not needed?
    #track_id_column = load_data.columns.get_loc('track_id')

    # Tracking (cell by cell)
    if Para1['useSegmentations']:
        # Sort data by cell_id
        full_track_array_sorted_for_cell_id = load_data.sort_values(by=load_data.columns[cell_id_column])
        
        # Find unique cell IDs
        cell_ids, ia, ic = np.unique(load_data.iloc[:, cell_id_column], return_index=True, return_inverse=True)

        # Prepare cellTrackCount
        counts = np.bincount(ic)
        cell_track_count = np.column_stack((cell_ids, counts, np.cumsum(counts)))

        # Check for unsegmented localizations
        if cell_track_count[0, 0] == -1:
            start_pos = cell_track_count[0, 2] + 1
            cell_track_count = cell_track_count[1:]  # Exclude localizations outside cells
        else:
            start_pos = 0

        load_data['tracks'] = pd.DataFrame()

        # Perform tracking for each segmented cell
        for num_cell in range(len(cell_track_count)):
            if num_cell % 10 == 0 or num_cell == len(cell_track_count) - 1:
                print(f"\n Tracking for valid cell {num_cell+1} of {len(cell_track_count)}...")

            track_id_shift = max(load_data['tracks'][:, 3]) if num_cell > 0 else 0
            part_track_array_sorted_for_cells = full_track_array_sorted_for_cell_id.iloc[start_pos:cell_track_count[num_cell, 2], :]

            # Extract relevant data
            xy_frame_temp = part_track_array_sorted_for_cells.iloc[:, [xpos_column, ypos_column, frame_id_column]].to_numpy()

            # Perform tracking
            if xy_frame_temp.shape[0] > 1:
                part_tracks_sorted_tracks = tracking_fixed(xy_frame_temp, track_params['maxDisp'], track_params)
            else:
                track_id_shift += 1
                part_tracks_sorted_tracks = np.hstack((xy_frame_temp, np.zeros((xy_frame_temp.shape[0], 1))))
            
            part_tracks_sorted_tracks[:, 3] += track_id_shift
            tracks = pd.DataFrame(part_tracks_sorted_tracks, columns=['x (nm)', 'y (nm)', 'time (frame)', 'track_id'])
            load_data['tracks'] = pd.concat([load_data['tracks'], tracks], ignore_index=True)

        # Update CSV file with track IDs
        load_data.to_csv(save_file, index=False)
        print('\n Tracking analysis done!\n')
        print('track_ids have been set in *_analysis.csv!\n')

    else:
        # No segmentation scenario
        track_params['quiet'] = 0
        xy_frame_temp = load_data.iloc[:, [xpos_column, ypos_column, frame_id_column]].to_numpy()
        load_data['tracks'] = tracking_fixed(xy_frame_temp, track_params['maxDisp'], track_params)
        track_params['quiet'] = 1

    # Export track_id to '*_analysis.csv'
    load_data.to_csv(save_file, index=False)
    print('\n Tracking analysis done!\n')
    print('track_ids have been set in *_analysis.csv!\n')

    Para1['tracks_all'] = load_data['tracks']
    print('Tracks have been stored in the Para1 structure!\n')

    return Para1
