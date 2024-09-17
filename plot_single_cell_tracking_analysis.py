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

# Assuming Para1 is a dictionary-like object
def plot_single_cell_tracking_analysis(para):

    print('\nRun Plot_SingleCellTrackingAnalysis()')
    print('  Start visualisation of tracks in valid cells')
    
    # Figure A: display tracks in cells (with color-coded diffusion coefficients)
    plot_tracks_in_cells(para)
 
    return para    
 
    
def plot_tracks_in_cells(para):

    # Load processed brightfield image with cells, filename: '*_procBrightfield.tif'
    print(f"  Load_proc_brightfield: {para['fn_proc_brightfield']}")
    bf_dict = {} 
    bf_dict['proc_brightfield_image'] = imread(para['data_dir'] + para['fn_proc_brightfield'])
    
    
    # Plot images initially segmented elsewhere
    fig2, ax = plt.subplots(1, 1, figsize=(14, 8)) # 
  
    
    # Show processed brightfield image
    ax.imshow(bf_dict['proc_brightfield_image'], cmap='gray')
    ax.set_title('Processed brightfield image (from MacroCellSegmentation.ijm)')
    ax.set_xlabel('Pixels')
    ax.set_ylabel('Pixels')
    ax.set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Prepare colormap
    myColorMap = plt.get_cmap('hot', 1000)

    # Plot valid tracks for each valid cell
    for cc in range(len(para['scta_table'])):
        if para['scta_table']['#tracks (filtered for #tracks per cell)'][cc] > 1:  # Display only if tracks exist
            
        
            # Select data from a particular cell_id
            # part_csv_data = csv_data[csv_data['cell_id'] == cell_ids[jj]]       
        
        
            tempCellDdata = para['diff_coeffs_filtered_list'][para['diff_coeffs_filtered_list']['cell_id'] == para['scta_table']['cell_id'][cc]]
            breakpoint()
            tempCellTracks = para['scta_tracks'][cc]

            # Plot each valid track
            for pp in range(len(tempCellDdata)):
                Dtrack = tempCellDdata[pp] 
                Dtrack = max(Dtrack, 0)  # Handle negative diffusion coefficients
                
                tmp_colindx = min(1 + np.floor(Dtrack * 999 / (para['plot_diff_hist_max'] * para['SCTA_vis_rangemax'])), 999).astype(int)
                lineColor = myColorMap(tmp_colindx)

                x = tempCellTracks[pp][:, 6] / para['pixel_size'] 
                y = tempCellTracks[pp][:, 5] / para['pixel_size'] 

                ax.plot(x, y, linewidth=para['linewidth'], color=lineColor)

                if para['plot_frame_number']:
                    ax.text(x[0], y[0], str(int(tempCellTracks[pp][0, 2])), fontsize=para['fontsize']-2)

    # Add colorbar for diffusion coefficients
    cbar = fig2.colorbar(plt.cm.ScalarMappable(cmap=myColorMap), ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Diffusion coefficient (µm²/sec)', fontsize=para['fontsize'])
    cbar.ax.tick_params(labelsize=para['fontsize'])

    
    plt.tight_layout()  # Adjust layout to prevent overlap
 
    # Save figure as PNG
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig03_tracks.png', dpi = para['dpi'])

    return para




