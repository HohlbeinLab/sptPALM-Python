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

def apply_cell_segmentation(para1):
    # Define filenames to load existing data
    para1['filename_procBrightfield_segm'] = para1['filename_procBrightfield'][:-4] + '_segm.tif'
    para1['filename_procBrightfield_segm_Table'] = para1['filename_procBrightfield_segm'][:-4] + '_Table.csv'

    # Load processed brightfield image with cells '*_procBrightfield.tif'
    load_procBrightfield = para1['dataPathName'] + para1['filename_procBrightfield']
    print(f' load_procBrightfield: {load_procBrightfield}')
    procBrightfield_image = imread(load_procBrightfield)

    # Load segmented image with cells '*_procBrightfield_segm.tif'
    load_procBrightfield_segm = para1['dataPathName'] + para1['filename_procBrightfield_segm']
    print(f' load_procBrightfield_segm: {load_procBrightfield_segm}')
    procBrightfield_segm_image = imread(load_procBrightfield_segm)
    #!!!!!!for python x and y changes in the following
    segm_image_yposMaxPixel, segm_image_xposMaxPixel = procBrightfield_segm_image.shape

    # Load table with information on the segmentations '*_procBrightfield_segm_Table.csv'
    load_procBrightfield_segm_Table = para1['dataPathName'] + para1['filename_procBrightfield_segm_Table']
    print(f' load_procBrightfield_segm_Table: {load_procBrightfield_segm_Table}')
    procBrightfield_segm_Table = pd.read_csv(load_procBrightfield_segm_Table).to_numpy()

    # Load table '*_analysis.csv'
    load_file = para1['dataPathName'] + para1['filename_analysis_csv']
    save_file = para1['dataPathName'] + para1['filename_analysis_csv']

    # Import '*_analysis.csv'
    csv_array = pd.read_csv(load_file)
    x_column = csv_array.columns.get_loc('x [nm]')
    y_column = csv_array.columns.get_loc('y [nm]')

    # Check for x- and y-positions and transform them into pixels
    loc_pixel_array = np.zeros((len(csv_array), 4))  # Initialize with zeros
    if x_column is not None and y_column is not None:
        loc_pixel_array[:, :2] = csv_array.iloc[:, [x_column, y_column]].to_numpy()
        loc_pixel_array[:, 0] = np.clip(np.round(loc_pixel_array[:, 0] / (para1['pixelSize'] * 1000)).astype(int), 1, segm_image_xposMaxPixel)
        loc_pixel_array[:, 1] = np.clip(np.round(loc_pixel_array[:, 1] / (para1['pixelSize'] * 1000)).astype(int), 1, segm_image_yposMaxPixel)
    else:
        print('\n Warning, column "x [nm]" and/or "y [nm]" not found!\n')

    loc_pixel_array[:, 2] = -1  # Will contain cell_id
    loc_pixel_array[:, 3] = -1  # Will contain cell_area_id

    # Warn if cell_ids are already assigned
    if (csv_array['cell_id'] != -1).sum() > 1:
        print('Warning: Previously assigned localisations in your analysis file have been overwritten!')

    # Plot images initially segmented elsewhere
    fig, ax = plt.subplots(2, 3, figsize=(14, 8))
    circle_spot_size = 4

    # Show processed brightfield image
    ax[0, 0].imshow(procBrightfield_image, cmap='gray')
    ax[0, 0].set_title('Processed brightfield image (MacroCellSegmentation.ijm)')
    ax[0, 0].set_xlabel('Pixels')
    ax[0, 0].set_ylabel('Pixels')

    # Show segmented brightfield image
    ax[0, 1].imshow(procBrightfield_segm_image, cmap='nipy_spectral')
    ax[0, 1].set_title(f'Segmentations of {len(procBrightfield_segm_Table)} cells')
    ax[0, 1].set_xlabel('Pixels')
    ax[0, 1].set_ylabel('Pixels')

    # Show histogram
    ax[0, 2].hist(para1['OutputTable']['brightness'], bins=np.arange(0, 10000, 500), edgecolor='#4A75AC', facecolor='#5B9BD5', alpha=0.9)
    ax[0, 2].set_title('Histogram: Intensity of all localisations')
    ax[0, 2].set_xlabel('Number of counts')
    ax[0, 2].set_ylabel('Number of localisations')

    # Show segmented brightfield image with all localisations
    ax[1, 0].imshow(procBrightfield_segm_image, cmap='nipy_spectral')
    #!!!!!!for python x and y changes in the following: 1,0 => 0,1
    ax[1, 0].scatter(loc_pixel_array[:, 0], loc_pixel_array[:, 1], circle_spot_size, 'black', label='Localisations')
    ax[1, 0].set_title(f'Segmented image containing {len(loc_pixel_array)} localisations')
    ax[1, 0].set_xlabel('Pixels')
    ax[1, 0].set_ylabel('Pixels')

    print(f'Total number of localisations: {len(loc_pixel_array)}')
    print(f'Number of cells before filtering: {len(procBrightfield_segm_Table)}')

    # Filter cell segments for size
    temp_cell_array = []
    for i in range(procBrightfield_segm_Table.shape[0]):
        if para1['CellAreaPix_min'] <= procBrightfield_segm_Table[i, 1] <= para1['CellAreaPix_max']:
            temp_cell_array.append([procBrightfield_segm_Table[i, 0], procBrightfield_segm_Table[i, 1]])
    temp_cell_array = np.array(temp_cell_array)

    print(f'Number of cells after filtering: {len(temp_cell_array)}')

    # # Check for each localisation whether it is part of a valid cell or not
    # for j in range(len(temp_cell_array)):
    #     if j % 50 == 0:
    #         print(f'Cell {j + 1} of {len(temp_cell_array)}')
    #     temp_im = (procBrightfield_segm_image == temp_cell_array[j, 0]).T
    #     for i in range(csv_array.shape[0]):
    #         if temp_im[loc_pixel_array[i, 0].astype(int) - 1, loc_pixel_array[i, 1].astype(int) - 1]:
    #             loc_pixel_array[i, 2] = temp_cell_array[j, 0]
    #             loc_pixel_array[i, 3] = temp_cell_array[j, 1]

   # Create a dictionary for the masks
    cell_masks = {}
    for j in range(len(temp_cell_array)):
        if j % 50 == 0:
            print(f'Cell {j + 1} of {len(temp_cell_array)}')
        cell_id = temp_cell_array[j, 0]
        cell_masks[cell_id] = (procBrightfield_segm_image == cell_id).T

    # Check each localization against all valid cells
    loc_y = loc_pixel_array[:, 0].astype(int) - 1
    loc_x = loc_pixel_array[:, 1].astype(int) - 1

    for cell_id, cell_mask in cell_masks.items():
        inside_mask = cell_mask[loc_y, loc_x]
        loc_pixel_array[inside_mask, 2] = cell_id
        loc_pixel_array[inside_mask, 3] = temp_cell_array[temp_cell_array[:, 0] == cell_id, 1]



    # Plot additional visualizations
    ax[1, 1].imshow(procBrightfield_segm_image, cmap='nipy_spectral')
    #!!!!! for python x and y changes in the following: 1,0 => 0,1
    ax[1, 1].scatter(loc_pixel_array[loc_pixel_array[:, 2] == -1, 0], loc_pixel_array[loc_pixel_array[:, 2] == -1, 1], circle_spot_size, 'black', label='Outside')
    ax[1, 1].scatter(loc_pixel_array[loc_pixel_array[:, 2] > 0, 0], loc_pixel_array[loc_pixel_array[:, 2] > 0, 1], circle_spot_size, 'magenta', label='Within cells')
    ax[1, 1].set_title(f'{np.sum(loc_pixel_array[:, 2] > 0)} localisations within {len(temp_cell_array)} cells')
    ax[1, 1].set_xlabel('Pixels')
    ax[1, 1].set_ylabel('Pixels')

    # Save figure as PNG
    if not para1.get('dataPathOutp'):
        plt.savefig(f"{para1['dataPathName']}{para1['filename_thunderstormCSV'][:-4]}-analysis-Fig01_segm.png")
    else:
        tmp_name = para1['filename_thunderstormCSV'].split("\\")[-1][:-4]
        plt.savefig(f"{para1['dataPathOutp']}{tmp_name}-analysis-Fig01_segm.png")

    print(f'Number of localisations within cells: {np.sum(loc_pixel_array[:, 2] > 0)}')
    print(f'Number of localisations outside cells: {np.sum(loc_pixel_array[:, 2] == -1)}')

    # Update cell_ids in '*_analysis.csv' and export
    csv_array['cell_id'] = loc_pixel_array[:, 2]
    csv_array['cell_area_id'] = loc_pixel_array[:, 3]
    csv_array.to_csv(save_file, index=False, quoting=0)

    para1['OutputTable'] = csv_array
    print('Segmentation analysis done!')
    print('cell_ids have been assigned in *_analysis.csv!')

    return para1

