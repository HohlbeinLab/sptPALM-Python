#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import warnings as warn
# import time
# import os


def plot_hist_diffusion_track_length(para):
    # Convert MATLAB table to a numpy array and multiply by ConversionFactor
    # diff_coeffs_temp = para['ConversionFactor'] * para['DiffCoeffsList']['DiffCoeffsFiltered'].to_numpy()
    diff_coeffs_temp = para['diff_coeffs_list']['diff_coeffs_filtered'].to_numpy()
    # Create figure for histograms
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))
    fig1.suptitle('Histogram: Diffusion coefficients and track lengths')

    # Plot histogram of diffusion coefficients
    edges = np.arange(np.log10(para['plot_diff_hist_min']), np.log10(para['plot_diff_hist_max']) + 0.1, 0.1)
    ax1.hist(diff_coeffs_temp, bins=10**edges, edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    ax1.hist(diff_coeffs_temp, bins=10**edges, density=True, edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    
    ax1.set_xscale('log')
    ax1.set_xlim([para['plot_diff_hist_min'], para['plot_diff_hist_max']])
    ax1.set_title(f"Diffusion coefficient: <D> = {np.mean(diff_coeffs_temp):.2f} ± {np.std(diff_coeffs_temp):.2f} µm²/sec")
    ax1.set_xlabel('Diffusion coefficient (µm²/sec)')
    ax1.set_ylabel('Probability')
    ax1.tick_params(axis='both', which='major', labelsize=para['fontsize'])

    # Find unique track IDs and create histogram for track lengths
    # breakpoint()
    track_ids, ia, ic = np.unique(para['tracks']['track_id'], return_index=True, return_inverse=True)
    ax2.hist(np.bincount(ic), bins=np.arange(0.5, 51.5, 1), density=(para['plot_norm_histograms'] == 'probability'),
             edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    
    ax2.set_yscale('log')
    ax2.set_xlim([0, 50])
    ax2.set_xlabel('Track length (frames)')
    ax2.set_ylabel('Probability')
    ax2.set_title('Distribution of all track lengths')
    ax2.tick_params(axis='both', which='major', labelsize=para['fontsize'])

    # # Save figure as .png
    # if para['dataPathOutp'] == '':
    #     fig1.savefig(f"{para1['dataPathName']}{para1['filename_thunderstormCSV'][:-4]}-analysis-Fig02_difc.png")
    # else:
    #     tmp_name = para['filename_thunderstormCSV'][:-4].split("\\")[-1]
    #     fig1.savefig(f"{para1['dataPathOutp']}{tmp_name}-analysis-Fig02_difc.png")

    plt.show()
    return para




