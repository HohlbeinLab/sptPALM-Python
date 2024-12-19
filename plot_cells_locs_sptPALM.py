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

def plot_cells_locs_sptPALM(para, bf_dict):
  
    print('  Run plot_locs_cells_sptPALM.py')
    # Plot images initially segmented elsewhere
    fig, ax = plt.subplots(2, 3, figsize=(14, 8)) # 
    fig.suptitle('Brightfield images, segmentations, and localisations + Histogram of localisation intensities')
    circle_spot_size = 1

    # Show processed brightfield image
    ax[0, 0].imshow(bf_dict['proc_brightfield_image'], cmap='gray')
    ax[0, 0].set_title('Proc. brightfield image (MacroCellSegmentation.ijm)')
    ax[0, 0].set_xlabel('Pixels')
    ax[0, 0].set_ylabel('Pixels')
    ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Show segmented brightfield image
    ax[0, 1].imshow(bf_dict['proc_brightfield_segm_image'], cmap = para['cmap_applied'])
    ax[0, 1].set_title(f"Proc. brightfield segm. image with {len(bf_dict['proc_brightfield_segm_table'])} cells")
    ax[0, 1].set_xlabel('Pixels')
    ax[0, 1].set_ylabel('Pixels')
    ax[0, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Show histogram of intensities over all (!) localisations
    ax[0, 2].hist(para['csv_data']['brightness'], bins=np.arange(0, max(para['csv_data']['brightness']), 500),
                  edgecolor='black', facecolor='lightgray', alpha=0.9)
    ax[0, 2].set_title('Histogram: Intensities of all localisations')
    ax[0, 2].set_xlabel('Number of counts (intensity)')
    ax[0, 2].set_ylabel('Number of localisations')

    # Show segmented brightfield image with all localisations
    ax[1, 0].imshow(bf_dict['proc_brightfield_segm_image'], cmap = para['cmap_applied'])
    ax[1, 0].scatter(bf_dict['loc_pixel_table'].loc[:, 'x'], bf_dict['loc_pixel_table'].loc[:, 'y'], circle_spot_size,
                     'black', label='Localisations')
    ax[1, 0].set_title(f"Segmented image with {len(bf_dict['loc_pixel_table'])} localisations")
    ax[1, 0].set_xlabel('Pixels')
    ax[1, 0].set_ylabel('Pixels')
    ax[1, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Show segmented brightfield image with localisations in valid cells
    ax[1, 1].imshow(bf_dict['proc_brightfield_segm_image'], cmap = para['cmap_applied']) 
    ax[1, 1].scatter(bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] == -1, 'x'], 
                     bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] == -1, 'y'],
                     circle_spot_size, 'black', label='Outside valid cells')
    ax[1, 1].scatter(bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] >= 0, 'x'],
                     bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] >= 0, 'y'],
                     circle_spot_size, 'magenta', label='Within valid cells')
    ax[1, 1].set_title(f"{np.sum(bf_dict['loc_pixel_table'].loc[:, 'cell_id'] >= 0)} localisations within {len(bf_dict['temp_cell_table'])} cells")
    ax[1, 1].set_xlabel('Pixels')
    ax[1, 1].set_ylabel('Pixels')
    ax[1, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Empty the 6th plot, also possible: ax[-1, -1].axis('off')
    ax[1, 2].axis('off')    

    plt.tight_layout()  # Adjust layout to prevent overlap
 
    # Save figure as PNG
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig01_segm.' + para['plot_option_save'], dpi = para['dpi'])
    
    plt.show()

    return
