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

import pandas as pd
import numpy as np
import os
from skimage.io import imread
from plot_cells_locs_sptPALM import plot_cells_locs_sptPALM

def apply_cell_segmentation_sptPALM(para):
    print('Run apply_cell_segmentation_sptPALM.py')
    
    # the following definition will it make easier to wrap other segmentation input
    # general structue: colum_names={'name_internally','name_from_extern'}
    segm_table_column_names = {'Label':'Label',
                    'volume':'volume'
                    } 
    
    # Define filenames to load existing data (requires correct settings in ImageJ/Fiji: 'Macro_CellSegmentation.imj')
    para['fn_proc_brightfield_segm'] = para['fn_proc_brightfield'][:-4] + '_segm.tif'
    para['fn_proc_brightfield_segm_table'] = para['fn_proc_brightfield_segm'][:-4] + '_table.csv'

    # Load processed brightfield image with cells, filename: '*_procBrightfield.tif'
    print(f"  Load_proc_brightfield: {para['fn_proc_brightfield']}")
    bf_dict = {} # brightfield_dictionary
    bf_dict['proc_brightfield_image'] = imread(para['data_dir'] + para['fn_proc_brightfield'])

    # Load segmented image with cells, filename '*_procBrightfield_segm.tif'
    print(f"  Load_proc_brightfield_segm: {para['fn_proc_brightfield_segm']}")
    bf_dict['proc_brightfield_segm_image'] = imread(para['data_dir'] + para['fn_proc_brightfield_segm'])
    
    # Load table with information on the segmentations, filename '*_procBrightfield_segm_table.csv'
    print(f"  Load_proc_brightfield_segm_table: {para['fn_proc_brightfield_segm_table']}")
    bf_dict['proc_brightfield_segm_table'] = pd.read_csv(para['data_dir'] + para['fn_proc_brightfield_segm_table'])
         
    # Import '*_analysis.csv'
    temp_path = os.path.join(para['data_dir'], para['default_output_dir'])
    csv_data = pd.read_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'])

    # Check for x- and y-positions and transform them into pixels
    # ATTENTION: replace with different column names if needed
    column_names = ['x', 'y', 'cell_id', 'cell_area'] 
    bf_dict['loc_pixel_table'] = pd.DataFrame(np.zeros((len(csv_data), len(column_names))), columns=column_names)

    bf_dict['loc_pixel_table'].loc[:, ['x','y']] = csv_data[['x [µm]', 'y [µm]']].to_numpy()
    
    bf_dict['loc_pixel_table'].loc[:, 'x'] = np.clip(np.round(bf_dict['loc_pixel_table'].loc[:, 'x'] / (
        para['pixelsize'])).astype(int), 1, bf_dict['proc_brightfield_segm_image'].shape[1])
    
    bf_dict['loc_pixel_table'].loc[:, 'y'] = np.clip(np.round(bf_dict['loc_pixel_table'].loc[:, 'y'] / (
        para['pixelsize'])).astype(int), 1, bf_dict['proc_brightfield_segm_image'].shape[0])

    bf_dict['loc_pixel_table'].loc[:, 'cell_id'] = -1  
    bf_dict['loc_pixel_table'].loc[:, 'cell_area'] = -1  

    # Warn if cell_ids are already assigned
    if (csv_data['cell_id'] != -1).sum() > 1:
        print('\n  Warning: Previously assigned localisations in your analysis file have been overwritten!')

    print(f"  Total number of localisations: {len(bf_dict['loc_pixel_table'])}")
    print(f"  Number of cells before filtering: {len(bf_dict['proc_brightfield_segm_table'])}")

    # Filter cells for size
    # e.g., Min, max size for cell-outline data in pixel^2
    # ATTENTION: replace with different column names if needed
    column_names = ['segm_cell_id', 'segm_cell_area']
    bf_dict['temp_cell_table'] = pd.DataFrame(columns=column_names)
    
    # Select "valid" cells if their area/volume is within the given boundaries
    for i in range(bf_dict['proc_brightfield_segm_table'].shape[0]):
        if para['cellarea_pixels_min'] <= bf_dict['proc_brightfield_segm_table'].loc[i, segm_table_column_names['volume']] <= para['cellarea_pixels_max']:
            new_row = pd.DataFrame({
                'segm_cell_id': [bf_dict['proc_brightfield_segm_table'].loc[i,segm_table_column_names['Label']]],
                'segm_cell_area': [bf_dict['proc_brightfield_segm_table'].loc[i, segm_table_column_names['volume']]]
                })
            bf_dict['temp_cell_table'] = pd.concat([bf_dict['temp_cell_table'], new_row], ignore_index=True)

    print(f"  Number of cells after filtering: {len(bf_dict['temp_cell_table'])}")

    # Check for each localisation whether it is part of a valid cell or not
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
    plot_cells_locs_sptPALM(para, bf_dict)

    # Update cell_ids in '*.csv' and export
    csv_data['cell_id'] = bf_dict['loc_pixel_table'].loc[:, 'cell_id']
    csv_data['cell_area'] = bf_dict['loc_pixel_table'].loc[:, 'cell_area']
    csv_data.to_csv(temp_path + para['fn_locs'][:-4] + para['fn_csv_handle'], index=False, quoting=0)

    para['csv_data'] = csv_data
    para['bf_dict'] = bf_dict
    print(f"  Cell_ids have been updated in {para['fn_locs'][:-4] + para['fn_csv_handle']}")
    print('  Segmentation analysis done!')
    
    return para

