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
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import time

def diffusion_simulation(sim_input, particle_data):
    print('\nRun diffusion_simulation.py')
    # Initialize particle localizations and add localization noise
    loc_error_matrix = np.random.normal(0, sim_input['loc_error'], (sim_input['total_number_particles'], 3))

    columns_pd = ['x [µm]', 'y [µm]', 'frame', 'track_id', 'frametime']
    tracks = pd.DataFrame(columns = columns_pd)
    valid_x = ~np.isnan(particle_data['xPos'])

    tracks[columns_pd] = pd.DataFrame({
        columns_pd[0]: particle_data.loc[valid_x, 'xPos'].values + loc_error_matrix[valid_x, 0],  # x-values with error
        columns_pd[1]: particle_data.loc[valid_x, 'yPos'].values + loc_error_matrix[valid_x, 1],  # y-values with error
        columns_pd[2]: 1,  # Frame number (set to 1)
        columns_pd[3]: particle_data.loc[valid_x, 'particle'].values,  # Track ID
        columns_pd[4]: sim_input['frametime']  # Frame time (constant)
    })
    
    # Initialize video recording if needed
    if sim_input['display_figures']:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # Manually open the video writer
        writer = PillowWriter(fps=5)  # Set the frame rate for GIF
        writer.setup(fig, "Diffusion.gif", dpi=200)

    start = time.time()
    
    # Main simulation loop
    for step_counter in range(1, int(max(sim_input['track_lengths']) * sim_input['frametime'] / sim_input['steptime']) + 1):

        temp_xyz_steps = np.zeros((sim_input['total_number_particles'], 3))
        
        for ii in range(sim_input['#_species']):
            # Get species-specific particles
            loc_species = np.where((particle_data['species'] == ii) & (particle_data['track_length_remaining'] > 0))[0]

            loc_state_changes = loc_species[particle_data.loc[loc_species, 'state_time_remaining'] < sim_input['steptime']]
            
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
                2 * particle_data.loc[loc_species, 'active_diff_quot'].values[:, np.newaxis] * sim_input['steptime']
            ) * np.random.randn(len(loc_species), 3)

            # Apply boundary conditions if needed
            if sim_input['confined_diffusion']:
                apply_boundary_conditions(particle_data, temp_xyz_steps, loc_species, sim_input)

            # Update particle positions
            particle_data.loc[loc_species, 'xPos'] += temp_xyz_steps[loc_species, 0] * (~particle_data.loc[loc_species, 'pos_reject'])
            particle_data.loc[loc_species, 'yPos'] += temp_xyz_steps[loc_species, 1] * (~particle_data.loc[loc_species, 'pos_reject'])
            particle_data.loc[loc_species, 'zPos'] += temp_xyz_steps[loc_species, 2] * (~particle_data.loc[loc_species, 'pos_reject'])

        # Decrease remaining track and state times
        check_length_remaining = particle_data['track_length_remaining'] > sim_input['avoidFloat0']
        particle_data.loc[check_length_remaining, 'track_length_remaining'] -= sim_input['steptime'] / sim_input['frametime']
        
        check_state_time_remaining = particle_data['state_time_remaining'] > sim_input['avoidFloat0']
        particle_data.loc[check_state_time_remaining, 'state_time_remaining'] -= sim_input['steptime']
        
        # Mark particles that 'bleached' as NaN
        delete_entries = np.where(particle_data['track_length_remaining'] < sim_input['avoidFloat0'])[0]
        particle_data.loc[delete_entries, ['xPos', 'yPos','zPos']] = np.nan
        particle_data.loc[delete_entries, 'track_length_remaining'] = 0

        # Record the positions every frame
        if step_counter % int(sim_input['frametime'] / sim_input['steptime']) == 0:
            print(f'  Frame {int(step_counter) // (sim_input["frametime"] / sim_input["steptime"])}: {step_counter} steps simulated')
            
            if sim_input['display_figures']:
                plt.cla()  # Clear the plot for the new frame
                # ax = fig.add_subplot(111, projection='3d')
                ax.scatter(particle_data['xPos'], particle_data['yPos'], particle_data['zPos'])
                ax.set_xlim([0, sim_input['total_length_cell']])
                ax.set_ylim([-sim_input['radius_cell'], sim_input['radius_cell']])
                ax.set_zlim([-sim_input['radius_cell'], sim_input['radius_cell']])
                ax.set_xlabel('x (µm)')
                ax.set_ylabel('y (µm)')
                ax.set_zlabel('z (µm)')
                ax.set_title(f'frame: {step_counter // (sim_input["frametime"] / sim_input["steptime"])}')
                # Save the current frame to the GIF
                writer.grab_frame()
            
            # loc_error_matrix = np.random.normal(0, sim_input['loc_error'], (len(particle_data['xPos']), 3))
            valid_x = ~np.isnan(particle_data['xPos'])
            loc_error_matrix[valid_x, :] = np.random.normal(0, sim_input['loc_error'], (np.sum(valid_x), 3))
            tracks_temp = pd.DataFrame(columns = columns_pd)            
            tracks_temp[columns_pd] = pd.DataFrame({
                columns_pd[0]: particle_data.loc[valid_x, 'xPos'].values + loc_error_matrix[valid_x, 0],  # x-values with error
                columns_pd[1]: particle_data.loc[valid_x, 'yPos'].values + loc_error_matrix[valid_x, 1],  # y-values with error
                columns_pd[2]: (1 + step_counter // (sim_input['frametime'] / sim_input['steptime'])), 
                columns_pd[3]: particle_data.loc[valid_x, 'particle'].values,  # Track ID
                columns_pd[4]: sim_input['frametime']  # Frame time (constant)
            })
            
            tracks = pd.concat([df for df in [tracks, tracks_temp] if not df.empty], ignore_index=True)
    print(f'  Number of remaining particles (not bleached): {np.sum(particle_data["track_length_remaining"] > sim_input["avoidFloat0"])}')

    if sim_input['display_figures']:
        # Manually close the video writer
        writer.finish()
        plt.close(fig)
        plt.show()

    # How long did the tracking take?
    end = time.time()
    rounded_time = round(end-start, 2)
    print(f"  Time for tracking: {rounded_time} seconds")

    return particle_data, tracks

def apply_boundary_conditions(particle_data, temp_xyz_steps, loc_species, sim_input):
    # Left part of the cell boundary condition
    reject_pos_left_part = (particle_data.loc[loc_species, 'xPos'][loc_species] + temp_xyz_steps[loc_species, 0] < sim_input['radius_cell']) & (
        (particle_data.loc[loc_species, 'xPos'] + temp_xyz_steps[loc_species, 0] - sim_input['radius_cell'])**2 +
        (particle_data.loc[loc_species, 'yPos'] + temp_xyz_steps[loc_species, 1])**2 +
        (particle_data.loc[loc_species, 'zPos'] + temp_xyz_steps[loc_species, 2])**2 > sim_input['radius_cell']**2
    )

    # Cylindrical part of the boundary condition
    reject_pos_cylinder_part = (
        (particle_data.loc[loc_species, 'yPos'] + temp_xyz_steps[loc_species, 1])**2 +
        (particle_data.loc[loc_species, 'zPos'] + temp_xyz_steps[loc_species, 2])**2 > sim_input['radius_cell']**2
    )

    # Right part of the cell boundary condition
    reject_pos_right_part = (particle_data.loc[loc_species, 'xPos'] + temp_xyz_steps[loc_species, 0] > (sim_input['length_cell'] + sim_input['radius_cell'])) & (
        (particle_data.loc[loc_species, 'xPos'] + temp_xyz_steps[loc_species, 0] - (sim_input['length_cell'] + sim_input['radius_cell']))**2 +
        (particle_data.loc[loc_species, 'yPos'] + temp_xyz_steps[loc_species, 1])**2 +
        (particle_data.loc[loc_species, 'zPos'] + temp_xyz_steps[loc_species, 2])**2 > sim_input['radius_cell']**2
    )

    # Combine all positions that violate the boundary conditions
    particle_data.loc[loc_species, 'pos_reject'] = reject_pos_left_part | reject_pos_cylinder_part | reject_pos_right_part


def handle_two_state(particle_data, loc_state_changes, rates, diff_quot, sim_input):
    kAB, kBA = rates
    particle_data.loc[loc_state_changes, 'active_state'] = particle_data.loc[loc_state_changes, 'next_state']
       
    active_states = particle_data.loc[loc_state_changes, 'active_state'].astype(int).to_numpy() 
    particle_data.loc[loc_state_changes, 'active_diff_quot'] = np.array(diff_quot[active_states])

    find_state_A = loc_state_changes[particle_data['active_state'][loc_state_changes] == 0]
    particle_data.loc[find_state_A, 'next_state'] = 1
    particle_data.loc[find_state_A, 'state_time_remaining'] = np.log(np.random.rand(len(find_state_A))) / (-kAB)
    
    find_state_B = loc_state_changes[particle_data['active_state'][loc_state_changes] == 1]
    particle_data.loc[find_state_B, 'next_state'] = 0
    particle_data.loc[find_state_B, 'state_time_remaining']= np.log(np.random.rand(len(find_state_B))) / (-kBA)


def handle_three_state(particle_data, loc_state_changes, rates, diff_quot, sim_input):
    kAB, kBA, kBC, kCB, kAC, kCA = rates

    # Change state to the next, already known state
    particle_data.loc[loc_state_changes, 'active_state'] = particle_data.loc[loc_state_changes, 'next_state']
    
    # Update diffusion coefficient depending on the current state
    active_states = particle_data.loc[loc_state_changes, 'active_state'].astype(int).to_numpy() 
    particle_data.loc[loc_state_changes, 'active_diff_quot'] = np.array(diff_quot[active_states])
    
    # Generate random values for state transitions
    temp_rand = np.random.rand(sim_input['total_number_particles'], 2)

    # State A transitions
    find_state_A =  loc_state_changes[particle_data['active_state'][loc_state_changes] == 0]
    # A to B
    temp_switch_AB = find_state_A[kAB / (kAB + kAC) >= temp_rand[find_state_A, 0]]
    particle_data.loc[temp_switch_AB, 'next_state']= 1
    particle_data.loc[temp_switch_AB, 'state_time_remaining']= np.log(temp_rand[temp_switch_AB, 1]) / -kAB
    # A to C
    temp_switch_AC = find_state_A[kAB / (kAB + kAC) < temp_rand[find_state_A, 0]]
    particle_data.loc[temp_switch_AC, 'next_state'] = 2
    particle_data.loc[temp_switch_AC, 'state_time_remaining'] = np.log(temp_rand[temp_switch_AC, 1]) / -kAC

    # State B transitions
    find_state_B =  loc_state_changes[particle_data['active_state'][loc_state_changes] == 1]
    # B to A
    temp_switch_BA = find_state_B[kBA / (kBA + kBC) >= temp_rand[find_state_B, 0]]
    particle_data.loc[temp_switch_BA, 'next_state']= 0
    particle_data.loc[temp_switch_BA, 'state_time_remaining'] = np.log(temp_rand[temp_switch_BA, 1]) / -kBA
    # B to C
    temp_switch_BC = find_state_B[kBA / (kBA + kBC) < temp_rand[find_state_B, 0]]
    particle_data.loc[temp_switch_BC, 'next_state']= 2
    particle_data.loc[temp_switch_BC, 'state_time_remaining'] = np.log(temp_rand[temp_switch_BC, 1]) / -kBC

    # State C transitions
    find_state_C =  loc_state_changes[particle_data['active_state'][loc_state_changes] == 2]
    # C to A
    temp_switch_CA = find_state_C[kCA / (kCA + kCB) >= temp_rand[find_state_C, 0]]
    particle_data.loc[temp_switch_CA, 'next_state'] = 0
    particle_data.loc[temp_switch_CA, 'state_time_remaining']= np.log(temp_rand[temp_switch_CA, 1]) / -kCA
    # C to B
    temp_switch_CB = find_state_C[kCA / (kCA + kCB) < temp_rand[find_state_C, 0]]
    particle_data.loc[temp_switch_CB, 'next_state']= 1
    particle_data.loc[temp_switch_CB, 'state_time_remaining']= np.log(temp_rand[temp_switch_CB, 1]) / -kCB


def handle_four_state(particle_data, loc_state_changes, rates, diff_quot, sim_input):
    kAB, kBA, kBC, kCB, kCD, kDC = rates

    # Change state to the next, already known state
    particle_data.loc[loc_state_changes, 'active_state'] = particle_data.loc[loc_state_changes, 'next_state']
    # Update diffusion coefficient depending on the current state
    active_states = particle_data.loc[loc_state_changes, 'active_state'].astype(int).to_numpy() 
    particle_data.loc[loc_state_changes, 'active_diff_quot'] = np.array(diff_quot[active_states])   
    
    # Generate random values for state transitions
    temp_rand = np.random.rand(sim_input['total_number_particles'], 2)

    # State A to B
    find_state_A = loc_state_changes[particle_data['active_state'][loc_state_changes] == 0]
    particle_data.loc[find_state_A, 'next_state'] = 1
    particle_data.loc[find_state_A, 'state_time_remaining'] = np.log(temp_rand[find_state_A]) / -kAB

    # State B transitions
    find_state_B = loc_state_changes[particle_data['active_state'][loc_state_changes] == 1]
    # B to A
    temp_switch_BA = find_state_B[kBA / (kBA + kBC) >= temp_rand[find_state_B, 0]]
    particle_data.loc[temp_switch_BA, 'next_state'] = 0
    particle_data.loc[temp_switch_BA, 'state_time_remaining']= np.log(temp_rand[temp_switch_BA,1]) / -kBA
    # B to C
    temp_switch_BC = find_state_B[kBA / (kBA + kBC) < temp_rand[find_state_B, 0]]
    particle_data.loc[temp_switch_BC, 'next_state'] = 2
    particle_data.loc[temp_switch_BC,'state_time_remaining'] = np.log(temp_rand[temp_switch_BC,1]) / -kBC

    # State C transitions
    find_state_C =  loc_state_changes[particle_data['active_state'][loc_state_changes] == 2]
    # C to B
    temp_switch_CB = find_state_C[kCB / (kCB + kCD) >= temp_rand[find_state_C, 0]]
    particle_data.loc[temp_switch_CB, 'next_state'] = 1
    particle_data.loc[temp_switch_CB, 'state_time_remaining'] = np.log(temp_rand[temp_switch_CB,1]) / -kCB
    # C to D
    temp_switch_CD = find_state_C[kCB / (kCB + kCD) < temp_rand[find_state_C, 0]]
    particle_data.loc[temp_switch_CD, 'next_state'] = 3
    particle_data.loc[temp_switch_CD, 'state_time_remaining'] = np.log(temp_rand[temp_switch_CD,1]) / -kCD

    # State D to C
    find_state_D =  loc_state_changes[particle_data['active_state'][loc_state_changes] == 3]
    particle_data.loc[find_state_D, 'next_state'] = 2
    particle_data.loc[find_state_D, 'state_time_remaining'] = np.log(temp_rand[find_state_D,1]) / -kDC
