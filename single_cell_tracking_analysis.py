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
    if (para['csv_data']['track_id'] == -1).sum() != len(para['csv_data']['track_id'] ):
        print('Warning: ...tracks do not seem to be assigned yet. Please run tracking!')

    cell_ids, cell_locs = np.unique(csv_data['cell_id'], return_counts=True)

    # Get the first occurrence of 'cell_area' for each 'cell_id'
    cell_areas = csv_data.drop_duplicates(subset='cell_id', keep='first').sort_values(by='cell_id').loc[:, 'cell_area']

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

    # breakpoint()


    cell_data_array = []
    tracks_temp = []
    number_tracks_temp = []



    # Loop through each valid cell
    for jj in range(len(cell_ids)):
        # # Select data from a particular cell_id
        # cell_data_temp = data_matrix_temp[data_matrix_temp['"cell_id"'] == cell_track_analysis_table.at[ii, 'cell_id']]
        part_csv_data = csv_data[csv_data['cell_id'] == cell_ids[jj]]       

        # Find unique track_ids
        track_ids_temp, track_counts_temp = np.unique(part_csv_data['track_id'], return_counts=True)
        track_count_temp = pd.DataFrame({'track_id': track_ids_temp, 'count': track_counts_temp})

        # Remove tracks with too few or too many localizations
        track_count_temp = track_count_temp[(track_count_temp['count'] > para['diff_hist_steps_min']) &
                                            (track_count_temp['count'] < para['diff_hist_steps_max'])]

        cell_tracks_temp = []

        if track_count_temp.empty:
            cell_data_array.append([jj, []])
            tracks_temp.append([jj, []])
        else:
            # For each track in a given cell
            for pp in range(track_count_temp.shape[0]):
                track_id = track_count_temp.iloc[pp]['track_id']
                cell_tracks_temp.append([
                    part_csv_data[part_csv_data['track_id'] == track_id],
                    track_count_temp.iloc[pp]['count']
                ])
                temp = np.where(para['diff_coeffs_filtered_list']['track_id'] == track_id)[0]
                if len(temp) > 0:
                    para['diffs_coeffs_list'].at[temp[0], '"cell_id"'] = cell_track_analysis_table.at[jj, 'cell_id']

            cell_data_array.append([jj, pd.concat([t[0] for t in cell_tracks_temp])])
            tracks_temp.append([jj, cell_tracks_temp])

        number_tracks_temp.append([jj, len(cell_tracks_temp)])

        # Check if given cell is within min/max thresholds for number of tracks
        if para['number_tracks_per_cell_min'] <= len(cell_tracks_temp) <= para['number_tracks_per_cell_max']:
            number_tracks_temp[jj].append(len(cell_tracks_temp))
        else:
            number_tracks_temp[jj].append(0)
            cell_data_array[jj][1] = []
            tracks_temp[jj][1] = []

    # Extend cellTrackAnalysis_table
    number_tracks_temp = np.array(number_tracks_temp)
    cell_track_analysis_table['#tracks (filtered for #tracks per cell)'] = number_tracks_temp[:, 1]
    cell_track_analysis_table['cum. #tracks (filtered for #tracks per cell)'] = np.cumsum(number_tracks_temp[:, 1])
    cell_track_analysis_table['#tracks (unfiltered for #tracks per cell)'] = number_tracks_temp[:, 0]
    cell_track_analysis_table['cum. #tracks (unfiltered for #tracks per cell)'] = np.cumsum(number_tracks_temp[:, 0])

    breakpoint()

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
    
    # # Vectorized solution using np.repeat
    # copynumber = np.repeat(
    #     cell_track_analysis_table['#tracks (unfiltered for #tracks per cell)'].values, 
    #     cell_track_analysis_table['#tracks (unfiltered for #tracks per cell)'].values
    #     )

    breakpoint()
    para['diff_coeffs_filtered_list']['copynumber'] = np.array(copynumber) # Number of tracks per cell

    # Update Para1 structure
    para['scta_table'] = cell_track_analysis_table
    para['scta_tracks'] = [t[1] for t in tracks_temp]
    para['tracks_filtered'] = pd.concat([t[1] for t in cell_data_array if t[1] != []], ignore_index=True)

    if not para['tracks_filtered'].empty:
        para['tracks_filtered'] = para['tracks_filtered'].iloc[:, [6, 7, 3, 5]]
    tracks_header = ['x [um]', 'y [um]', 'frame', 'track_id']
    para['tracks_filtered'].columns = tracks_header

    print(f"We sorted out {len(diff_coeffs_temp) - cell_track_analysis_table['#tracks (filtered for #tracks per cell)'].sum()} tracks that were in cells with too few or too many tracks per cell")

    return para



