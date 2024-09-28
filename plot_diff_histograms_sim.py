#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_diff_histograms_sim(D, D_track_length_matrix, sim_input):
    
    # Create the bin edges using logarithmic values
    edges = D_track_length_matrix['Bins']
    
    # Initialize the figure
    fig_handle = plt.figure(figsize=(8, 8))
    plt.suptitle('Histogram of diffusion coefficients per track length')
    
    # Loop through the track lengths and create histograms
    for ii, tra_len in enumerate(sim_input['track_lengths']):
        breakpoint()
        # Create a subplot for each track length
        ax = plt.subplot(int(np.ceil(len(sim_input['track_lengths']) / 2)), 2, ii + 1)
        
        if ii < max(sim_input['track_lengths']):
            ax.set_title(f'D distribution for track length {sim_input["track_lengths"][ii]} steps')
        else:
            ax.set_title(f'D distribution for track lengths > {sim_input["track_lengths"][ii]} steps')
        
        ax.set_xscale('log')  # Set the x-axis scale to logarithmic
        ax.set_xlabel('Diffusion coefficient (µm^2/s)')
        ax.set_ylabel('#')
        
        
        # Plot the histogram
        ax.stairs(D_track_length_matrix.loc[:,tra_len], edges, alpha=0.4)  # 'count' corresponds to `density=False`
        
        # Set the limits of the x-axis
        ax.set_xlim([sim_input['plot_diff_hist_min'], sim_input['plot_diff_hist_max']])
    
    # Show the plot
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout so the suptitle doesn't overlap
    plt.show()
    
    # # Create the bin edges using logarithmic values
    # edges = np.arange(np.log10(sim_input['plot_diff_hist_min']), 
    #                   np.log10(sim_input['plot_diff_hist_max']) + sim_input['binwidth'], 
    #                   sim_input['binwidth'])
    
    # # Initialize the figure
    # fig_handle = plt.figure(figsize=(8, 8))
    # plt.suptitle('Histogram of diffusion coefficients per track length')
    
    # # Loop through the track lengths and create histograms
    # for ii, tra_len in enumerate(sim_input['track_lengths']):

    #     # Create a subplot for each track length
    #     ax = plt.subplot(int(np.ceil(len(sim_input['track_lengths']) / 2)), 2, ii + 1)
        
    #     if ii < max(sim_input['track_lengths']):
    #         ax.set_title(f'D distribution for track length {sim_input["track_lengths"][ii]} steps')
    #     else:
    #         ax.set_title(f'D distribution for track lengths > {sim_input["track_lengths"][ii]} steps')
        
    #     ax.set_xscale('log')  # Set the x-axis scale to logarithmic
    #     ax.set_xlabel('Diffusion coefficient (µm^2/s)')
    #     ax.set_ylabel('#')
        
    #     # Filter the data for the current track length (ii)
    #     data_for_hist = D.loc[ D.loc[:, '#_locs'] == sim_input['track_lengths'][ii], 'D_coeff']
        
    #     # Plot the histogram
    #     ax.hist(data_for_hist, bins=10 ** edges, alpha=0.4, density=False)  # 'count' corresponds to `density=False`
        
    #     # Set the limits of the x-axis
    #     ax.set_xlim([sim_input['plot_diff_hist_min'], sim_input['plot_diff_hist_max']])
    
    # # Show the plot
    # plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout so the suptitle doesn't overlap
    # plt.show()

