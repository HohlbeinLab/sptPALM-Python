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

import numpy as np
import pandas as pd
import time



def diff_coeffs_from_tracks_fast(tracks, para):

# from typing import List, Tuple, Dict
# def diff_coeffs_from_tracks_fast(tracks: List[List], para: [Dict|none]) -> Tuple(int, np.ndarray()):

    """
    some description
    
    @params:
        tracks: a list of tracks
    """
    
    print("\nRun 'diff_coeffs_from_tracks_fast.py'")


    # Sort by track_id then frame so each track's localisations are contiguous
    # and in time order. calculate_MSD() reshapes rows into groups of group_size
    # and uses np.diff; without this sort, rows from different tracks interleave
    # and np.diff computes spurious cross-track displacements (verified: produces
    # unphysical D up to ~250 um^2/s). Both call sites now rely on this.
    tracks_data = tracks.copy().sort_values(['track_id', 'frame']).reset_index(drop=True)
    # Count occurrences of each unique track_ids
    tracklength_counts = tracks_data['track_id'].value_counts()
    
    # Map these counts back to the DataFrame as a new column '#_loc'
    tracks_data['#_locs'] = tracks_data['track_id'].map(tracklength_counts)
    tracks_data['MSD'] = np.nan
    tracks_data['D_coeff'] = np.nan
    tracks_data['frametime'] = para['frametime']
    
    start = time.time() 

    # For each tracklength in para
    for i, track_len in enumerate(para['tracklengths_steps']):
        # Find all tracks with a certain number of localisations per track
        idx = tracks_data.index[tracks_data['#_locs'] == track_len + 1].tolist()
        # If idx is not empty/false
        if idx: # implicit booleanness
            tracks_data.loc[idx,'MSD'] = calculate_MSD(tracks_data.loc[idx,:],
                                                       'x [µm]', 'y [µm]', track_len + 1,
                                                       frame_col='frame',
                                                       track_memory=para.get('track_memory', 0))
    
    # How long did the MSD calculation take?
    end = time.time()
    rounded_time = round(end-start, 2)
    print(f"  Time for MSD calculation: {rounded_time} seconds")


    # # Correct for localization error if specified (option in anaDDA does require to switch that off)
    # # what is the best correction here? Michelet 2010 reduced localization error? 
    # if 'correct_diff_calc_loc_error' in para: 
    #     if para['correct_diff_calc_loc_error']:
    #         loc_error_correction = np.random.normal(0, para['loc_error'], 
    #                                             len(tracks_data.loc[:, 'D_coeff']))**2 / para['frametime']
    # else:
    #     print('log error connection = 0')
    #     loc_error_correction = 0

    loc_error_correction =  (para['loc_error'] ** 2)/para['frametime']
    tracks_data['D_coeff'] = tracks_data['MSD'] / (4 * para['frametime']) - loc_error_correction

    # Create the histogram of diffusion coefficients as a function of track lengths
    if para['plot_option_axes'] == 'logarithmic':
        edges = np.arange(np.log10(para['plot_diff_hist_min']),
                      np.log10(para['plot_diff_hist_max']) + para['binwidth'],
                      para['binwidth'])
    else:
        edges = np.arange(0, para['plot_diff_hist_max'] + para['binwidth'],
                      para['binwidth'])      

    D_track_length_matrix = pd.DataFrame(np.zeros((len(edges),
                                                   len(para['tracklengths_steps']) + 1)),
                                         columns=['Bins'] + list(para['tracklengths_steps']))  
 
    if para['plot_option_axes'] == 'logarithmic':
        D_track_length_matrix.loc[:, 'Bins'] = 10 ** edges
    else:
        D_track_length_matrix.loc[:, 'Bins'] = edges
    
    for i, track_len in enumerate(para['tracklengths_steps']):
        # Use idx_track_ids to prevent counting diffusion coefficients several times
        idx = tracklength_counts.index[tracklength_counts[:] == track_len + 1].tolist()
        if idx:
            hist, _ = np.histogram(tracks_data.loc[idx, 'D_coeff'], D_track_length_matrix.loc[:, 'Bins'])
            D_track_length_matrix.loc[D_track_length_matrix.index[:-1], track_len] = hist

    # breakpoint()
    # # Find unique elements in the track_id column
    # track_ids, ic = np.unique(tracks_data['track_id'], return_inverse=True)
    # track_length_steps = np.bincount(ic) 

    # # Select tracks that are longer than diff_avg_steps_min and shorter than diff_avg_steps_max
    # filter_vec = (track_length_steps > para['diff_avg_steps_min']) & (track_length_steps < max(para['tracklengths_steps']))
    
    # track_ids_filtered = track_ids[filter_vec]
    # track_length_steps_filtered = track_length_steps[filter_vec]


    # temp_Dcoeff_data = tracks_data['D_coeff'].to_numpy()[ic]  
    # # Further filter based on filter_vec
    # temp_Dcoeff_data_filtered = temp_Dcoeff_data[filter_vec]

    # diffs_df = pd.DataFrame({
    #     'diff_coeffs_filtered': temp_Dcoeff_data_filtered,
    #     'track_length_filtered': track_length_steps_filtered,
    #     'track_id': track_ids_filtered,
    #     })


    return tracks_data, D_track_length_matrix

# Generalized function to calculate differences between two columns in groups of rows
def calculate_MSD(df, col_name1, col_name2, group_size, frame_col='frame', track_memory=0):

    """
    Mean single-frame squared displacement (MSD) for each track, where all tracks
    in `df` share the same length `group_size`.

    `df` is assumed sorted by (track_id, frame) so that each consecutive block of
    `group_size` rows is one track in time order. Rows are reshaped into
    (num_groups, group_size) and squared step displacements are averaged per track.

    Track-memory / frame-gap correction: when `track_memory > 0` a track may skip
    frames (a localisation missing but bridged by tracking). A step spanning `con`
    frames covers `con` single-frame intervals, so its squared displacement is
    divided by `con` to normalise it to a single-frame value. This matches the
    OLD analyse_diffusion_sptPALM behaviour (divide when 0 < con <= track_memory+1,
    leave raw otherwise). With the default track_memory=0 every step is 1 frame
    apart, so the correction divides by 1 and is a no-op.

    Parameters:
    df (DataFrame): data (sorted by track_id, frame), one track per group_size rows.
    col_name1, col_name2 (str): x and y position column names.
    group_size (int): localisations per track (= track length in locs).
    frame_col (str): column holding the frame number (for gap detection).
    track_memory (int): tracking memory in frames; gaps up to track_memory+1 are
        normalised, larger gaps are left raw (matches OLD).

    Returns:
    MSD (array): per-localisation MSD (the track's mean repeated group_size times).
    """
    # Extract the columns as NumPy arrays
    x_positions = df[col_name1].values
    y_positions = df[col_name2].values
    frames = df[frame_col].values

    # Determine the number of complete groups
    num_groups = len(x_positions) // group_size

    # Reshape the values into a matrix of shape (num_groups, group_size)
    reshaped_x_positions = x_positions[:num_groups * group_size].reshape(num_groups, group_size)
    reshaped_y_positions = y_positions[:num_groups * group_size].reshape(num_groups, group_size)
    reshaped_frames = frames[:num_groups * group_size].reshape(num_groups, group_size)

    squared_displacements = np.diff(reshaped_x_positions)**2 + np.diff(reshaped_y_positions)**2

    # Normalise gapped steps to a single-frame squared displacement (see docstring).
    frame_diff = np.diff(reshaped_frames)                       # 'con' per step
    normalise = (frame_diff > 0) & (frame_diff <= track_memory + 1)
    denom = np.where(normalise, frame_diff, 1)                  # avoid div-by-zero
    squared_displacements = np.where(normalise,
                                     squared_displacements / denom,
                                     squared_displacements)

    MSD = squared_displacements.mean(axis = 1)

    #Ensure that D_coff is showing up behind each localisation later
    MSD = np.repeat(MSD, group_size, axis = None)


    return MSD


def diff_coeffs_per_track(tracks, para):
    """One diffusion coefficient per track (for single-cell & combined analyses).

    For each track, D is computed from the gap-corrected mean single-frame MSD over
    the FIRST min(locs, tracklength_locs_max) localisations:
      - tracks with locs in [tracklength_locs_min .. tracklength_locs_max] use all
        their steps (identical to the per-length values from
        diff_coeffs_from_tracks_fast);
      - longer tracks are TRUNCATED to their first tracklength_locs_max
        localisations (kept, not dropped, but capped so every track has equal
        weight);
      - tracks with fewer than tracklength_locs_min localisations are excluded.

    This is the replacement for the OLD analyse_diffusion_sptPALM output. Note the
    track-length-resolved histogram (D_track_length_matrix) stays length-exact and
    is unaffected by the truncation here.

    Returns a DataFrame with columns: 'diff_coeffs_filtered', 'track_length_filtered'
    (the true, un-truncated track length in localisations), 'track_id'; ordered by
    track_id.
    """
    locs_min = int(para['tracklength_locs_min'])
    locs_max = int(para['tracklength_locs_max'])
    track_memory = int(para.get('track_memory', 0))
    frametime = para['frametime']
    loc_error = para['loc_error']

    # Order so each track's localisations are contiguous and in time order.
    df = tracks.sort_values(['track_id', 'frame']).copy()

    # True track length (localisations) per track, before truncation.
    locs = df.groupby('track_id').size()

    # Truncate long tracks to their first locs_max localisations.
    df['_pos'] = df.groupby('track_id').cumcount()
    trunc = df[df['_pos'] < locs_max]

    # Per-step squared displacement within each track (first row per track -> NaN).
    g = trunc.groupby('track_id')
    sq = g['x [µm]'].diff()**2 + g['y [µm]'].diff()**2
    con = g['frame'].diff()  # frames spanned by each step ('con' in the OLD code)

    # Gap correction: normalise a step spanning 'con' frames to a single frame by
    # dividing by con (only when 0 < con <= track_memory+1; raw otherwise).
    normalise = (con > 0) & (con <= track_memory + 1)
    sq = sq.where(~normalise, sq / con)

    # Mean single-frame MSD per track (skipna drops the first-row NaN step).
    msd_per_track = sq.groupby(trunc['track_id']).mean()

    # Diffusion coefficient with localisation-error correction.
    diff_coeffs = msd_per_track / (4 * frametime) - (loc_error ** 2) / frametime

    # Keep only tracks with at least locs_min localisations.
    keep = locs.index[locs >= locs_min]

    diffs_df = pd.DataFrame({
        'diff_coeffs_filtered': diff_coeffs.reindex(keep).to_numpy(),
        'track_length_filtered': locs.reindex(keep).to_numpy(),
        'track_id': keep.to_numpy(),
    })
    return diffs_df

