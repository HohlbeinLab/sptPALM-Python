# -*- coding: utf-8 -*-
"""
Omnipose image segmentation using files.
Script to execute the Omnipose segmentation in the command line.
Starts up GUI for easier settings selection.

Uses OmniposeForCommand.py for actually running Omnipose.
Python libraries loaded in when executing the GUI, instead of each time the
script OmniposeForCommand.py is run.

Script does not allow for checking intermediate results.
To do so, need to drag _cp_masks.tif into an image viewer, e.g. Fiji/ImageJ
Then change settings and run segmentation again and check until satisfied 
with the results.
"""

import tkinter as tk
from tkinter import filedialog, ttk
import os
import numpy as np

# Importing OmniposeForCommand pulls in torch + omnipose, which is slow on first
# launch (tens of seconds) and shows a spinning cursor. Announce it so the calling
# terminal isn't mistaken for a hang.
print("Loading Omnipose libraries (torch, omnipose) — this can take a while on first launch...", flush=True)
from OmniposeForCommand import run_segmentation_pipeline
print("Omnipose libraries loaded. Opening the segmentation GUI...", flush=True)

import argparse
import json


# Define trained models here for dropdown menu
MODEL_OPTIONS = [
    "bact_phase_omni",
    "bact_fluor_omni", 
    "cyto2_omni", 
    "worm_omni",
]

def browse_directory(var):
    dirname = filedialog.askdirectory()
    if dirname:
        var.set(dirname)  # Set the selected directory to the provided variable

def run_pipeline():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", required=True, help="JSON list of files to segment")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--min_size", required=True, type=int, help="Minimum mask size")
    
    args = parser.parse_args()
    
    # Deserialize JSON string to Python list
    files_to_segment = json.loads(args.files)
    output_dir = args.output
    min_size = args.min_size
    
    # For tracking segmentation
    with open(os.path.join(output_dir, "segmentation_done.txt"), "w") as f:
        f.write("None")
    
    
    model_name = model_var.get()


    try:
        chans = [int(chan1_var.get()), int(chan2_var.get())]
        for chan in chans:
            if not (0 <= chan <= 3): 
                raise ValueError("Channels must be an integer between 0 and 3.")
                print("Error: Channels must be an integer between 0 and 3.")
    except ValueError:
        message_var.set("Error: Channels must be integers.")
        message_label.config(fg="red")
        print("Error: Channels must be integers")
        return

    try:
        mask_threshold = float(mask_thresh_var.get())
        flow_threshold = float(flow_thresh_var.get())
        diameter = int(diameter_var.get())

    except ValueError:
        message_var.set("Error: Thresholds, diameter, and min size must be numeric.")
        print("Error: Thresholds, diameter, and min size must be numeric.")
        message_label.config(fg="red")
        return
    
    post_processing = post_processing_var.get()
    # In case post_processing is selected, check whether the inputs are allowed
    if post_processing == True:
        try:
            boundary_thickness = int(boundary_thickness_var.get())
        except (ValueError, TypeError):
            message_var.set("Error: Boundary thickness must be an integer.")
            message_label.config(fg="red")
            print("Error: Boundary thickness must be an integer.")
            return
            
        try:
            area_thresh_val = area_thresh_var.get()
            if str(area_thresh_val).strip().lower() in ("inf", "infinity", "np.inf"):
                area_thresh = np.inf
            else:
                area_thresh = int(area_thresh_val)
        except (ValueError, TypeError):
            message_var.set("Error: Area threshold is not an integer or np.inf.")
            message_label.config(fg="red")
            print("Error: Area threshold is not an integer or np.inf.")
            return
        
        try:
            cutoff = float(cutoff_var.get())
        except ValueError:
            message_var.set("Error: Cutoff is not a float.")
            message_label.config(fg="red")
            print("Error: Cutoff is not a float")
            return

    # In case post_processing is not selected, define variables as None
    else:
         boundary_thickness = None
         area_thresh = None
         cutoff = None    

    omni = omni_var.get()
    invert = invert_var.get()
    save_setting_text = save_setting_text_var.get()

    message_var.set("Running segmentation... (window will be unresponsive until done)")
    message_label.config(fg="black")
    # Force the GUI to repaint the status message BEFORE the blocking call below.
    # run_segmentation_pipeline() runs on this (main) thread, so the window cannot
    # process events while it works and macOS shows a spinning beachball. Painting
    # first makes clear it is busy, not hung.
    root.update_idletasks()

    run_segmentation_pipeline(
        basedir=files_to_segment, model_name=model_name, chans=chans, mask_threshold=mask_threshold,
        flow_threshold=flow_threshold, omni=omni, diameter=diameter, invert=invert, 
        min_size=min_size,
        boundary_thickness=boundary_thickness, area_thresh=area_thresh, cutoff=cutoff, 
        save_setting_text=save_setting_text, post_processing=post_processing, output_folder=output_dir)


    message_var.set("Segmentation completed successfully.")
    message_label.config(fg="green")
    
    # to keep track whether segmentation is finished
    with open(os.path.join(output_dir, "segmentation_done.txt"), "w") as f:
        f.write("success")

# Main window
root = tk.Tk()
root.title("Omnipose Segmentation (sptPALM)")
# No fixed geometry and no hardcoded fonts/colours: the window auto-sizes to its
# contents and uses the system default font, matching the Set Parameters GUI.
root.resizable(True, True)

# Variables
#basedir_var = tk.StringVar()
#outputdir_var = tk.StringVar()
model_var = tk.StringVar(value=MODEL_OPTIONS[0])
chan1_var = tk.StringVar(value="0")
chan2_var = tk.StringVar(value="0")
mask_thresh_var = tk.StringVar(value="0")
flow_thresh_var = tk.StringVar(value="0")
diameter_var = tk.StringVar(value="0")

omni_var = tk.BooleanVar(value=True)
invert_var = tk.BooleanVar(value=True)
boundary_thickness_var = tk.StringVar(value=1)
area_thresh_var = tk.StringVar(value='np.inf')
cutoff_var = tk.StringVar(value=0)
save_setting_text_var = tk.BooleanVar(value=True)
post_processing_var = tk.BooleanVar(value=False)

# Message Frame
message_var = tk.StringVar()
message_label = tk.Label(root, textvariable=message_var)
message_label.pack(pady=0
                   )

# Main Frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=18)

# Base Directory Frame

# Model Frame
model_frame = tk.Frame(main_frame)
model_frame.grid(row=2, column=0, sticky="w", pady=8)
tk.Label(model_frame, text="Model").grid(row=0, column=0, sticky="w", padx=5)
ttk.Combobox(model_frame, textvariable=model_var, values=MODEL_OPTIONS, width=47).grid(row=0, column=1, padx=5)

# Channel Frame
channel_frame = tk.Frame(main_frame)
channel_frame.grid(row=3, column=0, sticky="w", pady=8)
tk.Label(channel_frame, text="Channel 1").grid(row=0, column=0, sticky="w", padx=4)
tk.Entry(channel_frame, textvariable=chan1_var, width=10).grid(row=0, column=1, padx=5)
tk.Label(channel_frame, text="Channel 2").grid(row=0, column=2, sticky="w", padx=4)
tk.Entry(channel_frame, textvariable=chan2_var, width=10).grid(row=0, column=3, padx=5)
channel_frame.grid_columnconfigure(0, weight=1)
channel_frame.grid_columnconfigure(1, weight=1)
channel_frame.grid_columnconfigure(2, weight=1)
channel_frame.grid_columnconfigure(3, weight=1)
tk.Label(channel_frame,
         text="Select Channel 1 = 0, Channel 2 = 0 for gray-scale images.\n"
              "Use Channel 1 for the cytoplasm channel: 1,2,3 for red, green, blue.\n"
              "Use Channel 2 for the nuclear channel: 1,2,3 for red, green, blue.", justify="left").grid(
    row=1, column=0, columnspan=4, sticky="w", padx=(28, 5), pady=1
)
             
# Parameter Frame
param_frame = tk.Frame(main_frame)
param_frame.grid(row=4, column=0, sticky="w", pady=3)

# Mask Threshold frame
tk.Label(param_frame, text="Mask Threshold").grid(row=0, column=0, sticky="w", padx=5)
tk.Entry(param_frame, textvariable=mask_thresh_var, width=10).grid(row=0, column=1, padx=5)
tk.Label(param_frame, text="Erode or dilate masks with respectively higher or lower values between -5 and 5.\n"
         "Decrease this threshold if you are getting too few masks or if masks do not cover the entire cell.", justify="left").grid(row=1, column=0, columnspan=4, sticky="w", padx=(28, 5), pady=3)

# Flow Threshold Frame
tk.Label(param_frame, text="Flow Threshold").grid(row=2, column=0, sticky="w", padx=5)
tk.Entry(param_frame, textvariable=flow_thresh_var, width=10).grid(row=2, column=1, padx=5)
tk.Label(param_frame, 
         text="Only needed if there are spurious masks to clean up; slows down output.\n"
         "Increase in case of too many masks. Decrease in case of too many spurious masks.", justify="left").grid(row=3, column=0, columnspan=3, sticky="w", padx=(28, 5), pady=3)

# Diameter Frame
tk.Label(param_frame, text="Diameter").grid(row=4, column=0, sticky="w", padx=5)
tk.Entry(param_frame, textvariable=diameter_var, width=10).grid(row=4, column=1, padx=5)
tk.Label(param_frame, text="Select 0 for automatic determination or put in cell diameter in pixels.").grid(row=5, column=0, columnspan=3, sticky="w", padx=(28, 5), pady=3)

# Min Size Frame

# Options Frame
options_frame = tk.Frame(main_frame)
options_frame.grid(row=5, column=0, sticky="w", pady=3)

# left side
left_options_frame = tk.Frame(options_frame)
left_options_frame.grid(row=0, column=0, sticky="nw")

tk.Checkbutton(left_options_frame, text="Omnipose mask reconstruction (advised)", variable=omni_var).grid(row=0, column=0, sticky="w", padx=5)
tk.Checkbutton(left_options_frame, text="Invert Image", variable=invert_var).grid(row=1, column=0, sticky="w", padx=5)
tk.Checkbutton(left_options_frame, text="Save settings in a txt file", variable=save_setting_text_var).grid(row=2, column=0, sticky="w", padx=5)
# Run button
# NOTE: macOS renders tk.Button with the native grey background and ignores bg,
# so fg="white" made the label invisible (white on grey). Use black text.
tk.Button(left_options_frame, text="Run Segmentation", command=run_pipeline,
          fg="black", width=20).grid(row=3, column=0, pady=10, padx=5)

# Post-processing Frame
right_params_frame = tk.Frame(options_frame, highlightbackground="black", highlightthickness=1)
right_params_frame.grid(row=0, column=1, sticky="nw", padx=10)
tk.Checkbutton(right_params_frame, text="Post-processing", variable=post_processing_var).grid(row=0, column=0, columnspan=2, sticky="w", pady=3)

tk.Label(right_params_frame, text="Boundary Thickness: edge width.\nArea: remove boundary masks smaller than this.\nCutoff (0-1): remove masks with ≥ X% edge pixels.\nTo remove all boundary masks: area: np.inf, cutoff: 0.", justify="left").grid(row=1, column=0, columnspan=2, sticky="w", pady=0)

tk.Label(right_params_frame, text="Boundary Thickness").grid(row=2, column=0, sticky="w", pady=2)
tk.Entry(right_params_frame, textvariable=boundary_thickness_var, width=10).grid(row=2, column=1, pady=2)

tk.Label(right_params_frame, text="Area Threshold").grid(row=3, column=0, sticky="w", pady=2)
tk.Entry(right_params_frame, textvariable=area_thresh_var, width=10).grid(row=3, column=1, pady=2)

tk.Label(right_params_frame, text="Cutoff").grid(row=4, column=0, sticky="w", pady=10)
tk.Entry(right_params_frame, textvariable=cutoff_var, width=10).grid(row=4, column=1, pady=10)

# Start the GUI loop
root.mainloop()
