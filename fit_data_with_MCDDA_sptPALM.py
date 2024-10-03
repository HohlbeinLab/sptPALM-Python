#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, least_squares
from scipy.stats import chi2
from initiate_simulation import initiate_simulation
from diffusion_simulation import diffusion_simulation
from diff_coeffs_from_tracks_fast import diff_coeffs_from_tracks_fast

def fit_data_with_MCDDA_sptPALM(D_track_length_matrix, sim_input):
    print("\nRun diff_coeffs_from_tracks_fast.py")

    # Check if fitting is supported for multiple species
    if sim_input['#_species'] > 1:
        raise ValueError('Careful. Fitting is currently only supported for a single species!')
    
    ii = sim_input['species_to_select']  # Index for species

    # Temporarily set displayFigures to False
    sim_input['display_figures'] = False

    # Normalize the D_track_length_matrix
    D_track_length_matrix_normalized = D_track_length_matrix.copy()
    D_track_length_matrix_normalized.loc[:, list(sim_input['track_lengths'])] /= np.sum(D_track_length_matrix_normalized.loc[:, list(sim_input['track_lengths'])], axis=0)

    # Define the histogram edges for diffusion coefficients
    edges = D_track_length_matrix['Bins']

    # Plotting setup
    fig, axs = plt.subplots(nrows=(len(sim_input['track_lengths']) + 1) // 2, ncols=2, figsize=(10, 10))
    fig.suptitle('Histogram of diffusion coefficients per track length')

    # Initial guesses and bounds
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
    
        if sim_input['species'][ii]['#_states'] == 2:
            sim_input['species'][ii]['diff_quot'] = np.array(params[0:2]) #/ sim_input['multiplicator']
            sim_input['species'][ii]['rates'] = params[2:4]
        elif sim_input['species'][ii]['#_states'] == 3:
            sim_input['species'][ii]['diff_quot'] = np.array(params[0:3]) #/ sim_input['multiplicator']
            sim_input['species'][ii]['rates'] = params[3:9]
        
        # Run the simulation
        particleData, sim_input = initiate_simulation(sim_input)
        _, tracks = diffusion_simulation(sim_input, particleData)
    
        # Calculate diffusion coefficients and flatten the matrix
        sorted_tracks = tracks.sort_values(by=['track_id', 'frame'])
        _, D_track_length_matrix = diff_coeffs_from_tracks_fast(sorted_tracks, sim_input, max(sim_input['track_lengths']) + 1)
    
        # Normalize and linearize the matrix
        D_track_length_matrix.loc[:, list(sim_input['track_lengths'])] /= np.sum(D_track_length_matrix.loc[:, list(sim_input['track_lengths'])], axis=0)
        linearized_array = D_track_length_matrix.values.ravel()
    
        return linearized_array
    
    def residuals(params, sim_input, ground_truth):
        """Residual function for least_squares"""
        simulated_data = fitFunc_1D(None, params, sim_input)  # Simulate using params
        return simulated_data - ground_truth  # Return the difference


    # Options for curve fitting (using scipy's least_squares)
    experimental_data = D_track_length_matrix_normalized.values.ravel()
    if sim_input['perform_fitting']:
        
        
        # res = curve_fit(lambda x, *params: fitFunc_1D(x, params, sim_input),
        #                     np.arange(len(experimental_data)),
        #                     experimental_data,  
        #                     p0 = start_values_fitting,
        #                     method = 'dogbox', # options trf, dogbox
        #                     bounds=(lower_bounds, upper_bounds),
        #                     ) 
        res = least_squares(residuals, 
                            start_values_fitting,
                            method = 'dogbox', # options trf, dogbox
                            bounds=(lower_bounds, upper_bounds),
                            args=(sim_input,experimental_data),
                            loss = 'soft_l1', # cauchy: crap
                            x_scale = [1,1,0.01, 0.01],
                            diff_step = [0.2, 0.2, 25, 25],
                            # max_nfev = 10,
                            verbose=2) #,callback=callback_func
        
        shiftX = res.x

        # Calculate 95% confidence interval (using jacobian and residuals)
        residuals = res.fun
        _, s, VT = np.linalg.svd(res.jac, full_matrices=False)
        threshold = np.finfo(float).eps * max(res.jac.shape) * s[0]
        s = s[s > threshold]
        pcov = np.dot(VT.T / s**2, VT)
        confidenceInterval = np.sqrt(np.diag(pcov)) * chi2.ppf(0.95, df=len(residuals))
        out_final_fit = fitFunc(shiftX, sim_input)
   
    # Plot histograms for each track length
    # for i, ax in enumerate(axs.flat):
    for i, ax in enumerate(axs.flat):

        if i < len(sim_input['track_lengths']):
            ax.set_title(f"D distribution for track length {sim_input['track_lengths'][i]} steps")
        else:
            ax.set_title(f"D distribution for track lengths > {sim_input['track_lengths'][i]} steps")

        # breakpoint()
        # Filter the experimental data for the current track length (i)
        ax.stairs(D_track_length_matrix_normalized.loc[D_track_length_matrix_normalized.index[:-1],
                  sim_input['track_lengths'][i]],
                  edges, color='lightgray', fill = True)  # 'count' corresponds to `density=False`


        # Plot steps for initial guesses
        ax.step(edges, out_initial_guess.loc[out_initial_guess.index[:],sim_input['track_lengths'][i]],
                color = 'red',
                where = 'post')  # 'count' corresponds to `density=False`
  
        # Plot final fit results if fitting was performed
        if sim_input['perform_fitting']:
            # ax.plot(out_final_fit[:, 0], out_final_fit[:, i + 1], color='black')
            ax.step(edges, out_final_fit.loc[out_final_fit.index[:],sim_input['track_lengths'][i]],
                    color = 'black',
                    where = 'post')  # 'count' corresponds to `density=False`
 
        ax.set_xscale('log')
        ax.set_xlim([sim_input['plot_diff_hist_min'], sim_input['plot_diff_hist_max']])
        ax.set_xlabel('Diffusion coefficient (µm^2/s)')
        ax.set_ylabel('#')
        
        part_guess = out_initial_guess.loc[out_initial_guess.index[:-1],sim_input['track_lengths'][i]]       
        part_data = D_track_length_matrix_normalized.loc[D_track_length_matrix_normalized.index[:-1], sim_input['track_lengths'][i]]
        part_fit = out_final_fit.loc[out_final_fit.index[:-1], sim_input['track_lengths'][i]]

        print(f"ii: {i}, sum-of-squares [guess vs. data]: {round(np.sum(( part_guess - part_data )**2),3)}")
        print(f"ii: {i}, sum-of-squares [fit vs. data]: {round(np.sum(( part_fit - part_data )**2),3)}")
        # print(f"ii: {i}, sum-of-squares: {np.sum((out_initial_guess.loc[out_initial_guess.index[:-1],sim_input['track_lengths'][i]] - D_track_length_matrix_normalized[:, i+1])**2)}")
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout so the suptitle doesn't overlap
    plt.show()

    # # Display shiftX based on species states
    # if sim_input['species'][sim_input['species_to_select'] ]['#_states'] == 2:
    #     shiftX[:2] = shiftX[:2] / sim_input['multiplicator']
    # elif sim_input['species'][sim_input['species_to_select'] ]['#_states'] == 3:
    #     shiftX[:3] = shiftX[:3] / sim_input['multiplicator']
    
    print(f"shiftX: {np.round(shiftX,2)}")

def fitFunc(start_values_fitting, sim_input):
    """ Sub-function for fitting """   
    print("...Sub-function for fitting...")
    ii = sim_input['species_to_select'] 

    # sim_input.species(ii).rates = [kAB, kBA];
    if sim_input['species'][ii]['#_states'] == 2:
        # Python: to get the first two values use 0:2 not 0:1
        sim_input['species'][ii]['diff_quot'] = np.array(start_values_fitting[0:2]) #/ sim_input['multiplicator']
        sim_input['species'][ii]['rates'] = start_values_fitting[2:4]
    # sim_input.species(ii).rates = [0,kAB,kAC; kBA,0,kBC; kCA,kCB,0];
    elif sim_input['species'][ii]['#_states'] == 3:
        sim_input['species'][ii]['diff_quot'] = np.array(start_values_fitting[0:3]) #/ sim_input['multiplicator']
        sim_input['species'][ii]['rates'] = start_values_fitting[3:9]
    
    # Call the simulation initialization function
    particleData, sim_input = initiate_simulation(sim_input)

    # Simulate the particle diffusion and generate tracks
    _, tracks = diffusion_simulation(sim_input, particleData)

    # Function to calculate diffusion coefficients for different track lengths
    sorted_tracks = tracks.sort_values(by=['track_id', 'frame']) 
    _, D_track_length_matrix = diff_coeffs_from_tracks_fast(sorted_tracks, sim_input, max(sim_input['track_lengths']) + 1)

    # Normalize the matrix
    D_track_length_matrix.loc[:, list(sim_input['track_lengths'])] /= np.sum(D_track_length_matrix.loc[:, list(sim_input['track_lengths'])], axis=0)
    
    return D_track_length_matrix


