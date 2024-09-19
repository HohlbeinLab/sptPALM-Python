#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""


import matplotlib.pyplot as plt
import os
# import numpy as np
from skimage.io import imread

# Assuming Para1 is a dictionary-like object
def plot_single_cell_tracking_analysis(para):

    print('\nRun Plot_SingleCellTrackingAnalysis()')
    
    # Figure A: display tracks in cells (with color-coded diffusion coefficients)
    para = plot_tracks_in_cells(para)


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
                x = selected_rows['x [um]']/para['pixel_size']
                y = selected_rows['y [um]']/para['pixel_size'] 
                
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
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig03_tracks.png', dpi = para['dpi'])

    plt.show()

    return para


def plot_tracks_histograms(para):
    # Plot images initially segmented elsewhere
    fig, ax = plt.subplots(2, 3, figsize=(14, 8)) # 
    circle_spot_size = 2

    # Show segmented brightfield image with all localisations
    ax[0, 0].imshow(para['bf_dict']['proc_brightfield_segm_image'], cmap = para['cmap_applied'])
    ax[0, 0].scatter(para['bf_dict']['loc_pixel_table'].loc[:, 'x'], para['bf_dict']['loc_pixel_table'].loc[:, 'y'], circle_spot_size,
                      'black', label='Localisations')
    ax[0, 0].set_title(f"Segmented image containing {len(para['bf_dict']['loc_pixel_table'])} localisations")
    ax[0, 0].set_xlabel('Pixels')
    ax[0, 0].set_ylabel('Pixels')
    ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # # Show processed brightfield image
    # ax[0, 0].imshow(bf_dict['proc_brightfield_image'], cmap='gray')
    # ax[0, 0].set_title('Processed brightfield image (from MacroCellSegmentation.ijm)')
    # ax[0, 0].set_xlabel('Pixels')
    # ax[0, 0].set_ylabel('Pixels')
    # ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # # Show segmented brightfield image
    # ax[0, 1].imshow(bf_dict['proc_brightfield_segm_image'], cmap = para['cmap_applied'])
    # ax[0, 1].set_title(f"Segmentations of {len(bf_dict['proc_brightfield_segm_table'])} cells")
    # ax[0, 1].set_xlabel('Pixels')
    # ax[0, 1].set_ylabel('Pixels')
    # ax[0, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # # Show histogram
    # ax[0, 2].hist(para['csv_data']['brightness'], bins=np.arange(0, 10000, 500),
    #               edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    # ax[0, 2].set_title('Histogram: Intensity of all localisations')
    # ax[0, 2].set_xlabel('Number of counts')
    # ax[0, 2].set_ylabel('Number of localisations')



    # # Plot additional visualizations
    # ax[1, 1].imshow(bf_dict['proc_brightfield_segm_image'], cmap = para['cmap_applied']) 
    # ax[1, 1].scatter(bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] == -1, 'x'], 
    #                  bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] == -1, 'y'],
    #                  circle_spot_size, 'black', label='Outside valid cells')
    # ax[1, 1].scatter(bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] >= 0, 'x'],
    #                  bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] >= 0, 'y'],
    #                  circle_spot_size, 'magenta', label='Within valid cells')
    # ax[1, 1].set_title(f"{np.sum(bf_dict['loc_pixel_table'].loc[:, 'cell_id'] > 0)} localisations within {len(bf_dict['temp_cell_table'])} cells")
    # ax[1, 1].set_xlabel('Pixels')
    # ax[1, 1].set_ylabel('Pixels')
    # ax[1, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
 
    plt.tight_layout()  # Adjust layout to prevent overlap
 
    # Save figure as PNG
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig04_cells.png', dpi = para['dpi'])
    
    plt.show()


    return para

