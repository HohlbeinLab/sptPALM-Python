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
import os


def plot_diffusion_tracklengths_sptPALM(para):
    print('\nRun plot_diffusion_tracklengths_sptPALM.py')

    diff_coeffs_temp = para['diff_coeffs_filtered_list']['diff_coeffs_filtered'].to_numpy()

    # Create figure for histograms
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5)) #
    fig1.suptitle('Histogram: Diffusion coefficients and track lengths')

    # Plot histogram of diffusion coefficients (density= False,)
    edges = np.arange(np.log10(para['plot_diff_hist_min']), np.log10(para['plot_diff_hist_max']) + para['binwidth'], para['binwidth'])
    ax1.hist(diff_coeffs_temp, bins=10**edges, edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    # Plot weighted or something else:
    # ax1.hist(diff_coeffs_temp, bins=10**edges, density=True, weights=1/len(diff_coeffs_temp)* np.ones(len(diff_coeffs_temp)), edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    ax1.set_xscale('log')
    ax1.set_xlim([para['plot_diff_hist_min'], para['plot_diff_hist_max']])
    ax1.set_title(f"Diffusion coefficient: <D> = {np.mean(diff_coeffs_temp):.2f} ± {np.std(diff_coeffs_temp):.2f} µm²/sec")
    ax1.set_xlabel('Diffusion coefficient (µm²/sec)')
    ax1.set_ylabel('Number of tracks')
    ax1.tick_params(axis='both', which='major', labelsize=para['fontsize'])

    # Find unique track IDs and create histogram for track lengths
    track_ids, ia, ic = np.unique(para['tracks']['track_id'], return_index=True, return_inverse=True)
    ax2.hist(np.bincount(ic), bins=np.arange(0.5, 51.5, 1), density=(para['plot_norm_histograms'] == 'probability'),
             edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    
    ax2.set_yscale('log')
    ax2.set_xlim([0, 50])
    ax2.set_xlabel('Track length (frames)')
    ax2.set_ylabel('Probability')
    ax2.set_title('Distribution of all track lengths')
    ax2.tick_params(axis='both', which='major', labelsize=para['fontsize'])

    # Save figure as PNG
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig02_diff.png', dpi = para['dpi'])

    plt.show()
    return para




