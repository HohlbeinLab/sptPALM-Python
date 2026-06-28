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


def single_cell_analysis_sptPALM(para):
    """Link per-track diffusion coefficients to individual cells.

    Consumes para['diff_coeffs_filtered_list'] (one row per valid track, produced
    by diff_coeffs_from_tracks_fast.diff_coeffs_per_track: columns
    'diff_coeffs_filtered', 'track_length_filtered', 'track_id'). Each track is
    assigned to its cell via a direct track_id -> cell_id lookup from csv_data, and
    per-cell statistics are computed by grouping on cell_id.

    (This replaces an earlier version that relied on positional alignment between
    the diffusion-coefficient list and cumulative per-cell track counts, which
    silently broke if the two were filtered or ordered differently.)

    Produces:
      para['scta_table']                per-cell summary table
      para['diff_coeffs_filtered_list'] with 'cell_id' and 'copynumber' added
      para['scta_tracks_csv']           localisations of valid tracks in kept cells
      para['tracks_filtered']           subset of columns of the above
    """
    print('\nRun single_cell_analysis_sptPALM.py')

    csv_data_all = para['csv_data']

    # Warn if tracking has not been run yet
    if (csv_data_all['track_id'] == -1).sum() == len(csv_data_all['track_id']):
        print('Warning: ...tracks do not seem to be assigned yet. Please run tracking!')

    # Localisations that fall inside a segmented cell
    csv_data = csv_data_all[csv_data_all['cell_id'] != -1]

    # Per-cell localisation count and area (one row per cell, sorted by cell_id)
    cell_ids, cell_locs = np.unique(csv_data['cell_id'], return_counts=True)
    cell_areas = (csv_data.drop_duplicates(subset='cell_id', keep='first')
                          .sort_values('cell_id')['cell_area'].to_numpy())

    # --- Assign each valid track to its cell via a direct lookup (robust) -------
    diffs = para['diff_coeffs_filtered_list'].copy()
    track_to_cell = csv_data.drop_duplicates('track_id').set_index('track_id')['cell_id']
    diffs['cell_id'] = diffs['track_id'].map(track_to_cell)
    # Keep only tracks that map to a cell (all should, since they came from in-cell tracking)
    diffs = diffs[diffs['cell_id'].notna()].copy()
    diffs['cell_id'] = diffs['cell_id'].astype(int)

    # Number of valid tracks per cell, and copynumber per track (= tracks in its cell)
    tracks_per_cell = diffs.groupby('cell_id').size()
    diffs['copynumber'] = diffs['cell_id'].map(tracks_per_cell).astype(int)

    # --- Per-cell summary table ------------------------------------------------
    cell_df = pd.DataFrame({
        'movie': -1.0,
        'cell_id': cell_ids,
        'cell_locs': cell_locs,
        'cell_area': cell_areas,
    })
    n_tracks = cell_df['cell_id'].map(tracks_per_cell).fillna(0).astype(int)
    cell_df['#tracks (unfiltered for #tracks per cell)'] = n_tracks

    # Keep cells whose number of valid tracks is within [min, max]
    keep = ((n_tracks >= para['number_tracks_per_cell_min']) &
            (n_tracks <= para['number_tracks_per_cell_max']) &
            (n_tracks > 0))
    cell_df['keep_cells'] = keep
    cell_df['#tracks (filtered for #tracks per cell)'] = np.where(keep, n_tracks, 0)
    cell_df['cum. #tracks (filtered for #tracks per cell)'] = \
        cell_df['#tracks (filtered for #tracks per cell)'].cumsum()
    cell_df['cum. #tracks (unfiltered for #tracks per cell)'] = \
        cell_df['#tracks (unfiltered for #tracks per cell)'].cumsum()

    # Average diffusion coefficient per kept cell
    kept_ids = set(cell_df.loc[cell_df['keep_cells'], 'cell_id'])
    avg_d = (diffs[diffs['cell_id'].isin(kept_ids)]
             .groupby('cell_id')['diff_coeffs_filtered'].mean())
    cell_df['average_diff_coeff_per_cell'] = cell_df['cell_id'].map(avg_d)

    # Column order kept consistent with the historical table layout
    cell_df = cell_df[['movie', 'cell_id', 'cell_locs', 'cell_area',
                       '#tracks (filtered for #tracks per cell)',
                       'cum. #tracks (filtered for #tracks per cell)',
                       '#tracks (unfiltered for #tracks per cell)',
                       'cum. #tracks (unfiltered for #tracks per cell)',
                       'keep_cells', 'average_diff_coeff_per_cell']]

    # --- Localisations of valid tracks in kept cells (for plotting/downstream) --
    valid_track_ids = diffs.loc[diffs['cell_id'].isin(kept_ids), 'track_id']
    scta_tracks_csv = csv_data[csv_data['track_id'].isin(valid_track_ids)].reset_index(drop=True)
    para['scta_tracks_csv'] = scta_tracks_csv
    para['tracks_filtered'] = scta_tracks_csv[['track_id', 'frame', 'x [µm]', 'y [µm]',
                                               'loc_id']].reset_index(drop=True)

    # Store updated diffusion list (with cell_id + copynumber) and the cell table
    para['diff_coeffs_filtered_list'] = diffs[['diff_coeffs_filtered',
                                               'track_length_filtered', 'track_id',
                                               'cell_id', 'copynumber']].reset_index(drop=True)
    para['scta_table'] = cell_df

    sorted_out = int(n_tracks.sum() - cell_df['#tracks (filtered for #tracks per cell)'].sum())
    print(f"  We sorted out {sorted_out} tracks that were in cells with too few or too many tracks per cell")

    return para
