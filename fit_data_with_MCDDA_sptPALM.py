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

def FitSimulatedData(D, DtrackLengthMatrix, simInput):
    # Check if fitting is supported for multiple species
    if simInput['numberSpecies'] > 1:
        raise ValueError('Careful. Fitting is currently only supported for a single species!')
    
    ii = 1  # Index for species

    # Temporarily set displayFigures to False
    simInput['displayFigures'] = False

    # Normalize the DtrackLengthMatrix
    DtrackLengthMatrixNorm = DtrackLengthMatrix.copy()
    DtrackLengthMatrixNorm[:, 1:] = DtrackLengthMatrixNorm[:, 1:] / np.sum(DtrackLengthMatrixNorm[:, 1:], axis=0)

    # Define the histogram edges for diffusion coefficients
    edges = np.arange(np.log10(simInput['plotDiffHist_min']), np.log10(simInput['plotDiffHist_max']), simInput['binWidth'])

    # Fit function (see subfunction)
    def fitFunc(shiftX, *args):
        return funcFit(shiftX, simInput)
    
    # Plotting setup
    fig, axs = plt.subplots(nrows=(len(simInput['trackLengths']) + 1) // 2, ncols=2, figsize=(10, 10))
    fig.suptitle('Histogram of diffusion coefficients per track length')

    # Initial guesses and bounds
    startValuesFitting = np.concatenate([simInput['species'][ii]['diffQuot_initGuess'], simInput['species'][ii]['rates_initGuess']])
    lowerbound = np.concatenate([simInput['species'][ii]['diffQuot_lb_ub'][0], simInput['species'][ii]['rates_lb_ub'][0]])
    upperbound = np.concatenate([simInput['species'][ii]['diffQuot_lb_ub'][1], simInput['species'][ii]['rates_lb_ub'][1]])

    # Initial output
    outInitGuess = fitFunc(startValuesFitting, simInput)

    # Options for curve fitting (using scipy's least_squares)
    if simInput['performFitting']:
        res = least_squares(fitFunc, startValuesFitting, bounds=(lowerbound, upperbound), args=(simInput,))
        shiftX = res.x

        # Calculate 95% confidence interval (using jacobian and residuals)
        residuals = res.fun
        _, s, VT = np.linalg.svd(res.jac, full_matrices=False)
        threshold = np.finfo(float).eps * max(res.jac.shape) * s[0]
        s = s[s > threshold]
        pcov = np.dot(VT.T / s**2, VT)
        confidenceInterval = np.sqrt(np.diag(pcov)) * chi2.ppf(0.95, df=len(residuals))
        outFinalFit = fitFunc(shiftX, simInput)

    # Plot histograms for each track length
    for i, ax in enumerate(axs.flat):
        if i < len(simInput['trackLengths']):
            ax.set_title(f"D distribution for track length {simInput['trackLengths'][i]} steps")
        else:
            ax.set_title(f"D distribution for track lengths > {simInput['trackLengths'][i]} steps")

        ax.hist(D[D[:, 1] == i, 0], bins=10 ** edges, density=True, alpha=0.4, color='gray')

        # Plot initial guesses
        ax.plot(outInitGuess[:, 0], outInitGuess[:, i + 1], color='red')

        # Plot final fit results if fitting was performed
        if simInput['performFitting']:
            ax.plot(outFinalFit[:, 0], outFinalFit[:, i + 1], color='black')

        ax.set_xscale('log')
        ax.set_xlim([simInput['plotDiffHist_min'], simInput['plotDiffHist_max']])
        ax.set_xlabel('Diffusion coefficient (µm^2/s)')
        ax.set_ylabel('#')

        print(f"ii: {i}, sum-of-squares: {np.sum((outInitGuess[:, i+1] - DtrackLengthMatrixNorm[:, i+1])**2)}")

    plt.tight_layout()
    plt.show()

    # Display shiftX based on species states
    if simInput['species'][0]['numberStates'] == 2:
        shiftX[:2] = shiftX[:2] / simInput['multiplicator']
    elif simInput['species'][0]['numberStates'] == 3:
        shiftX[:3] = shiftX[:3] / simInput['multiplicator']
    
    print(f"shiftX: {shiftX}")

def funcFit(start, simInput):
    """ Sub-function for fitting """
    if simInput['species'][0]['numberStates'] == 2:
        simInput['species'][0]['diffQuot'] = start[:2] / simInput['multiplicator']
        simInput['species'][0]['rates'] = start[2:4]
    elif simInput['species'][0]['numberStates'] == 3:
        simInput['species'][0]['diffQuot'] = start[:3] / simInput['multiplicator']
        simInput['species'][0]['rates'] = start[3:9]

    # Call the simulation initialization function
    particleData, simInput = InitiateSimulation(simInput)

    # Simulate the particle diffusion and generate tracks
    _, tracks = particleDiffusion(simInput, particleData)

    # Generate diffusion coefficients from the tracks
    _, DtrackLengthMatrix = GenerateDfromtracks_Sim(tracks, simInput, max(simInput['trackLengths']) + 1)

    # Normalize the matrix
    DtrackLengthMatrix[:, 1:] = DtrackLengthMatrix[:, 1:] / np.sum(DtrackLengthMatrix[:, 1:], axis=0)
    
    return DtrackLengthMatrix
