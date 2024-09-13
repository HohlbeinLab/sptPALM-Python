#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import pandas as pd
import numpy as np

def single_cell_tracking_analysis(para):
    print('\nRun single_cell_tracking_analysis()')

    # Check wether tracks_ids have been assigned
    if (para['csv_data']['track_id'] == -1).sum() != len(para['csv_data']['track_id'] ):
        print('Warning: ...tracks do not seem to be not assigneds, please run tracking!')

    breakpoint()

    # # Create a temporary copy of the data matrix
    data_matrix_temp = para['csv_data'].copy()

    # # Check '*_analysis.csv' for the presence of specific columns (sanity check)
    # track_id_column = para['csvHeader'].index('"track_id"')
    
    # Remove all localizations with cell_id == -1 (outside valid cells)
    data_matrix_temp = para['csv_data'][para['csv_data']['"cell_id"'] != -1]
    
    # Sort the table by "cell_id"
    data_matrix_temp = data_matrix_temp.sort_values(by='cell_id')

    # Find unique cell_ids
    cell_ids = data_matrix_temp['cell_id'].unique()
    cell_area_ids = data_matrix_temp.loc[data_matrix_temp['cell_id'].isin(cell_ids), '"cell_area_id'].values

    # Prepare a table with remaining cell_ids, number of localizations per cell, and cumulative sum
    cell_counts = data_matrix_temp['"cell_id"'].value_counts().sort_index()
    cumulative_counts = cell_counts.cumsum()
    cell_track_analysis_table = pd.DataFrame({
        'cell_id': cell_ids,
        '#locs per cell': cell_counts.values,
        'cumulative #locs': cumulative_counts.values,
        'cell_area_id': cell_area_ids
    })

    diff_coeffs_temp = para['diffs_coeffs_list']['"diffs_coeffs_list_filtered"'].values

    # Initialize additional columns in the DiffCoeffsList dataframe
    para['diffs_coeffs_list']['cell_id'] = -1
    para['diffs_coeffs_list']['copynumber'] = -1

    cell_data_array = []
    tracks_temp = []
    number_tracks_temp = []

    # Loop through each unique cell
    for ii in range(len(cell_track_analysis_table)):
        # Select data from a particular cell_id
        cell_data_temp = data_matrix_temp[data_matrix_temp['"cell_id"'] == cell_track_analysis_table.at[ii, 'cell_id']]
        
        # Find unique track_ids
        track_ids_temp, track_counts_temp = np.unique(cell_data_temp.iloc[:, track_id_column], return_counts=True)
        track_count_temp = pd.DataFrame({'track_id': track_ids_temp, 'count': track_counts_temp})

        # Remove tracks with too few or too many localizations
        track_count_temp = track_count_temp[(track_count_temp['count'] > para['DiffHistSteps_min']) &
                                            (track_count_temp['count'] < para['DiffHistSteps_max'])]

        cell_tracks_temp = []

        if track_count_temp.empty:
            cell_data_array.append([ii, []])
            tracks_temp.append([ii, []])
        else:
            for pp in range(track_count_temp.shape[0]):
                track_id = track_count_temp.iloc[pp]['track_id']
                cell_tracks_temp.append([
                    cell_data_temp[cell_data_temp.iloc[:, track_id_column] == track_id],
                    track_count_temp.iloc[pp]['count']
                ])
                temp = np.where(para['DiffCoeffsList']['"track_id"'] == track_id)[0]
                if len(temp) > 0:
                    para['DiffCoeffsList'].at[temp[0], '"cell_id"'] = cell_track_analysis_table.at[ii, 'cell_id']

            cell_data_array.append([ii, pd.concat([t[0] for t in cell_tracks_temp])])
            tracks_temp.append([ii, cell_tracks_temp])

        number_tracks_temp.append([ii, len(cell_tracks_temp)])

        # Check if given cell is within min/max thresholds for number of tracks
        if para['numberTracksPerCell_min'] <= len(cell_tracks_temp) <= para['numberTracksPerCell_max']:
            number_tracks_temp[ii].append(len(cell_tracks_temp))
        else:
            number_tracks_temp[ii].append(0)
            cell_data_array[ii][1] = []
            tracks_temp[ii][1] = []

    # Extend cellTrackAnalysis_table
    number_tracks_temp = np.array(number_tracks_temp)
    cell_track_analysis_table['#tracks (filtered for #tracks per cell)'] = number_tracks_temp[:, 1]
    cell_track_analysis_table['cum. #tracks (filtered for #tracks per cell)'] = np.cumsum(number_tracks_temp[:, 1])
    cell_track_analysis_table['#tracks (unfiltered for #tracks per cell)'] = number_tracks_temp[:, 0]
    cell_track_analysis_table['cum. #tracks (unfiltered for #tracks per cell)'] = np.cumsum(number_tracks_temp[:, 0])

    # Indicate cells that match minimum/maximum number of tracks
    cell_track_analysis_table['keep_cells'] = (cell_track_analysis_table['#tracks (filtered for #tracks per cell)'] >= para['numberTracksPerCell_min']) & \
                                              (cell_track_analysis_table['cum. #tracks (filtered for #tracks per cell)'] <= para['numberTracksPerCell_max'])

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

    cell_track_analysis_table['averageDiffCoeffperCell'] = res_avgD_cell

    # Add copy numbers of respective diffusion coefficients
    copynumber = []
    for ii in range(len(cell_track_analysis_table)):
        copynumber.extend([cell_track_analysis_table.at[ii, '#tracks (unfiltered for #tracks per cell)']] * cell_track_analysis_table.at[ii, '#tracks (unfiltered for #tracks per cell)'])

    para['DiffCoeffsList']['"copynumber"'] = copynumber

    # Update Para1 structure
    para['SCTA_table'] = cell_track_analysis_table
    para['SCTA_tracks'] = [t[1] for t in tracks_temp]
    para['tracks_filtered'] = pd.concat([t[1] for t in cell_data_array if t[1] != []], ignore_index=True)

    if not para['tracks_filtered'].empty:
        para['tracks_filtered'] = para['tracks_filtered'].iloc[:, [6, 7, 3, 5]]
        tracks_header = ['x [um]', 'y [um]', 'frame', 'track_id']
        para['tracks_filtered'].columns = tracks_header

    print(f'We sorted out {len(diff_coeffs_temp) - cell_track_analysis_table["#tracks (filtered for #tracks per cell)"].sum()} tracks that were in cells with too few or too many tracks per cell')

    return para



