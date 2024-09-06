#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread

def apply_cell_segmentation(para):
    
    CMAP_APPLIED = 'gist_ncar' ##was: 'nipy_spectral', tab20c, 
    # Define filenames to load existing data
    para['filename_proc_brightfield_segm'] = para['filename_proc_brightfield'][:-4] + '_segm.tif'
    para['filename_proc_brightfield_segm_table'] = para['filename_proc_brightfield_segm'][:-4] + '_Table.csv'

    # Load processed brightfield image with cells '*_procBrightfield.tif'
    load_proc_brightfield = para['data_pathname'] + para['filename_proc_brightfield']
    print(f' load_proc_brightfield: {load_proc_brightfield}')
    proc_brightfield_image = imread(load_proc_brightfield)

    # Load segmented image with cells '*_procBrightfield_segm.tif'
    load_proc_brightfield_segm = para['data_pathname'] + para['filename_proc_brightfield_segm']
    print(f' load_proc_brightfield_segm: {load_proc_brightfield_segm}')
    proc_brightfield_segm_image = imread(load_proc_brightfield_segm)
    segm_image_y_pos_max_pixel, segm_image_x_pos_max_pixel = proc_brightfield_segm_image.shape

    # Load table with information on the segmentations '*_procBrightfield_segm_Table.csv'
    load_proc_brightfield_segm_table = para['data_pathname'] + para['filename_proc_brightfield_segm_table']
    print(f' load_proc_brightfield_segm_table: {load_proc_brightfield_segm_table}')
    proc_brightfield_segm_table = pd.read_csv(load_proc_brightfield_segm_table).to_numpy()

    # Load table '*_analysis.csv'
    load_file = para['data_pathname'] + para['filename_analysisPy_csv']
    save_file = para['data_pathname'] + para['filename_analysisPy_csv']

    # Import '*_analysis.csv'
    csv_array = pd.read_csv(load_file)
    x_column = csv_array.columns.get_loc('x [um]')
    y_column = csv_array.columns.get_loc('y [um]')

    # Check for x- and y-positions and transform them into pixels
    loc_pixel_array = np.zeros((len(csv_array), 4))  # Initialize with zeros
    if x_column is not None and y_column is not None:
        loc_pixel_array[:, :2] = csv_array.iloc[:, [x_column, y_column]].to_numpy()
        loc_pixel_array[:, 0] = np.clip(np.round(loc_pixel_array[:, 0] / (
            para['pixel_size'])).astype(int), 1, segm_image_x_pos_max_pixel)
        loc_pixel_array[:, 1] = np.clip(np.round(loc_pixel_array[:, 1] / (
            para['pixel_size'])).astype(int), 1, segm_image_y_pos_max_pixel)
    else:
        print('\n Warning, column "x [um]" and/or "y [um]" not found!\n')

    loc_pixel_array[:, 2] = -1  # Will contain cell_id
    loc_pixel_array[:, 3] = -1  # Will contain cell_area_id

    # Warn if cell_ids are already assigned
    if (csv_array['cell_id'] != -1).sum() > 1:
        print('Warning: Previously assigned localisations in your analysis file have been overwritten!')

    # Plot images initially segmented elsewhere
    fig, ax = plt.subplots(2, 3, figsize=(14, 8))
    circle_spot_size = 2

    # Show processed brightfield image
    ax[0, 0].imshow(proc_brightfield_image, cmap='gray')
    ax[0, 0].set_title('Processed brightfield image (MacroCellSegmentation.ijm)')
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
    ax[0, 2].hist(para['output_table']['brightness'], bins=np.arange(0, 10000, 500),
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

    print(f'Total number of localisations: {len(loc_pixel_array)}')
    print(f'Number of cells before filtering: {len(proc_brightfield_segm_table)}')

    # Filter cell segments for size
    temp_cell_array = []
    for i in range(proc_brightfield_segm_table.shape[0]):
        if para['cellarea_pixels_min'] <= proc_brightfield_segm_table[i, 1] <= para['cellarea_pixels_max']:
            temp_cell_array.append([proc_brightfield_segm_table[i, 0], proc_brightfield_segm_table[i, 1]])
    temp_cell_array = np.array(temp_cell_array)

    print(f'Number of cells after filtering: {len(temp_cell_array)}')

    # Check for each localisation whether it is part of a valid cell or not
    # Create a dictionary for the masks
    cell_masks = {}
    for j in range(len(temp_cell_array)):
        if j % 50 == 0:
            print(f' Cell {j + 1} of {len(temp_cell_array)}')
        cell_id = temp_cell_array[j, 0]
        cell_masks[cell_id] = (proc_brightfield_segm_image == cell_id).T

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
    plt.show()

    # Save figure as PNG
    if not para.get('data_path_Outp'):
        plt.savefig(f"{para['data_pathname']}{para['filename_thunderstorm_csv'][:-4]}-analysis-Fig01_segm.png", dpi=para['dpi'])
    else:
        tmp_name = para['filename_thunderstorm_csv'].split("\\")[-1][:-4]
        plt.savefig(f"{para['data_path_outp']}{tmp_name}-analysis-Fig01_segm.png", dpi=para['dpi'])

    print(f'Number of localisations within cells: {np.sum(loc_pixel_array[:, 2] > 0)}')
    print(f'Number of localisations outside cells: {np.sum(loc_pixel_array[:, 2] == -1)}')

    # Update cell_ids in '*_analysis.csv' and export
    csv_array['cell_id'] = loc_pixel_array[:, 2]
    csv_array['cell_area_id'] = loc_pixel_array[:, 3]
    csv_array.to_csv(save_file, index=False, quoting=0)

    para['output_table'] = csv_array
    print('Segmentation analysis done!')
    print('cell_ids have been assigned in *_analysisPy.csv!')

    return para

