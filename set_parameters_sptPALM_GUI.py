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
from tkinter import filedialog
from set_parameters_sptPALM import set_parameters_sptPALM
from ast import literal_eval # Safely parse the string back to a list of lists
import pickle

def set_parameters_sptPALM_GUI(para = None):
    print('\nRun set_parameters_sptPALM_GUI.py')
    if para is None:
        print(" re-run set_parameters_sptPALM")
        para = set_parameters_sptPALM()
      
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

    def load_params(): #careful, we need to overwrite all default parameters
        filename = filedialog.askopenfilename(
                                    filetypes = [("pickle file", "*.pkl")],
                                    title = "Select *.pkl file from sptPALM_analyse_movies.py")
        if filename:
            with open(filename, 'rb') as f:
                new_para = pickle.load(f)
                print("Input parameters loaded")
                    
            # Update the entries with the newly loaded parameters
            data_dir_entry.delete(0, tk.END)
            data_dir_entry.insert(0, new_para['data_dir'])
    
            fn_locs_entry.delete(0, tk.END)
            fn_locs_entry.insert(0, ', '.join(map(str, new_para['fn_locs'])))
    
            fn_proc_brightfield_entry.delete(0, tk.END)
            fn_proc_brightfield_entry.insert(0, ', '.join(map(str, new_para['fn_proc_brightfield'])))
    
            condition_names_entry.delete(0, tk.END)
            condition_names_entry.insert(0, ', '.join(map(str, new_para['condition_names'])))
    
            condition_files_entry.delete(0, tk.END)
            condition_files_entry.insert(0, ', '.join(map(str, new_para['condition_files'])))
    
            copynumber_intervals_entry.delete(0, tk.END)
            copynumber_intervals_entry.insert(0, ', '.join(map(str, new_para['copynumber_intervals'])))
    
            default_output_dir_entry.delete(0, tk.END)
            default_output_dir_entry.insert(0, new_para['default_output_dir'])
    
            fn_csv_handle_entry.delete(0, tk.END)
            fn_csv_handle_entry.insert(0, new_para['fn_csv_handle'])
    
            fn_dict_handle_entry.delete(0, tk.END)
            fn_dict_handle_entry.insert(0, new_para['fn_dict_handle'])
    
            fn_diffs_handle_entry.delete(0, tk.END)
            fn_diffs_handle_entry.insert(0, new_para['fn_diffs_handle'])
    
            fn_movies_entry.delete(0, tk.END)
            fn_movies_entry.insert(0, new_para['fn_movies'])
    
            fn_combined_movies_entry.delete(0, tk.END)
            fn_combined_movies_entry.insert(0, new_para['fn_combined_movies'])
    
            pixelsize_entry.delete(0, tk.END)
            pixelsize_entry.insert(0, new_para['pixelsize'])
    
            cellarea_min_entry.delete(0, tk.END)
            cellarea_min_entry.insert(0, new_para['cellarea_pixels_min'])
    
            cellarea_max_entry.delete(0, tk.END)
            cellarea_max_entry.insert(0, new_para['cellarea_pixels_max'])
    
            number_tracks_per_cell_min_entry.delete(0, tk.END)
            number_tracks_per_cell_min_entry.insert(0, new_para['number_tracks_per_cell_min'])
    
            number_tracks_per_cell_max_entry.delete(0, tk.END)
            number_tracks_per_cell_max_entry.insert(0, new_para['number_tracks_per_cell_max'])
    
            frametime_entry.delete(0, tk.END)
            frametime_entry.insert(0, new_para['frametime'])
    
            loc_error_entry.delete(0, tk.END)
            loc_error_entry.insert(0, new_para['loc_error'])
    
            track_steplength_entry.delete(0, tk.END)
            track_steplength_entry.insert(0, new_para['track_steplength_max'])
    
            track_memory_entry.delete(0, tk.END)
            track_memory_entry.insert(0, new_para['track_memory'])
    
            diff_hist_steps_min_entry.delete(0, tk.END)
            diff_hist_steps_min_entry.insert(0, new_para['diff_hist_steps_min'])
    
            diff_hist_steps_max_entry.delete(0, tk.END)
            diff_hist_steps_max_entry.insert(0, new_para['diff_hist_steps_max'])
    
            tracklength_locs_min_entry.delete(0, tk.END)
            tracklength_locs_min_entry.insert(0, new_para['tracklength_locs_min'])
    
            tracklength_locs_max_entry.delete(0, tk.END)
            tracklength_locs_max_entry.insert(0, new_para['tracklength_locs_max'])
    
            diff_hist_min_entry.delete(0, tk.END)
            diff_hist_min_entry.insert(0, new_para['plot_diff_hist_min'])
    
            diff_hist_max_entry.delete(0, tk.END)
            diff_hist_max_entry.insert(0, new_para['plot_diff_hist_max'])
    
            binwidth_entry.delete(0, tk.END)
            binwidth_entry.insert(0, new_para['binwidth'])
    
            fontsize_entry.delete(0, tk.END)
            fontsize_entry.insert(0, new_para['fontsize'])
    
            dpi_entry.delete(0, tk.END)
            dpi_entry.insert(0, new_para['dpi'])
    
            linewidth_entry.delete(0, tk.END)
            linewidth_entry.insert(0, new_para['linewidth'])
    
            use_segmentations_var.set(new_para['use_segmentations'])
            plot_norm_histograms_var.set(new_para['plot_norm_histograms'])
            use_plot_frame_number_var.set(new_para['plot_frame_number'])
            scta_vis_cells_var.set(new_para['scta_vis_cells'])
            scta_vis_interactive_var.set(new_para['scta_vis_interactive'])
            cmap_applied_var.set(new_para['cmap_applied'])
            
            scta_plot_cell_window_entry.delete(0, tk.END)
            scta_plot_cell_window_entry.insert(0, new_para['scta_plot_cell_window'])
    
            scta_vis_rangemax_entry.delete(0, tk.END)
            scta_vis_rangemax_entry.insert(0, new_para['scta_vis_rangemax'])              
                
        else:
            raise ValueError("No file selected!")

    def exit_GUI():
        root.quit()  # Exits the Tkinter event loop
        root.destroy()  # Destroys the Tkinter window
    
    def save_params():
        nonlocal para
        # Collect all parameters from the GUI
        para = {
            # File and directory selection
            'data_dir': data_dir_entry.get(),
            'default_output_dir': default_output_dir_entry.get(),
            'fn_locs': list(map(str.strip, fn_locs_entry.get().split(','))),
            'fn_proc_brightfield': list(map(str.strip, fn_proc_brightfield_entry.get().split(','))),
            
            'condition_names': list(map(str.strip, condition_names_entry.get().split(','))),
            'condition_files': literal_eval(f'[{condition_files_entry.get()}]'),  # Wrap with [] to make it a valid list of lists
            'copynumber_intervals': literal_eval(f'[{copynumber_intervals_entry.get()}]'),
           
            'fn_csv_handle': fn_csv_handle_entry.get(),
            'fn_dict_handle': fn_dict_handle_entry.get(),
            'fn_diffs_handle': fn_diffs_handle_entry.get(),
            'fn_movies': fn_movies_entry.get(),    
            'fn_combined_movies': fn_combined_movies_entry.get(),
            
            # Pixelsize and segmentation
            'pixelsize': float(pixelsize_entry.get()),
            'cellarea_pixels_min': int(cellarea_min_entry.get()),
            'cellarea_pixels_max': int(cellarea_max_entry.get()),
            'use_segmentations': use_segmentations_var.get(),
            'track_steplength_max': float(track_steplength_entry.get()),
            'track_memory': int(track_memory_entry.get()),
            'frametime': float(frametime_entry.get()),
            'loc_error': float(loc_error_entry.get()),
            'diff_hist_steps_min': int(diff_hist_steps_min_entry.get()),
            'diff_hist_steps_max': int(diff_hist_steps_max_entry.get()),
            'tracklength_locs_min': int(tracklength_locs_min_entry.get()),
            'tracklength_locs_max': int(tracklength_locs_max_entry.get()),
            
            'number_tracks_per_cell_min': int(number_tracks_per_cell_min_entry.get()),
            'number_tracks_per_cell_max': int(number_tracks_per_cell_max_entry.get()),
            
            'scta_vis_cells': scta_vis_cells_var.get(),
            'scta_plot_cell_window': int(scta_plot_cell_window_entry.get()),
            'scta_vis_interactive': scta_vis_interactive_var.get(),
            'scta_vis_rangemax': float(scta_vis_rangemax_entry.get()),
            'plot_diff_hist_min': float(diff_hist_min_entry.get()),
            'plot_diff_hist_max': float(diff_hist_max_entry.get()),
            'binwidth': float(binwidth_entry.get()),
            'fontsize': int(fontsize_entry.get()),
            'linewidth': int(linewidth_entry.get()),
            'plot_norm_histograms': plot_norm_histograms_var.get(),
            'plot_frame_number': use_plot_frame_number_var.get(),
            'dpi': int(dpi_entry.get()),
            'cmap_applied': cmap_applied_var.get()
        }
        # # Initialize Tkinter root window
        # root = tk.Tk()
        # root.withdraw()  # Hide the root window
        
        # Ask the user where to save the file, default filename is input_parameter.pkl
        save_file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            initialdir=para['data_dir'],  # Set the initial directory if provided
            filetypes=[("Pickle files", "*.pkl")],
            initialfile="input_parameter.pkl",
            title="Save input_parameter as"
        )
        
        if save_file_path:  # If the user selects a file path
            with open(save_file_path, 'wb') as file:
                pickle.dump(para, file)  # Save the dictionary to the file
            print(f"input_parameter saved to {save_file_path}")
        else:
            print("Save operation canceled.")
        
    root = tk.Tk()
    root.title("SPT-PALM Parameter GUI (defaults imported from set_parameter_sptPALM.py)")
    
    # Adjust the column configuration of the root window to split into two
    root.grid_columnconfigure(0, weight=1)  # First column gets full width (file_frame)
    root.grid_columnconfigure(1, weight=1)  # Second column (numeric_frame) gets half width
    
    # Create two separate container frames for left and right columns
    left_frame = tk.Frame(root)
    left_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")  # Left half

    right_frame = tk.Frame(root)
    right_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")  # Right half
    
    """
    # Frame for File Selection and Directory Input
    """

    file_frame = tk.LabelFrame(root, text="File & directory selection", padx=10, pady=10)
    file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
    width_text_labels = 20
    width_text_fileIO = 95
    width_text_box = 8
    
    row_index = 0;
    # Data Directory
    tk.Label(file_frame, text="Data directory", width = width_text_labels, 
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    data_dir_entry = tk.Entry(file_frame, width=width_text_fileIO)
    data_dir_entry.grid(row=row_index, column=1)
    data_dir_entry.insert(0, para['data_dir'])
    tk.Button(file_frame, text="Browse...", command=browse_directory).grid(row=row_index, column=2)

    row_index+=1
    # File Names for Localizations
    tk.Label(file_frame, text="Localization file(s) (*.csv)", width = width_text_labels,
             anchor="w").grid(row=1, column=0, sticky=tk.W)
    fn_locs_entry = tk.Entry(file_frame, width=width_text_fileIO)
    fn_locs_entry.grid(row=1, column=1)
    fn_locs_entry.insert(0, ', '.join(map(str, para['fn_locs'])))   
    tk.Button(file_frame, text="Browse...", command=browse_files).grid(row=1, column=2)

    row_index+=1
    # Brightfield Image Files
    tk.Label(file_frame, text="Brightfield image file(s) (*.tiff)", width = width_text_labels,
             anchor="w").grid(row=2, column=0, sticky=tk.W)
    fn_proc_brightfield_entry = tk.Entry(file_frame, width=width_text_fileIO)
    fn_proc_brightfield_entry.grid(row=2, column=1)
    fn_proc_brightfield_entry.insert(0, ', '.join(map(str, para['fn_proc_brightfield'])))
    tk.Button(file_frame, text="Browse...", command=browse_files).grid(row=2, column=2)

    row_index+=1
    # Name of conditions
    tk.Label(file_frame, text="Name of conditions", width = width_text_labels,
             anchor="w").grid(row=3, column=0, sticky=tk.W)
    condition_names_entry = tk.Entry(file_frame, width=width_text_fileIO)
    condition_names_entry.grid(row=3, column=1)
    # condition_names_entry.insert(0, para['condition_names'])
    condition_names_entry.insert(0, ', '.join(map(str, para['condition_names'])))

    row_index+=1
    # Condition files
    tk.Label(file_frame, text="Condition files", width = width_text_labels,
             anchor="w").grid(row=4, column=0, sticky=tk.W)
    condition_files_entry = tk.Entry(file_frame, width=width_text_fileIO)
    condition_files_entry.grid(row=4, column=1)
    # condition_files_entry.insert(0, para['condition_files'])
    condition_files_entry.insert(0, ', '.join(map(str, para['condition_files'])))

    row_index+=1    
    # Histogramming of diffusion coefficients per copynumber
    tk.Label(file_frame, text="Copy number intervals", width = width_text_labels,
             anchor="w").grid(row=5, column=0, sticky=tk.W)
    copynumber_intervals_entry = tk.Entry(file_frame, width=width_text_fileIO)
    copynumber_intervals_entry.grid(row=5, column=1)
    # condition_files_entry.insert(0, para['condition_files'])
    copynumber_intervals_entry.insert(0, ', '.join(map(str, para['copynumber_intervals'])))

    row_index+=1    
    # Handle: output directory
    tk.Label(file_frame, text="Handle: output directory", width = width_text_labels,
             anchor="w").grid(row=6, column=0, sticky=tk.W)
    default_output_dir_entry = tk.Entry(file_frame, width=width_text_fileIO)
    default_output_dir_entry.grid(row=6, column=1)
    default_output_dir_entry.insert(0, para['default_output_dir'])

    row_index+=1
    # Handle: CSV File 
    tk.Label(file_frame, text="Handle: csv files", width = width_text_labels,
             anchor="w").grid(row=7, column=0, sticky=tk.W)
    fn_csv_handle_entry = tk.Entry(file_frame, width=width_text_fileIO)
    fn_csv_handle_entry.grid(row=7, column=1)
    fn_csv_handle_entry.insert(0, para['fn_csv_handle'])

    row_index+=1
    # Handle: fn_dict_handle 
    tk.Label(file_frame, text="Handle: dictionary ", width = width_text_labels,
             anchor="w").grid(row=8, column=0, sticky=tk.W)
    fn_dict_handle_entry = tk.Entry(file_frame, width=width_text_fileIO)
    fn_dict_handle_entry.grid(row=8, column=1)
    fn_dict_handle_entry.insert(0, para['fn_dict_handle'])

    row_index+=1
    # Handle: fn_diffs_handle 
    tk.Label(file_frame, text="Handle: diffusion coeff. ", width = width_text_labels,
             anchor="w").grid(row=9, column=0, sticky=tk.W)
    fn_diffs_handle_entry = tk.Entry(file_frame, width=width_text_fileIO)
    fn_diffs_handle_entry.grid(row=9, column=1)
    fn_diffs_handle_entry.insert(0, para['fn_diffs_handle'])

    row_index+=1
    # Handle: fn_movies     
    tk.Label(file_frame, text="Handle: movies", width = width_text_labels,
             anchor="w").grid(row=10, column=0, sticky=tk.W)
    fn_movies_entry = tk.Entry(file_frame, width=width_text_fileIO)
    fn_movies_entry.grid(row=10, column=1)
    fn_movies_entry.insert(0, para['fn_movies'])

    row_index+=1
    # Handle: fn_combined_movies     
    tk.Label(file_frame, text="Handle: combined-movies", width = width_text_labels,
             anchor="w").grid(row=11, column=0, sticky=tk.W)
    fn_combined_movies_entry = tk.Entry(file_frame, width=width_text_fileIO)
    fn_combined_movies_entry.grid(row=11, column=1)
    fn_combined_movies_entry.insert(0, para['fn_combined_movies'])

    """
    # Frame for Segmentation inputs
    """

    segmentation_frame = tk.LabelFrame(left_frame, text="Pixelsize and segmentation", padx=10, pady=10)
    segmentation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")
   
    row_index = 0
    # Pixelsize
    tk.Label(segmentation_frame, text="Pixel size (µm)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    pixelsize_entry = tk.Entry(segmentation_frame, width=width_text_box)
    pixelsize_entry.grid(row=row_index, column=1)
    pixelsize_entry.insert(1, para['pixelsize'])

    # Use Segmentations
    use_segmentations_var = tk.BooleanVar(value = para['use_segmentations'])
    tk.Checkbutton(segmentation_frame, text="Use segmentations", variable=use_segmentations_var,
                   width = width_text_labels, anchor="w").grid(row=row_index, column=2, sticky=tk.W)

    row_index+=1
    # Cell area (min/max)
    tk.Label(segmentation_frame, text="Min. cell area (pixels)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    cellarea_min_entry = tk.Entry(segmentation_frame, width=width_text_box)
    cellarea_min_entry.grid(row=row_index, column=1)
    cellarea_min_entry.insert(0, para['cellarea_pixels_min'])


    tk.Label(segmentation_frame, text="Max. cell area (pixels)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    cellarea_max_entry = tk.Entry(segmentation_frame, width=width_text_box)
    cellarea_max_entry.grid(row=row_index, column=3)
    cellarea_max_entry.insert(0, para['cellarea_pixels_max'])
    
    row_index+=1
    # Minimum number of steps per track
    tk.Label(segmentation_frame, text="Min. number tracks/cell", width = width_text_labels,
             anchor="w").grid(row=2, column=0, sticky=tk.W)
    number_tracks_per_cell_min_entry = tk.Entry(segmentation_frame, width=width_text_box)
    number_tracks_per_cell_min_entry.grid(row=2,  column=1)
    number_tracks_per_cell_min_entry.insert(0, para['number_tracks_per_cell_min'])
    
    # Maximum number of steps per track
    tk.Label(segmentation_frame, text="Max. number tracks/cell", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    number_tracks_per_cell_max_entry = tk.Entry(segmentation_frame, width=width_text_box)
    number_tracks_per_cell_max_entry.grid(row=row_index, column=3)
    number_tracks_per_cell_max_entry.insert(0, para['number_tracks_per_cell_max'])

    """
    # Frame for Tracking inputs 
    """
  
    tracking_frame = tk.LabelFrame(left_frame, text="Tracking and diffusion analysis",
                                   padx=10, pady=10)
    tracking_frame.grid(row=2, column=0, padx=10, pady=10, sticky="new")

    row_index = 0
    # Frame time (sec)
    tk.Label(tracking_frame, text="Frame time (sec)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    frametime_entry = tk.Entry(tracking_frame, width=width_text_box)
    frametime_entry.grid(row=row_index, column=1)
    frametime_entry.insert(0, para['frametime'])   
    
    # Localisation error
    tk.Label(tracking_frame, text="Loc. error (µm)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    loc_error_entry = tk.Entry(tracking_frame, width=width_text_box)
    loc_error_entry.grid(row=row_index, column=3)
    loc_error_entry.insert(0, para['loc_error'])

    row_index+=1
    # Track steplength
    tk.Label(tracking_frame, text="Max. steplength (µm)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    track_steplength_entry = tk.Entry(tracking_frame, width=width_text_box)
    track_steplength_entry.grid(row=row_index, column=1)
    track_steplength_entry.insert(0, para['track_steplength_max'])

    # Track memory
    tk.Label(tracking_frame, text="Track memory (frames)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    track_memory_entry = tk.Entry(tracking_frame, width=width_text_box)
    track_memory_entry.grid(row=row_index, column=3)
    track_memory_entry.insert(0, para['track_memory'])

    row_index+=1
    # Minimum number of steps per track
    tk.Label(tracking_frame, text="Min. number steps", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    diff_hist_steps_min_entry = tk.Entry(tracking_frame, width=width_text_box)
    diff_hist_steps_min_entry.grid(row=row_index,  column=1)
    diff_hist_steps_min_entry.insert(0, para['diff_hist_steps_min'])
    
    # Maximum number of steps per track
    tk.Label(tracking_frame, text="Max. number steps", width = width_text_labels,
             anchor="w").grid(row=2, column=2, sticky=tk.W)
    diff_hist_steps_max_entry = tk.Entry(tracking_frame, width=width_text_box)
    diff_hist_steps_max_entry.grid(row=2, column=3)
    diff_hist_steps_max_entry.insert(0, para['diff_hist_steps_max'])    
 
    row_index+=1
    # Min locks per track
    tk.Label(tracking_frame, text="Min number locs per track", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    tracklength_locs_min_entry = tk.Entry(tracking_frame, width=width_text_box)
    tracklength_locs_min_entry.grid(row=row_index, column=1)
    tracklength_locs_min_entry.insert(0, para['tracklength_locs_min'])   
                
    # Max locks per track  
    tk.Label(tracking_frame, text="Min number locs per track", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    tracklength_locs_max_entry = tk.Entry(tracking_frame, width=width_text_box)
    tracklength_locs_max_entry.grid(row=row_index, column=3)
    tracklength_locs_max_entry.insert(0, para['tracklength_locs_max'])   
               
 
    """
    # Frame for plotting
    """
    plotting_frame = tk.LabelFrame(right_frame, text="Plotting and data output", padx=10, pady=10)
    plotting_frame.grid(row=1, column=1, padx=10, pady=10, sticky="new")  # Right half

    row_index = 0    
    # plot_diff_hist_min
    tk.Label(plotting_frame, text="Diff. hist. min (µm^2/s)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    diff_hist_min_entry = tk.Entry(plotting_frame, width=width_text_box)
    diff_hist_min_entry.grid(row=row_index, column=1)
    diff_hist_min_entry.insert(0, para['plot_diff_hist_min'])  

    # plot_diff_hist_max
    tk.Label(plotting_frame, text="Diff. hist. max (µm^2/s)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    diff_hist_max_entry = tk.Entry(plotting_frame, width=width_text_box)
    diff_hist_max_entry.grid(row=row_index, column=3)
    diff_hist_max_entry.insert(0, para['plot_diff_hist_max'])  
    
    row_index+=1
    # Binwidth
    tk.Label(plotting_frame, text="Binwith histograms", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    binwidth_entry = tk.Entry(plotting_frame, width=width_text_box)
    binwidth_entry.grid(row=row_index, column=1)
    binwidth_entry.insert(0, para['binwidth'])  
    
    # fontsize
    tk.Label(plotting_frame, text="Font size (px)", width = width_text_labels, 
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    fontsize_entry = tk.Entry(plotting_frame, width=width_text_box)
    fontsize_entry.grid(row=row_index, column=3)
    fontsize_entry.insert(0, para['fontsize'])   
  
    row_index+=1
    # dpi
    tk.Label(plotting_frame, text="Resolution figus (dpi)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    dpi_entry = tk.Entry(plotting_frame, width=width_text_box)
    dpi_entry.grid(row=row_index, column=1)
    dpi_entry.insert(0, para['dpi']) 
    
    # linewidth
    tk.Label(plotting_frame, text="Line width (px)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    linewidth_entry = tk.Entry(plotting_frame, width=width_text_box)
    linewidth_entry.grid(row=row_index, column=3)
    linewidth_entry.insert(0, para['linewidth'])  
    
    row_index+=1
    # Plot frame numbers next to tracks
    use_plot_frame_number_var = tk.BooleanVar(value=para['plot_frame_number'])
    tk.Checkbutton(plotting_frame, text="Plot frame number", variable=use_plot_frame_number_var,
                   width = width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)
  
    # Plot frame numbers next to tracks
    scta_vis_cells_var = tk.BooleanVar(value=para['scta_vis_cells'])
    tk.Checkbutton(plotting_frame, text="Show individual cells", variable=scta_vis_cells_var,
                   width = width_text_labels, anchor="w").grid(row=row_index, column=2, sticky=tk.W)

    row_index+=1
    # Plot frame numbers next to tracks
    scta_vis_interactive_var = tk.BooleanVar(value=para['scta_vis_interactive'])
    tk.Checkbutton(plotting_frame, text="Cycle through cells", variable=scta_vis_interactive_var,
                   width = width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)

    row_index+=1
    # Dropdown Menu for Colormap Selection
    tk.Label(plotting_frame, text="Select color map", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    # Create StringVar for dropdown selection
    cmap_applied_var = tk.StringVar()
    cmap_applied_var.set("gist_ncar")  # Default option
    # Create a dropdown menu
    cmap_applied_entry = tk.OptionMenu(plotting_frame, cmap_applied_var, "gist_ncar", "nipy_spectral", "tab20c")
    # cmap_dropdown.config(width=10)
    cmap_applied_entry.grid(row=row_index, column=1, sticky=tk.W)

    
    # Dropdown Menu for plotting diffusion histrograms Selection
    tk.Label(plotting_frame, text="Select plotting option", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    plot_norm_histograms_var = tk.StringVar()
    plot_norm_histograms_var.set("probability")  # Default option
    plot_norm_histograms_entry = tk.OptionMenu(plotting_frame, plot_norm_histograms_var, 
                                               "probability", "counts")
    plot_norm_histograms_entry.grid(row=row_index, column=3, sticky=tk.W)
    
    row_index+=1
    # Radius in pixels for plotting individual cells and their tracks
    tk.Label(plotting_frame, text="Radius plotting cells (px)", width = width_text_labels, 
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    scta_plot_cell_window_entry = tk.Entry(plotting_frame, width=width_text_box)
    scta_plot_cell_window_entry.grid(row=row_index, column=1)
    scta_plot_cell_window_entry.insert(0, para['scta_plot_cell_window'])  
     
    # Color-coding in the range of [0:plot_DiffHist_max)], default: 0.4
    tk.Label(plotting_frame, text="Color-coding [0:D_max)]", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    scta_vis_rangemax_entry = tk.Entry(plotting_frame, width=width_text_box)
    scta_vis_rangemax_entry.grid(row=row_index, column=3)
    scta_vis_rangemax_entry.insert(0, para['scta_vis_rangemax'])  
    
#############################
    # Load, Save, and Exit buttons
#############################
    button_frame = tk.Frame(right_frame)
    button_frame.grid(row=4, column=1, pady=10)

    tk.Button(button_frame, text="Load...",
              command=load_params).grid(row=0, column=0, padx=5)

    tk.Button(button_frame, text="Save...",
              command=save_params).grid(row=0, column=1, padx=5)

    tk.Button(button_frame, text="Exit",
              command=exit_GUI).grid(row=0, column=4, padx=5)

    root.mainloop()

    # Return collected parameters after window closes
    return para



