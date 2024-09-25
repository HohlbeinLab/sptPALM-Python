#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 20:58:09 2024

@author: hohlbein
"""
 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

def particle_diffusion(sim_input, particle_data):
    
    # Initialize particle localizations and add localization noise
    loc_error_matrix = np.random.normal(0, sim_input['loc_error'], (sim_input['total_number_particles'], 3))

    # Tracks matrix: structure -> x values, y values, frame number, track id, frame time
    tracks = np.zeros((0, 5))
    valid_x = ~np.isnan(particle_data['xPos'])
    tracks = np.column_stack((
        particle_data['xPos'][valid_x] + loc_error_matrix[valid_x, 0],  # x-values
        particle_data['yPos'][valid_x] + loc_error_matrix[valid_x, 1],  # y-values
        np.ones(np.sum(valid_x)),  # frame, currently first frame
        particle_data['particle'][valid_x],  # track_ID
        sim_input['frametime'] * np.ones(np.sum(valid_x))  # frametime
    ))

    print('Start of simulation')

    # Initialize video recording if needed
    if sim_input['display_figures']:
        writer = FFMpegWriter(fps=10)
        fig = plt.figure()
        plt.xlim([0, sim_input['radius_cell'] + 2 * sim_input['length_cell']])
        plt.ylim([-sim_input['radius_cell'], sim_input['radius_cell']])
        ax = fig.add_subplot(111, projection='3d')

    # Main simulation loop
    for step_counter in range(1, int(max(sim_input['track_lengths']) * sim_input['frametime'] / sim_input['steptime']) + 1):
        
        temp_xyz_steps = np.zeros((sim_input['total_number_particles'], 3))
        
        for ii in range(sim_input['#_species']):
            # Get species-specific particles
            loc_species = np.where(particle_data['species'] == ii + 1)[0]
            loc_state_changes = loc_species[particle_data['state_time_remaining'][loc_species] < sim_input['steptime']]
            
            if len(loc_state_changes) > 0:
                num_states = sim_input['species'][ii]['#_states']
                rates = sim_input['species'][ii]['rates']
                diff_quot = sim_input['species'][ii]['diff_quot']

                if num_states == 2:
                    handle_two_state(particle_data, loc_state_changes, rates, diff_quot, sim_input)
                elif num_states == 3:
                    handle_three_state(particle_data, loc_state_changes, rates, diff_quot, sim_input)
                elif num_states == 4:
                    handle_four_state(particle_data, loc_state_changes, rates, diff_quot, sim_input)
                else:
                    raise ValueError('Something went wrong with the state handling')

            # Calculate random steps in X, Y, Z direction
            temp_xyz_steps[loc_species, :] = np.sqrt(
                2 * particle_data['active_diff_quot'][loc_species] * sim_input['steptime']
            ) * np.random.randn(len(loc_species), 3)

            # Apply boundary conditions if needed
            if sim_input['confineDiffusion']:
                apply_boundary_conditions(particle_data, temp_xyz_steps, loc_species, sim_input)

            # Update particle positions
            particle_data['xPos'][loc_species] += temp_xyz_steps[loc_species, 0] * (~particle_data['posReject'][loc_species])
            particle_data['yPos'][loc_species] += temp_xyz_steps[loc_species, 1] * (~particle_data['posReject'][loc_species])
            particle_data['zPos'][loc_species] += temp_xyz_steps[loc_species, 2] * (~particle_data['posReject'][loc_species])

        # Decrease remaining track and state times
        particle_data['trackLengthRemain'][particle_data['trackLengthRemain'] > sim_input['avoidFloat0']] -= sim_input['steptime'] / sim_input['frametime']
        particle_data['state_time_remaining'][particle_data['state_time_remaining'] > sim_input['avoidFloat0']] -= sim_input['steptime']
        
        # Mark particles that 'bleached' as NaN
        delete_entries = np.where(particle_data['trackLengthRemain'] < sim_input['avoidFloat0'])[0]
        particle_data['xPos'][delete_entries] = np.nan
        particle_data['yPos'][delete_entries] = np.nan
        particle_data['zPos'][delete_entries] = np.nan
        particle_data['trackLengthRemain'][delete_entries] = 0

        # Record the positions every frame
        if step_counter % int(sim_input['frametime'] / sim_input['steptime']) == 0:
            print(f' Round: {step_counter // (sim_input["frametime"] / sim_input["steptime"])}, Steps simulated: {step_counter}')
            
            if sim_input['displayFigures']:
                plt.cla()
                ax.scatter(particle_data['xPos'], particle_data['yPos'], particle_data['zPos'])
                ax.set_xlabel('x (µm)')
                ax.set_ylabel('y (µm)')
                ax.set_zlabel('z (µm)')
                ax.set_title(f'frame: {step_counter // (sim_input["frametime"] / sim_input["steptime"])}')
                writer.grab_frame()

            loc_error_matrix = np.random.normal(0, sim_input['loc_error'], (len(particle_data['xPos']), 3))
            valid_x = ~np.isnan(particle_data['xPos'])
            tracks_temp = np.column_stack((
                particle_data['xPos'][valid_x] + loc_error_matrix[valid_x, 0],  # x-values
                particle_data['yPos'][valid_x] + loc_error_matrix[valid_x, 1],  # y-values
                np.ones(np.sum(valid_x)) * (1 + step_counter // (sim_input['frametime'] / sim_input['steptime'])),
                particle_data['particle'][valid_x],  # track_ID
                sim_input['frametime'] * np.ones(np.sum(valid_x))  # frametime
            ))
            tracks = np.vstack([tracks, tracks_temp])

    print(f'Number of remaining particles (not bleached): {np.sum(particle_data["trackLengthRemain"] > sim_input["avoidFloat0"])}')

    if sim_input['displayFigures']:
        plt.close()

    return particle_data, tracks

def apply_boundary_conditions(particle_data, temp_xyz_steps, loc_species, sim_input):
    # Left part of the cell boundary condition
    reject_pos_left_part = (particle_data['xPos'][loc_species] + temp_xyz_steps[loc_species, 0] < sim_input['radius_cell']) & (
        (particle_data['xPos'][loc_species] + temp_xyz_steps[loc_species, 0] - sim_input['radius_cell'])**2 +
        (particle_data['yPos'][loc_species] + temp_xyz_steps[loc_species, 1])**2 +
        (particle_data['zPos'][loc_species] + temp_xyz_steps[loc_species, 2])**2 > sim_input['radius_cell']**2
    )

    # Cylindrical part of the boundary condition
    reject_pos_cylinder_part = (
        (particle_data['yPos'][loc_species] + temp_xyz_steps[loc_species, 1])**2 +
        (particle_data['zPos'][loc_species] + temp_xyz_steps[loc_species, 2])**2 > sim_input['radius_cell']**2
    )

    # Right part of the cell boundary condition
    reject_pos_right_part = (particle_data['xPos'][loc_species] + temp_xyz_steps[loc_species, 0] > (sim_input['length_cell'] + sim_input['radius_cell'])) & (
        (particle_data['xPos'][loc_species] + temp_xyz_steps[loc_species, 0] - (sim_input['length_cell'] + sim_input['radius_cell']))**2 +
        (particle_data['yPos'][loc_species] + temp_xyz_steps[loc_species, 1])**2 +
        (particle_data['zPos'][loc_species] + temp_xyz_steps[loc_species, 2])**2 > sim_input['radius_cell']**2
    )

    # Combine all positions that violate the boundary conditions
    particle_data['posReject'][loc_species] = reject_pos_left_part | reject_pos_cylinder_part | reject_pos_right_part


def handle_two_state(particle_data, loc_state_changes, rates, diff_quot, sim_input):
    kAB, kBA = rates
    particle_data['active_state'][loc_state_changes] = particle_data['next_state'][loc_state_changes]
    
    
    
    particle_data['active_diff_quot'][loc_state_changes] = diff_quot[particle_data['active_state'][loc_state_changes]]


        # Assign active diffusion quotient for each particle
        # Convert 'active_state' to a numpy array
        active_states = particle_data.loc[loc_species, 'active_state'].astype(int).to_numpy() 
        
        # Use the active_states array to index into the diff_quot list
        particle_data.loc[loc_species, 'active_diff_quot'] = np.array(sim_input['species'][ii]['diff_quot'])[active_states]



    
    find_state_A = loc_state_changes[particle_data['active_state'][loc_state_changes] == 1]
    particle_data['next_state'][find_state_A] = 2
    particle_data['state_time_remaining'][find_state_A] = np.log(np.random.rand(len(find_state_A))) / (-kAB)
    
    find_state_B = loc_state_changes[particle_data['active_state'][loc_state_changes] == 2]
    particle_data['next_state'][find_state_B] = 1
    particle_data['state_time_remaining'][find_state_B] = np.log(np.random.rand(len(find_state_B))) / (-kBA)


def handle_three_state(particle_data, loc_state_changes, rates, diff_quot, sim_input):
    kAB, kBA, kBC, kCB, kAC, kCA = rates

    # Change state to the next, already known state
    particle_data['active_state'][loc_state_changes] = particle_data['next_state'][loc_state_changes]
    # Update diffusion coefficient depending on the current state
    particle_data['active_diff_quot'][loc_state_changes] = diff_quot[particle_data['active_state'][loc_state_changes]]
    
    # Generate random values for state transitions
    temp_rand = np.random.rand(len(loc_state_changes), 2)

    # State A transitions
    find_state_A = loc_state_changes[particle_data['active_state'][loc_state_changes] == 1]
    # A to B
    temp_switch_AB = find_state_A[kAB / (kAB + kAC) >= temp_rand[find_state_A, 0]]
    particle_data['next_state'][temp_switch_AB] = 2
    particle_data['state_time_remaining'][temp_switch_AB] = np.log(temp_rand[temp_switch_AB, 1]) / -kAB
    # A to C
    temp_switch_AC = find_state_A[kAB / (kAB + kAC) < temp_rand[find_state_A, 0]]
    particle_data['next_state'][temp_switch_AC] = 3
    particle_data['state_time_remaining'][temp_switch_AC] = np.log(temp_rand[temp_switch_AC, 1]) / -kAC

    # State B transitions
    find_state_B = loc_state_changes[particle_data['active_state'][loc_state_changes] == 2]
    # B to A
    temp_switch_BA = find_state_B[kBA / (kBA + kBC) >= temp_rand[find_state_B, 0]]
    particle_data['next_state'][temp_switch_BA] = 1
    particle_data['state_time_remaining'][temp_switch_BA] = np.log(temp_rand[temp_switch_BA, 1]) / -kBA
    # B to C
    temp_switch_BC = find_state_B[kBA / (kBA + kBC) < temp_rand[find_state_B, 0]]
    particle_data['next_state'][temp_switch_BC] = 3
    particle_data['state_time_remaining'][temp_switch_BC] = np.log(temp_rand[temp_switch_BC, 1]) / -kBC

    # State C transitions
    find_state_C = loc_state_changes[particle_data['active_state'][loc_state_changes] == 3]
    # C to A
    temp_switch_CA = find_state_C[kCA / (kCA + kCB) >= temp_rand[find_state_C, 0]]
    particle_data['next_state'][temp_switch_CA] = 1
    particle_data['state_time_remaining'][temp_switch_CA] = np.log(temp_rand[temp_switch_CA, 1]) / -kCA
    # C to B
    temp_switch_CB = find_state_C[kCA / (kCA + kCB) < temp_rand[find_state_C, 0]]
    particle_data['next_state'][temp_switch_CB] = 2
    particle_data['state_time_remaining'][temp_switch_CB] = np.log(temp_rand[temp_switch_CB, 1]) / -kCB


def handle_four_state(particle_data, loc_state_changes, rates, diff_quot, sim_input):
    kAB, kBA, kBC, kCB, kCD, kDC = rates

    # Change state to the next, already known state
    particle_data['active_state'][loc_state_changes] = particle_data['next_state'][loc_state_changes]
    # Update diffusion coefficient depending on the current state
    particle_data['active_diff_quot'][loc_state_changes] = diff_quot[particle_data['active_state'][loc_state_changes]]
    
    # Generate random values for state transitions
    temp_rand = np.random.rand(len(loc_state_changes), 1)

    # State A to B
    find_state_A = loc_state_changes[particle_data['active_state'][loc_state_changes] == 1]
    particle_data['next_state'][find_state_A] = 2
    particle_data['state_time_remaining'][find_state_A] = np.log(temp_rand[find_state_A]) / -kAB

    # State B transitions
    find_state_B = loc_state_changes[particle_data['active_state'][loc_state_changes] == 2]
    # B to A
    temp_switch_BA = find_state_B[kBA / (kBA + kBC) >= temp_rand[find_state_B, 0]]
    particle_data['next_state'][temp_switch_BA] = 1
    particle_data['state_time_remaining'][temp_switch_BA] = np.log(temp_rand[temp_switch_BA]) / -kBA
    # B to C
    temp_switch_BC = find_state_B[kBA / (kBA + kBC) < temp_rand[find_state_B, 0]]
    particle_data['next_state'][temp_switch_BC] = 3
    particle_data['state_time_remaining'][temp_switch_BC] = np.log(temp_rand[temp_switch_BC]) / -kBC

    # State C transitions
    find_state_C = loc_state_changes[particle_data['active_state'][loc_state_changes] == 3]
    # C to B
    temp_switch_CB = find_state_C[kCB / (kCB + kCD) >= temp_rand[find_state_C, 0]]
    particle_data['next_state'][temp_switch_CB] = 2
    particle_data['state_time_remaining'][temp_switch_CB] = np.log(temp_rand[temp_switch_CB]) / -kCB
    # C to D
    temp_switch_CD = find_state_C[kCB / (kCB + kCD) < temp_rand[find_state_C, 0]]
    particle_data['next_state'][temp_switch_CD] = 4
    particle_data['state_time_remaining'][temp_switch_CD] = np.log(temp_rand[temp_switch_CD]) / -kCD

    # State D to C
    find_state_D = loc_state_changes[particle_data['active_state'][loc_state_changes] == 4]
    particle_data['next_state'][find_state_D] = 3
    particle_data['state_time_remaining'][find_state_D] = np.log(temp_rand[find_state_D]) / -kDC
