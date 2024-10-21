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
import pickle
from pathlib import Path

def set_parameters_simulation_GUI(sim_input = None):
    print('\nRun set_parameters_simulation_GUI.py')
    if sim_input is None:
        print(" re-run set_parameters_simulation")
        sim_input = set_parameters_simulation()
      
    def load_params(): #careful, we need to overwrite all default parameters
        filename = filedialog.askopenfilename(
                                    filetypes = [("pickle file", "*.pkl")],
                                    title = "Select *.pkl file")
        if filename:
            with open(filename, 'rb') as f:
                new_sim_input = pickle.load(f)
                print("Input parameters for simulation loaded")
                    
            # Update the entries with the newly loaded parameters
            number_species_entry.delete(0, tk.END)
            number_species_entry.insert(0, new_sim_input['#_species'])
            
            number_particles_per_species_entry.delete(0, tk.END)
            number_particles_per_species_entry.insert(0, ','.join(map(str, new_sim_input['#_particles_per_species'])))
            
            radius_cell_entry.delete(0, tk.END)
            radius_cell_entry.insert(0, new_sim_input['radius_cell'])
            
            length_cell_entry.delete(0, tk.END)
            length_cell_entry.insert(0, new_sim_input['length_cell'])
            
            tracklength_locs_min_entry.delete(0, tk.END)
            tracklength_locs_min_entry.insert(0, new_sim_input['tracklength_locs_min'])
            
            tracklength_locs_max_entry.delete(0, tk.END)
            tracklength_locs_max_entry.insert(0, new_sim_input['tracklength_locs_max'])
            
            mean_track_length_entry.delete(0, tk.END)
            mean_track_length_entry.insert(0, new_sim_input['mean_track_length'])
            
            confined_diffusion_var.set(new_sim_input['confined_diffusion'])
            
            loc_error_entry.delete(0, tk.END)
            loc_error_entry.insert(0, new_sim_input['loc_error'])
            
            correct_diff_calc_loc_error_var.set(new_sim_input['correct_diff_calc_loc_error'])
            
            steptime_entry.delete(0, tk.END)
            steptime_entry.insert(0, new_sim_input['steptime'])
            
            frametime_entry.delete(0, tk.END)
            frametime_entry.insert(0, new_sim_input['frametime'])
            
            perform_fitting_var.set(new_sim_input['perform_fitting'])
            
            display_figures_var.set(new_sim_input['display_figures'])
            
            diff_hist_min_entry.delete(0, tk.END)
            diff_hist_min_entry.insert(0, new_sim_input['plot_diff_hist_min'])
            
            diff_hist_max_entry.delete(0, tk.END)
            diff_hist_max_entry.insert(0, new_sim_input['plot_diff_hist_max'])
            
            binwidth_entry.delete(0, tk.END)
            binwidth_entry.insert(0, new_sim_input['binwidth'])
            
            species_to_select_entry.delete(0, tk.END)
            species_to_select_entry.insert(0, new_sim_input['species_to_select'])
            
            avoidFloat0_entry.delete(0, tk.END)
            avoidFloat0_entry.insert(0, new_sim_input['avoidFloat0'])
            
            dpi_entry.delete(0, tk.END)
            dpi_entry.insert(0, new_sim_input['dpi'])
            
            # If 'species' needs to be updated, handle accordingly
            # For example, assuming species is a list of dictionaries, you'd need to handle that more specifically
            # You can loop through 'species' from new_sim_input and update corresponding widgets or data structure
   
        else:
            raise ValueError("No file selected!")

    def exit_GUI():
        root.quit()  # Exits the Tkinter event loop
        root.destroy()  # Destroys the Tkinter window
    
    def save_params():
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
            'confined_diffusion': confined_diffusion_var.get(),  # Confine diffusion within a cell
            'loc_error': loc_error_entry.get(),  # (µm) Localization error (in µm), default: 0.035
            'correct_diff_calc_loc_error': correct_diff_calc_loc_error_var.get(),  # Match anaDDA settings, default: False
            
            # Timing parameters
            'steptime': steptime_entry.get(),  # (s) step time in seconds, default: 0.001
            'frametime': frametime_entry.get(),  # (s) frame time in seconds, default: 0.02
            
            # Fitting and plotting options
            'perform_fitting': perform_fitting_var.get(),  # Whether to perform fitting or not
            'display_figures': display_figures_var.get(),  # Display figures
            'plot_diff_hist_min': float(diff_hist_min_entry.get()),  # Diffusion coefficient histogram min (µm^2/s), default: 0.004
            'plot_diff_hist_max': float(diff_hist_max_entry.get()),  # Diffusion coefficient histogram max (µm^2/s), deafult: 10.0
            'binwidth': float(binwidth_entry.get()),   # Bin width for histogram, default 0.1
            'species_to_select': species_to_select_entry.get(), # For fitting, only one specis can be selected, set here which one, default:0
            
            # Error handling values
            'avoidFloat0': avoidFloat0_entry.get(),  # To avoid rates being exactly zero, default: 1e-09
           
            # Species-specific parameters
            'species': [], #defined below
           
            #Plotting stuff
            'dpi': dpi_entry.get(), # DPI setting for plotting figures, default: 300
            
        }

        # Get the current working directory
        current_directory = Path.cwd()
        
        # Ask the user where to save the file, default filename is input_parameter.pkl
        save_file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            initialdir=current_directory,  # Set the initial directory if provided
            filetypes=[("Pickle files", "*.pkl")],
            initialfile="sim_input_parameter.pkl",
            title="Save sim_input_parameter as"
        )
        
        if save_file_path:  # If the user selects a file path
            with open(save_file_path, 'wb') as file:
                pickle.dump(sim_input, file)  # Save the dictionary to the file
            print(f" Input parameters for simulation saved to {save_file_path}")
        else:
            print("Save operation canceled.")
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
    row_index = 0
    
    """
    # Frame for simulation I
    """

    sim_frame = tk.LabelFrame(left_frame, text="Parameters for simulation",
                                   padx=0, pady=0)
    sim_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")

    # Number of species
    tk.Label(sim_frame, text="Number of species: ", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    number_species_entry = tk.Entry(sim_frame, width=width_text_box)
    number_species_entry.grid(row=row_index, column=1)
    number_species_entry.insert(0, sim_input['#_species'])   

    # Number particles per species
    row_index +=1
    tk.Label(sim_frame, text="Number particles per species", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    number_particles_per_species_entry = tk.Entry(sim_frame, width=(2*width_text_box)+width_text_labels+2)
    number_particles_per_species_entry.grid(row=row_index, column=1, columnspan=3)
    number_particles_per_species_entry.insert(0, ', '.join(map(str, sim_input['#_particles_per_species'])))   

    # Radius cell
    row_index +=1
    tk.Label(sim_frame, text="Radius of cell (µm)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    radius_cell_entry = tk.Entry(sim_frame, width=width_text_box)
    radius_cell_entry.grid(row=row_index, column=1)
    radius_cell_entry.insert(0, sim_input['radius_cell'])   

    # Length cell
    tk.Label(sim_frame, text="Length of cell (µm)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    length_cell_entry = tk.Entry(sim_frame, width=width_text_box)
    length_cell_entry.grid(row=row_index, column=3)
    length_cell_entry.insert(0, sim_input['length_cell'])  

    # Tracklength localisations min
    row_index +=1
    tk.Label(sim_frame, text="Tracklength: min locs", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    tracklength_locs_min_entry = tk.Entry(sim_frame, width=width_text_box)
    tracklength_locs_min_entry.grid(row=row_index, column=1)
    tracklength_locs_min_entry.insert(0, sim_input['tracklength_locs_min'])  

    # Tracklengths localisation max
    tk.Label(sim_frame, text="Tracklength: max locs", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    tracklength_locs_max_entry = tk.Entry(sim_frame, width=width_text_box)
    tracklength_locs_max_entry.grid(row=row_index, column=3)
    tracklength_locs_max_entry.insert(0, sim_input['tracklength_locs_max'])  

    # Mean track length
    row_index +=1
    tk.Label(sim_frame, text="Mean tracklength (frames)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    mean_track_length_entry = tk.Entry(sim_frame, width=width_text_box)
    mean_track_length_entry.grid(row=row_index, column=1)
    mean_track_length_entry.insert(0, sim_input['mean_track_length'])  


    # Confine the diffusion to the bacterial cell
    row_index +=1
    confined_diffusion_var = tk.BooleanVar(value=sim_input['confined_diffusion'])
    tk.Checkbutton(sim_frame, text="Confine diffusion", variable=confined_diffusion_var,
                   width = width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)

    # Simulate localisation error
    row_index +=1
    tk.Label(sim_frame, text="Localisation error (µm)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    loc_error_entry = tk.Entry(sim_frame, width=width_text_box)
    loc_error_entry.grid(row=row_index, column=1)
    loc_error_entry.insert(0, sim_input['loc_error'])  

    #Correct localisation error
    correct_diff_calc_loc_error_var = tk.BooleanVar(value=sim_input['correct_diff_calc_loc_error'])
    tk.Checkbutton(sim_frame, text="Correct_diff_calc_loc_error", variable=correct_diff_calc_loc_error_var,
                   width = width_text_labels, anchor="w").grid(row=row_index, column=2, sticky=tk.W, columnspan = 3)
    
    # steptime
    row_index +=1
    tk.Label(sim_frame, text="Steptime (s)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    steptime_entry = tk.Entry(sim_frame, width=width_text_box)
    steptime_entry.grid(row=row_index, column=1)
    steptime_entry.insert(0, sim_input['steptime'])  

    # Tracklengths localisation max
    tk.Label(sim_frame, text="Frametime (s)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    frametime_entry = tk.Entry(sim_frame, width=width_text_box)
    frametime_entry.grid(row=row_index, column=3)
    frametime_entry.insert(0, sim_input['frametime'])  



    """
    # Empty...
    """

    segmentation_frame = tk.LabelFrame(left_frame, text="Simulation parameters", padx=10, pady=10)
    segmentation_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")
   
                       
              
    """
    # Frame for plotting
    """

    plotting_frame = tk.LabelFrame(right_frame, text="Fitting and plotting options", padx=0, pady=0)
    plotting_frame.grid(row=0, column=1, padx=10, pady=10, sticky="new")  # Right half

    # Display figures
    row_index = 0
    display_figures_var = tk.BooleanVar(value=sim_input['display_figures'])
    tk.Checkbutton(plotting_frame, text="Display figures", variable=display_figures_var,
                   width = width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)

    # Whether to perform MC-DDA fitting
    row_index +=1
    perform_fitting_var = tk.BooleanVar(value=sim_input['perform_fitting'])
    tk.Checkbutton(plotting_frame, text="Perform MC-DDA fitting", variable=perform_fitting_var,
                   width = width_text_labels, anchor="w").grid(row=row_index, column=0, sticky=tk.W)
 
    # Species to select for fitting
    tk.Label(plotting_frame, text="Species to select", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    species_to_select_entry = tk.Entry(plotting_frame, width=width_text_box)
    species_to_select_entry.grid(row=row_index, column=3)
    species_to_select_entry.insert(0, sim_input['species_to_select'])  

    # plot_diff_hist_min
    row_index +=1
    tk.Label(plotting_frame, text="D. hist. min (µm^2/s)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    diff_hist_min_entry = tk.Entry(plotting_frame, width=width_text_box)
    diff_hist_min_entry.grid(row=row_index, column=1)
    diff_hist_min_entry.insert(0, sim_input['plot_diff_hist_min'])  

    # plot_diff_hist_max
    tk.Label(plotting_frame, text="D. hist. max (µm^2/s)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    diff_hist_max_entry = tk.Entry(plotting_frame, width=width_text_box)
    diff_hist_max_entry.grid(row=row_index, column=3)
    diff_hist_max_entry.insert(0, sim_input['plot_diff_hist_max'])  
    
    # Binwidth
    row_index +=1
    tk.Label(plotting_frame, text="Binwith histograms", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    binwidth_entry = tk.Entry(plotting_frame, width=width_text_box)
    binwidth_entry.grid(row=row_index, column=1)
    binwidth_entry.insert(0, sim_input['binwidth'])  

    # dpi
    tk.Label(plotting_frame, text="Resolution figus (dpi)", width = width_text_labels,
             anchor="w").grid(row=row_index, column=0, sticky=tk.W)
    dpi_entry = tk.Entry(plotting_frame, width=width_text_box)
    dpi_entry.grid(row=row_index, column=1)
    dpi_entry.insert(0, sim_input['dpi']) 

    # Avoid float number = 0
    tk.Label(plotting_frame, text="Avoid float 0", width = width_text_labels,
             anchor="w").grid(row=row_index, column=2, sticky=tk.W)
    avoidFloat0_entry = tk.Entry(plotting_frame, width=width_text_box)
    avoidFloat0_entry.grid(row=row_index, column=3)
    avoidFloat0_entry.insert(0, sim_input['avoidFloat0']) 


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
    return sim_input



