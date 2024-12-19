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


def plot_single_cell_analysis_sptPALM(para):
    print('\nRun plot_single_cell_analysis_sptPALM.py')
    
    # Figure A: display tracks in cells (with color-coded diffusion coefficients)
    para = plot_tracks_in_cells(para) 

    # Check for x- and y-positions and transform them into pixels
    column_names = ['x', 'y', 'cell_id', 'cell_area']  # Replace with your actual column names
    para['bf_dict']['loc_pixel_table_filt'] = pd.DataFrame(np.zeros((len(para['tracks_filtered']), len(column_names))), columns=column_names)
    para['bf_dict']['loc_pixel_table_filt'].loc[:, ['x','y']] = para['tracks_filtered'][['x [µm]', 'y [µm]']].to_numpy()
  
    para['bf_dict']['loc_pixel_table_filt'].loc[:, 'x'] = np.clip(np.round(para['bf_dict']['loc_pixel_table_filt'].loc[:, 'x'] / (
        para['pixelsize'])).astype(int), 1, para['bf_dict']['proc_brightfield_segm_image'].shape[1])
    para['bf_dict']['loc_pixel_table_filt'].loc[:, 'y'] = np.clip(np.round(para['bf_dict']['loc_pixel_table_filt'].loc[:, 'y'] / (
        para['pixelsize'])).astype(int), 1, para['bf_dict']['proc_brightfield_segm_image'].shape[0])
    
    # Figure B
    para = plot_tracks_histograms(para)
    
    return para    
 
def plot_tracks_in_cells(para):

    # Load processed brightfield image with cells, filename: '*_procBrightfield.tif'
    print('  Start visualisation of tracks in valid cells')    
    print(f"  Load_proc_brightfield: {para['fn_proc_brightfield']}")
    bf_dict = {} 
    bf_dict['proc_brightfield_image'] = imread(para['data_dir'] + para['fn_proc_brightfield'])
    
    # Plot images initially segmented elsewhere
    fig2, ax = plt.subplots(1, 1, figsize=(14, 8)) 
  
    # Show processed brightfield image
    ax.imshow(bf_dict['proc_brightfield_image'], cmap='gray')
    ax.set_title('Processed brightfield image (from MacroCellSegmentation.ijm)')
    ax.set_xlabel('Pixels')
    ax.set_ylabel('Pixels')
    ax.set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Prepare colormap (1000 elements, distributed between 0 and 1)
    myColorMap = plt.get_cmap('hot', 1000)

    # Plot valid tracks for each valid cell
    for cc in range(len(para['scta_table'])):
        if para['scta_table']['#tracks (filtered for #tracks per cell)'][cc] > 1:  # Display only if tracks exist
            
            # Select data from a particular cell_id
            tempCellDdata = para['diff_coeffs_filtered_list'][para['diff_coeffs_filtered_list']['cell_id'] == para['scta_table']['cell_id'][cc]].reset_index(drop=True)
            tempCellTracks = para['scta_tracks_csv'][para['scta_tracks_csv']['cell_id'] == int(para['scta_table']['cell_id'][cc])].reset_index(drop=True)

            # Plot each valid track
            for pp in range(len(tempCellDdata)):
                # breakpoint()
                Dtrack = tempCellDdata['diff_coeffs_filtered'][pp] 
                Dtrack = max(Dtrack, 0)  # Handle negative diffusion coefficients

                tmp_colindx = min(Dtrack / (para['plot_diff_hist_max'] * para['scta_vis_rangemax']), 1)
                lineColor = myColorMap(tmp_colindx)
                
                # Select rows from tempCellTracks where 'track_id' matches tempCellTracks['track_id'][pp]
                selected_rows = tempCellTracks[tempCellTracks['track_id'] == tempCellTracks['track_id'][pp]]
                x = selected_rows['x [µm]']/para['pixelsize']
                y = selected_rows['y [µm]']/para['pixelsize'] 
                
                ax.plot(x, y, linewidth=para['linewidth'], color=lineColor)

                if para['plot_frame_number']:
                    ax.text(x.iat[0], y.iat[0], str(int(tempCellDdata['track_id'][pp])), fontsize=para['fontsize']-2)

    # Add colorbar for diffusion coefficients
    cbar = fig2.colorbar(plt.cm.ScalarMappable(cmap=myColorMap, norm=plt.Normalize(vmin=0, vmax=para['plot_diff_hist_max'] * para['scta_vis_rangemax'])), ax=ax)
    cbar.set_label('Diffusion coefficient (µm²/sec)', fontsize=para['fontsize'])
    cbar.ax.tick_params(labelsize=para['fontsize'])

    plt.tight_layout()  # Adjust layout to prevent overlap
 
    # Save figure as PNG
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig05_tracks.' + para['plot_option_save'], dpi = para['dpi'])

    plt.show()

    return para


def plot_tracks_histograms(para):
    # Plot images initially segmented elsewhere
    fig, ax = plt.subplots(2, 3, figsize=(14, 8)) # 
    circle_spot_size = 2
    fig.suptitle('Segmentations images and localisations + various histogram for valid cells')

    # Show segmented brightfield image with all localisations
    ax[0, 0].imshow(para['bf_dict']['proc_brightfield_segm_image'], cmap = para['cmap_applied'])
    ax[0, 0].scatter(para['bf_dict']['loc_pixel_table'].loc[:, 'x'], para['bf_dict']['loc_pixel_table'].loc[:, 'y'], circle_spot_size,
                      'black', label='Localisations')
    ax[0, 0].set_title(f"Segmented image containing {len(para['bf_dict']['loc_pixel_table'])} localisations")
    ax[0, 0].set_xlabel('Pixels')
    ax[0, 0].set_ylabel('Pixels')
    ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Show segmented brightfield image with all localisations
    ax[0, 1].imshow(para['bf_dict']['proc_brightfield_segm_image'], cmap = para['cmap_applied'])
    ax[0, 1].scatter(para['bf_dict']['loc_pixel_table_filt'].loc[:, 'x'], para['bf_dict']['loc_pixel_table_filt'].loc[:, 'y'], circle_spot_size,
                      'magenta', label='Localisations')
    ax[0, 1].set_title(f"{len(para['bf_dict']['loc_pixel_table_filt'])} localisations that are parts pf tracks")
    ax[0, 1].set_xlabel('Pixels')
    ax[0, 1].set_ylabel('Pixels')
    ax[0, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Blank out axes
    ax[0, 2].axis('off')

    # Scatter plot 
    x = para['scta_table']['cell_locs']
    y = para['scta_table']['#tracks (filtered for #tracks per cell)']
    colors = para['scta_table']['average_diff_coeff_per_cell']  # Color based on diffusion coefficient
    sc = ax[1, 0].scatter(x, y, c=colors, s=20, cmap='viridis', edgecolor='k')  # 'cmap' sets the color map
    ax[1, 0].set_title('Histogram: Number of localisations per cell')
    ax[1, 0].set_xlabel('Number of localisations per cell')
    ax[1, 0].set_ylabel('Number of tracks per cell')
    ax[1, 0].set_xlim(0, max(x)+max(x)/20)
    ax[1, 0].set_ylim(0, max(y)+max(y)/20)
    
    cbar = fig.colorbar(sc, ax = ax[1, 0])
    cbar.set_label('Average Diffusion coefficient (μm²/sec)', fontsize=para['fontsize'])
    cbar.ax.tick_params(labelsize=para['fontsize'])

    # Show histogram: areas per cell
    temp_area = para['scta_table']['cell_area']*(para['pixelsize']*para['pixelsize'])
    ax[1, 1].hist( temp_area, bins=np.arange(0, max(temp_area), max(temp_area)/10),
                  edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    ax[1, 1].set_title('Histogram: Area per cell')
    ax[1, 1].set_xlabel('Area (µm$^2$) per cell')
    ax[1, 1].set_ylabel('Number of cells')

    # Show histogram: Number of tracks per cell
    temp_tracks = para['scta_table']['#tracks (filtered for #tracks per cell)']
    ax[1, 2].hist(temp_tracks, bins=np.arange(0, max(temp_tracks), max(temp_tracks)/10),
                  edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    ax[1, 2].set_title('Histogram: Number of tracks per cell')
    ax[1, 2].set_xlabel('Tracks per cell')
    ax[1, 2].set_ylabel('Number of cells')
    
    # Adjust layout to prevent overlap
    plt.tight_layout()  
 
    # Save figure as PNG
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig06_cells.' + para['plot_option_save'], dpi = para['dpi'])
    
    plt.show()

    return para

