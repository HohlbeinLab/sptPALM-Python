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

import matplotlib.pyplot as plt
import os
import numpy as np
from skimage.io import imread
import pandas as pd
import pickle
from set_parameters_sptPALM_GUI import set_parameters_sptPALM_GUI
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming Para1 is a dictionary-like object
def plot_compare_conditions(comb_data=None, input_parameter=None):

    print('\nRun plot_combined_data_sptPALM.py')

    # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    filename = '/Users/hohlbein/Documents/WORK-DATA-local/2024-TypeIII/input_parameter.pkl'
    with open(filename, 'rb') as f:
        input_parameter = pickle.load(f)
        
    # TEMPORARY For bugfixing - Replace the following line with your file path if needed
    filename = '/Users/hohlbein/Documents/WORK-DATA-local/2024-TypeIII/output_python/sptData_combined_movies.pkl'
    with open(filename, 'rb') as f:
        comb_data = pickle.load(f)
    
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
        sns.boxplot(data=data_temp, y="average_diff_coeff_per_cell", x="condition", whis=np.inf,fill= False, ax=ax[1, 0], color="black")
        sns.stripplot(data=data_temp, y="average_diff_coeff_per_cell", x="condition", hue="movie", ax=ax[1, 0], legend=False, dodge=True, size=dot_size)
        stats = data_temp.groupby('condition')["average_diff_coeff_per_cell"].agg(["mean", "std", "median", "min", "max"])
        print('\nAvg. diffusion coefficient per cell per movie per condition')
        print(stats)
    ax[1, 0].set_title('Avg. diffusion coefficient per cell per movie per condition')
    ax[1, 0].set_ylabel('Avg. diffusion coefficient (µm$^2$/s)')        # breakpoint()
    ax[1, 0].set_xlabel(None)        # breakpoint()
    ax[1, 0].set_ylim(0, None)   
 
    # C) Avg. area per cell per movie per condition
    for ii, condition_name in enumerate(comb_data['condition_names']):
    
        data_temp = pd.DataFrame({'average_diff_coeff_per_cell': comb_data['cell_data'][ii]['average_diff_coeff_per_cell'], 
                                  'movie': comb_data['cell_data'][ii]['movie'],
                                  'condition': condition_name,
                                  })
        data_temp = data_temp.dropna(axis=0)  
        sns.boxplot(data=data_temp, y="average_diff_coeff_per_cell", x="condition", whis=np.inf,fill= False, ax=ax[1, 0], color="black")
        sns.stripplot(data=data_temp, y="average_diff_coeff_per_cell", x="condition", hue="movie", ax=ax[1, 0], legend=False, dodge=True, size=dot_size)
        stats = data_temp.groupby('condition')["average_diff_coeff_per_cell"].agg(["mean", "std", "median", "min", "max"])
        print('\nAvg. diffusion coefficient per cell per movie per condition')
        print(stats)
    ax[1, 0].set_title('Avg. diffusion coefficient per cell per movie per condition')
    ax[1, 0].set_ylabel('Avg. diffusion coefficient (µm$^2$/s)')        # breakpoint()
    ax[1, 0].set_xlabel(None)        # breakpoint()
    ax[1, 0].set_ylim(0, None)   
    
 
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
    
    plt.show()
   
    return input_parameter, comb_data    
 
if __name__ == "__main__":
     plot_compare_conditions()   
 
