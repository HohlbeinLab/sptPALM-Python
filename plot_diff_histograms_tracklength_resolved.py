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
import matplotlib.pyplot as plt
import seaborn as sns

# note that 'plot_input' can be either 'sim_input' or 
def plot_diff_histograms_tracklength_resolved(D_track_length_matrix, plot_input, D=None):
    print("\nRun plot_diff_histograms_tracklength_resolved.py")
    
    # More classical view
    plot_diff_histograms_conventional(D_track_length_matrix, plot_input)
    
    #Ridgeplot with seaborn
    plot_diff_histograms_ridgeplot1(D_track_length_matrix, plot_input, D)
    
    # breakpoint()
    # Ridgeplot KDE with seaborn
    # plot_diff_histograms_KDE(D, plot_input)
      
def plot_diff_histograms_conventional(D_track_length_matrix, plot_input):
    # Create the bin edges using logarithmic values
    edges = D_track_length_matrix['Bins']
    
    # Initialize the figure
    plt.figure(figsize=(8, 8))
    plt.suptitle('Histogram of diffusion coefficients per track length')
    
    # Loop through the track lengths and create histograms
    for ii, tra_len in enumerate(plot_input['track_lengths']):
        # Create a subplot for each track length
        ax = plt.subplot(int(np.ceil(len(plot_input['track_lengths']) / 2)), 2, ii + 1)
        
        if ii < max(plot_input['track_lengths']):
            ax.set_title(f'D distribution for track length {plot_input["track_lengths"][ii]} steps')
        else:
            ax.set_title(f'D distribution for track lengths > {plot_input["track_lengths"][ii]} steps')
        
        if plot_input['plot_option']=='logarithmic':
            ax.set_xscale('log')  # Set the x-axis scale to logarithmic
                
        ax.set_xlabel('Diffusion coefficient (µm$^2$/s)')
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
 
    
def plot_diff_histograms_ridgeplot1(D_track_length_matrix, plot_input, D): 
    sns.set_style('white', rc={
        'xtick.bottom': True,
        'ytick.left': False,
    })
    # Assuming D_track_length_matrix is your DataFrame
    x_values = D_track_length_matrix['Bins']  # The first column as x-values (bin edges or midpoints)
    y_columns = D_track_length_matrix.columns[1:]  # The next 7 columns as histogrammed y-values
    
    # Normalize each column (y-values)
    normalized_data = D_track_length_matrix.iloc[:, 1:].div(D_track_length_matrix.iloc[:, 1:].sum(axis=0), axis=1)
    
    # Set up the figure and axes
    plt.figure(figsize=(4, 5))
    
    # Create a color palette
    palette = sns.color_palette("viridis", len(y_columns))
    
    # Adjust this value to control the amount of vertical overlap between curves
    vertical_offset = 0.04  # Smaller offset for partial overlap, 0.1 is  a goog value
    
    # Loop through the 7 columns and plot each with vertical offset, normalized, and fill area

    # for i, column in enumerate(reversed(y_columns)):
    for i, column in enumerate(y_columns):
        print(i, column, plot_input['track_lengths'][i])
        
        # Get the normalized column data
        y_values = normalized_data[column]
        

        
        # Plot the filled area under the curve, applying vertical offset for partial overlap
        plt.fill_between(x_values, y_values + (len(y_columns)-1-i) * vertical_offset, (len(y_columns)-1-i) * vertical_offset, 
                         color=palette[len(y_columns)-1-i], alpha=0.6, label=column)
        # plt.fill_between(x_values, y_values + i * vertical_offset, i * vertical_offset, 
        #                  color=palette[i], alpha=0.6, label=column)
         
        # Label each curve
        if plot_input['plot_option']=='logarithmic':
            plt.text(0.005, (len(y_columns)-1-i) * vertical_offset + 0.5*vertical_offset,
                     f"steps per track: {column}", va='center') 
            D_avg = np.mean(D.loc[ D.loc[:, '#_locs'] == column+1, 'D_coeff'])
            plt.text(1, (len(y_columns)-1-i) * vertical_offset + 0.5*vertical_offset,
                     f"D_avg: {round(D_avg,2)} µm$^2$/s", va='center') 
        else:
            plt.text(4, i * vertical_offset + 0.5*vertical_offset,
                     f"steps per track: {column}", va='center') #np.median(x_values)
    # Set log scale on the x-axis
    
    if plot_input['plot_option']=='logarithmic':
        plt.xscale('log')
    
    # Remove the frame (spines)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    # plt.gca().spines['left'].set_visible(False)
    
    plt.yticks([])
    
    # # Customize x-axis ticks (size, width, length, color, and direction)
    # plt.tick_params(axis='x', which='major', width=1, length=6, color='black', labelcolor='black', direction='out')  # Force ticks pointing outwards
    # plt.tick_params(axis='x', which='minor', width=0.5, length=4, color='black', labelcolor='black', direction='out')
    
    # Adjust y-limits to ensure the curves don't go off the plot
    plt.ylim(0, len(y_columns) * vertical_offset + vertical_offset)
    plt.xlim(np.min(x_values), np.max(x_values))
    
    # Add labels and styling
    plt.title("Distribution of diff. coeffs. for different track lengths")
    plt.xlabel("Diffusion coefficient (µm$^2$/s)")
    plt.ylabel("")  # No y-axis label for aesthetic purposes
     
    plt.tight_layout()
    
    # Show the plot
    plt.show()  

    
def plot_diff_histograms_KDE(D, plot_input):
    """
        Older option to plot the histograms from the dataframe D with all diffusion coefficients
    """

    # Set up the figure and axes
    plt.figure(figsize=(4, 5))

    # Create a color palette
    palette = sns.color_palette("coolwarm", len(plot_input['track_lengths']))
  
    for ii, tra_len in enumerate(reversed(plot_input['track_lengths'])):

        data_for_hist = D.loc[ D.loc[:, '#_locs'] == plot_input['track_lengths'][ii], 'D_coeff']
        # Shift the y-values to stack the KDE plots vertically
        sns.kdeplot(
            # x=x_values, 
            data_for_hist, 
            fill=True, 
            color=palette[ii], 
        alpha=0.6, 
        bw_adjust=0.7
        ).set_label(tra_len)

    # Offset the y-axis by adding ii to the density plots (y-offset)
    plt.text(data_for_hist.mean(), 1, tra_len, va='center')  # Label each ridge

    plt.xscale('log')
    # Show the plot
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout so the suptitle doesn't overlap
    plt.show()

