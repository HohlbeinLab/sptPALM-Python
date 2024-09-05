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

def plot_trackPy_data(linked):
    # 6. Filter out Short Trajectories
    filtered = tp.filter_stubs(linked, threshold=2)

    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    ax[0, 0].set_title('Particle Trajectories')
    ax[0, 0].set_ylabel('y')
    ax[0, 0].set_xlabel('x')
    ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
    tp.plot_traj(filtered, ax = ax[0,0], pos_columns= ['x [nm]', 'y [nm]'])


    # very interesting: allows to calculate and correct drift!!!
    # Keep in mind!!!
    d = tp.compute_drift(filtered, pos_columns= ['x [nm]', 'y [nm]'])
    d.plot(ax = ax[1, 0])
    ax[1, 0].set_ylabel('y')
    ax[1, 0].set_xlabel('x')
    ax[1, 0].set_title('Drift')

    filtered_drift_corrected = tp.subtract_drift(filtered.copy(), d)
    tp.plot_traj(filtered_drift_corrected, ax = ax[0,1], pos_columns= ['x [nm]', 'y [nm]'])
    ax[0, 1].set_title('Particle Trajectories:drift corrected')
    ax[0, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # 7. Compute Mean Squared Displacement (MSD)
    msd = tp.emsd(filtered_drift_corrected, mpp=1, fps=100, max_lagtime = 7, pos_columns= ['x [nm]', 'y [nm]'])

    # 8. Plot Mean Squared Displacement (MSD)
    # plt.figure()
    # plt.plot(msd.index, msd, 'o')
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.xlabel('Lag time')
    # plt.ylabel('MSD')
    # plt.title('Mean Squared Displacement')

    ax[1, 1].set_title('Mean Squared Displacement: with fit')
    ax[1, 1].set_ylabel(r'$\langle \Delta r^2 \rangle$ [p\mu m$^2$]')
    plt.xlabel('lag time $t$')
    fit = tp.utils.fit_powerlaw(msd, ax = ax[1,1])  # performs linear best fit in log space, plots]
    print(fit)

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()
    return ()

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

    # # Set tracking parameters
    # track_params = {
    #     'maxDisp': para['track_steplength_max'],
    #     'mem': para['track_memory'],
    #     'dim': 2,
    #     'good': 0,
    #     'quiet': 1
    # }

    # # Check for required columns in CSV file
    # xpos_column = csv_data.columns.get_loc('x [nm]')
    # ypos_column = csv_data.columns.get_loc('y [nm]')
    # frame_id_column = csv_data.columns.get_loc('frame')
    # cell_id_column = csv_data.columns.get_loc('cell_id') if 'cell_id' in csv_data.columns else None
    # track_id_column = csv_data.columns.get_loc('track_id')

    # Tracking (cell by cell)
    tp.quiet() #make tracking silent
    if para['use_segmentations']:
        # Sort data by cell_id
        #full_track_array_sorted_for_cell_id = csv_data.sort_values(by = ['cell_id', 'frame_id'])

        csv_data_sort = csv_data.sort_values(by = ['cell_id', 'frame'])
  
        
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
            if num_cell % 10 == 0 or num_cell == len(cell_track_count) - 1:
                print(f" Tracking for valid cell {num_cell+1} of {len(cell_track_count)+1}...")

            # track_id_shift = max(csv_data['tracks'][:, 3]) if num_cell > 0 else 0        
            # part_track_array_sorted_for_cells = full_track_array_sorted_for_cell_id.iloc[start_pos:cell_track_count[num_cell, 2], :]
            
            part_csv_data_sort = csv_data_sort[csv_data_sort['cell_id'] == num_cell+1]

            # # Extract required data for tracking
            xy_frame_temp = part_csv_data_sort[['x [nm]', 'y [nm]', 'frame']] #if num_cell > 0 else 0
            
            # Perform tracking
            if len(xy_frame_temp) > 0:
                # breakpoint()
                
                # part_tracks_sorted_tracks = tracking_fixed(xy_frame_temp, track_params['maxDisp'], track_params)
       
                # Link Positions to Form Trajectories
                linked = []
                linked = tp.link_df(xy_frame_temp, search_range=para['track_steplength_max']/1000, memory=para['track_memory'], pos_columns= ['x [nm]', 'y [nm]'])
         
       
            else:
                # track_id_shift += 1
                # part_tracks_sorted_tracks = np.hstack((xy_frame_temp, np.zeros((xy_frame_temp.shape[0], 1))))
                print('else')
            # part_tracks_sorted_tracks[:, 3] += track_id_shift
            # tracks = pd.DataFrame(part_tracks_sorted_tracks, columns=['x (nm)', 'y (nm)', 'time (frame)', 'track_id'])
            # csv_data['tracks'] = pd.concat([csv_data['tracks'], tracks], ignore_index=True)

        # Update CSV file with track IDs
        csv_data.to_csv(save_file, index=False)
        print('\n Tracking analysis done!\n')
        print('track_ids have been set in *_analysis.csv!\n')

    else:
        # No segmentation scenario
        # track_params['quiet'] = 0
        # xy_frame_temp = csv_data.iloc[:, [xpos_column, ypos_column, frame_id_column]].to_numpy()
        # csv_data['tracks'] = tracking_fixed(xy_frame_temp, track_params['maxDisp'], track_params)
        # track_params['quiet'] = 1
        # breakpoint()
        xy_frame_temp = csv_data[['x [nm]', 'y [nm]', 'frame']] #if num_cell > 0 else 0
        xy_frame_temp['x [nm]']=xy_frame_temp['x [nm]']/1000
        xy_frame_temp['y [nm]']=xy_frame_temp['y [nm]']/1000
        # xy_frame_temp.rename(columns={'x [nm]': 'x', 'y [nm]': 'y'}, inplace=True)
        linked = tp.link_df(xy_frame_temp, search_range=para['track_steplength_max']/1000, memory=para['track_memory'], pos_columns= ['x [nm]', 'y [nm]'])
        plot_trackPy_data(linked)







    # # Export track_id to '*_analysis.csv'
    # csv_data.to_csv(save_file, index=False)
    # print('\n Tracking analysis done!\n')
    # print('track_ids have been set in *_analysis.csv!\n')

    # para['tracks_all'] = csv_data['tracks']
    # print('Tracks have been stored in the para structure!\n')

    return para
