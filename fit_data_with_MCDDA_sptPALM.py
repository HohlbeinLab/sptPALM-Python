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

import numpy as np
import matplotlib.pyplot as plt
import math
import os
from scipy.optimize import least_squares
from scipy.stats import chi2
from initiate_simulation import initiate_simulation
from diffusion_simulation import diffusion_simulation
from diff_coeffs_from_tracks_fast import diff_coeffs_from_tracks_fast


def fit_data_with_MCDDA_sptPALM(D_track_length_matrix, sim_input, input_parameter):
    print("\nRun diff_coeffs_from_tracks_fast.py")

    # Check if fitting is supported for multiple species
    if sim_input['#_species'] > 1 and sim_input['perform_fitting']:
        print('Careful. Fitting is currently only supported for a single species!')
        print("Careful. 'perform_fitting' changed to 'False'")
        sim_input['perform_fitting']=False
        
    ii = sim_input['species_to_select']  # Index for species

    # Temporarily set displayFigures to False
    sim_input['display_figures'] = False

    # Normalize the D_track_length_matrix
    D_track_length_matrix_normalized = D_track_length_matrix.copy()
    D_track_length_matrix_normalized.loc[:, list(sim_input['tracklengths_steps'])] /= np.sum(D_track_length_matrix_normalized.loc[:, list(sim_input['tracklengths_steps'])], axis=0) 

    # Initial guesses and bounds
    if sim_input['species'][ii]['#_states'] == 1:
        start_values_fitting = np.concatenate([sim_input['species'][ii]['diff_quot_init_guess']])
        lower_bounds = np.concatenate([sim_input['species'][ii]['diff_quot_lb_ub'][0]])
        upper_bounds = np.concatenate([sim_input['species'][ii]['diff_quot_lb_ub'][1]])  
    else:
        start_values_fitting = np.concatenate([sim_input['species'][ii]['diff_quot_init_guess'], sim_input['species'][ii]['rates_init_guess']])
        lower_bounds = np.concatenate([sim_input['species'][ii]['diff_quot_lb_ub'][0], sim_input['species'][ii]['rates_lb_ub'][0]])
        upper_bounds = np.concatenate([sim_input['species'][ii]['diff_quot_lb_ub'][1], sim_input['species'][ii]['rates_lb_ub'][1]])

    # Initial output
    out_initial_guess = fitFunc(start_values_fitting, sim_input)
    
    def fitFunc_1D(xdata, params, sim_input):
        """ 
        Simulation function using params to simulate the output, 
        ignoring xdata here for now.
        """
        ii = sim_input['species_to_select'] 
   
        if sim_input['species'][ii]['#_states'] == 1:
            sim_input['species'][ii]['diff_quot'] = np.array(params[0:1])
        elif sim_input['species'][ii]['#_states'] == 2:
            sim_input['species'][ii]['diff_quot'] = np.array(params[0:2]) 
            sim_input['species'][ii]['rates'] = params[2:4]
        elif sim_input['species'][ii]['#_states'] >= 3:
            sim_input['species'][ii]['diff_quot'] = np.array(params[0:3]) 
            sim_input['species'][ii]['rates'] = params[3:9]
        
        # Run the simulation
        particleData, sim_input = initiate_simulation(sim_input)
        _, tracks = diffusion_simulation(sim_input, particleData)
    
        # Calculate diffusion coefficients and flatten the matrix
        sorted_tracks = tracks.sort_values(by=['track_id', 'frame'])
        _, D_track_length_matrix = diff_coeffs_from_tracks_fast(sorted_tracks, sim_input)
   
        # Normalize and linearize the matrix
        D_track_length_matrix.loc[:, list(sim_input['tracklengths_steps'])] /= np.sum(D_track_length_matrix.loc[:, list(sim_input['tracklengths_steps'])], axis=0)
        linearized_array = D_track_length_matrix.values.ravel()

        return linearized_array
    
    def def_residuals(params, sim_input, ground_truth):
        """Residual function for least_squares"""
        simulated_data = fitFunc_1D(None, params, sim_input)  # Simulate using params
        residuals = simulated_data - ground_truth  # Return the difference
        return residuals


    # Options for curve fitting (using scipy's least_squares)
    experimental_data = D_track_length_matrix_normalized.values.ravel()
    if sim_input['perform_fitting']:
        if sim_input['species'][ii]['#_states'] == 1:
            res = least_squares(def_residuals, 
                             start_values_fitting,
                             method = 'dogbox', # options trf, dogbox
                             bounds=(lower_bounds, upper_bounds),
                             args=(sim_input,experimental_data),
                             loss = 'linear', # cauchy: crap; soft_l1
                             x_scale = [1],
                             diff_step = [0.5],
                             # max_nfev = 10,
                             verbose=2)     
        elif sim_input['species'][ii]['#_states'] == 2:
            res = least_squares(def_residuals, 
                            start_values_fitting,
                            method = 'dogbox', # options trf, dogbox
                            bounds=(lower_bounds, upper_bounds),
                            args=(sim_input,experimental_data),
                            loss = 'linear', # cauchy: crap; soft_l1
                            x_scale = [1,1,0.1, 0.1],
                            diff_step = [0.1, 0.5, 25, 25],
                            # max_nfev = 10,
                            verbose=2) #,callback=callback_func
        elif sim_input['species'][ii]['#_states'] >= 3:
            res = least_squares(def_residuals, 
                             start_values_fitting,
                             method = 'dogbox', # options trf, dogbox
                             bounds=(lower_bounds, upper_bounds),
                             args=(sim_input,experimental_data),
                             loss = 'linear', # cauchy: crap; soft_l1
                             x_scale = [1,1,1,0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                             diff_step = [0.1, 0.1, 0.5, 25, 25, 25, 25, 25, 25],
                             # max_nfev = 10,
                             verbose=2) #,callback=callback_func       
            
        shiftX = res.x

        # # Calculate 95% confidence interval (using jacobian and residuals)
        # residuals = res.fun
        # _, s, VT = np.linalg.svd(res.jac, full_matrices=False)
        # threshold = np.finfo(float).eps * max(res.jac.shape) * s[0]
        # s = s[s > threshold]
        # pcov = np.dot(VT.T / s**2, VT)
        # confidenceInterval = np.sqrt(np.diag(pcov)) * chi2.ppf(0.95, df=len(residuals))
        out_final_fit = fitFunc(shiftX, sim_input)
    else:
        out_final_fit = {}
        shiftX = {}
        
    plot_MCDDA_histograms(D_track_length_matrix,
                              D_track_length_matrix_normalized,
                              sim_input,
                              out_initial_guess,
                              out_final_fit,
                              input_parameter,
                              shiftX,
                              start_values_fitting)

def plot_MCDDA_histograms(D_track_length_matrix,
                          D_track_length_matrix_normalized,
                          sim_input,
                          out_initial_guess,
                          out_final_fit,
                          input_parameter,
                          shiftX,
                          start_values_fitting):
    # Define the histogram edges for diffusion coefficients
    edges = D_track_length_matrix['Bins']

    # Plotting setup
    nrows_temp = math.ceil(len(sim_input['tracklengths_steps']) / 2.0)    
    fig, axs = plt.subplots(nrows = nrows_temp, ncols=2, figsize=(10, 10))

    # Plot histograms for each track length
    sum_of_squares=0
    # for i, ax in enumerate(axs.flat):
    for i, ax in enumerate(sim_input['tracklengths_steps']):
        ax = axs.flat[i]
        print(f"i: {i}, sim_input['tracklengths_steps'][i]: {sim_input['tracklengths_steps'][i]}")
        if i < len(sim_input['tracklengths_steps']):
            ax.set_title(f"D distribution for track length {sim_input['tracklengths_steps'][i]} steps")
        else:
            ax.set_title(f"D distribution for track lengths >= {sim_input['tracklengths_steps'][i]} steps")

        # Filter the experimental data for the current track length (i)
        ax.stairs(D_track_length_matrix_normalized.loc[D_track_length_matrix_normalized.index[:-1],
                  sim_input['tracklengths_steps'][i]],
                  edges, color='lightgray', fill = True)  

        # Plot steps for initial guesses
        ax.step(edges, out_initial_guess.loc[out_initial_guess.index[:],
                sim_input['tracklengths_steps'][i]],
                color = 'red',
                where = 'post')  
  
        # Plot final fit results if fitting was performed
        if sim_input['perform_fitting']:
            ax.step(edges, out_final_fit.loc[out_final_fit.index[:],
                    sim_input['tracklengths_steps'][i]],
                    color = 'black',
                    where = 'post') 
 
        if sim_input['plot_option_axes']=='logarithmic':
            ax.set_xscale('log')
        
        
        ax.set_xlim([sim_input['plot_diff_hist_min'], sim_input['plot_diff_hist_max']])
        ax.set_xlabel('Diffusion coefficient (µm^2/s)')
        ax.set_ylabel('Probability')
        
        part_guess = out_initial_guess.loc[out_initial_guess.index[:-1],
                                           sim_input['tracklengths_steps'][i]]       
        part_data = D_track_length_matrix_normalized.loc[D_track_length_matrix_normalized.index[:-1],
                                                         sim_input['tracklengths_steps'][i]]
        print(f"i: {i}, sum-of-squares [guess vs. data]: {round(np.sum(( part_guess - part_data )**2),4)}")
        
        if sim_input['perform_fitting']:
            part_fit = out_final_fit.loc[out_final_fit.index[:-1],
                                         sim_input['tracklengths_steps'][i]]
            sum_of_squares += np.sum(( part_fit - part_data )**2)
            print(f"i: {i}, sum-of-squares [fit vs. data]: {round(sum_of_squares,4)}")
                      
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout so the suptitle doesn't overlap
    if sim_input['perform_fitting']:
        string_out = np.round(shiftX,2)
        fig.suptitle(f"Histogram of diffusion coefficients per track length: Final D_s and k_s: {string_out}")
    else:
        fig.suptitle("Histogram of diffusion coefficients per track length")
    
    # fig.suptitle('Histogram of diffusion coefficients per track length')
    temp_path = os.path.join(input_parameter['data_dir'],
                             input_parameter['default_output_dir'])
    
    # breakpoint()
    plt.savefig(temp_path + input_parameter['fn_combined_movies'][:-4] + 
                '_Fig03_MCDDA.' + input_parameter['plot_option_save'],
                dpi = input_parameter['dpi'])
  
    plt.show()
   
    if sim_input['perform_fitting']:
        print(f"Sum of squares: {round(sum_of_squares/len(sim_input['tracklengths_steps']),4)}")
        print(f"Final parameters D_s and k_s: {np.round(shiftX,2)}")
        print(f"Initial guesses: {np.round(start_values_fitting,2)}")
        print(f"Loc error (µm): {np.round(sim_input['loc_error'],4)}")

def fitFunc(start_values_fitting, sim_input):
    """ Sub-function for fitting """   
    print("...Sub-function for fitting...")
    ii = sim_input['species_to_select'] 
    if sim_input['species'][ii]['#_states'] == 1:
        # Python: to get the first two values use 0:2 not 0:1
        sim_input['species'][ii]['diff_quot'] = np.array(start_values_fitting[0:1]) 
    elif sim_input['species'][ii]['#_states'] == 2:
        sim_input['species'][ii]['diff_quot'] = np.array(start_values_fitting[0:2]) 
        sim_input['species'][ii]['rates'] = start_values_fitting[2:4]
    elif sim_input['species'][ii]['#_states'] >= 3:
        sim_input['species'][ii]['diff_quot'] = np.array(start_values_fitting[0:3])
        sim_input['species'][ii]['rates'] = start_values_fitting[3:9]
    
    # Call the simulation initialization function
    particleData, sim_input = initiate_simulation(sim_input)

    # Simulate the particle diffusion and generate tracks
    _, tracks = diffusion_simulation(sim_input, particleData)

    # Function to calculate diffusion coefficients for different track lengths
    sorted_tracks = tracks.sort_values(by=['track_id', 'frame']) 
    _, D_track_length_matrix = diff_coeffs_from_tracks_fast(sorted_tracks, sim_input)

    # Normalize the matrix
    D_track_length_matrix.loc[:, list(sim_input['tracklengths_steps'])] /= np.sum(D_track_length_matrix.loc[:, list(sim_input['tracklengths_steps'])], axis=0)
    
    return D_track_length_matrix


