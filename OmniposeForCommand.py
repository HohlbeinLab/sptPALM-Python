# -*- coding: utf-8 -*-
"""
Omnipose image segmentation using files.
Script to execute the Omnipose segmentation in the command line.
Currently executed when 'Run Segmentation' is pressed in the custom GUI 
from OmniposeForCommandGUI.py.

The script is based on the example notebook: "The basics in 2D",
available in the Omnipose documentation:
https://omnipose.readthedocs.io/examples/mono_channel_bact.html
"""

import omnipose
import torch
from cellpose_omni import io
import cellpose_omni
from cellpose_omni import models
import time
from cellpose_omni import io, transforms
from omnipose.utils import normalize99, clean_boundary
from skimage.io import imread
from skimage.measure import label, regionprops, regionprops_table
import os
import numpy as np

import networkx as nx
from skimage.morphology import skeletonize
from scipy.ndimage import gaussian_filter1d, distance_transform_edt

def skeleton_total_length(skeleton):
    # Use total skeleton length as there are also curved cells
    # Skeletonise traces the object's medial axis
    skel_coords = np.column_stack(np.nonzero(skeleton)) # get all coordinates of skeleton
    G = nx.Graph()

    # Add nodes with coordinates as attributes
    for i, (y, x) in enumerate(skel_coords):
        G.add_node(i, pos=(y, x))
    # Build graph with pixel and coordinates as nodes

    # Connect nodes if neighbors
    for i, (y1, x1) in enumerate(skel_coords):
        for j in range(i + 1, len(skel_coords)):
            y2, x2 = skel_coords[j]
            dist = np.linalg.norm([y1 - y2, x1 - x2])
            if dist <= np.sqrt(2):  # adjacent pixel distance if diagonal (V(2)), 1 if next to each other
                G.add_edge(i, j, weight=dist)

    # Total skeleton length is sum of all edge weights
    total_length = sum(nx.get_edge_attributes(G, 'weight').values())
    return total_length


def run_segmentation_pipeline(basedir, model_name, chans, mask_threshold, 
                              flow_threshold, omni, diameter, invert, min_size, save_setting_text,
                              post_processing=False, boundary_thickness=None, area_thresh=None,
                              cutoff=None, output_folder=''):
    """
    This function consists of two main paths.
    1. The Omnipose segmentation algorithm + post-processing (if selected) and saving the results.
    2. Using the saved masks to extract cell measurements (label and area)
    
    Input: 
        - basedir: string
            filenames for input
        - model_name: string
            the model Omnipose will use for segmentation
        - chans: list
            specifying the channel parameters in the format [0, 0]
             - First channel for cytoplasm 
                 (0: grayscale, 1: red, 2: green, 3: blue)
             - Second channel for nucleus 
                 (0: no channel,  1: red, 2: green, 3: blue) 
        - mask_threshold: int
            Erode or dilate masks with higher or lower values 
            between -5 and 5 
            Decrease in case of too few masks or masks not convering the
            entire cell.
        - flow_threshold: int
            Only needed if there are spurious masks to clean up; 
            slows down output
            Increase in case of too many masks. 
            Decrease in case of too many spurious masks.
        - omni: bool
            Can turn off Omnipose mask reconstruction, not advised 
        - diameter: int
            parameter to set the diameter in pixels for the cells. 
            In case of 0, Omnipose determines it itself.
        - invert: bool
            parameter to invert the image
        - min_size: int
            parameter to set the minimum size of the masks in the amount of pixels for the masks
        - post_processing: bool
            parameter to enable or disable post-processing
        - boundary_thickness: int
            number of pixels of edge used for candidate masks for removal
        - area_thresh: int
            Remove boundary masks that are smaller than the defined area
        - cutoff = float
            Masks with overlap (0-1) with edge larger than the cutoff will be removed
        - save_setting_text: bool
            Save settings used in a separate txt-file
        - output_folder: directory where the masks and cell measurements are stored
        
    Output:
        - Masks: .tif files with the masks corresponding to the original image
        - Settings: .txt file with the defined settings (if save_setting_text=True)
        - CSV table: cell measurements and label corresponding to 
            the masks obtained by running Omnipose.
    
    """
    # Check GPU availability
    # This checks to see if a GPU is available for image processing.
    # CPU performance is slower.
    use_GPU = torch.cuda.is_available()
    if use_GPU == True:
        print("GPU will be used for the segmentation script.", )
    else:
        print("GPU is not available. Using CPU for the segmentation script.", )
    
    # ----------- Part 1: Omnipose Segmentation -----------
    
    # Print model selection
    print(f"Running Omnipose using: {model_name}", )
    
    # Provide directory to workflow
    image_files = basedir
    files = [os.path.join(output_folder, f) for f in image_files]
    
    # Select model and settings
    model = models.CellposeModel(gpu=use_GPU, model_type=model_name)
    
    imgs = [io.imread(f) for f in files] # Read in files as images
    
    n = range(len(imgs)) # Select all images for segmentation
    
    # Define parameters
    params = {'channels':chans,
              'rescale': None, # upscale or downscale your images, None = no rescaling 
              'mask_threshold': mask_threshold, 
              'flow_threshold': flow_threshold, 
              'transparency': True, # transparency in flow output
              'omni': omni, 
              'cluster': True, # use DBSCAN clustering
              'resample': True, # whether or not to run dynamics on rescaled grid or original grid 
              'verbose': False, # turn on if you want to see more output 
              'tile': False, # average the outputs from flipped (augmented) images; slower, usually not needed 
              'niter': None, # default None lets Omnipose calculate # of Euler iterations (usually <20) but you can tune it for over/under segmentation 
              'augment': False, # Can optionally rotate the image and average network outputs, usually not needed 
              'diameter': diameter, 
              'invert': invert, 
              'min_size': min_size 
             }
    
    # Run the segmentation
    tic = time.time() 
    masks, flows, styles = model.eval([imgs[i] for i in n],**params)
    net_time = time.time() - tic
    print('total segmentation time: {}s'.format(net_time), )
    
    # Post-processing
    # Clean up masks at the borders
    if post_processing == True:
        print("Post-processing the masks.", )
        masks_clean = []
        for mask in masks:
            masks_clean.append(clean_boundary(mask, boundary_thickness=boundary_thickness, area_thresh=area_thresh, cutoff=cutoff))
        masks = masks_clean
        

    # Create the directory if output folder does not exist
    os.makedirs(output_folder, exist_ok=True)

    # Save the segmented image
    io.save_masks(imgs, masks, flows, files, 
                  png=False,
                  tif=True, # whether to use PNG or TIF format
                  suffix='', # suffix to add to files if needed  (automatically adds _masks to original filename for saving)
                  save_flows=False, # saves both RGB depiction as *_flows.png and the raw components as *_dP.tif
                  save_outlines=False, # save outline images 
                  dir_above=0, # save output in the image directory or in the directory above (at the level of the image directory)
                  #in_folders=True, # save output in folders (recommended) (saves into a folder called masks)
                  savedir = output_folder, # Save masks in the defined output folder
                  save_txt=False, # txt file for outlines in imageJ
                  save_ncolor=False) # save ncolor version of masks for visualization and editing, instead of each mask its own color
    
    print(f"Masks saved under {output_folder}", )
    
    if save_setting_text == True:
        with open(os.path.join(output_folder, "settings.txt"), 'w') as file:
            file.write(f"basedir,{basedir}\n")
            file.write(f"output_folder,{output_folder}\n")
            file.write(f"mask_threshold,{mask_threshold}\n")
            file.write(f"flow_threshold,{flow_threshold}\n")
            file.write(f"model_name,{model_name}\n")
            file.write(f"channels,{chans}\n")
            file.write(f"diameter,{diameter}\n")
            file.write(f"min_size,{min_size}\n")
            file.write(f"omni (omnipose mask reconstruction),{omni}\n")
            file.write(f"invert,{invert}\n")
            file.write(f"post_processing,{post_processing}\n")
           # if post_processing == True:
            file.write(f"boundary_thickness,{boundary_thickness}\n")
            file.write(f"area_threshold,{area_thresh}\n")
            file.write(f"cutoff,{cutoff}\n")
        print(f"Settings saved under {output_folder}\settings.txt", )
    
    # ----------- Part 2: Extract Cell Measurements -----------
    
    # Analyse labeled images for measurements
    # Gets measurements from images already saved to disc
    print("Analysing cell sizes.", )
    
    images_path = output_folder
    
    for im in os.listdir(images_path):
        if im.endswith("_masks.tif"):  # Standard suffix added by Omnipose
            image_path = os.path.join(images_path, im)
            image = imread(image_path)  # Read in the image
    
            # Label the image
            label_img = label(image)
    
            # Extract label and area properties using regionprobs
            props = regionprops_table(
                label_img,
                properties=('label', 'area')
            )
    
            label_data = props["label"]
            area_data = props["area"]
    
            # Preparing CSV output
            filename_table = im[:-4] + "_table.csv" # Image name with suffix _table
            output_path = os.path.join(images_path, filename_table)
    
            with open(output_path, "w") as file:
                file.write("Label,Area,MeanWidth,MajorAxis,SkelLength,AvgLength\n")
    
                for i, label_nr in enumerate(label_data): # Loop over all labels obtained from regionprobs
                    # Create a binary mask for the current label
                    cell_mask = label_img == label_nr
    
                    # Skeletonize mask
                    skeleton = skeletonize(cell_mask)
    
                    # Euclidean distance transform and mean width
                    distance_map = distance_transform_edt(cell_mask)
                    widths = distance_map[skeleton] * 2
                    mean_width = np.mean(widths) if widths.size > 0 else 0
    
                    # Regionprobs major length extract
                    region = regionprops(cell_mask.astype(int))
                    major_len = region[0].major_axis_length if region else 0
    
                    # Skeleton length
                    total_skel_len = skeleton_total_length(skeleton)
    
                    # Averaged length
                    avg_length = (major_len + total_skel_len) / 2
    
                    # Write to file
                    line = f'{label_nr},{area_data[i]},{mean_width},{major_len},{total_skel_len},{avg_length}\n'
                    file.write(line)
                  
    print(f"Measurements saved under {output_folder}", )
    
    print("Segmentation is finished", )


    