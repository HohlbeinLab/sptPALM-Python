# -*- coding: utf-8 -*-
"""
Created on Mon May 19 11:25:51 2025

@author: demia
"""

import subprocess
import json
import os
import numpy as np
import tifffile
from skimage.exposure import rescale_intensity
from scipy.ndimage import median_filter

from set_parameters_sptPALM import set_parameters_sptPALM
from set_parameters_sptPALM_GUI import set_parameters_sptPALM_GUI
from helper_functions import yes_no_input

def enhance_contrast_saturated(image, saturation_percent=0.1):
    """Enhance Contrast with normalization and saturation clipping for raw stack image"""
    # Flatten the image and compute saturation limits
    low_cut = np.percentile(image, saturation_percent)
    high_cut = np.percentile(image, 100 - saturation_percent)

    # Clip and normalise
    clipped = np.clip(image, low_cut, high_cut)
    normalized = (clipped - low_cut) / (high_cut - low_cut)
    normalized = np.clip(normalized, 0, 1)
    return (normalized * 255).astype(np.uint8)

def start_omnipose(input_parameter):
    if input_parameter['used_segmentation_method'] == 'Cellpose/Omnipose' and not input_parameter['applied_segmentation']:
        files_to_segment = input_parameter['fn_proc_brightfield']  # list of filenames
        output_directory = input_parameter['data_dir'] # output same directory as where images are stored
        
        # In case z-projection is selected, do z-projection first
        # Save processed brightfield files in same folder
        if input_parameter['z_projection']:
            print("Running z-projection")
            #average intensity
            for i in range(len(files_to_segment)):
                stack = tifffile.imread(os.path.join(output_directory, files_to_segment[i]))
        
                # Z-projection (average intensity)
                z_proj = np.mean(stack, axis=0)
        
                # Subtract global min
                min_val = np.min(z_proj)
                z_proj -= min_val
        
                # Apply median filter
                z_proj = median_filter(z_proj, size=3)
        
                # Enhance contrast and save as 8-bit (like saturated=0.1 normalize)
                z_proj_8bit = enhance_contrast_saturated(z_proj, saturation_percent=0.1)
        
                # Save result
                output_filename = files_to_segment[i][:-4] + '_ProcBrightfield.tif'
                output_path = os.path.join(output_directory, output_filename)
                tifffile.imwrite(output_path, z_proj_8bit)
        
                files_to_segment[i] = output_filename
                        
                print("Additional processing completed")
                
        print("Images not segmented yet")
        print("Starting up GUI for segmentation...")
        
        min_size = str(input_parameter['cellarea_pixels_min']) # Passing parameter to subprocess requires a string value
        script_path = "OmniposeForCommandGUI.py" # Name of script to start up Omnipose GUI
                                                # In same folder as all other files
        files_json = json.dumps(files_to_segment)
        
        # Launch subprocess with Omnipose environment
        # omnipose is the environment name in this case, in case of other name change the setting here
        process = subprocess.Popen([
            "conda", "run", "-n", "omnipose", "python", script_path,
            "--files", files_json,
            "--output", output_directory,
            "--min_size", min_size,
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, text=True)
        
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
        
        process.stdout.close()
        process.wait()
        
        # Check for segmentation done flag
        success_flag_file = "segmentation_done.txt"
        full_path = os.path.join(output_directory, success_flag_file)
        
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                first_line = f.readline().strip()
                if first_line == "success":
                    input_parameter['applied_segmentation'] = True
                    print("Segmentation completed successfully")
                else:
                    print("Segmentation flag file found, but status is not 'success'")
                    input_parameter['applied_segmentation'] = False
        else:
            print("Segmentation failed, flag file not found")
            input_parameter['applied_segmentation'] = False
        
    return

