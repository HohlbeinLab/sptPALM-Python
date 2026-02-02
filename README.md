# sptPALM data analysis (Python & ImageJ)
This work is licensed under the CC BY 4.0 License.
You are free to share and adapt this work, even for commercial purposes, as long as you provide appropriate credit to the original creator. Original Creator: Johannes Hohlbein (Wageningen University & Research), Date of Creation: September, 2024. Full license details can be found at https://creativecommons.org/licenses/by/4.0/

Basic Markdown syntax: [[link]](https://www.markdownguide.org/basic-syntax/), Export to PDF

Workflow and code for single-particle, single-cell tracking analysis. 

## Content
1. [Literature](#literature) 
2. [Known issues](#issues) 
3. [Experimental and computational workflow ](#workflow)
4. [ImageJ / Fiji: segmentation and localisation](#ImageJFiji)
5. [Omnipose: set-up + segmentation](#Omnipose)
6. [Python: sptPALM analysis](#Python)

<a name="literature"></a>

## 1. Literature
1. "Evaluating single-particle tracking by photo-activation localization microscopy (sptPALM) in Lactococcus lactis." S.P.B. van Beljouw, S. van der Els, K.J.A. Martens, M. Kleerebezem, P.A. Bron, J. Hohlbein, Physical Biology, 16, 035001, 2019, [[link]](https://doi.org/10.1088/1478-3975/ab0162)
2. "Visualisation of dCas9 target search in vivo using an open-microscopy framework." K.J.A. Martens, S. van Beljouw, S. van der Els, J.N.A. Vink, S. Baas, G.A. Vogelaar, S.J.J. Brouns, P. van Baarlen, M. Kleerebezem, J. Hohlbein, Nature Communications, 10, 3552, 2019, [[link]](https://doi.org/10.1038/s41467-019-11514-0)
3. “Live-cell imaging reveals the trade-off between target search flexibility and efficiency for Cas9 and Cas12a”, L. Olivi, C. Bagchus, V. Pool, E. Bekkering, K. Speckner, H. Offerhaus, W.Y. Wu, M. Depken, K.J.A Martens, R. Staals*, J. Hohlbein*, Nucleic Acids Research, 52, 5241, 2024, [[link]](https://doi.org/10.1093/nar/gkae283)
4. "Direct visualization of native CRISPR target search in live bacteria reveals Cascade DNA surveillance mechanism", J.N.A. Vink, K.J.A. Martens, M. Vlot, R.E. McKenzie, C. Almendros, B. Estrada Bonilla, D.J.W. Brocken, J. Hohlbein, S.J.J. Brouns, Molecular Cell, 77, 39-50.e10, 2020, [[link]](https://doi.org/10.1016/j.molcel.2019.10.021)
5. "Extracting transition rates in particle tracking using analytical diffusion distribution analysis (anaDDA)", J. Vink, S.J.J. Brouns, and J. Hohlbein, Biophysical Journal, 119, 1970–83, 2020, [[link]](https://doi.org/10.1016/j.bpj.2020.09.033)

Python code to analyse experimental data and simulate single-particle tracking in bacteria.
Make sure that you have, (1) a Python installation (e.g., Anaconda), (2) a  Python development environment (e.g., Spyder), and (3) trackpy (e.g., 'pip install trackpy') installed.

## 2. Known issues
1. --

<a name="workflow"></a>

## 3. Experimental and computational workflow 
1. Run experiments on the **miCube** to obtain:
    1. single-molecule data, e.g., 'MyRawData.tif', recorded using single-particle-tracking photoactivaltion light microscopy (sptPALM).
    2. cell outlines, e.g., 'MyBrightfield.tif', recorded using bright field microscopy.
2. run script called *Macro_thunderSTORM.ijm* in **ImageJ/Fiji** on 'MyRawData.tif' to obtain 'MyRawData_thunder.csv' which contains the localisations of the fluorophores. Details: [ImageJ / Fiji: segmentation and localisation](#ImageJFiji).
3. For cell segmentation, there are two options:
    1. Watershed: run script called *Macro_CellSegmentation.ijm* in **ImageJ/Fiji** on 'MyBrightfield.tif' to obtain 'MyBrightfield_procBrightfield.tif', 'MyBrightfield_procBrightfield_segm.tif', and 'MyBrightfield_procBrightfield_segm_Table.csv' containing segmented cells and associated data. Details: [ImageJ / Fiji: segmentation and localisation](#ImageJFiji).
    2. Omnipose: runs Omnipose from anaconda environment **after** selecting Cellpose/Omnipose as the input parameter when running the **Python** pipeline. Omnipose uses 'MyBrightfield.tif' or 'MyBrightfield_ProcBrightfield.tif' to obtain 'MyBrightfield_procBrightfield_cp_masks.tif' and 'MyBrightfield_procBrightfield_cp_masks_table.csv' containing the segmented cells and areas. Details: [Omnipose: segmentation](#Omnipose_seg)

4. Run script called 'sptPALM_main.py' in **Python**. Select Watershed or Cellpose/Omnipose in the GUI when setting the parameters depending on the used segmentation method.
For details: [Python: sptPALM analysis](#Python).

<a name="ImageJFiji"></a>

## 4. ImageJ/Fiji
We run two macros *Macro_thunderSTORM.ijm* and *Macro_CellSegmentation.ijm* to prepare the raw data for subsequent analysis. There are a number of parameters set in the functions that might have to be adjusted depending on the specific circumstances of your measurements. When in doubt, ask! To open and later run the macro, drag & drop each macro into **ImageJ/Fiji**. To have all required (sub-)functions available in **ImageJ/Fiji**, check the following
1. -> ImageJ/Fiji -> Help -> Update... -> Manage Update sites -> tick the box for 'HohlbeinLab' and 'SCF MPI CBG'
2. restart ImageJ/Fiji

### 4.1 *Macro_CellSegmentation.ijm*
Macro_CellSegmentation.ijm is used to segment cells on 'MyBrightfield.tif'. Currrently, the macro runs trough the following steps and allows selecting more than one file.
1. Load raw data 'MyBrightfield.tif' using a GUI or providing a filename in the script. 
2. Run function for z-projection, averaging over all frames to reduce noise
3. Further data post-processing for stability of cell segmentation
4. Save processed brightield image 'MyBrightfield_procBrightfield.tif' in current folder
5. Run segmentation and save segmented image 'MyBrightfield_procBrightfield.tif' and labels 'MyBrightfield_procBrightfield_segm_Table.csv' in the current folder

### 4.2 *Macro_thunderSTORM.ijm*
*Macro_thunderSTORM.ijm* is used to perform the subpixel localisation of single-molecule data 'MyRawData.tif'. Currrently, the macro runs trough the following steps
1. Load raw data 'MyRawData.tif' using a GUI or providing a filename in the script
2. Remove first 500 frames to prevent attempted localisation of overlapping fluorophores
3. Run FTM2 (fast temporal medium filter 2). More information here [[Github FTM2]](https://github.com/HohlbeinLab/FTM2).
4. Run thunderSTORM-phasor to localise all fluorophores and save data in the form of a CSV table named 'MyRawData_thunder.csv'. ThunderSTORM can be run either with 'phasor' (faster) or 'MLE' (slower but allows filterring for PSF widths')

<a name="Omnipose"></a>
## 5. Omnipose

### 5.1 Installation and set-up
To install Omnipose, follow the official documentation.
- Omnipose Installation Guide [[link]](https://omnipose.readthedocs.io/installation.html)  
- Omnipose GitHub Repository [[link]](https://github.com/kevinjohncutler/omnipose)

Call the anaconda environment 'omnipose'. In case of using a different environment name, change the environment name in the script *OmniposeFromMain.py* from 'omnipose' to the used environment name.

#### 5.1.1 Check required packages
The default Omnipose installation should include `scikit-image`.
This package is used to obtain area measurements. To verify whether it is installed, take the following steps:

1. Open the Anaconda Prompt and activate the Omnipose environment:

```bash
conda activate omnipose
```
2. Check whether `scikit-image is installed`:
```bash
python -c "import skimage; print(skimage.__version__)"
```

3. If `sci-kit image` is not installed, you can download it by using:
```bash
conda install -c conda-forge scikit-image
```

For more installation options, see the scikit-image documentation [[link]](https://pypi.org/project/scikit-image/).

<a name="Omnipose_seg"></a>
### 5.2 Segmentation pipeline
Omnipose is used to segment cells from 'MyBrightfield_ProcBrightfield.tif', but also takes 'MyBrightfield.tif as input'. Omnipose only runs **after** selecting Cellpose/Omnipose as the segmentation method in the set parameter GUI. It runs the file 'OmniposeFromMain.py', which currently runs through the following steps with the help of 'OmniposeForCommand.py' and 'OmniposeForCommandGUI.py'.

1. In case 'Run Z-projection' is selected: loads raw data 'MyBrightfield.tif' and averages over all frames to reduce noise. Saves processed brightfield image 'MyBrightfield_procBrightfield.tif' in the data directory folder.
2. Takes 'MyBrightfield_procBrightfield' and segments using Omnipose with the defined settings in the custom Omnipose GUI and minimum cell area defined in sptPALM GUI. Defining minimum cell area allows for dropping small masks obtained from the background/image noise. If post-processing is selected, also boundary masks are dropped. Masks are saved as 'MyBrightfield_procBrightfield_cp_masks.tif' in the data directory.
3. Takes the saved masks to extract cell measurements (currently label and area) and saves in 'MyBrightfield_procBrightfield_cp_masks_table.csv' in the data directory.

In case the cells are already segmented and you are satisfied with the results, the box 'Already segmented' can be checked, to prevent the custom Omnipose GUI from starting.

To check different settings for Omnipose, current option is to load obtained masks in an image viewer after segmentation while keeping the custom Omnipose GUI open and opening them in Fiji/ImageJ for example. This way Omnipose dependencies do not have to be reloaded each time want to check segmentation results.

For further analysis steps, the code keeps track of whether the segmentation was successful using a flag file.
In case not successful, will not run further analysis steps, until the settings are changed or segmentation is completed.

If Omnipose is selected, maximum cell area is not required as with Watershed and can be set to a high value to prevent large masks from being dropped.

<a name="Python"></a>

## 6 Python 

### 6.1 sptPALM_main.py
Main function to analyse experimental data. We require:

1. *.csv file(s) containing the x,y and, optionally, z positions of individual emitters as obtainbed via, for example, ThunderSTORM or any other SMLM data suite. 
2. (optional) brightfield images of cells, their segmentation, and a *.csv table containing relevant information on the segmentation

Run the function in the command line of your Python development environment by typing:  *runfile('/...your folder.../GitHub/sptPALM-Python/sptPALM_main.py', wdir='/...your folder.../GitHub/sptPALM-Python')* and pressing Enter.

The following prompt will appear:

    0: Exit
    1: Set parameters GUI
    2: Analyse individual movies
    3: Combine individually analysed movies
    4: Plot combined data
    5: Monte-Carlo DDA
    6: Auxillary functions

| <div style="width:200px"> <span style="color: red;">Option</span> </div>  |  <div style="width:100px"> Description </div> |
|---|---|
|0: Exit | Closes the prompt and returns to the command line.|
|1: Set parameters GUI | Runs *set_parameters_sptPALM.py* loading default settings for the data analysis followed by *set_parameters_sptPALM_GUI.py* that allows changing, loading, and saving specific sets of parameters to analyse the experimental data. Then runs *OmniposeFromMain.py*, which starts Omnipose segmentation if 'Cellpose/Omnipose' is selected and 'Already segmented' is unchecked.|
|2: Analyse individual movies | Runs *analyse_movies_sptPALM.py* to analyse individual movies as earlier defined option 1. If no output from 1 is in memory, the option 1 is run again. Returns a DataFrame called 'data' which contains all localisations and further information. Results are saved into '**sptData_movies.pkl**' or similar|
|3: Combine individually analysed movies | Runs *Combine_individually_analysed_movies.py* to group the data of individually analysed files available in the DataFrame 'data' based on conditions defined in *set_parameters_sptPALM.py*. If no data is in memory, a GUI will open to load '**sptData_movies.pkl'**' or similar. Function returns a DataFrame called 'comb_data'. Results are are saved into '**sptData_combined_movies.pkl**' or similar|
|4: Plot combined data|Graphical output of the data combined in Option 3. Name of function: plot_combined_data_sptPALM.py|
|5: Monte-Carlo DDA|Runs *MC_diffusion_distribution_analysis_sptPALM.py* to perform fitting of the experimental data based on parameters defined in *set_parameters_simulation.py*|
|6: Auxillary functions|Provides option to combine *.csv files to enable particle counting per cell over many movies|

## 6.2 simulation_main.py
To simulate distributions of diffusion coefficients, the following functions are run after each other:
| <div style="width:200px"> **<span style="color: red;">Name</span>** </div>  |  <div style="width:100px"> Description </div> |
|---|---|
| *set_parameters_simulation.py* | Function for setting all parameters|
| *initiate_simulation.py*  | Function for setting all starting positions, starting states etc | 
| *diffusion_simulation.py* | Function for moving particles and checking for state changes|
| *diff_coeffs_from_tracks_fast.py* |  Function to calculate diffusion coefficients for different track lengths|
| *plot_diff_histograms_tracklength_resolved.py* | Function for plotting the data|


## 6.3. Settings defined in '*set_parameters_sptPALM.py*'
SCTA: Single-cell tracking analysis. Parameters in order of appearance.
| <div style="width:200px"> name </div>  |  <div style="width:100px"> Default </div> |  <div style="width:100px"> Description </div> |
|---|:---|---|
| data_dir| -  | Directory where the data is found (selection via GUI or pre-defined, see below)  |
| default_output_dir | output_python/ | Initialise new directory to which analysed data is saved | 
| fn_locs | - |Initialise filename to the localisation data | 
| fn_proc_brightfield | - | Initialise filename to the brighfield data  |
| fn_csv_handle | _py_out.csv |Will be used to name the csv file of the analysed data|
| fn_dict_handle | _py_out.pkl | Will be used to name the pickle file of the analysed data |
| fn_diffs_handle | _diff_coeffs.csv |Will be used to name the file of diffusion coefficients|
| fn_movies | sptData_movies.pkl | Will be used to name the pickle file of the analysed data |
| fn_combined_movies | sptData_combined_movies.pkl |filename of combined conditions output|
| condition_names| [] | Initialise, further defined below
| condition_files | [] | Will be used to name the pickle file of the analysed data |
| copynumber_intervals | [] |ilename of combined conditions output|
| pixelsize (µm)| 0.119  | Effective pixel size of the camera (also set in *Macro_thunderSTORM.ijm*). The number is close to the actual pixel size of the camera (Photometrics 95B: 15 µm, Andor Zyla 4+: 13 µm after 2x2 binning) divided by the magnification of the objective 100x (Nikon, N.A. = 1.49) |
| used_segmentation_method | Watershed | Select the used or to be used segmentation method. Options: Watershed or Cellpose/Omnipose |
| use_segmentations | True | Segmentation of cells allows linking localisations to individual cells |
| applied_segmentation | False | Omnipose only. Select False to start Omnipose segmentation. Select True if segmentation was already run. |
| z_projection | False | Omnipose only. Allows 'MyBrightfield.tif' as input. Averages over all frames of the raw image data. |
| cellarea_pixels_min | 50 | Filter cells for minum area (area is given in number of pixels), default: 50. | 
| cellarea_pixels_max | 300 | Filter cells for area (area is given in number of pixels), default: 500 | 
| track_steplength_max (µm) | 0.5 |Used for tracking. Maximum distance that two localisations in consecutive farmes can be apart to still be considered belonging to a single track. Avoids linking of non-related localisations. Note that that this thresholds can effect the histogram of diffusion coefficients|
| trackMemory | 0 | Set tracking memory in frames. Allows tracks to have missing localisations. default 1|
| frametime | 0.01 | Length of a single movie frame in seconds |
| loc_error (µm)| 0.035 | Assumed localisation error (µm). Could be calculated based on the localisation precisionin ThunderSTORM, but not possible with phasor-based localisation. |
| diff_hist_steps_min | 3 | Minimum number of steps for a track to be analyzed. Note that the actual number of localisations is one higher  |
| diff_hist_steps_max |  100 | Minimum number of steps for a track to be analyzed.  
| track_lengths |  1,2,3,4,5,6,7,8 | Minimum number of steps for a track to be analyzed.  
| number_tracks_per_cell_min  | 1 | Minimum number of tracks that each cell must contain |
| number_tracks_per_cell_max | 10000 | Maximum number of tracks that each cell must contain |
| scta_vis_cells | False | Visualize individual cells true/false |
| scta_plot_cell_window | 15 | Radius in pixels for plotting individual cells and their tracks|
| scta_vis_interactive | False | Interactively cycle through indiviudally plotted cells true/false |
| scta_vis_rangemax | 0.3 | Color-coding in the range of 0 to (SCTA_vis_rangemax * plotDiffHist_max) |
| plot_diff_hist_min | 4E-3 | plot and histogram from min µm<sup>2</sup>/s to max µm<sup>2</sup>/s |
| plot_diff_hist_max | 10 | plot and histogram from µm<sup>2</sup>/s to µm<sup>2</sup>/s |
| binwith | 0.1 | width of bins, default: 0.1 |
| fontsize | 10 | Fontsize used to plot figures |
| linewidth | 1 | linewidth used to plot figures |
| plot_norm_histograms | 'probability' | Choose style of plotting some histograms. Optiomns:  'count', 'probability', 'countdensity', 'pdf', cumcount', 'cdf'| 
| plot_frame_number | True | whether to plot the frame numbers next to the tracks in 'Plot_SingleCellTrackingAnalysis.m' |
| dpi | 150 | DPI setting for plotting figures, default: 300 |
|cmap_applied | gist_ncar | color map for segmented cells was: 'nipy_spectral', tab20c, 

### 6.4 Omnipose settings

#### 6.4.1 Settings sptPALM GUI
From *set_parameters_sptPALM.py*, Omnipose takes the data directory, input files (stored as fn_proc_brightfield) and the minimum size for the cell masks.

#### 6.4.2 Settings defined in custom Omnipose GUI
| <div style="width:200px">Name in GUI</div>  |  <div style="width:100px"> Default </div> |  <div style="width:100px"> Description </div> |
|---|---|---|
|Model  |bact_phase_omni   |The model Omnipose will use for segmentation. Pre-trained available models: bact_phase_omni, bact_fluor_omni, cyto2_omni, worm_omni.|
|Channel 1, Channel 2   |[0,0]   |Specify the channel parameters. First channel for cytoplasm (0: grayscale, 1: red, 2: green, 3: blue). Second channel for nucleus (0: no channel,  1: red, 2: green, 3: blue)   |
|Mask Threshold   |0   | Erode or dilate masks with higher or lower values between -5 and 5. Decrease in case of too few masks or masks not convering theentire cell.  |
|Flow Threshold   |0   | Only needed if there are spurious masks to clean up; slows down output. Increase in case of too many masks. Decrease in case of too many spurious masks.  |
|Diameter   |0   | Set the diameter in pixels for the cells. In case of 0, Omnipose determines it itself.  |
|Omnipose mask reconstruction   | True  | Use Omnipose mask reconstruction  |
|Invert Image   | True  | Invert the colour scheme of the input images.  |
|Post-processing | False | Enable or disable removal of edge masks after segmentation.|
|Boundary Thickness | 3 | Edge width in pixels to select candidate masks for removal. |
|Area Threshold | np.inf | Remove boundary masks that are smaller than the defined area |
|Cutoff | 0 | Masks in which the edge overlap (range 0-1) is larger than the cutoff will be removed.
|Save settings in a txt file   | True  | Saves the settings defined above in a `.txt` file in the output folder.   |

## 6.5. Variables internally used in the Python analysis
| <div style="width:200px"> Name </div>  |  <div style="width:100px"> Default </div> |  <div style="width:100px"> Description </div> |
|---|:---|---|
| data_dir| **<span style="color: red;">User defined</span>** | Directory containing your data
| default_output_dir| **<span style="color: red;">User defined</span>** | Directory to which new data is saved. Default: 'output_python/'
| fn_locs| **<span style="color: red;">User defined</span>** | List of one or more '_thunder.csv' files to be analysed
| fn_proc_brightfield |  **<span style="color: red;">User defined</span>** | List of one or more processed brightield images for cell segmentation '_procBrightfield.tif'. Filename is also used to locate the segmented image and corresponding *.csv table! |
|**<span style="color: green;">csv data saved as '\_py_out.csv' </span>** | initialised in *load_csv.py*| Columns: loc_id, movie_id, frame_id, track_id, cell_id, x [µm], y [µm], z [µm], brightness, bg, i0, sx, sy, empty (NaN). CSV table based on the structure of the CSV output provided by ThunderSTORM (software used for sub-pixel localisation)
|**<span style="color: green;">tracks</span>** | -- |  Some 'tracks' have a length of one thereby representing single localisations! Columns: x(µm), y(µm), time(frame), track_id. If 'useSegmentations = true', 'TrackingAnalysis.m' runs for each valid cell (cellarea_pixels min/max thresholds active) using all localisations found therein. **Not filtered for 'diff_hist_steps_min(max)' and 'number_tracks_per_cell_min(max)'!**|
|**<span style="color: green;">DiffsCoeffsList</span>** | -- | List of diffusion coefficients (unit: µm^2/s!) and more. Columns: DiffCoeffsFiltered, #localisations, track_id, cell_id and copynumber. **Filtered for 'diff_hist_steps_min(max)'**   |
|**<span style="color: green;">scta_table</span>** | -- | Overview table after filtering for 'DiffHistSteps', 'numberTracksPerCell' in valid cells (CellAreaPix_min/max thresholds active). Columns: cell_id, #locs per cell, cumulative #locs, #tracks (filtered for #tracks per cell), cum. #tracks (filtered for #tracks per cell), cum. #tracks (unfiltered for #tracks per cell), keep_cells, averageDiffCoeffperCell
|**<span style="color: green;">scta_tracks</span>** | -- | Table containg for each valid cell, the full information for each localisation of each valid track 
|**<span style="color: green;">tracks_filtered</span>** | -- | Columns: x(µm), y(µm), time(frame), track_id. **Filtered for 'diff_hist_steps_min(max)s' and 'number_tracks_per_cell_min(max)'! using valid cells** |
