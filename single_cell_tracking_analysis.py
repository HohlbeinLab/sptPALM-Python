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

    # csv_data = para['csv_data']
    csv_data = para['csv_data'][para['csv_data']['cell_id'] != -1]
    
    
    # Check wether tracks_ids have been assigned
    if (para['csv_data']['track_id'] == -1).sum() == len(para['csv_data']['track_id'] ):
        print('Warning: ...tracks do not seem to be assigned yet. Please run tracking!')

    cell_ids, cell_locs = np.unique(csv_data['cell_id'], return_counts=True)

    # Get the first occurrence of 'cell_area' for each 'cell_id'
    cell_areas = csv_data.drop_duplicates(subset='cell_id', 
                                          keep='first').sort_values(by='cell_id').loc[:, 'cell_area'].to_numpy()

    # Prepare a table with remaining cell_ids, number of localizations per cell, and cumulative sum
    cell_track_analysis_table = pd.DataFrame({
        'cell_id': cell_ids,
        'cell_locs': cell_locs,
        'cell_area': cell_areas,
    })

    diff_coeffs_temp = para['diff_coeffs_filtered_list']['diff_coeffs_filtered'].values

    # Initialize additional columns in the DiffCoeffsList dataframe
    para['diff_coeffs_filtered_list']['cell_id'] = -1
    para['diff_coeffs_filtered_list']['copynumber'] = -1

    cell_data_array = []
    tracks_temp = []

    number_tracks_temp = pd.DataFrame(-1, index=range(len(cell_ids)), columns=['nonfiltered', 'filtered'])


    # Loop through each valid cell
    for jj in range(len(cell_ids)):
        # Select data from a particular cell_id
        part_csv_data = csv_data[csv_data['cell_id'] == cell_ids[jj]]       

        # Find unique track_ids and total number of trackslocalisations per track
        track_ids_temp, track_locs_temp = np.unique(part_csv_data['track_id'], return_counts=True)
        track_df = pd.DataFrame({'track_id': track_ids_temp, 'locs': track_locs_temp})

        # Remove tracks with too few or too many localizations
        track_df = track_df[(track_df['locs'] > para['diff_hist_steps_min']) &
                                            (track_df['locs'] < para['diff_hist_steps_max'])]

        cell_tracks_temp = []
        
        # Check for presence of tracks in particular cell              
        if track_df.empty:
            cell_data_array.append([jj, []])
            tracks_temp.append([jj, []])
        else:
            # For each track in a particular cell
            for pp in range(track_df.shape[0]):
                track_id = track_df.iloc[pp]['track_id']
                cell_tracks_temp.append([
                    part_csv_data[part_csv_data['track_id'] == track_id], 
                    track_df.iloc[pp]['locs']
                ])
                temp = np.where(para['diff_coeffs_filtered_list']['track_id'] == track_id)[0]
                
                #Check whether a valid track_id was found
                if len(temp) > 0:
                    para['diff_coeffs_filtered_list'].loc[jj,'cell_id'] = cell_track_analysis_table.at[jj, 'cell_id']

            cell_data_array.append([jj, pd.concat([t[0] for t in cell_tracks_temp])])
            tracks_temp.append([jj, cell_tracks_temp])

        number_tracks_temp.loc[jj,'nonfiltered'] = len(cell_tracks_temp)

        # Check if given cell is within min/max thresholds for number of tracks
        if para['number_tracks_per_cell_min'] <= len(cell_tracks_temp) <= para['number_tracks_per_cell_max']:
            number_tracks_temp.loc[jj,'filtered'] = number_tracks_temp.loc[jj,'nonfiltered']
            cell_data_array[jj][0] = cell_data_array[jj][1]
            tracks_temp[jj][0] = tracks_temp[jj][1]
            
        else:
            cell_data_array[jj][0] = []
            tracks_temp[jj][0] = []
            number_tracks_temp.loc[jj,'filtered'] = 0
    
    # Extend cellTrackAnalysis_table
    # number_tracks_temp = np.array(number_tracks_temp)
    cell_track_analysis_table['#tracks (filtered for #tracks per cell)'] = number_tracks_temp.loc[:,'filtered'] 
    cell_track_analysis_table['cum. #tracks (filtered for #tracks per cell)'] = np.cumsum(number_tracks_temp.loc[:,'filtered'])
    cell_track_analysis_table['#tracks (unfiltered for #tracks per cell)'] = number_tracks_temp.loc[:,'nonfiltered'] 
    cell_track_analysis_table['cum. #tracks (unfiltered for #tracks per cell)'] = np.cumsum(number_tracks_temp.loc[:,'nonfiltered'])

    # Indicate cells that match minimum/maximum number of tracks
    cell_track_analysis_table['keep_cells'] = (cell_track_analysis_table['#tracks (filtered for #tracks per cell)'] >= para['number_tracks_per_cell_min']) & \
                                              (cell_track_analysis_table['cum. #tracks (filtered for #tracks per cell)'] <= para['number_tracks_per_cell_max'])

    difdata_filtered = []
    res_avgD_cell = []

    # Calculate average diffusion coefficients per cell
    for ii in range(len(cell_track_analysis_table)):
        if cell_track_analysis_table.at[ii, 'keep_cells']:
            cum_ids_temp = np.concatenate(([0], cell_track_analysis_table['cum. #tracks (unfiltered for #tracks per cell)'].values))
            cell_diff_coeff_data_temp = diff_coeffs_temp[cum_ids_temp[ii]:cum_ids_temp[ii+1]]
            res_avgD_cell.append(np.mean(cell_diff_coeff_data_temp))
            difdata_filtered.extend(cell_diff_coeff_data_temp)
        else:
            res_avgD_cell.append(np.nan)

    cell_track_analysis_table['average_diff_coeff_per_cell'] = res_avgD_cell

    # Add copy numbers of respective diffusion coefficients
    # Loop through each row of the dataframe
    copynumber = []
    for ii in range(len(cell_track_analysis_table)):
        # Get the number of tracks for the current row
        num_tracks = cell_track_analysis_table.iloc[ii]['#tracks (unfiltered for #tracks per cell)']
        # Create a list of ones of size num_tracks and multiply by num_tracks, then extend copynumber list
        copynumber.extend([num_tracks]* num_tracks)
    


    para['diff_coeffs_filtered_list']['copynumber'] = np.array(copynumber) # Number of tracks per cell

    # Update Para1 structure
    para['scta_table'] = cell_track_analysis_table
    para['scta_tracks'] = [t[1] for t in tracks_temp]
    
    breakpoint()
    
    
    # cell_data_array[0]
    # my_list_filtered = [x for x in cell_data_array if isinstance(x, pd.DataFrame)]
    
    
    # para['tracks_filtered'] = []
    # para['tracks_filtered'] = np.vstack(cell_data_array[:, 0])
    # para['tracks_filtered'] = pd.concat(cell_data_array[0].to_list(), axis=0)
    
    # para['tracks_filtered'] = np.concatenate([x[0] for x in cell_data_array])
    
    # para['tracks_filtered'] = pd.concat([t[0] for t in cell_data_array if t[0] != []], ignore_index=True)

    # if not para['tracks_filtered'].empty:
    #     para['tracks_filtered'] = para['tracks_filtered'].iloc[:, [6, 7, 3, 5]]
    # tracks_header = ['x [um]', 'y [um]', 'frame', 'track_id']
    # para['tracks_filtered'].columns = tracks_header


    print(f"We sorted out {len(diff_coeffs_temp) - cell_track_analysis_table['#tracks (filtered for #tracks per cell)'].sum()} tracks that were in cells with too few or too many tracks per cell")

    return para



