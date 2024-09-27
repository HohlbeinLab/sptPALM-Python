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
    kk = 0

    # Get a count of unique track ids and the number of occurrences for each
    table = tracks['track_id'].value_counts().reset_index()
    table.columns = ['track_id', '#_locs']

    # For each track length in sim_input
    for i, track_len in enumerate(sim_input['track_lengths']):
        print(f" track length: {i+1} out of {truncation}")

        # Select molecules where number of locs per track is 1 + tracklength
        selected_molecules = table[table['#_locs'] == track_len + 1 ]

        if not selected_molecules.empty:
            kk_start = kk

            # Loop over each selected molecule
            for _, selected_molecule in selected_molecules.iterrows():
                

                # Get the indices of the selected track
                selected_track = tracks[tracks['track_id'] == selected_molecule['track_id']].iloc[:, :3].reset_index()

                maxlength = min([truncation + 1, len(selected_track)])
                
                # Sum all squared displacements in the track
                for jj in range(maxlength -1):

                    displacement_x = selected_track.loc[jj+1, 'x [µm]'] - selected_track.loc[jj, 'x [µm]']
                    displacement_y = selected_track.loc[jj+1, 'y [µm]'] - selected_track.loc[jj, 'y [µm]']

                    # Check if frame difference is 2
                    if selected_track.loc[jj+1, 'frame'] - selected_track.loc[jj, 'frame'] == 2:
                        particle_data.loc[kk, 'D_coeff'] += (displacement_x**2 + displacement_y**2) / 2
                    else:
                        particle_data.loc[kk, 'D_coeff'] += (displacement_x**2 + displacement_y**2)

                particle_data.loc[kk, 'D_coeff'] /= jj + 1  # Mean squared displacement
                kk += 1

            # Store the length of the track
            particle_data.loc[kk_start:kk-1, 'tracklength'] = maxlength-1


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


    D_track_length_matrix = pd.DataFrame(np.zeros((len(edges), len(sim_input['track_lengths']) + 1)), columns=['Bins'] + list(sim_input['track_lengths']))
   
    D_track_length_matrix.loc[:, 'Bins'] = 10 ** edges

    for i, track_len in enumerate(sim_input['track_lengths']):
        hist, _ = np.histogram(D.loc[D.loc[:, 'tracklength']== track_len, 'D_coeff'], bins=10 ** edges)
        D_track_length_matrix.loc[D_track_length_matrix.index[:-1], track_len] = hist

    return D, D_track_length_matrix
