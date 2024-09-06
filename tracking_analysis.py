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

def plot_trackPy_data(linked, para):
    # Filter out Short Trajectories
    filtered = tp.filter_stubs(linked, threshold=para['diff_hist_steps_min'])

    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    ax[0, 0].set_title('Particle Trajectories')
    # ax[0, 0].set_ylabel('y (\mum)')
    # ax[0, 0].set_xlabel('x (\mum)')
    ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
    tp.plot_traj(filtered, mpp=para['pixel_size'],ax = ax[0,0], pos_columns= ['x [um]', 'y [um]'])


    # Calculate and correct drift!
    d = tp.compute_drift(filtered, pos_columns= ['x [um]', 'y [um]'])
    d.plot(ax = ax[1, 0])
    ax[1, 0].set_ylabel('y,y (\mum)')
    ax[1, 0].set_xlabel('frames')
    ax[1, 0].set_title('Drift')

    filtered_drift_corrected = tp.subtract_drift(filtered.copy(), d)
    tp.plot_traj(filtered_drift_corrected, ax = ax[0,1], pos_columns= ['x [um]', 'y [um]'])
    ax[0, 1].set_title('Particle Trajectories: drift corrected')
    ax[0, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Compute Mean Squared Displacement (MSD)
    msd = tp.emsd(filtered, mpp=1, fps=1/para['frametime'], max_lagtime = 7, pos_columns= ['x [um]', 'y [um]'])

    # Plots and fits Mean Squared Displacement (MSD)
    ax[1, 1].set_title('Mean Squared Displacement: with fit, no drift correction')
    ax[1, 1].set_ylabel(r'$\langle \Delta r^2 \rangle$ [p\mu m$^2$]')
    ax[1, 1].set_xlabel('lag time $t$')
    fit = tp.utils.fit_powerlaw(msd, ax = ax[1,1])  # performs linear best fit in log space, plots]
    print(fit)

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()
    return ()

def tracking_analysis(para):
    # Load the CSV file
    if not para['use_segmentations']:
        print('\n Tracking without cell segmentations...\n')
        load_file = f"{para['data_pathname']}{para['filename_analysisPy_csv']}"
    elif para['use_segmentations']:
        print('\n Tracking with cell segmentations...\n')
        load_file = f"{para['data_pathname']}{para['filename_analysisPy_csv']}"
    else:
        raise ValueError(f"\n Problem! para['use_segmentations'] = {para['use_segmentations']}, should be True or False!\n")

    # Load data into a DataFrame
    print(f" loadFile [tracking]: {load_file}")
    csv_data = pd.read_csv(load_file)

    # Prepare filename for saving data
    save_file = f"{para['data_pathname']}{para['filename_analysisPy_csv']}"
    print(f" saveFile [tracking]: {save_file}")

    # Check for existing 'track_id' and warn if necessary
    if ('track_id' in csv_data.columns) and (csv_data['track_id'] != -1).any():
        warn('Previously assigned tracks in your analysis file will be overwritten!')

    # Tracking (cell by cell)
    tp.quiet() #make tracking silent

    start = time.time()
    if para['use_segmentations']:
        # Sort data by cell_id
        csv_data_sort = csv_data.sort_values(by = ['cell_id', 'frame'])
 
        # Find unique cell_ids
        cell_ids, ia, ic = np.unique(csv_data_sort['cell_id'], return_index=True, return_inverse=True)

        # Prepare cellTrackCount
        counts = np.bincount(ic)
        cell_particle_count = np.column_stack((cell_ids, counts, np.cumsum(counts)))

        # Remove unsegmented localizations for tracking
        cell_particle_count = cell_particle_count[1:] if cell_particle_count[0, 0] == -1 else cell_particle_count 

        # Initialise DataFrame (will contain *.csv and more) 
        tracks = pd.DataFrame()
        # output['tracks'] = {} #pd.DataFrame()
       
        # Perform tracking for each segmented cell
        for num_cell in range(len(cell_particle_count)):
            if num_cell % 10 == 0 or num_cell == len(cell_particle_count) - 1:
                print(f" Tracking for valid cell {num_cell+1} of {len(cell_particle_count)+1}...")
            #makes sure that track_id continues increasing for every new (bacterial) cell
            track_id_shift = 0 if num_cell == 0 else max(tracks['particle'])
            
            # Select all data of a particular (bacterial cell)
            part_csv_data_sort = csv_data_sort[csv_data_sort['cell_id'] == num_cell+1]

            # Extract required data for tracking: x [um]', 'y [um]', 'frame'
            xy_frame_temp = part_csv_data_sort[['x [um]', 'y [um]', 'frame']] 
            
            # Perform tracking
            if len(xy_frame_temp) > 0:
                # Link Positions to Form Trajectories
                linked = pd.DataFrame()
                # Tracking: linked will contain ['x [um]', 'y [um]'], 'frame', 'particle' => track_id
                linked = tp.link_df(xy_frame_temp, 
                                    search_range=para['track_steplength_max'],
                                    memory=para['track_memory'],
                                    pos_columns= ['x [um]', 'y [um]'],)
            else:
                track_id_shift += 1
                linked = xy_frame_temp 
                linked['particle'] = -1

            # Again, make sure that particle counting increases for each bacterial cell
            linked['particle'] += track_id_shift
            
            # Sort for frames
            tracks_temp = linked.sort_values(by = ['frame'])
                       
            # Update 'track' column in the csv_data
            csv_data_sort.loc[tracks_temp.index.tolist(), 'track_id'] = tracks_temp['particle']
            # Accumulate track structure
            tracks = pd.concat([tracks, tracks_temp], ignore_index=True)

        # Update CSV file with track IDs
        csv_data.to_csv(save_file, index=False)
        print('\n Tracking analysis done!\n')
        print('track_ids have been set in *_analysis.csv!\n')

    else:
        # No segmentation scenario
        xy_frame_temp = csv_data[['x [um]', 'y [um]', 'frame']] #if num_cell > 0 else 0
        csv_data['tracks'] = tp.link_df(xy_frame_temp,
                                        memory=para['track_memory'],
                                        search_range=para['track_steplength_max'],
                                        pos_columns= ['x [um]', 'y [um]'])
        plot_trackPy_data(csv_data['tracks'] , para)

    # How long did the tracking take?
    end = time.time()
    print(f"time for tracking:  {end-start}")
    
    # # Export track_id to '*_analysis.csv'
    # csv_data.to_csv(save_file, index=False)
    # print('\n Tracking analysis done!\n')
    # print('track_ids have been set in *_analysis.csv!\n')

    para['tracks_all'] = tracks
    print('Tracks have been stored in the para structure!\n')

    return para
