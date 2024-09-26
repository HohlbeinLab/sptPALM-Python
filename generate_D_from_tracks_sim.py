#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

import numpy as np
import pandas as pd

def generate_D_from_tracks_sim(tracks, sim_input, truncation):
    # Initialize
    particle_data = pd.DataFrame(np.zeros((len(tracks), 3)), columns=['D_coeff', 'tracklength', 'frametime'])

 #   MSD = np.zeros((n_molecules, 3))  # Initialize with 3 columns: D, track length, frame time
    kk = 0

    # Get a count of unique track ids and the number of occurrences for each
    table = tracks['track_id'].value_counts().reset_index()
    table.columns = ['track_id', 'count']

    # For each track length in sim_input
    for i, track_len in enumerate(sim_input['track_lengths']):
        print(f" track length: {i}")
        # Select molecules where the count of track frames equals (i + 1)
        selected_molecules = table[table['count'] == i + 2]

        if not selected_molecules.empty:
            kk_start = kk

            # Loop over each selected molecule
            for _, selected_molecule in selected_molecules.iterrows():
                # Get the indices of the selected track
                selected_track = tracks[tracks['track_id'] == selected_molecule['track_id']].iloc[:, :3]

                maxlength = min([truncation + 1, len(selected_track)])
                
                # breakpoint()
                # Sum all squared displacements in the track
                for jj in range(maxlength -1):
                    displacement_x = selected_track.iloc[jj+1, 0] - selected_track.iloc[jj, 0]
                    displacement_y = selected_track.iloc[jj+1, 1] - selected_track.iloc[jj, 1]

                    # Check if frame difference is 2
                    if selected_track.iloc[jj+1, 2] - selected_track.iloc[jj, 2] == 2:
                        particle_data.loc[kk, 'D_coeff'] += (displacement_x**2 + displacement_y**2) / 2
                    else:
                        particle_data.loc[kk, 'D_coeff'] += (displacement_x**2 + displacement_y**2)

                particle_data.loc[kk, 'D_coeff'] /= jj + 1  # Mean squared displacement
                kk += 1

            # Store the length of the track
            particle_data.loc[kk_start:kk, 'tracklength'] = maxlength - 1

    # Set frame time for all tracks
    particle_data.loc[:, 'frametime'] = sim_input['frametime']

    # Correct for localization error if specified
    if sim_input['correct_diff_calc_loc_error']:
        loc_error_correction = np.random.normal(0, sim_input['loc_error'], len(particle_data.loc[:, 'D_coeff']))**2 / sim_input['frametime']
        particle_data.loc[:, 'D_coeff'] = particle_data.loc[:, 'D_coeff'] / (4 * sim_input['frametime']) - loc_error_correction
    else:
        particle_data.loc[:, 'D_coeff'] = particle_data.loc[:, 'D_coeff'] / (4 * sim_input['frametime'])

    D = particle_data.copy()

    # Create the histogram bins and track length matrix
    edges = np.arange(np.log10(sim_input['plot_diff_hist_min']),
                      np.log10(sim_input['plot_diff_hist_max']) + sim_input['binwidth'],
                      sim_input['binwidth'])

    D_track_length_matrix = np.zeros((len(edges), len(sim_input['track_lengths']) + 1))
    D_track_length_matrix[:, 0] = 10 ** edges

    for i in range(len(sim_input['track_lengths'])):
        hist, _ = np.histogram(D[D[:, 1] == i, 0], bins=10 ** edges)
        D_track_length_matrix[:-1, i + 1] = hist

    return D, D_track_length_matrix
