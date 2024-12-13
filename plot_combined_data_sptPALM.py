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


import os
import numpy as np
from skimage.io import imread
import pandas as pd
import pickle
from set_parameters_sptPALM import set_parameters_sptPALM
from set_parameters_sptPALM_GUI import set_parameters_sptPALM_GUI
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming Para1 is a dictionary-like object
def plot_combined_data_sptPALM(comb_data=None, input_parameter=None):
    print('\nRun plot_combined_data_sptPALM.py')
  
    # # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    # print("  TEMP! SPECIFIC FILE is being loaded: input_parameter.pkl!")  
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/2024-TypeIII/input_parameter.pkl'
    # with open(filename, 'rb') as f:
    #     input_parameter = pickle.load(f)

    # # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    # print("  TEMP! SPECIFIC FILE is being loaded: sptData_combined_movies.pkl!")  
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/2024-TypeIII/output_python/sptData_combined_movies.pkl'
    # with open(filename, 'rb') as f:
    #     comb_data = pickle.load(f)

    #  Check whether data was passed to the function
    if not input_parameter:
        input_parameter = set_parameters_sptPALM()
        input_parameter = set_parameters_sptPALM_GUI(input_parameter)        
    
    if not comb_data:
        Tk().withdraw()  # Close root window
        starting_directory = os.path.join(input_parameter['data_dir'],
                                                  input_parameter['default_output_dir'])
        filename = askopenfilename(initialdir = starting_directory, 
                                    filetypes = [("pickle file", "*.pkl")],
                                    title = "Select *.pkl file from sptPALM_combine_movies.py")
        if filename:
            with open(filename, 'rb') as f:
                comb_data = pickle.load(f)
        else:
            raise ValueError("No file selected!")
    
    # Figure A: plot stack plot with diffusion coefficients)
    if input_parameter['use_segmentations']:
        plot_diff_tracklength_combined(comb_data,input_parameter)
        plot_stacked_diff_histo(comb_data,input_parameter)
        plot_compare_conditions(comb_data, input_parameter)
    else:
        print("Let's skip plotting cell-dependend copy number analysis if no segmentation is present...")
    return comb_data    
 
 
def plot_diff_tracklength_combined(comb_data, input_parameter):
    print('\nRun plot_diffusion_tracklengths_sptPALM.py')


    breakpoint()
    for ii, condition_name in enumerate(comb_data['condition_names']):
        # Create figure for histograms
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5)) #
        fig1.suptitle(f"Histogram condition {ii}: Diffusion coefficients and track lengths combined movies")
        
      
        
        data_temp = pd.DataFrame({'diff_coeffs_filtered': comb_data['diff_data'][ii]['diff_coeffs_filtered'],
                                  'tracklength': comb_data['diff_data'][ii]['track_length_filtered'],
                                  'movie': comb_data['cell_data'][ii]['movie'],
                                  'condition': condition_name,
                                  })
     
        edges = np.arange(np.log10(input_parameter['plot_diff_hist_min']), np.log10(input_parameter['plot_diff_hist_max']) + input_parameter['binwidth'], input_parameter['binwidth'])
        ax1.hist(data_temp['diff_coeffs_filtered'], 10**edges, edgecolor='black', facecolor='lightgray', alpha=0.9)
        # 'count' corresponds to `density=False`
        ax1.set_xlim([input_parameter['plot_diff_hist_min'], input_parameter['plot_diff_hist_max']])
    
    
        if input_parameter['plot_option_axes']=='logarithmic':
            ax1.set_xscale('log')  # Set the x-axis scale to logarithmic
    
        ax1.set_title(f" Avg. D_coeff calculated from { input_parameter['diff_avg_steps_min'] } steps ") # ": <D> = {np.mean(diff_coeffs_temp):.2f} ± {np.std(diff_coeffs_temp):.2f} µm²/sec")
        ax1.set_xlabel('Diffusion coefficient (µm²/sec)')
        ax1.set_ylabel('Number of tracks')
    
    
        # Create histogram of filtered track lengths
        ax2.hist(data_temp['tracklength'], bins=np.arange(0.5, 51.5, 1), density=(input_parameter['plot_norm_histograms'] == 'probability'),
                 edgecolor='black', facecolor='lightgray')
        
        ax2.set_yscale('log')
        ax2.set_xlim([0, 50])
        ax2.set_xlabel('Track length (frames)')
        ax2.set_ylabel('Probability')
        ax2.set_title('Distribution of all all track lengths')
        ax2.tick_params(axis='both', which='major', labelsize=input_parameter['fontsize'])
    
        plt.tight_layout()
        
        
        # Save figure as PNG/SVG/PDF
        temp_path = os.path.join(input_parameter['data_dir'], input_parameter['default_output_dir'])
        plt.savefig(temp_path + input_parameter['fn_combined_movies'][:-4] + '-Cond:-' + f'{ii}' +'_Fig2_BoxPlots' + input_parameter['plot_option_save'], dpi = input_parameter['dpi'])

        
        plt.show()
    
    return 



   
def plot_stacked_diff_histo(comb_data, input_parameter):
      
    fig1 = plt.figure('Diffusion coefficients versus copy numbers per cell')
    plt.clf()
    
    # Aspect ratio (pbaspect equivalent)
    fig1.set_size_inches(5, 8)
    
    edges = np.arange(np.log10(comb_data['input_parameter']['plot_diff_hist_min']),
                      np.log10(comb_data['input_parameter']['plot_diff_hist_max']) + 0.1, 0.1)
    
    # Initialize a list to store axes
    axes = []
    
    # Loop through each copy number interval
    for jj in range(len(comb_data['input_parameter']['copynumber_intervals'])):
        
        # Create subplot in the specified grid
        temp = (len(comb_data['input_parameter']['copynumber_intervals']), 1, jj + 1)
        ax = plt.subplot(*temp)
        axes.append(ax)    
    
# Histogram could be plotted better nexto each other without shading, 
# see here:  https://matplotlib.org/stable/gallery/statistics/histogram_multihist.html#sphx-glr-gallery-statistics-histogram-multihist-py
        # Loop through each condition
        for ff in range(comb_data['#_conditions']):

            # Filter data based on copy number intervals
            data_temp = pd.DataFrame({'diff_temp': comb_data['diff_data'][ff]['diff_coeffs_filtered'],
                                      'copy_temp': comb_data['diff_data'][ff]['copynumber']
                                      })

            # Define the copy number interval for the current `jj`
            copy_interval_min = comb_data['input_parameter']['copynumber_intervals'][jj][0]
            copy_interval_max = comb_data['input_parameter']['copynumber_intervals'][jj][1]

            # Filter data_temp based on the copy number intervals
            data_temp = data_temp[(data_temp['copy_temp'] >= copy_interval_min) & 
                      (data_temp['copy_temp'] < copy_interval_max)]

            # Plot histogram
            ax.hist(data_temp['diff_temp'], bins=10**edges, alpha=0.4) # edgecolor='lightgray', facecolor='lightgray')
    
        # Set x limits and log scale
        ax.set_xlim([comb_data['input_parameter']['plot_diff_hist_min'],
                     comb_data['input_parameter']['plot_diff_hist_max']])
        ax.set_xscale('log')
        
        # Configure x-axis label only for the last subplot
        if jj == len(comb_data['input_parameter']['copynumber_intervals'])-1:
            ax.legend(comb_data['condition_names'], loc='upper left')
            ax.set_xlabel('Diffusion coefficient (μm²/sec)')
        else:
            ax.set_xticklabels([])
    
        # Set y-axis label
        ax.set_ylabel(comb_data['input_parameter']['plot_norm_histograms'])
        
        # Set font size
        ax.tick_params(axis='both', which='major', labelsize=comb_data['input_parameter']['fontsize'])
    
        # Set title
        ax.set_title(f"Avg. Diffcoeff for copynumber: {comb_data['input_parameter']['copynumber_intervals'][jj][0] } to {comb_data['input_parameter']['copynumber_intervals'][jj][1] }")
    
    
    plt.tight_layout()
    plt.show()
    
    # Save figure as PNG
    temp_path = os.path.join(input_parameter['data_dir'], input_parameter['default_output_dir'])
    plt.savefig(temp_path + input_parameter['fn_combined_movies'][:-4] + '_Fig01_Diffs.' + input_parameter['plot_option_save'],
                dpi = input_parameter['dpi'])


    return 
 
# Assuming Para1 is a dictionary-like object
def plot_compare_conditions(comb_data=None, input_parameter=None):

    print('\nRun plot_combined_data_sptPALM.py')

    # # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/2024-TypeIII/input_parameter.pkl'
    # with open(filename, 'rb') as f:
    #     input_parameter = pickle.load(f)
        
    # # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/2024-TypeIII/output_python/sptData_combined_movies.pkl'
    # with open(filename, 'rb') as f:
    #     comb_data = pickle.load(f)
    
    fig, ax = plt.subplots(2, 2, figsize=(14, 10)) # 
    dot_size = 5
    
    # A) Avg. diffusion coefficient per cell per condition
    for ii, condition_name in enumerate(comb_data['condition_names']):
        data_temp = pd.DataFrame({'cell_area': comb_data['cell_data'][ii]['cell_area']*input_parameter['pixelsize']*input_parameter['pixelsize'], 
                                  'diff_temp': comb_data['cell_data'][ii]['average_diff_coeff_per_cell']
                                      })
        data_temp = data_temp.dropna(axis=0)
        sns.scatterplot(data=data_temp, y='diff_temp', x='cell_area', ax=ax[0,0], size=dot_size, legend=False)  # 'cmap' sets the color map
    ax[0, 0].set_title('Avg. diffusion coefficient per cell per condition')
    ax[0, 0].set_xlabel('Area per cell (µm$^2$)')
    ax[0, 0].set_ylabel("Average Diff. Coeff. (µm$^2$/s)")
    ax[0, 0].set_xlim(0, None)
    ax[0, 0].set_ylim(0, None)
    
    # B) Avg. area per cell per movie per condition
    for ii, condition_name in enumerate(comb_data['condition_names']):
    
        data_temp = pd.DataFrame({'cell_area': comb_data['cell_data'][ii]['cell_area']*input_parameter['pixelsize']*input_parameter['pixelsize'], 
                                  'movie': comb_data['cell_data'][ii]['movie'],
                                  'condition': condition_name,
                                  })
        data_temp = data_temp.dropna(axis=0)  
        sns.boxplot(data=data_temp, y="cell_area", x="condition", whis=np.inf,fill= False, ax=ax[0, 1], color="black")
        sns.stripplot(data=data_temp, y="cell_area", x="condition", hue="movie", ax=ax[0, 1], legend=False, dodge=True, size=dot_size)
        stats = data_temp.groupby('condition')["cell_area"].agg(["mean", "std", "median", "min", "max"])
        print('\nAvg. area per cell per movie per condition')
        print(stats)
    ax[0, 1].set_title('Avg. area per cell per movie per condition')
    ax[0, 1].set_ylabel('Area per cell (µm$^2$)')        # breakpoint()
    ax[0, 1].set_xlabel(None)        # breakpoint()
    ax[0, 1].set_ylim(0, None)
    
    
    # C) Avg. area per cell per movie per condition
    for ii, condition_name in enumerate(comb_data['condition_names']):
    
        data_temp = pd.DataFrame({'average_diff_coeff_per_cell': comb_data['cell_data'][ii]['average_diff_coeff_per_cell'], 
                                  'movie': comb_data['cell_data'][ii]['movie'],
                                  'condition': condition_name,
                                  })
        data_temp = data_temp.dropna(axis=0)  
        sns.boxplot(data=data_temp, y="average_diff_coeff_per_cell", x="condition",
                    log_scale = True, whis=np.inf,fill= False, ax=ax[1, 0], color="black")
        sns.stripplot(data=data_temp, y="average_diff_coeff_per_cell", x="condition", 
                      log_scale = True, hue="movie", ax=ax[1, 0], legend=False, dodge=True, size=dot_size)
        stats = data_temp.groupby('condition')["average_diff_coeff_per_cell"].agg(["mean", "std", "median", "min", "max"])
        print('\nAvg. diffusion coefficient per cell per movie per condition')
        print(stats)
    ax[1, 0].set_title('Avg. diffusion coefficient per cell per movie per condition')
    ax[1, 0].set_ylabel('Avg. diffusion coefficient (µm$^2$/s)')        # breakpoint()
    ax[1, 0].set_xlabel(None)        # breakpoint()
    ax[1, 0].set_ylim(input_parameter['plot_diff_hist_min'], input_parameter['plot_diff_hist_max']) 
 
    # D) Average number of tracks per cell per condition
    for ii, condition_name in enumerate(comb_data['condition_names']):
    
        data_temp = pd.DataFrame({'tracks_number': comb_data['cell_data'][ii]['#tracks (unfiltered for #tracks per cell)'], 
                                  'movie': comb_data['cell_data'][ii]['movie'],
                                  'condition': condition_name,
                                  })
        data_temp = data_temp.dropna(axis=0)  
        sns.boxplot(data=data_temp, y="tracks_number", x="condition", whis=np.inf,fill= False, ax=ax[1, 1], color="black")
        sns.stripplot(data=data_temp, y="tracks_number", x="condition", hue="movie", ax=ax[1, 1], legend=False, dodge=True, size=dot_size)
        stats = data_temp.groupby('condition')["tracks_number"].agg(["mean", "std", "median", "min", "max"])
        print('\nAverage number of tracks per cell per condition')
        print(stats)
    ax[1, 1].set_title('Average number of tracks per cell per condition')
    ax[1, 1].set_ylabel('Avg. number of tracks')        # breakpoint()
    ax[1, 1].set_xlabel(None)        # breakpoint()
    ax[1, 1].set_ylim(0, None)   
   
    # Blank out axes
    # ax[1, 1].axis('off')  
    
    plt.tight_layout()
   
    # Save figure as PNG/SVG/PDF
    temp_path = os.path.join(input_parameter['data_dir'], input_parameter['default_output_dir'])
    plt.savefig(temp_path + input_parameter['fn_combined_movies'][:-4] + '_Fig2_BoxPlots' + input_parameter['plot_option_save'], dpi = input_parameter['dpi'])

    plt.show()
   
    return input_parameter, comb_data    
 