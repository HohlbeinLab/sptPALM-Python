#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:52:59 2024

@author: hohlbein
"""

import numpy as np
import matplotlib.pyplot as plt

# note that 'plot_input' can be either 'sim_input' or 
def plot_diff_histograms_tracklength_resolved(D_track_length_matrix, plot_input):
    print("\nRun plot_diff_histograms_tracklength_resolved.py")
    # Create the bin edges using logarithmic values
    edges = D_track_length_matrix['Bins']
    
    # Initialize the figure
    plt.figure(figsize=(8, 8))
    plt.suptitle('Histogram of diffusion coefficients per track length')
    
    # Loop through the track lengths and create histograms
    for ii, tra_len in enumerate(plot_input['track_lengths']):
        # breakpoint()
        # Create a subplot for each track length
        ax = plt.subplot(int(np.ceil(len(plot_input['track_lengths']) / 2)), 2, ii + 1)
        
        if ii < max(plot_input['track_lengths']):
            ax.set_title(f'D distribution for track length {plot_input["track_lengths"][ii]} steps')
        else:
            ax.set_title(f'D distribution for track lengths > {plot_input["track_lengths"][ii]} steps')
        
        ax.set_xscale('log')  # Set the x-axis scale to logarithmic
        ax.set_xlabel('Diffusion coefficient (µm^2/s)')
        ax.set_ylabel('#')
               
        # Plot the histogram: bars
        ax.stairs(D_track_length_matrix.loc[D_track_length_matrix.index[:-1],tra_len], edges, color='lightgray', fill = True)  # 'count' corresponds to `density=False`
        
        # Plot the histogram: steps
        # ax.step(edges, D_track_length_matrix.loc[D_track_length_matrix.index[:],tra_len], where = 'post', color='red')  # 'count' corresponds to `density=False`
        
        # Set the limits of the x-axis
        ax.set_xlim([plot_input['plot_diff_hist_min'], plot_input['plot_diff_hist_max']])
    
    # Show the plot
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout so the suptitle doesn't overlap
    plt.show()
 
    
   
"""
    Older option to plot the histograms from the dataframe D with all diffusion coefficients
"""
    
    # # Create the bin edges using logarithmic values
    # edges = np.arange(np.log10(plot_input['plot_diff_hist_min']), 
    #                   np.log10(plot_input['plot_diff_hist_max']) + plot_input['binwidth'], 
    #                   plot_input['binwidth'])
    
    # # Initialize the figure
    # fig_handle = plt.figure(figsize=(8, 8))
    # plt.suptitle('Histogram of diffusion coefficients per track length')
    
    # # Loop through the track lengths and create histograms
    # for ii, tra_len in enumerate(plot_input['track_lengths']):

    #     # Create a subplot for each track length
    #     ax = plt.subplot(int(np.ceil(len(plot_input['track_lengths']) / 2)), 2, ii + 1)
        
    #     if ii < max(plot_input['track_lengths']):
    #         ax.set_title(f'D distribution for track length {plot_input["track_lengths"][ii]} steps')
    #     else:
    #         ax.set_title(f'D distribution for track lengths > {plot_input["track_lengths"][ii]} steps')
        
    #     ax.set_xscale('log')  # Set the x-axis scale to logarithmic
    #     ax.set_xlabel('Diffusion coefficient (µm^2/s)')
    #     ax.set_ylabel('#')
        
    #     # Filter the data for the current track length (ii)
    #     data_for_hist = D.loc[ D.loc[:, '#_locs'] == plot_input['track_lengths'][ii], 'D_coeff']
        
    #     # Plot the histogram
    #     ax.hist(data_for_hist, bins=10 ** edges, alpha=0.4, density=False)  # 'count' corresponds to `density=False`
        
    #     # Set the limits of the x-axis
    #     ax.set_xlim([plot_input['plot_diff_hist_min'], plot_input['plot_diff_hist_max']])
    
    # # Show the plot
    # plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout so the suptitle doesn't overlap
    # plt.show()

