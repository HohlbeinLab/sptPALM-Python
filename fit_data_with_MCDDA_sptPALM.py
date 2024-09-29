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
from diff_coeffs_from_tracks_simulation import diff_coeffs_from_tracks_simulation

def FitSimulatedData(D, D_track_length_matrix, sim_input):
    print("\n  Run diff_coeffs_from_tracks_simulation.py")
    breakpoint()
    # Check if fitting is supported for multiple species
    if sim_input['numberSpecies'] > 1:
        raise ValueError('Careful. Fitting is currently only supported for a single species!')
    
    ii = 1  # Index for species

    # Temporarily set displayFigures to False
    sim_input['displayFigures'] = False

    # Normalize the D_track_length_matrix
    D_track_length_matrixNorm = D_track_length_matrix.copy()
    D_track_length_matrixNorm[:, 1:] = D_track_length_matrixNorm[:, 1:] / np.sum(D_track_length_matrixNorm[:, 1:], axis=0)

    # Define the histogram edges for diffusion coefficients
    edges = np.arange(np.log10(sim_input['plotDiffHist_min']), np.log10(sim_input['plotDiffHist_max']), sim_input['binWidth'])

    # Fit function (see subfunction)
    def fitFunc(shiftX, *args):
        return funcFit(shiftX, sim_input)
    
    # Plotting setup
    fig, axs = plt.subplots(nrows=(len(sim_input['trackLengths']) + 1) // 2, ncols=2, figsize=(10, 10))
    fig.suptitle('Histogram of diffusion coefficients per track length')

    # Initial guesses and bounds
    startValuesFitting = np.concatenate([sim_input['species'][ii]['diffQuot_initGuess'], sim_input['species'][ii]['rates_initGuess']])
    lowerbound = np.concatenate([sim_input['species'][ii]['diffQuot_lb_ub'][0], sim_input['species'][ii]['rates_lb_ub'][0]])
    upperbound = np.concatenate([sim_input['species'][ii]['diffQuot_lb_ub'][1], sim_input['species'][ii]['rates_lb_ub'][1]])

    # Initial output
    outInitGuess = fitFunc(startValuesFitting, sim_input)

    # Options for curve fitting (using scipy's least_squares)
    if sim_input['performFitting']:
        res = least_squares(fitFunc, startValuesFitting, bounds=(lowerbound, upperbound), args=(sim_input,))
        shiftX = res.x

        # Calculate 95% confidence interval (using jacobian and residuals)
        residuals = res.fun
        _, s, VT = np.linalg.svd(res.jac, full_matrices=False)
        threshold = np.finfo(float).eps * max(res.jac.shape) * s[0]
        s = s[s > threshold]
        pcov = np.dot(VT.T / s**2, VT)
        confidenceInterval = np.sqrt(np.diag(pcov)) * chi2.ppf(0.95, df=len(residuals))
        outFinalFit = fitFunc(shiftX, sim_input)

    # Plot histograms for each track length
    for i, ax in enumerate(axs.flat):
        if i < len(sim_input['trackLengths']):
            ax.set_title(f"D distribution for track length {sim_input['trackLengths'][i]} steps")
        else:
            ax.set_title(f"D distribution for track lengths > {sim_input['trackLengths'][i]} steps")

        ax.hist(D[D[:, 1] == i, 0], bins=10 ** edges, density=True, alpha=0.4, color='gray')

        # Plot initial guesses
        ax.plot(outInitGuess[:, 0], outInitGuess[:, i + 1], color='red')

        # Plot final fit results if fitting was performed
        if sim_input['performFitting']:
            ax.plot(outFinalFit[:, 0], outFinalFit[:, i + 1], color='black')

        ax.set_xscale('log')
        ax.set_xlim([sim_input['plotDiffHist_min'], sim_input['plotDiffHist_max']])
        ax.set_xlabel('Diffusion coefficient (µm^2/s)')
        ax.set_ylabel('#')

        print(f"ii: {i}, sum-of-squares: {np.sum((outInitGuess[:, i+1] - D_track_length_matrixNorm[:, i+1])**2)}")

    plt.tight_layout()
    plt.show()

    # Display shiftX based on species states
    if sim_input['species'][0]['numberStates'] == 2:
        shiftX[:2] = shiftX[:2] / sim_input['multiplicator']
    elif sim_input['species'][0]['numberStates'] == 3:
        shiftX[:3] = shiftX[:3] / sim_input['multiplicator']
    
    print(f"shiftX: {shiftX}")

def funcFit(start, sim_input):
    """ Sub-function for fitting """
    if sim_input['species'][0]['numberStates'] == 2:
        sim_input['species'][0]['diffQuot'] = start[:2] / sim_input['multiplicator']
        sim_input['species'][0]['rates'] = start[2:4]
    elif sim_input['species'][0]['numberStates'] == 3:
        sim_input['species'][0]['diffQuot'] = start[:3] / sim_input['multiplicator']
        sim_input['species'][0]['rates'] = start[3:9]

    # Call the simulation initialization function
    particleData, sim_input = initiate_simulation(sim_input)

    # Simulate the particle diffusion and generate tracks
    _, tracks = diffusion_simulation(sim_input, particleData)

    # Generate diffusion coefficients from the tracks
    _, D_track_length_matrix = diff_coeffs_from_tracks_simulation(tracks, sim_input, max(sim_input['trackLengths']) + 1)

    # Normalize the matrix
    D_track_length_matrix[:, 1:] = D_track_length_matrix[:, 1:] / np.sum(D_track_length_matrix[:, 1:], axis=0)
    
    return D_track_length_matrix
