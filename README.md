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
5. [Python: sptPALM analysis](#Python)

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
3. run script called *Macro_CellSegmentation.ijm* in **ImageJ/Fiji** on 'MyBrightfield.tif' to obtain 'MyBrightfield_procBrightfield.tif', 'MyBrightfield_procBrightfield_segm.tif', and 'MyBrightfield_procBrightfield_segm_Table.csv' containing segmented cells and associated data. Details: [ImageJ / Fiji: segmentation and localisation](#ImageJFiji).
4. Run script called 'Run_sptPALM_analysis.m' in **Matlab**. For details: [Matlab: sptPALM analysis](#Matlab).

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

<a name="Python"></a>

## 5 Python 

### 5.1 sptPALM_main.py
Main function to analyse experimental data. We require:

1. *.csv file(s) containing the x,y and, optionally, z positions of individual emitters as obtainbed via, for example, ThunderSTORM or any other SMLM data suite. 
2. (optional) brightfield images of cells, their segmentation and a *.csv table containing relevant information on the segmentation

Run the function in the command line of your Python development environment by typing:  *runfile('/...your folder.../GitHub/sptPALM-Python/sptPALM_main.py', wdir='/...your folder.../GitHub/sptPALM-Python')* and pressing Enter.

The following prompt will appear:

    0: Exit
    1: Analyse individual movies
    2: Combine individually analysed movies
    3: Plot combined data
    4: Monte-Carlo DDA
    5: Additional functions...

| <div style="width:200px"> <span style="color: red;">Option</span> </div>  |  <div style="width:100px"> Description </div> |
|---|---|
|**0: Exit**|Closes the prompt and returns to the command line.|
|**1: Analyse individual movies**|Runs *analyse_movies_sptPALM.py* to analyse individual movies as either defined in *set_parameters_sptPALM.py* or selected via a graphical user interface. Returns a DataFrame called 'data' which contains the localisations and further information. Results are saved into '**sptData_movies.pkl'**' or similar|
|**2: Combine individually analysed movies**|Runs *Combine_individually_analysed_movies.py* to group the data of individually analysed files available in the DataFrame 'data' based on conditions defined in *set_parameters_sptPALM.py*. Returns a DataFrame called 'comb_data'. Results are are saved into '**sptData_combined_movies.pkl**'|
|**3: Plot combined data**|Graphical output of the data combined in **Option 2**. Name of function called in Matlab: 'sptPALM_PlotCombinedData(CombinedDATA)'|
|**4: Monte-Carlo DDA**|Runs *MC_diffusion_distribution_analysis_sptPALM.py* to perform fitting of the experimental data based on parameters defined in *set_parameters_simulation.py*|



In *analyse_movies_sptPALM.py*, the following subfunctions are called:
1. *load_localisations_from_csv.py*
2. *apply_cell_segmentation_sptPALM.py*
3. *tracking_sptPALM.py*
4. *analyse_diffusion_sptPALM.py*
5. *plot_diffusion_tracklengths_sptPALM.py*
6. (optional) *single_cell_analysis_sptPALM.py*
7. (optional) *plot_single_cell_analysis_sptPALM.py*



## 5.1 simulation_main.py
To simulate distributions of diffusion coefficients, the following functions are run after each other 
1. *set_parameters_simulation.py*
2. *initiate_simulation.py* 
3. *diffusion_simulation.py*
4. *diff_coeffs_from_tracks_fast.py*
5. *plot_diff_histograms_tracklength_resolved.py*