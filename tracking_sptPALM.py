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
import trackpy as tp
import matplotlib.pyplot as plt
import warnings as warn
import time
import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def tracking_sptPALM(para):
    print('\nRun tracking_sptPALM.py')
    
    # Load the *.csv file
    if not para['use_segmentations']:
        print('  Tracking without applying cell segmentations...')
    elif para['use_segmentations']:
        print('  Tracking with applying cell segmentations...')
    else:
        raise ValueError(f"\n Problem! para['use_segmentations'] = {para['use_segmentations']}, should be True or False!\n")

    # Load csv data into a DataFrame
    print(f"  LoadFile [tracking]: {para['fn_locs'][:-4] + para['fn_csv_handle']}")
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    csv_data = pd.read_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'])

    # Check for existing 'track_id' and warn if necessary
    if ('track_id' in csv_data.columns) and (csv_data['track_id'] != -1).any():
        warn('Previously assigned tracks in your analysis file will be overwritten!')

    # Tracking (cell by cell)
    tp.quiet() #make tracking silent
    start = time.time()
    
    if para['use_segmentations']:
        # Find unique cell_ids
        cell_ids, ia, ic = np.unique(csv_data['cell_id'], return_index=True, return_inverse=True)
        
        # Find and remove any instances of cell_ids = -1
        cell_ids = cell_ids[1:] if cell_ids[0] == -1 else cell_ids 

        # Initialise tracks DataFrame 
        tracks = pd.DataFrame(columns = ['x [µm]', 'y [µm]', 'frame', 'track_id'])
       
        # Perform tracking for each segmented cell
        print("  Tracking...")
        for jj in range(len(cell_ids)):
            if jj % 50 == 0 and jj > 0: 
                print(f"   ...cell {jj} of {len(cell_ids)},")
            
            # Make sure that track_id continues increasing for every new (bacterial) cell
            track_id_shift = 0 if jj == 0 else max(tracks['track_id']+1)
            
            # Select all data of a particular (bacterial cell)
            part_csv_data = csv_data[csv_data['cell_id'] == cell_ids[jj]]

            # Extract required data for tracking:
            xy_frame_temp = part_csv_data[['x [µm]', 'y [µm]', 'frame', 'loc_id']] 

            # Perform tracking
            if len(xy_frame_temp) > 0:
                # Link positions to form trajectories
                linked = pd.DataFrame()
                
                # Tracking: linked will contain ['x [µm]', 'y [µm]'], 'frame', 'particle' => track_id
                linked = tp.link_df(xy_frame_temp, 
                                    search_range=para['track_steplength_max'],
                                    memory=para['track_memory'],
                                    pos_columns= ['x [µm]', 'y [µm]'],)
                
                #trackPy returns "particle' let's rename it 'track_id'
                linked.rename(columns={'particle': 'track_id'}, inplace=True)
            else:
                track_id_shift += 1
                linked = xy_frame_temp 
                linked['track_id'] = -1

            # Again, make sure that particle counting increases for each bacterial cell
            linked['track_id'] += track_id_shift
            
            # Sort for frames (might not be needed)
            tracks_temp = tracks.iloc[0:0].copy()
            tracks_temp = linked.sort_values(by = ['loc_id'])
            
            # Update 'track' column in the csv_data
            csv_data.loc[tracks_temp.index.tolist(), 'track_id'] = tracks_temp['track_id']

            # Accumulate track structure, check that tracks_temp isn't empty
            if len(tracks_temp)>0:
                tracks = pd.concat([df for df in [tracks, tracks_temp] if not df.empty], ignore_index=True)
        print(f"   ...cell {jj+1} of {len(cell_ids)}.")
    else:
        # No segmentation scenario
        xy_frame_temp = csv_data[['x [µm]', 'y [µm]', 'frame', 'loc_id']] #if num_cell > 0 else 0
        linked = tp.link_df(xy_frame_temp,
                                        memory=para['track_memory'],
                                        search_range=para['track_steplength_max'],
                                        pos_columns= ['x [µm]', 'y [µm]'])
       
        #trackPy returns "particle' let's rename for track_id
        linked.rename(columns={'particle': 'track_id'}, inplace=True)
        
        # Sort for frames (might not be neded)
        tracks = linked.sort_values(by = ['loc_id'])

        # Update 'track' column in the csv_data
        csv_data.loc[tracks.index.tolist(), 'track_id'] = tracks['track_id']
 

    # How long did the tracking take?
    end = time.time()
    rounded_time = round(end-start, 2)
    print(f"  Time for tracking: {rounded_time} seconds")
    
    # Plot all tracks
    print('  Plot and analyse first 50000 tracks using trackpy')
    temp_linked = tracks.rename(columns={'track_id': 'particle'}) # naming back...
    plot_trackPy_data(temp_linked.iloc[:50000], para) #Take only the first 50k entries

    # Update CSV file with track_ids
    csv_data.to_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'], index=False, quoting=0)
    print(f"  Track_ids have updated in {para['fn_locs'][:-4] + para['fn_csv_handle']}")

    tracks['frametime'] = para['frametime'] # add column with frametime
    para['tracks'] = tracks

    
    print('  Tracks have been stored in the para dictionary!')
    
    # Update para structure
    para['csv_data'] = csv_data
    
    return para

def plot_trackPy_data(linked, para):
    # Filter out Short Trajectories
    filtered = tp.filter_stubs(linked, threshold=para['diff_avg_steps_min'])
    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Some output provided by trackpy')
    ax[0, 0].set_title('Subset of particle trajectories')
    ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
    tp.plot_traj(filtered, mpp=para['pixelsize'], ax=ax[0,0], pos_columns=['x [µm]', 'y [µm]'])
    ax[0, 0].set_ylabel('y (um)')
    ax[0, 0].set_xlabel('x (um)')

    # Compute Mean Squared Displacement (MSD)
    msd = tp.emsd(filtered, mpp=1, fps=1/para['frametime'], max_lagtime = 7, pos_columns= ['x [µm]', 'y [µm]'])
    # Plots and fits Mean Squared Displacement (MSD)
    ax[0, 1].set_title('Mean Squared Displacement: with fit, no drift correction')
    ax[0, 1].set_ylabel(r'$\langle \Delta r^2 \rangle$ [µm$^2$]')
    ax[0, 1].set_xlabel('lag time $t$')
    fit = tp.utils.fit_powerlaw(msd, ax = ax[0,1])  # performs linear best fit in log space, plots]
    print(f"  MSD-FIT trackpy: {fit}")
 
    # Calculate drift
    d = tp.compute_drift(filtered, pos_columns= ['x [µm]', 'y [µm]'])
    d.plot(ax = ax[1, 0])
    ax[1, 0].set_ylabel('x,y (um)')
    ax[1, 0].set_xlabel('frames')
    ax[1, 0].set_title('Drift calculated from tracking')

       
    msd = tp.emsd(filtered, mpp=1, fps=1/para['frametime'], max_lagtime = 2, pos_columns= ['x [µm]', 'y [µm]'])
    MSD_fitting(ax, msd)


    plt.tight_layout()  # Adjust layout to prevent overlap  

    temp_path =  os.path.join(para['data_dir'], para['default_output_dir'])
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig02_track.png', dpi = para['dpi'])
    
    plt.show()
    return ()

def MSD_fitting(ax, msd):
    
    tau = msd.index.to_numpy()
    msd_ =  msd.to_numpy() # MSD values

    # Define the MSD equation
    def msd_function(tau, D, sigma):
        return 4 * D * tau + 4 * sigma**2

    # Fit the MSD data to the equation
    popt, pcov = curve_fit(msd_function, tau, msd_)

    # Extract the diffusion coefficient and localization variance
    D_fit, sigma_fit = popt
    text_lines = [
        "  MSD fitted for one frame using MSD = 4 * D * tau + 4 * sigma**2",
        f"  Fitted diffusion coefficient (D): {D_fit:.3f} µm/s^2",
        f"  Fitted localization variance (σ): {sigma_fit:.3f} µm",
        ]
 
    print(text_lines)
    ax[1, 1].scatter(tau, msd_, label="Data", color="blue")
    ax[1, 1].plot(tau, msd_function(tau, *popt), label="Fit", color="red")
    ax[1, 1].set_xlabel("Lag time (τ)")
    ax[1, 1].set_ylabel("MSD (τ)")
    ax[1, 1].legend()
    ax[1, 1].set_title("MSD Fit over all (!) tracks using lagtime of one frame only")
    
    # Add text to the subplot
    text_y_position = 0.9  # Starting y-position (normalized, from 0 to 1)
    for line in text_lines:
        ax[1, 1].text(0.05, text_y_position, line, transform=ax[1, 1].transAxes, fontsize=10, verticalalignment='top')
        text_y_position -= 0.05  # Move down for the next line

    
    return()