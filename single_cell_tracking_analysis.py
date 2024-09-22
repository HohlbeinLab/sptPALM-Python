#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import pandas as pd
import numpy as np

def single_cell_tracking_analysis(para):
    print('\nRun single_cell_tracking_analysis.py')

    # csv_data = para['csv_data'] but only take rows in which 'cell_id_ != -1
    csv_data = para['csv_data'][para['csv_data']['cell_id'] != -1]
     
    # Check whether tracks_ids have been assigned
    if (para['csv_data']['track_id'] == -1).sum() == len(para['csv_data']['track_id'] ):
        print('Warning: ...tracks do not seem to be assigned yet. Please run tracking!')

    # Return ids of valid cells and count the number of localisations per cell
    cell_ids, cell_locs = np.unique(csv_data['cell_id'], return_counts=True)

    # Get the first occurrence of 'cell_area' for each 'cell_id'
    cell_areas = csv_data.drop_duplicates(subset='cell_id', 
                                          keep='first').sort_values(by='cell_id').loc[:, 'cell_area'].to_numpy()

    # Prepare a table with remaining cell_ids, number of localizations per cell, and cumulative sum
    cell_df = pd.DataFrame({
        'cell_id': cell_ids,
        'cell_locs': cell_locs,
        'cell_area': cell_areas,
        '#tracks (filtered for #tracks per cell)': 0,
        'cum. #tracks (filtered for #tracks per cell)': 0,
        '#tracks (unfiltered for #tracks per cell)': 0, 
        'cum. #tracks (unfiltered for #tracks per cell)': 0,
        'keep_cells': np.NaN,
        'average_diff_coeff_per_cell': np.NaN,
    })
    
    # Initialize additional columns in the DiffCoeffsList dataframe
    para['diff_coeffs_filtered_list']['cell_id'] = -1
    para['diff_coeffs_filtered_list']['copynumber'] = -1

    # Predefine some DataFrames
    para['scta_tracks_csv'] =  para['csv_data'].iloc[0:0].copy()
    para['tracks_filtered'] =  para['tracks'].iloc[0:0].copy()

    
    # Loop through each valid cell
    for jj in range(len(cell_ids)):
        # Select data from a particular cell_id
        part_csv_data = csv_data[csv_data['cell_id'] == cell_ids[jj]]       

        # Find unique track_ids and total number of trackslocalisations per track
        track_ids, track_locs = np.unique(part_csv_data['track_id'], return_counts=True)
        
        # Write data into DataFrame
        track_df = pd.DataFrame({'track_id': track_ids, 'locs': track_locs})

        # Select tracks that have neither too few or too many localizations
        track_df = track_df[(track_df['locs'] > para['diff_hist_steps_min']) &
                                            (track_df['locs'] < para['diff_hist_steps_max'])]
     
        # Check for presence of tracks in particular cell              
        if track_df.empty == False:
            # If we found tracks, write number of tracks
            cell_df.loc[jj,'#tracks (unfiltered for #tracks per cell)'] = len(track_df)
            
            # Filter for number of tracks per cell
            if para['number_tracks_per_cell_min'] <= len(track_df) <= para['number_tracks_per_cell_max']:
                cell_df.loc[jj,'#tracks (filtered for #tracks per cell)'] = len(track_df)
                
                # Probably not needed later?!
                para['scta_tracks_csv'] = pd.concat(
                    [para['scta_tracks_csv'],
                    part_csv_data[part_csv_data['track_id'].isin(track_df['track_id'])]],
                    ignore_index=True
                    )
                
                # List of columns to select from part_csv_data for concatenation
                columns_to_concatenate = ['track_id', 'frame', 'x [um]', 'y [um]', 'loc_id']  # Example columns

                # Concatenate only the selected columns
                para['tracks_filtered'] = pd.concat(
                   [para['tracks_filtered'],
                    part_csv_data.loc[part_csv_data['track_id'].isin(track_df['track_id']), columns_to_concatenate]],
                   ignore_index=True
                   )   
     
            else:
                cell_df.loc[jj,'#tracks (filtered for #tracks per cell)'] = 0
                
    
    # Extend cellTrackAnalysis_table
    cell_df['cum. #tracks (filtered for #tracks per cell)'] = np.cumsum(cell_df.loc[:,'#tracks (filtered for #tracks per cell)'])
    cell_df['cum. #tracks (unfiltered for #tracks per cell)'] = np.cumsum(cell_df.loc[:,'#tracks (unfiltered for #tracks per cell)'])

    # Indicate cells that match minimum/maximum number of tracks
    cell_df['keep_cells'] = (cell_df['#tracks (filtered for #tracks per cell)'] >= para['number_tracks_per_cell_min']) & \
                                              (cell_df['cum. #tracks (filtered for #tracks per cell)'] <= para['number_tracks_per_cell_max']
                                               )
    difdata_filtered = []
    res_avgD_cell = []
    diff_coeffs_temp = para['diff_coeffs_filtered_list']['diff_coeffs_filtered'].values
    
    # Calculate average diffusion coefficients per cell
    for ii in range(len(cell_df)):
        if cell_df.at[ii, 'keep_cells']:
            cum_ids_temp = np.concatenate(([0], cell_df['cum. #tracks (unfiltered for #tracks per cell)'].values))
            cell_diff_coeff_data_temp = diff_coeffs_temp[cum_ids_temp[ii]:cum_ids_temp[ii+1]]
            res_avgD_cell.append(np.mean(cell_diff_coeff_data_temp))
            difdata_filtered.extend(cell_diff_coeff_data_temp)
        else:
            res_avgD_cell.append(np.nan)

    cell_df['average_diff_coeff_per_cell'] = res_avgD_cell

    # Add copy numbers and cell_ids of respective diffusion coefficients
    copynumber = []
    cell_temp = []
    for ii in range(len(cell_df)):
        # Get the number of tracks for the current row
        num_tracks = int(cell_df.iloc[ii]['#tracks (unfiltered for #tracks per cell)'])
        num_cell_ids = int(cell_df.iloc[ii]['cell_id'])
        # Create a list of ones of size num_tracks and multiply by num_tracks, then extend copynumber list
        copynumber.extend(num_tracks*[num_tracks])
        cell_temp.extend(num_tracks*[num_cell_ids])

    para['diff_coeffs_filtered_list']['copynumber'] = np.array(copynumber) # Number of tracks per cell
    para['diff_coeffs_filtered_list']['cell_id'] = np.array(cell_temp) # Number of tracks per cell

    # Update Para1 structure
    para['scta_table'] = cell_df

    # Avoid potential issue of returning an empty list (not sure whether it works)
    if para['tracks_filtered'].empty:
        para['tracks_filtered'] = para['tracks_filtered'].iloc[:, [-1, -1, -1, -1]]

    print(f"  We sorted out {cell_df['#tracks (unfiltered for #tracks per cell)'].sum() - cell_df['#tracks (filtered for #tracks per cell)'].sum()} tracks that were in cells with too few or too many tracks per cell")


    return para



