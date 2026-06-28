# sptPALM-Python — Data Contract

What the main in-memory objects hold, and what each function **reads** and
**writes**. This complements the README (which documents the on-disk CSV schema in
§5.3–5.4) by describing the in-memory data flow. Last updated: 2026-06-28.

> Design note: most functions take a single dictionary (`para` / `input_parameter`)
> and both read settings from it and write results back into it ("god-dict"
> pattern). A future refactor may separate settings from results; until then, the
> tables below are the de-facto contract. See `docs/REFACTOR_PLAN.md` §3.3.

## 1. The core dictionaries

| Object | Created by | Role |
|---|---|---|
| `input_parameter` | `set_parameters_sptPALM` (+ GUI) | Global analysis settings (paths, file lists, conditions, tracking/diffusion/plot parameters). Saved/loaded as JSON. |
| `para` | `analyse_movies_sptPALM` (per movie) | A **copy of `input_parameter`** for one movie, progressively extended with that movie's data and results (`csv_data`, `tracks`, `bf_dict`, `diff_coeffs_filtered_list`, `scta_table`, …). |
| `data` | `analyse_movies_sptPALM` | `data['movies'][i]` = the `para` of movie *i*; `data['input_parameter']` = the settings used. Saved as `sptData_movies.pkl`. |
| `comb_data` | `combine_analysed_data_sptPALM` | Per-condition aggregates across movies (`cell_data`, `diff_data`, `anaDDA_tracks`, …). Saved as `sptData_combined_movies.pkl`. |
| `sim_input` | `set_parameters_simulation` (+ GUI) | Simulation/MCDDA settings and per-species state model. |

### Key settings in `input_parameter` (selected)
- Paths/files: `data_dir`, `default_output_dir`, `fn_locs` (list), `fn_proc_brightfield` (list), `fn_csv_handle`, `fn_movies`, `fn_combined_movies`
- Conditions: `condition_names`, `condition_files`, `copynumber_intervals`
- Segmentation: `use_segmentations`, `pixelsize`, `cellarea_pixels_min/max`
- Tracking: `track_steplength_max`, `track_memory`, `frametime`, `loc_error`
- Diffusion: `tracklength_locs_min/max`, `tracklengths_steps` (derived), `diff_avg_steps_min/max`
- Per-cell: `number_tracks_per_cell_min/max`
- Plotting: `plot_diff_hist_min/max`, `binwidth`, `fontsize`, `dpi`, `plot_option_axes`, `plot_option_save`, `cmap_applied`, `scta_*`

## 2. Key DataFrames (in-memory)

| Name | Lives in | Important columns |
|---|---|---|
| `csv_data` | `para['csv_data']` | `loc_id, movie_id, frame, cell_id, track_id, x [µm], y [µm], z [µm], brightness, background, i0, sx, sy, cell_area` (see README §5.4). `cell_id`/`track_id` are `-1` until segmentation/tracking fill them. |
| `tracks` | `para['tracks']` | `x [µm], y [µm], frame, track_id, loc_id, frametime`. After `diff_coeffs_from_tracks_fast` also `#_locs, MSD, D_coeff`. Sorted by `(track_id, frame)`. |
| `D_tracklengths_matrix` | `para['D_tracklengths_matrix']` | `Bins` + one column per track-length step: a length-resolved histogram of D (the MCDDA/anaDDA input). |
| `diff_coeffs_filtered_list` | `para['diff_coeffs_filtered_list']` | One row per valid track: `diff_coeffs_filtered, track_length_filtered, track_id` (+ `cell_id, copynumber` after single-cell analysis). |
| `scta_table` | `para['scta_table']` | Per cell: `movie, cell_id, cell_locs, cell_area, #tracks (filtered/unfiltered for #tracks per cell), cum. …, keep_cells, average_diff_coeff_per_cell`. |

## 3. Per-movie pipeline (inside `analyse_movies_sptPALM`)

Each function takes `para` and returns it mutated (unless noted).

| Function | Reads | Writes |
|---|---|---|
| `load_localisations_from_csv` | `data_dir, fn_locs, movie_number, default_output_dir, fn_csv_handle` | `para['csv_data']`; writes `*_py_out.csv` |
| `apply_cell_segmentation_sptPALM` | `data_dir, fn_proc_brightfield, csv_data, cellarea_pixels_min/max, pixelsize` | `para['csv_data']` (fills `cell_id`, `cell_area`), `para['bf_dict']` |
| `tracking_sptPALM` | `csv_data, use_segmentations, track_steplength_max, track_memory` | `para['tracks']`, `para['csv_data']` (fills `track_id`); plots `Fig02` |
| `diff_coeffs_from_tracks_fast(tracks, para)` | `tracks, tracklengths_steps, frametime, loc_error, track_memory, plot_*` | returns `(tracks_data, D_tracklengths_matrix)` |
| `diff_coeffs_per_track(tracks, para, locs_min, locs_max)` | `tracks, frametime, loc_error, track_memory` | returns per-track `diff_coeffs_filtered_list` |
| `plot_diff_histograms_tracklength_resolved` | `D_tracklengths_matrix, tracks, plot_*` | plots |
| `plot_diffusion_tracklengths_sptPALM` | `D_tracklengths_matrix, tracks, diff_avg_steps_min, plot_*` | plots `Fig04` |
| `single_cell_analysis_sptPALM` | `csv_data, diff_coeffs_filtered_list, number_tracks_per_cell_min/max` | `para['scta_table']`, `diff_coeffs_filtered_list` (+`cell_id, copynumber`), `para['scta_tracks_csv']`, `para['tracks_filtered']` |
| `plot_single_cell_analysis_sptPALM` | `scta_table, diff_coeffs_filtered_list, scta_tracks_csv, tracks_filtered, bf_dict, plot_*` | plots `Fig05`, `Fig06` |

Diffusion-coefficient note (Step 2 decision): the length-resolved histogram uses
all track lengths in `tracklengths_steps` (locs 2–8 by default); the per-cell /
combined per-track coefficients use a higher minimum
(`locs > diff_avg_steps_min`) and truncate long tracks to their first
`tracklength_locs_max` localisations. See `docs/REFACTOR_PLAN.md` §3.2.

## 4. Top-level functions (driven by `sptPALM_main`)

| Function | Reads | Writes |
|---|---|---|
| `analyse_movies_sptPALM(input_parameter)` | `input_parameter` | `data` (per-movie `para`s); `sptData_movies.pkl` |
| `combine_analysed_data_sptPALM(data, input_parameter)` | `data['movies'][*]` `scta_table` / `diff_coeffs_filtered_list` / `tracks` | `comb_data` (`cell_data`, `diff_data`, `anaDDA_tracks`, `condis_#_cells`); `sptData_combined_movies.pkl` |
| `plot_combined_data_sptPALM(comb_data, input_parameter)` | `comb_data['cell_data'/'diff_data']` | plots combined figures |
| `MC_diffusion_distribution_analysis_sptPALM(comb_data, input_parameter, sim_input)` | `comb_data['anaDDA_tracks']`, `sim_input` | MCDDA fit; plots |

## 5. `comb_data` keys

`#_movies_loaded`, `#_conditions`, `#_movies_per_condition`, `condition_names`,
`condition_files`, `cell_data` (per-condition `scta_table`s), `diff_data`
(per-condition `diff_coeffs_filtered_list`s), `anaDDA_tracks` (per-condition
tracks for MCDDA), `condis_#_cells`, `input_parameter`.
