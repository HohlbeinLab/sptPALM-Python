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
from set_parameters_simulation import set_parameters_simulation


def set_parameters_simulation_GUI(sim_input = None):
    print('\nRun set_parameters_simulation_GUI.py')
    if sim_input is None:
        print(" re-run set_parameters_simulation")
        sim_input = set_parameters_simulation()
      
    # # Function to create the GUI
    # def browse_directory():
    #     dirname = filedialog.askdirectory()
    #     if dirname:
    #         data_dir_entry.delete(0, tk.END)
    #         data_dir_entry.insert(0, dirname)

    # def browse_files():
    #     files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    #     if files:
    #         fn_locs_entry.delete(0, tk.END)
    #         fn_locs_entry.insert(0, ', '.join(files))

    def save_params_exit():
        nonlocal sim_input
        # Collect all parameters from the GUI
        sim_input = {
            # Number of species and particles per species
            '#_species': number_species_entry.get(),  # number of species
            '#_particles_per_species': list(map(int,
                                                number_particles_per_species_entry.get().split(','))),  # particles per species
            
            # Cell dimensions (in µm)
            'radius_cell': radius_cell_entry.get(),  # (µm) radius of the cap, edefault: 0.5
            'length_cell': length_cell_entry.get(),    # (µm) length of the cylindrical part, default: 2.0
            
            # Track lengths and diffusion constraints (also track_lengths': [1,2,3,4,5,6,7,8])
            'tracklength_locs_min': tracklength_locs_min_entry.get(),  # Track lengths (2 to 8 frames) tracklength of 1 is two locs, or track_lengths': [1,2,3,4,5,6,7,8]
            'tracklength_locs_max': tracklength_locs_max_entry.get(),  # Track lengths (2 to 8 frames) tracklength of 1 is two locs, or track_lengths': [1,2,3,4,5,6,7,8]
            'mean_track_length': mean_track_length_entry.get(),  # Mean track length for exponential distribution, default 3
            
            # Simulation parameters
            'confined_diffusion': True,  # Confine diffusion within a cell
            'loc_error': 0.035,  # (µm) Localization error (in µm), default: 0.035
            'correct_diff_calc_loc_error': False,  # Match anaDDA settings, default: False
            
            # Timing parameters
            'steptime': 0.001,  # (s) step time in seconds, default: 0.001
            'frametime': 0.01,  # (s) frame time in seconds, default: 0.02
            
            # Fitting and plotting options
            'perform_fitting': perform_fitting_var.get(),  # Whether to perform fitting or not
            'display_figures': display_figures_var.get(),  # Display figures
            'plot_diff_hist_min': float(diff_hist_min_entry.get()),  # Diffusion coefficient histogram min (µm^2/s), default: 0.004
            'plot_diff_hist_max': float(diff_hist_max_entry.get()),  # Diffusion coefficient histogram max (µm^2/s), deafult: 10.0
            'binwidth': float(binwidth_entry.get()),   # Bin width for histogram, default 0.1
            'species_to_select': 0, # For fitting, only one specis can be selected, set here which one, default:0
            
            # Error handling values
            'avoidFloat0': 1e-09,  # To avoid rates being exactly zero, default: 1e-09
           
            # Species-specific parameters
            'species': [], #defined below
           
           #Plotting stuff
           'dpi': 150, # DPI setting for plotting figures, default: 300
            
           
            
            # # File and directory selection
            # 'data_dir': data_dir_entry.get(),
            # 'default_output_dir': default_output_dir_entry.get(),
            # 'fn_locs': list(map(str.strip, fn_locs_entry.get().split(','))),
            # 'fn_proc_brightfield': list(map(str.strip, fn_proc_brightfield_entry.get().split(','))),
            
            # 'condition_names': list(map(str.strip, condition_names_entry.get().split(','))),
            # 'condition_files': list(map(int,condition_files_entry.get().split(','))),
            # # 'copynumber_intervals': list(map(int, copynumber_intervals.get().split(','))),
           
            # 'fn_csv_handle': fn_csv_handle_entry.get(),
            # 'fn_dict_handle': fn_dict_handle_entry.get(),
            # 'fn_diffs_handle': fn_diffs_handle_entry.get(),
            # 'fn_movies': fn_movies_entry.get(),    
            # 'fn_combined_movies': fn_combined_movies_entry.get(),
            
            # # Pixelsize and segmentation
            # 'pixelsize': float(pixelsize_entry.get()),
            # 'cellarea_pixels_min': int(cellarea_min_entry.get()),
            # 'cellarea_pixels_max': int(cellarea_max_entry.get()),
            # 'use_segmentations': use_segmentations_var.get(),
            # 'track_steplength_max': float(track_steplength_entry.get()),
            # 'track_memory': int(track_memory_entry.get()),
            # 'frametime': float(frametime_entry.get()),
            # 'loc_error': float(loc_error_entry.get()),
            # 'diff_hist_steps_min': int(diff_hist_steps_min_entry.get()),
            # 'diff_hist_steps_max': int(diff_hist_steps_max_entry.get()),
            # 'track_lengths': list(map(int, track_lengths_entry.get().split(','))),
            # 'number_tracks_per_cell_min': int(number_tracks_per_cell_min_entry.get()),
            # 'number_tracks_per_cell_max': int(number_tracks_per_cell_max_entry.get()),
            
            # 'scta_vis_cells': scta_vis_cells_var.get(),
            # 'scta_plot_cell_window': int(scta_plot_cell_window_entry.get()),
            # 'scta_vis_interactive': scta_vis_interactive_var.get(),
            # 'scta_vis_rangemax': float(scta_vis_rangemax_entry.get()),
            # 'plot_diff_hist_min': float(diff_hist_min_entry.get()),
            # 'plot_diff_hist_max': float(diff_hist_max_entry.get()),
            # 'binwidth': float(binwidth_entry.get()),
            # 'fontsize': int(fontsize_entry.get()),
            # 'linewidth': int(linewidth_entry.get()),
            # 'plot_norm_histograms': plot_norm_histograms_var.get(),
            # 'plot_frame_number': use_plot_frame_number_var.get(),
            # 'dpi': int(dpi_entry.get()),
            # 'cmap_applied': cmap_applied_var.get()
        }

        root.quit()  # Exits the Tkinter event loop
        # root.destroy()  # Destroys the Tkinter window

    root = tk.Tk()
    root.title("SPT-PALM simulation GUI (defaults imported from set_parameter_simulation.py)")
    
    # Adjust the column configuration of the root window to split into two
    root.grid_columnconfigure(0, weight=1)  # First column gets full width (file_frame)
    root.grid_columnconfigure(1, weight=1)  # Second column (numeric_frame) gets half width
    
    # Create two separate container frames for left and right columns
    left_frame = tk.Frame(root)
    left_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")  # Left half

    right_frame = tk.Frame(root)
    right_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")  # Right half
    
    
    width_text_labels = 20
    width_text_fileIO = 95
    width_text_box = 8
    
    """
    # Frame for simulation I
    """

    sim_frame = tk.LabelFrame(left_frame, text="Tracking and diffusion analysis",
                                   padx=0, pady=0)
    sim_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")

    # Number of species
    tk.Label(sim_frame, text="Number of species: ", width = width_text_labels,
             anchor="w").grid(row=0, column=0, sticky=tk.W)
    number_species_entry = tk.Entry(sim_frame, width=width_text_box)
    number_species_entry.grid(row=0, column=1)
    number_species_entry.insert(0, sim_input['#_species'])   

    # Number particles per species
    tk.Label(sim_frame, text="Number particles per species", width = width_text_labels,
             anchor="w").grid(row=1, column=0, sticky=tk.W)
    number_particles_per_species_entry = tk.Entry(sim_frame, width=3*width_text_box)
    number_particles_per_species_entry.grid(row=1, column=1)
    number_particles_per_species_entry.insert(0, ', '.join(map(str, sim_input['#_particles_per_species'])))   

    # Radius cell
    tk.Label(sim_frame, text="Radius of cell (µm)", width = width_text_labels,
             anchor="w").grid(row=2, column=0, sticky=tk.W)
    radius_cell_entry = tk.Entry(sim_frame, width=width_text_box)
    radius_cell_entry.grid(row=2, column=1)
    radius_cell_entry.insert(0, sim_input['radius_cell'])   

    # Length cell
    tk.Label(sim_frame, text="Length of cell (µm)", width = width_text_labels,
             anchor="w").grid(row=2, column=2, sticky=tk.W)
    length_cell_entry = tk.Entry(sim_frame, width=width_text_box)
    length_cell_entry.grid(row=2, column=3)
    length_cell_entry.insert(0, sim_input['length_cell'])  

    # Tracklength localisations min
    tk.Label(sim_frame, text="Tracklength localisations min", width = width_text_labels,
             anchor="w").grid(row=3, column=0, sticky=tk.W)
    tracklength_locs_min_entry = tk.Entry(sim_frame, width=width_text_box)
    tracklength_locs_min_entry.grid(row=3, column=1)
    tracklength_locs_min_entry.insert(0, sim_input['tracklength_locs_min'])  

    # Tracklengths localisation max
    tk.Label(sim_frame, text="Tracklength localisations max", width = width_text_labels,
             anchor="w").grid(row=3, column=2, sticky=tk.W)
    tracklength_locs_max_entry = tk.Entry(sim_frame, width=width_text_box)
    tracklength_locs_max_entry.grid(row=3, column=3)
    tracklength_locs_max_entry.insert(0, sim_input['tracklength_locs_max'])  

    # Mean track length
    tk.Label(sim_frame, text="Mean track length (frames)", width = width_text_labels,
             anchor="w").grid(row=4, column=0, sticky=tk.W)
    mean_track_length_entry = tk.Entry(sim_frame, width=width_text_box)
    mean_track_length_entry.grid(row=4, column=1)
    mean_track_length_entry.insert(0, sim_input['mean_track_length'])  


    """
    # 
    """

    segmentation_frame = tk.LabelFrame(left_frame, text="Simulation parameters", padx=10, pady=10)
    segmentation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")
   
    # # Pixelsize
    # tk.Label(segmentation_frame, text="Pixel size (µm)", width = width_text_labels,
    #          anchor="w").grid(row=0, column=0, sticky=tk.W)
    # pixelsize_entry = tk.Entry(segmentation_frame, width=width_text_box)
    # pixelsize_entry.grid(row=0, column=1)
    # pixelsize_entry.insert(1, sim_input['pixelsize'])

    # # Use Segmentations
    # use_segmentations_var = tk.BooleanVar(value = sim_input['use_segmentations'])
    # tk.Checkbutton(segmentation_frame, text="Use segmentations", variable=use_segmentations_var,
    #                width = width_text_labels, anchor="w").grid(row=0, column=2, sticky=tk.W)

    # # Cell area (min/max)
    # tk.Label(segmentation_frame, text="Min. cell area (pixels)", width = width_text_labels,
    #          anchor="w").grid(row=1, column=0, sticky=tk.W)
    # cellarea_min_entry = tk.Entry(segmentation_frame, width=width_text_box)
    # cellarea_min_entry.grid(row=1, column=1)
    # cellarea_min_entry.insert(0, sim_input['cellarea_pixels_min'])

    # tk.Label(segmentation_frame, text="Max. cell area (pixels)", width = width_text_labels,
    #          anchor="w").grid(row=1, column=2, sticky=tk.W)
    # cellarea_max_entry = tk.Entry(segmentation_frame, width=width_text_box)
    # cellarea_max_entry.grid(row=1, column=3)
    # cellarea_max_entry.insert(0, sim_input['cellarea_pixels_max'])
    
    # # Minimum number of steps per track
    # tk.Label(segmentation_frame, text="Min. number tracks/cell", width = width_text_labels,
    #          anchor="w").grid(row=2, column=0, sticky=tk.W)
    # number_tracks_per_cell_min_entry = tk.Entry(segmentation_frame, width=width_text_box)
    # number_tracks_per_cell_min_entry.grid(row=2,  column=1)
    # number_tracks_per_cell_min_entry.insert(0, sim_input['number_tracks_per_cell_min'])
    
    # # Maximum number of steps per track
    # tk.Label(segmentation_frame, text="Max. number tracks/cell", width = width_text_labels,
    #          anchor="w").grid(row=2, column=2, sticky=tk.W)
    # number_tracks_per_cell_max_entry = tk.Entry(segmentation_frame, width=width_text_box)
    # number_tracks_per_cell_max_entry.grid(row=2, column=3)
    # number_tracks_per_cell_max_entry.insert(0, sim_input['number_tracks_per_cell_max'])

    # """
    # # Frame for Tracking inputs 
    # """
  
    # tracking_frame = tk.LabelFrame(left_frame, text="Tracking and diffusion analysis",
    #                                padx=10, pady=10)
    # tracking_frame.grid(row=2, column=0, padx=10, pady=10, sticky="new")

    # # Frame time (sec)
    # tk.Label(tracking_frame, text="Frame time (sec)", width = width_text_labels,
    #          anchor="w").grid(row=0, column=0, sticky=tk.W)
    # frametime_entry = tk.Entry(tracking_frame, width=width_text_box)
    # frametime_entry.grid(row=0, column=1)
    # frametime_entry.insert(0, sim_input['frametime'])   
      
    # # Localisation error
    # tk.Label(tracking_frame, text="Loc. error (µm)", width = width_text_labels,
    #          anchor="w").grid(row=0, column=2, sticky=tk.W)
    # loc_error_entry = tk.Entry(tracking_frame, width=width_text_box)
    # loc_error_entry.grid(row=0, column=3)
    # loc_error_entry.insert(0, sim_input['loc_error'])


    
    # # Maximum number of steps per track
    # tk.Label(tracking_frame, text="Max. number steps", width = width_text_labels,
    #          anchor="w").grid(row=2, column=2, sticky=tk.W)
    # diff_hist_steps_max_entry = tk.Entry(tracking_frame, width=width_text_box)
    # diff_hist_steps_max_entry.grid(row=2, column=3)
    # diff_hist_steps_max_entry.insert(0, sim_input['diff_hist_steps_max'])    
 
    # # Track lengths min
    # tk.Label(tracking_frame, text="Tracklength (frames)", width = width_text_labels,
    #          anchor="w").grid(row=3, column=0, sticky=tk.W)
    # track_lengths_entry = tk.Entry(tracking_frame, width=width_text_box)
    # track_lengths_entry.grid(row=4, column=1)
    # track_lengths_entry.insert(0, ', '.join(map(str, sim_input['tracklengths_locs_min'])))   
                        
              
    """
    # Frame for plotting
    """
    plotting_frame = tk.LabelFrame(right_frame, text="Fitting and plotting options", padx=10, pady=10)
    plotting_frame.grid(row=0, column=1, padx=10, pady=10, sticky="new")  # Right half

    
    # Plot frame numbers next to tracks
    perform_fitting_var = tk.BooleanVar(value=sim_input['perform_fitting'])
    tk.Checkbutton(plotting_frame, text="Perform fitting", variable=perform_fitting_var,
                   width = width_text_labels, anchor="w").grid(row=0, column=0, sticky=tk.W)
  
    # Display figures
    display_figures_var = tk.BooleanVar(value=sim_input['display_figures'])
    tk.Checkbutton(plotting_frame, text="Display figures", variable=display_figures_var,
                   width = width_text_labels, anchor="w").grid(row=0, column=2, sticky=tk.W)

    # plot_diff_hist_min
    tk.Label(plotting_frame, text="D. hist. min (µm^2/s)", width = width_text_labels,
             anchor="w").grid(row=1, column=0, sticky=tk.W)
    diff_hist_min_entry = tk.Entry(plotting_frame, width=width_text_box)
    diff_hist_min_entry.grid(row=1, column=1)
    diff_hist_min_entry.insert(0, sim_input['plot_diff_hist_min'])  

    # plot_diff_hist_max
    tk.Label(plotting_frame, text="D. hist. max (µm^2/s)", width = width_text_labels,
             anchor="w").grid(row=1, column=2, sticky=tk.W)
    diff_hist_max_entry = tk.Entry(plotting_frame, width=width_text_box)
    diff_hist_max_entry.grid(row=1, column=3)
    diff_hist_max_entry.insert(0, sim_input['plot_diff_hist_max'])  
    
    # Binwidth
    tk.Label(plotting_frame, text="Binwith histograms", width = width_text_labels,
             anchor="w").grid(row=2, column=0, sticky=tk.W)
    binwidth_entry = tk.Entry(plotting_frame, width=width_text_box)
    binwidth_entry.grid(row=2, column=1)
    binwidth_entry.insert(0, sim_input['binwidth'])  

    # dpi
    tk.Label(plotting_frame, text="Resolution figus (dpi)", width = width_text_labels,
             anchor="w").grid(row=1, column=0, sticky=tk.W)
    dpi_entry = tk.Entry(plotting_frame, width=width_text_box)
    dpi_entry.grid(row=1, column=1)
    dpi_entry.insert(0, sim_input['dpi']) 



    # # Fitting and plotting options
    # 'perform_fitting': True,  # Whether to perform fitting or not
    # 'display_figures': True,  # Display figures
    # 'plot_diff_hist_min': 0.004,  # Diffusion coefficient histogram min (µm^2/s), default: 0.004
    # 'plot_diff_hist_max': 10.0,  # Diffusion coefficient histogram max (µm^2/s), deafult: 10.0
    # 'binwidth': 0.1,  # Bin width for histogram, default 0.1
    # 'species_to_select': 0, # For fitting, only one specis can be selected, set here which one, default:0
 

#############################
    # Save and Exit buttons
#############################
    button_frame = tk.Frame(right_frame)
    button_frame.grid(row=4, column=1, pady=10)

    tk.Button(button_frame, text="Save and Exit",
              command=save_params_exit).grid(row=0, column=0, padx=5)

    root.mainloop()

    # Return collected parameters after window closes
    return sim_input



