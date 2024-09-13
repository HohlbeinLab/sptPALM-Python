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
    print('\nRun apply_cell_segmentation.py')
    CMAP_APPLIED = 'gist_ncar' ##was: 'nipy_spectral', tab20c, 
    # Define filenames to load existing data (requires correct settings in ImageJ/Fiji macro 'Cell Segmentation')
    para['fn_proc_brightfield_segm'] = para['fn_proc_brightfield'][:-4] + '_segm.tif'
    para['fn_proc_brightfield_segm_table'] = para['fn_proc_brightfield_segm'][:-4] + '_table.csv'

    # Load processed brightfield image with cells, filename: '*_procBrightfield.tif'
    print(f"  load_proc_brightfield: {para['fn_proc_brightfield']}")
    proc_brightfield_image = imread(para['data_pathname'] + para['fn_proc_brightfield'])

    # Load segmented image with cells, filename '*_procBrightfield_segm.tif'
    print(f"  load_proc_brightfield_segm: {para['fn_proc_brightfield_segm']}")
    proc_brightfield_segm_image = imread(para['data_pathname'] + para['fn_proc_brightfield_segm'])
    segm_image_y_pos_max_pixel, segm_image_x_pos_max_pixel = proc_brightfield_segm_image.shape

    # Load table with information on the segmentations, filename '*_procBrightfield_segm_table.csv'
    print(f"  load_proc_brightfield_segm_table: {para['fn_proc_brightfield_segm_table']}")
    proc_brightfield_segm_table = pd.read_csv(para['data_pathname'] + para['fn_proc_brightfield_segm_table']).to_numpy()

    # Import '*_analysis.csv'
    temp_path = os.path.join(para['data_pathname'], para['default_output_dir'])
    csv_data = pd.read_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'])
    x_column = csv_data.columns.get_loc('x [um]')
    y_column = csv_data.columns.get_loc('y [um]')

    # Check for x- and y-positions and transform them into pixels
    loc_pixel_array = np.zeros((len(csv_data), 4))  # Initialize with zeros
    if x_column is not None and y_column is not None:
        loc_pixel_array[:, :2] = csv_data.iloc[:, [x_column, y_column]].to_numpy()
        loc_pixel_array[:, 0] = np.clip(np.round(loc_pixel_array[:, 0] / (
            para['pixel_size'])).astype(int), 1, segm_image_x_pos_max_pixel)
        loc_pixel_array[:, 1] = np.clip(np.round(loc_pixel_array[:, 1] / (
            para['pixel_size'])).astype(int), 1, segm_image_y_pos_max_pixel)
    else:
        print('\n Warning, column "x [um]" and/or "y [um]" not found!\n')

    loc_pixel_array[:, 2] = -1  # Will contain cell_id
    loc_pixel_array[:, 3] = -1  # Will contain cell_area_id

    # Warn if cell_ids are already assigned
    if (csv_data['cell_id'] != -1).sum() > 1:
        print('\n  Warning: Previously assigned localisations in your analysis file have been overwritten!')

    # Plot images initially segmented elsewhere
    fig, ax = plt.subplots(2, 3, figsize=(14, 8)) # 
    circle_spot_size = 2

    # Show processed brightfield image
    ax[0, 0].imshow(proc_brightfield_image, cmap='gray')
    ax[0, 0].set_title('Processed brightfield image (from MacroCellSegmentation.ijm)')
    ax[0, 0].set_xlabel('Pixels')
    ax[0, 0].set_ylabel('Pixels')
    ax[0, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Show segmented brightfield image
    ax[0, 1].imshow(proc_brightfield_segm_image, cmap = CMAP_APPLIED)
    ax[0, 1].set_title(f'Segmentations of {len(proc_brightfield_segm_table)} cells')
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
    ax[1, 0].imshow(proc_brightfield_segm_image, cmap = CMAP_APPLIED)
    ax[1, 0].scatter(loc_pixel_array[:, 0], loc_pixel_array[:, 1], circle_spot_size,
                     'black', label='Localisations')
    ax[1, 0].set_title(f'Segmented image containing {len(loc_pixel_array)} localisations')
    ax[1, 0].set_xlabel('Pixels')
    ax[1, 0].set_ylabel('Pixels')
    ax[1, 0].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    print(f'  Total number of localisations: {len(loc_pixel_array)}')
    print(f'  Number of cells before filtering: {len(proc_brightfield_segm_table)}')

    # Filter cell segments for size
    temp_cell_array = []
    for i in range(proc_brightfield_segm_table.shape[0]):
        if para['cellarea_pixels_min'] <= proc_brightfield_segm_table[i, 1] <= para['cellarea_pixels_max']:
            temp_cell_array.append([proc_brightfield_segm_table[i, 0], proc_brightfield_segm_table[i, 1]])
    temp_cell_array = np.array(temp_cell_array)

    print(f'  Number of cells after filtering: {len(temp_cell_array)}')

    # Check for each localisation whether it is part of a valid cell or not
    # Create a dictionary for the masks
    cell_masks = {}
    print("  Cell... ")
    for j in range(len(temp_cell_array)):
        if j % 50 == 0 and j > 0:
            print(f'   ...cell {j} of {len(temp_cell_array)},')
        
        cell_id = temp_cell_array[j, 0]
        cell_masks[cell_id] = (proc_brightfield_segm_image == cell_id).T
    print(f'   ...cell {j+1} of {len(temp_cell_array)}.')
    
    # Check each localization against all valid cells
    loc_y = loc_pixel_array[:, 0].astype(int) - 1
    loc_x = loc_pixel_array[:, 1].astype(int) - 1

    for cell_id, cell_mask in cell_masks.items():
        inside_mask = cell_mask[loc_y, loc_x]
        loc_pixel_array[inside_mask, 2] = cell_id
        loc_pixel_array[inside_mask, 3] = temp_cell_array[temp_cell_array[:, 0] == cell_id, 1]

    # Plot additional visualizations
    ax[1, 1].imshow(proc_brightfield_segm_image, cmap = CMAP_APPLIED) 
    ax[1, 1].scatter(loc_pixel_array[loc_pixel_array[:, 2] == -1, 0], 
                     loc_pixel_array[loc_pixel_array[:, 2] == -1, 1],
                     circle_spot_size, 'black', label='Outside valid cells')
    ax[1, 1].scatter(loc_pixel_array[loc_pixel_array[:, 2] > 0, 0],
                     loc_pixel_array[loc_pixel_array[:, 2] > 0, 1],
                     circle_spot_size, 'magenta', label='Within valid cells')
    ax[1, 1].set_title(f'{np.sum(loc_pixel_array[:, 2] > 0)} localisations within {len(temp_cell_array)} cells')
    ax[1, 1].set_xlabel('Pixels')
    ax[1, 1].set_ylabel('Pixels')
    ax[1, 1].set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    plt.tight_layout()  # Adjust layout to prevent overlap

    # Save figure as PNG
    plt.savefig(temp_path + para['fn_locs'][:-4] + '_Fig01_segm.png', dpi = para['dpi'])
    
    plt.show()

    print(f'  Number of localisations within cells: {np.sum(loc_pixel_array[:, 2] > 0)}')
    print(f'  Number of localisations outside cells: {np.sum(loc_pixel_array[:, 2] == -1)}')

    # Update cell_ids in '*.csv' and export
    csv_data['cell_id'] = loc_pixel_array[:, 2]
    csv_data['cell_area_id'] = loc_pixel_array[:, 3]
    csv_data.to_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'], index=False, quoting=0)

    para['csv_data'] = csv_data
    print(f"  Cell_ids have been updated in {para['fn_locs'][:-4] + para['fn_csv_handle']}")
    print('  Segmentation analysis done!')
    return para

