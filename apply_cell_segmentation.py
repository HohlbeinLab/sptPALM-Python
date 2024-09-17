#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.io import imread

def apply_cell_segmentation(para):
    print('Run apply_cell_segmentation.py')
    
    # Define filenames to load existing data (requires correct settings in ImageJ/Fiji macro 'Cell Segmentation')
    para['fn_proc_brightfield_segm'] = para['fn_proc_brightfield'][:-4] + '_segm.tif'
    para['fn_proc_brightfield_segm_table'] = para['fn_proc_brightfield_segm'][:-4] + '_table.csv'

    # Load processed brightfield image with cells, filename: '*_procBrightfield.tif'
    print(f"  Load_proc_brightfield: {para['fn_proc_brightfield']}")
    bf_dict = {} 
    bf_dict['proc_brightfield_image'] = imread(para['data_dir'] + para['fn_proc_brightfield'])

    # Load segmented image with cells, filename '*_procBrightfield_segm.tif'
    print(f"  Load_proc_brightfield_segm: {para['fn_proc_brightfield_segm']}")
    # proc_brightfield_segm_image = imread(para['data_dir'] + para['fn_proc_brightfield_segm'])
    bf_dict['proc_brightfield_segm_image'] = imread(para['data_dir'] + para['fn_proc_brightfield_segm'])
    
    # Load table with information on the segmentations, filename '*_procBrightfield_segm_table.csv'
    print(f"  Load_proc_brightfield_segm_table: {para['fn_proc_brightfield_segm_table']}")
    bf_dict['proc_brightfield_segm_table'] = pd.read_csv(para['data_dir'] + para['fn_proc_brightfield_segm_table'])
    
    # To go with Python convention start labels from 0 (image segmentation , labels start from 1!!!)
    bf_dict['proc_brightfield_segm_image'] -= 1 if bf_dict['proc_brightfield_segm_image'].min() == 1 else 0
    bf_dict['proc_brightfield_segm_table'] -= 1 if bf_dict['proc_brightfield_segm_table'].loc[:, 'Label'].min() == 1 else 0
    
    # Import '*_analysis.csv'
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    csv_data = pd.read_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'])

    # Check for x- and y-positions and transform them into pixels
    column_names = ['x', 'y', 'cell_id', 'cell_area']  # Replace with your actual column names
    bf_dict['loc_pixel_table'] = pd.DataFrame(np.zeros((len(csv_data), len(column_names))), columns=column_names)

    bf_dict['loc_pixel_table'].loc[:, ['x','y']] = csv_data[['x [um]', 'y [um]']].to_numpy()
    bf_dict['loc_pixel_table'].loc[:, 'x'] = np.clip(np.round(bf_dict['loc_pixel_table'].loc[:, 'x'] / (
        para['pixel_size'])).astype(int), 1, bf_dict['proc_brightfield_segm_image'].shape[1])
    bf_dict['loc_pixel_table'].loc[:, 'y'] = np.clip(np.round(bf_dict['loc_pixel_table'].loc[:, 'y'] / (
        para['pixel_size'])).astype(int), 1, bf_dict['proc_brightfield_segm_image'].shape[0])

    bf_dict['loc_pixel_table'].loc[:, 'cell_id'] = -1  
    bf_dict['loc_pixel_table'].loc[:, 'cell_area'] = -1  

    # Warn if cell_ids are already assigned
    if (csv_data['cell_id'] != -1).sum() > 1:
        print('\n  Warning: Previously assigned localisations in your analysis file have been overwritten!')

    print(f"  Total number of localisations: {len(bf_dict['loc_pixel_table'])}")
    print(f"  Number of cells before filtering: {len(bf_dict['proc_brightfield_segm_table'])}")

    # Filter cells for size
    # e.g., Min, max size for cell-outline data in pixel^2
    column_names = ['segm_cell_id', 'segm_cell_area']  # Replace with your actual column names
    bf_dict['temp_cell_table'] = pd.DataFrame(columns=column_names)
    
    # Select "valid" cells if their area/volume is within the given range
    for i in range(bf_dict['proc_brightfield_segm_table'].shape[0]):
        if para['cellarea_pixels_min'] <= bf_dict['proc_brightfield_segm_table'].loc[i, 'volume'] <= para['cellarea_pixels_max']:
            new_row = pd.DataFrame({
                'segm_cell_id': [bf_dict['proc_brightfield_segm_table'].loc[i,'Label']],
                'segm_cell_area': [bf_dict['proc_brightfield_segm_table'].loc[i, 'volume']]
                })
            bf_dict['temp_cell_table'] = pd.concat([bf_dict['temp_cell_table'], new_row], ignore_index=True)

    print(f"  Number of cells after filtering: {len(bf_dict['temp_cell_table'])}")

    # Check for each localisation whether it is part of a valid cell or not
    # Create a dictionary for the masks
    cell_masks = {}
    print("  Cell... ")
    
    # Run loop for each "valid" cell
    for j in range(len(bf_dict['temp_cell_table'])):
        if j % 50 == 0 and j > 0:
            print(f"   ...cell {j} of {len(bf_dict['temp_cell_table'])},")  
        cell_id = bf_dict['temp_cell_table'].loc[j,'segm_cell_id']
        cell_masks[j] = (bf_dict['proc_brightfield_segm_image'] == cell_id).T # .T transpose matrix
    print(f"   ...cell {j+1} of {len(bf_dict['temp_cell_table'])}.")
      
    # Check each localization against all valid cells
    loc_y = bf_dict['loc_pixel_table'].loc[:, 'x'].astype(int)-1
    loc_x = bf_dict['loc_pixel_table'].loc[:, 'y'].astype(int)-1

    for i, cell_mask in cell_masks.items(): 
        inside_mask = cell_mask[loc_y, loc_x]
        bf_dict['loc_pixel_table'].loc[inside_mask, 'cell_id'] = bf_dict['temp_cell_table'].loc[i,'segm_cell_id']
        bf_dict['loc_pixel_table'].loc[inside_mask, 'cell_area'] = bf_dict['temp_cell_table'].loc[i,'segm_cell_area']

    print(f"  Number of localisations within cells: {np.sum(bf_dict['loc_pixel_table'].loc[:, 'cell_id'] >= 0)}")
    print(f"  Number of localisations outside cells: {np.sum(bf_dict['loc_pixel_table'].loc[:, 'cell_id'] == -1)}")

    # Plot data
    plot_locs_cells(bf_dict, para)

    # Update cell_ids in '*.csv' and export
    csv_data['cell_id'] = bf_dict['loc_pixel_table'].loc[:, 'cell_id']
    csv_data['cell_area'] = bf_dict['loc_pixel_table'].loc[:, 'cell_area']
    csv_data.to_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'], index=False, quoting=0)

    para['csv_data'] = csv_data
    print(f"  Cell_ids have been updated in {para['fn_locs'][:-4] + para['fn_csv_handle']}")
    print('  Segmentation analysis done!')
    
    # breakpoint()
    return para

def plot_locs_cells(bf_dict, para):
    
    # Plot images initially segmented elsewhere
    fig, ax = plt.subplots(2, 3, figsize=(14, 8)) # 
    circle_spot_size = 2

    # Show processed brightfield image
    ax[0, 0].imshow(bf_dict['proc_brightfield_image'], cmap='gray')
    ax[0, 0].set_title('Processed brightfield image (from MacroCellSegmentation.ijm)')
    ax[0, 0].set_xlabel('Pixels')
    ax[0, 0].set_ylabel('Pixels')
    ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Show segmented brightfield image
    ax[0, 1].imshow(bf_dict['proc_brightfield_segm_image'], cmap = para['cmap_applied'])
    ax[0, 1].set_title(f"Segmentations of {len(bf_dict['proc_brightfield_segm_table'])} cells")
    ax[0, 1].set_xlabel('Pixels')
    ax[0, 1].set_ylabel('Pixels')
    ax[0, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Show histogram
    ax[0, 2].hist(para['csv_data']['brightness'], bins=np.arange(0, 10000, 500),
                  edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    ax[0, 2].set_title('Histogram: Intensity of all localisations')
    ax[0, 2].set_xlabel('Number of counts')
    ax[0, 2].set_ylabel('Number of localisations')

    # Show segmented brightfield image with all localisations
    ax[1, 0].imshow(bf_dict['proc_brightfield_segm_image'], cmap = para['cmap_applied'])
    ax[1, 0].scatter(bf_dict['loc_pixel_table'].loc[:, 'x'], bf_dict['loc_pixel_table'].loc[:, 'y'], circle_spot_size,
                     'black', label='Localisations')
    ax[1, 0].set_title(f"Segmented image containing {len(bf_dict['loc_pixel_table'])} localisations")
    ax[1, 0].set_xlabel('Pixels')
    ax[1, 0].set_ylabel('Pixels')
    ax[1, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Plot additional visualizations
    ax[1, 1].imshow(bf_dict['proc_brightfield_segm_image'], cmap = para['cmap_applied']) 
    ax[1, 1].scatter(bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] == -1, 'x'], 
                     bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] == -1, 'y'],
                     circle_spot_size, 'black', label='Outside valid cells')
    ax[1, 1].scatter(bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] >= 0, 'x'],
                     bf_dict['loc_pixel_table'].loc[bf_dict['loc_pixel_table'].loc[:, 'cell_id'] >= 0, 'y'],
                     circle_spot_size, 'magenta', label='Within valid cells')
    ax[1, 1].set_title(f"{np.sum(bf_dict['loc_pixel_table'].loc[:, 'cell_id'] > 0)} localisations within {len(bf_dict['temp_cell_table'])} cells")
    ax[1, 1].set_xlabel('Pixels')
    ax[1, 1].set_ylabel('Pixels')
    ax[1, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
 
    plt.tight_layout()  # Adjust layout to prevent overlap
 
    # Save figure as PNG
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig01_segm.png', dpi = para['dpi'])
    
    plt.show()

    return