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
import tkinter as tk
from tkinter import filedialog, messagebox
from set_parameters_sptPALM import set_parameters_sptPALM


def set_parameters_sptPALM_GUI(para = None):
    
    if para is None:
        para = set_parameters_sptPALM()
    
    # # Initialize empty input_parameter dictionary to be returned
    # input_parameter = {}
    
    # Function to create the GUI
    def browse_directory():
        dirname = filedialog.askdirectory()
        if dirname:
            data_dir_entry.delete(0, tk.END)
            data_dir_entry.insert(0, dirname)

    def browse_files():
        files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        if files:
            fn_locs_entry.delete(0, tk.END)
            fn_locs_entry.insert(0, ', '.join(files))

    def save_params_exit():
        nonlocal para
        # Collect all parameters from the GUI
        para = {
            'data_dir': data_dir_entry.get(),
            'default_output_dir': default_output_dir_entry.get(),
            'fn_locs': fn_locs_entry.get().split(', '),
            'fn_proc_brightfield': fn_proc_brightfield_entry.get(),
            'fn_csv_handle': fn_csv_handle_entry.get(),
            'fn_dict_handle': fn_dict_handle_entry.get(),
            'fn_diffs_handle': fn_diffs_handle_entry.get(),
            'fn_movies': fn_movies_entry.get(),
            'fn_combined_movies': fn_combined_movies_entry.get(),
            'condition_names': condition_names_entry.get().split(','),
            'condition_files': condition_files_entry.get().split(','),
            'pixelsize': float(pixelsize_entry.get()),
            'cellarea_pixels_min': int(cellarea_min_entry.get()),
            'cellarea_pixels_max': int(cellarea_max_entry.get()),
            'use_segmentations': use_segmentations_var.get(),
            'track_steplength_max': float(track_steplength_entry.get()),
            # 'track_memory': int(track_memory_entry.get()),
            # 'frametime': float(frametime_entry.get()),
            # 'loc_error': float(loc_error_entry.get()),
            # 'diff_hist_steps_min': int(diff_min_entry.get()),
            # 'diff_hist_steps_max': int(diff_max_entry.get()),
            # 'number_tracks_per_cell_min': int(tracks_min_entry.get()),
            # 'number_tracks_per_cell_max': int(tracks_max_entry.get()),
            # 'scta_vis_cells': scta_vis_cells_var.get(),
            # 'scta_plot_cell_window': int(scta_plot_window_entry.get()),
            # 'scta_vis_interactive': scta_vis_interactive_var.get(),
            # 'scta_vis_rangemax': float(scta_vis_rangemax_entry.get()),
            # 'plot_diff_hist_min': float(diff_hist_min_entry.get()),
            # 'plot_diff_hist_max': float(diff_hist_max_entry.get()),
            # 'binwidth': float(binwidth_entry.get()),
            'fontsize': int(fontsize_entry.get()),
            'linewidth': int(linewidth_entry.get()),
            'plot_norm_histograms': plot_hist_entry.get(),
            'plot_frame_number': use_plot_frame_number_var.get(),
            'dpi': int(dpi_entry.get()),
            'cmap_applied': cmap_entry.get()
        }

        root.quit()  # Exits the Tkinter event loop
        root.destroy()  # Destroys the Tkinter window

    root = tk.Tk()
    root.title("SPT-PALM Parameters")
    
    # Adjust the column configuration of the root window to split into two
    root.grid_columnconfigure(0, weight=1)  # First column gets full width (file_frame)
    root.grid_columnconfigure(1, weight=1)  # Second column (numeric_frame) gets half width
    
###################
    # Frame for File Selection and Directory Input
    file_frame = tk.LabelFrame(root, text="File & directory selection", padx=10, pady=10)
    file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=1)

    # Data Directory
    tk.Label(file_frame, text="Data directory").grid(row=0, column=0, sticky=tk.W)
    data_dir_entry = tk.Entry(file_frame, width=60)
    data_dir_entry.grid(row=0, column=1)
    data_dir_entry.insert(0, para['data_dir'])
    tk.Button(file_frame, text="Browse", command=browse_directory).grid(row=0, column=2)

    # File Names for Localizations
    tk.Label(file_frame, text="Localization file(s) (CSV)").grid(row=1, column=0, sticky=tk.W)
    fn_locs_entry = tk.Entry(file_frame, width=60)
    fn_locs_entry.grid(row=1, column=1)
    data_dir_entry.insert(0, para['fn_locs'])
    tk.Button(file_frame, text="Browse", command=browse_files).grid(row=1, column=2)

    # Brightfield Image Files
    tk.Label(file_frame, text="Brightfield image file(s)").grid(row=2, column=0, sticky=tk.W)
    fn_proc_brightfield_entry = tk.Entry(file_frame, width=60)
    fn_proc_brightfield_entry.grid(row=2, column=1)
    fn_proc_brightfield_entry.insert(0, para['fn_proc_brightfield'])
    tk.Button(file_frame, text="Browse", command=browse_files).grid(row=2, column=2)

    # Condition names
    tk.Label(file_frame, text="Condition names").grid(row=3, column=0, sticky=tk.W)
    condition_names_entry = tk.Entry(file_frame, width=60)
    condition_names_entry.grid(row=3, column=1)
    condition_names_entry.insert(0, para['condition_names'])

    # Condition files names
    tk.Label(file_frame, text="Condition files").grid(row=4, column=0, sticky=tk.W)
    condition_files_entry = tk.Entry(file_frame, width=60)
    condition_files_entry.grid(row=4, column=1)
    condition_files_entry.insert(0, para['condition_files'])
  
    # Default output Directory
    tk.Label(file_frame, text="Default output directory").grid(row=3, column=0, sticky=tk.W)
    default_output_dir_entry = tk.Entry(file_frame, width=60)
    default_output_dir_entry.grid(row=3, column=1)
    default_output_dir_entry.insert(0, para['default_output_dir'])

    # CSV File Handle
    tk.Label(file_frame, text="CSV handle").grid(row=4, column=0, sticky=tk.W)
    fn_csv_handle_entry = tk.Entry(file_frame, width=60)
    fn_csv_handle_entry.grid(row=4, column=1)
    fn_csv_handle_entry.insert(0, para['fn_csv_handle'])

    # fn_dict_handle Handle
    tk.Label(file_frame, text="Dictionary handle").grid(row=5, column=0, sticky=tk.W)
    fn_dict_handle_entry = tk.Entry(file_frame, width=60)
    fn_dict_handle_entry.grid(row=5, column=1)
    fn_dict_handle_entry.insert(0, para['fn_dict_handle'])

    # fn_dict_handle Handle
    tk.Label(file_frame, text="Diffusion coefficients handle").grid(row=6, column=0, sticky=tk.W)
    fn_diffs_handle_entry = tk.Entry(file_frame, width=60)
    fn_diffs_handle_entry.grid(row=6, column=1)
    fn_diffs_handle_entry.insert(0, para['fn_diffs_handle'])

    # fn_movies Handle    
    tk.Label(file_frame, text="Movies handle").grid(row=7, column=0, sticky=tk.W)
    fn_movies_entry = tk.Entry(file_frame, width=60)
    fn_movies_entry.grid(row=7, column=1)
    fn_movies_entry.insert(0, para['fn_movies'])

    # fn_combined_movies Handle    
    tk.Label(file_frame, text="Combined movies handle").grid(row=8, column=0, sticky=tk.W)
    fn_combined_movies_entry = tk.Entry(file_frame, width=60)
    fn_combined_movies_entry.grid(row=8, column=1)
    fn_combined_movies_entry.insert(0, para['fn_combined_movies'])


#####################
    # Frame for Numerical Inputs
    numeric_frame = tk.LabelFrame(root, text="Numerical Inputs", padx=10, pady=10)
    numeric_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Pixelsize
    tk.Label(numeric_frame, text="Pixel size (µm)").grid(row=0, column=0, sticky=tk.W)
    pixelsize_entry = tk.Entry(numeric_frame, width=10)
    pixelsize_entry.grid(row=0, column=1)
    pixelsize_entry.insert(0, para['pixelsize'])

    # Cell area (min/max)
    tk.Label(numeric_frame, text="Cell Area (Min Pixels)").grid(row=1, column=0, sticky=tk.W)
    cellarea_min_entry = tk.Entry(numeric_frame, width=10)
    cellarea_min_entry.grid(row=1, column=1)
    cellarea_min_entry.insert(0, para['cellarea_pixels_min'])

    tk.Label(numeric_frame, text="Cell Area (Max Pixels)").grid(row=1, column=2, sticky=tk.W)
    cellarea_max_entry = tk.Entry(numeric_frame, width=10)
    cellarea_max_entry.grid(row=1, column=3)
    cellarea_max_entry.insert(0, para['cellarea_pixels_max'])


    # # Frame for Numerical Inputs 2 - place it in the second column (1)
    # numeric_frame_2 = tk.LabelFrame(root, text="Numerical Inputs 2", padx=10, pady=10)
    # numeric_frame_2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # tk.Label(numeric_frame_2, text="Cell Area (Max Pixels)").grid(row=1, column=2, sticky=tk.W)
    # cellarea_max_entry = tk.Entry(numeric_frame, width=10)
    # cellarea_max_entry.grid(row=1, column=3)
    # cellarea_max_entry.insert(0, '500')


########################
    # Frame for Tracking and Segmentation
    tracking_frame = tk.LabelFrame(root, text="Tracking & Segmentation", padx=10, pady=10)
    tracking_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    # Use Segmentations
    use_segmentations_var = tk.BooleanVar(value = para['use_segmentations'])
    tk.Checkbutton(tracking_frame, text="Use Segmentations", variable=use_segmentations_var).grid(row=0, column=0, sticky=tk.W)

    # Track Steplength
    tk.Label(tracking_frame, text="Track Steplength (Max)").grid(row=1, column=0, sticky=tk.W)
    track_steplength_entry = tk.Entry(tracking_frame, width=10)
    track_steplength_entry.grid(row=1, column=1)
    track_steplength_entry.insert(0, para['track_steplength_max'])


########################
    # Frame for plotting
    plotting_frame = tk.LabelFrame(root, text="Plotting and data output", padx=10, pady=10)
    plotting_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        # # Parameters for plotting figures etc
        # 'fontsize': 10, # Default: 10
        # 'linewidth': 1, # Default: 1
        # 'plot_norm_histograms': 'probability', # Carefull: Matlab: choose either 'count' (default) | 'probability' | 'countdensity' | 'pdf' | 'cumcount' | 'cdf'
        # 'plot_frame_number': True, # Plot frame numbers next to the tracks in Plot_SingleCellTrackingAnalysis.m
        # 'dpi': 150, # DPI setting for plotting figures, default: 300
        # 'cmap_applied': 'gist_ncar', ##was: 'nipy_spectral', tab20c, 
  
    # fontsize
    tk.Label(plotting_frame, text="Font size (px)").grid(row=0, column=0, sticky=tk.W)
    fontsize_entry = tk.Entry(plotting_frame, width=10)
    fontsize_entry.grid(row=0, column=1)
    fontsize_entry.insert(0, para['fontsize'])   
    
    # linewidth
    tk.Label(plotting_frame, text="Line width (px_").grid(row=0, column=2, sticky=tk.W)
    linewidth_entry = tk.Entry(plotting_frame, width=10)
    linewidth_entry.grid(row=0, column=3)
    linewidth_entry.insert(0, para['linewidth'])  
    
    # dpi
    tk.Label(plotting_frame, text="Resolution figures (dpi)").grid(row=1, column=0, sticky=tk.W)
    dpi_entry = tk.Entry(plotting_frame, width=10)
    dpi_entry.grid(row=1, column=1)
    dpi_entry.insert(0, para['dpi'])  
    
    # Plot frame numbers next to tracks
    use_plot_frame_number_var = tk.BooleanVar(value=para['plot_frame_number'])
    tk.Checkbutton(plotting_frame, text="Plot frame numbers", variable=use_plot_frame_number_var).grid(row=1, column=2, sticky=tk.W)
   
    # Dropdown Menu for Colormap Selection
    tk.Label(plotting_frame, text="Select color map").grid(row=2, column=0, sticky=tk.W)
    # Create StringVar for dropdown selection
    selected_cmap = tk.StringVar()
    selected_cmap.set("gist_ncar")  # Default option
    # Create a dropdown menu
    cmap_entry = tk.OptionMenu(plotting_frame, selected_cmap, "gist_ncar", "nipy_spectral", "tab20c")
    # cmap_dropdown.config(width=10)
    cmap_entry.grid(row=2, column=1, sticky=tk.W)

    # Dropdown Menu for plotting diffusion histrograms Selection
    tk.Label(plotting_frame, text="Select plotting option (not active)").grid(row=2, column=2, sticky=tk.W)
    selected_cmap = tk.StringVar()
    selected_cmap.set("probability")  # Default option
    plot_hist_entry = tk.OptionMenu(plotting_frame, selected_cmap, "probability", "counts")
    plot_hist_entry.grid(row=2, column=3, sticky=tk.W)
   
    
#############################
    # Save and Exit buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=3, column=0, pady=10)

    tk.Button(button_frame, text="Save and Exit", command=save_params_exit).grid(row=0, column=0, padx=5)

    root.mainloop()

    # # # Return collected parameters after window closes
    return para



