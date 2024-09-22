#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import matplotlib.pyplot as plt
import os
import numpy as np
from skimage.io import imread
import pandas as pd
import pickle
from define_input_parameters import define_input_parameters
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
import matplotlib.pyplot as plt

# Assuming Para1 is a dictionary-like object
def sptPALM_plot_combined_data(comb_data=None):

    print('\nRun sptPALM_plot_comb_data()')
    # loaded more as a dummy here: define input parameters
    # Best to use only 
    input_parameter = define_input_parameters()
    
    # # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    # filename = '/Users/hohlbein/Documents/WORK-DATA-local/TestData_CRISPR-Cas/output_python/sptData_combined_movies.pkl'
    # with open(filename, 'rb') as f:
    #     comb_data = pickle.load(f)
    
    # 1.1 Check whether DATA was passed to the function
    if comb_data is None:
        # Use Tkinter for file dialog
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
    else:
        print('  Careful, there might be no data available to proceed!')
    
    # Figure A: plot stack plot with diffusion coefficients)
    plot_stacked_diff_histo(comb_data)

    # Figure B: cell by cell specific plots
    
    
    return comb_data    
 
def plot_stacked_diff_histo(comb_data):
      
    fig1 = plt.figure('Diffusion coefficients versus copy numbers per cell')
    plt.clf()
    
    # Aspect ratio (pbaspect equivalent)
    fig1.set_size_inches(10, 1)
    
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
            ax.hist(data_temp['diff_temp'], bins=10**edges, alpha=0.4)
            # ax.hist(data_filtered, bins=10 ** edges, alpha=0.4, density=(Para1.PlotNormHistograms == 'probability'))
    
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
        ax.set_title(f"Diffcoeff for copynumber: {comb_data['input_parameter']['copynumber_intervals'][jj][0] } to {comb_data['input_parameter']['copynumber_intervals'][jj][1] }")
    
    # Adjust figure position and size
    fig1.set_size_inches(5, 8)
    plt.tight_layout()
    
    plt.show()
        
    
    return 
 
    
 