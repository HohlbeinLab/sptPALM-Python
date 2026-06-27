# sptPALM-Python — Refactoring Plan & Design Decisions

Status: living document. Captures decisions made while modernising the analysis
pipeline so they travel with the code (collaborators, future maintainers, and the
original author). Last updated: 2026-06-27.

Progress: MSD bug fix done; **Step 1 done** (§3.1); faster startup done (§2.2b).
Next: Step 2 (§3.2).

## 1. Goals

Evolve the codebase (originally translated fairly literally from MATLAB) toward a
structure that is:

1. **Modular / maintainable** — today state is carried in one large `para` /
   `input_parameter` dictionary that mixes settings with raw DataFrames and
   results. One function per file.
2. **Faster** — remove duplicated diffusion calculation and per-row Python loops.
3. **Configurable from a human-readable file** — parameters currently live in
   pickle (`*.pkl`): not human-readable, version-fragile, undiffable in git.
4. **Usable by others** — audience is the author, the group, and external
   researchers on the same topic. Generalisation, clear comments, and no
   machine-specific assumptions matter.

**Usage philosophy:** the tool is meant to be *script-like* — set parameters once
in a readable config, run, with minimal changes between runs. A human-editable
JSON/config that you edit and rerun is the primary interface; the tkinter GUI and
the interactive numbered prompt are optional conveniences, not the core.

## 2. Completed

### 2.1 Cross-track MSD bug fix (done 2026-06-27)

`diff_coeffs_from_tracks_fast.py`: `calculate_MSD()` reshapes rows into groups of
`group_size` and uses `np.diff`, which is only correct if each track's
localisations are contiguous and time-ordered. `para['tracks']` arrived in
cell / `loc_id` order (tracks interleaved within a cell), so `np.diff` computed
spurious displacements *across different tracks*.

- **Fix:** sort by `['track_id','frame']` at the top of
  `diff_coeffs_from_tracks_fast` so both call sites are correct regardless of how
  the caller pre-sorts.
- **Verified empirically** on `Cas12aScrambled_part1`: buggy max apparent D
  = 250.9 µm²/s → 15.9 after fix; mean 0.96 → 0.82. The binned histogram only
  shifted ~0.7% because it is capped at `plot_diff_hist_max = 10`, so the worst
  spurious values fell off the edge.
- **Why it was latent (not yet corrupting published results):**
  `analyse_movies_sptPALM.py` currently runs BOTH the fast function AND the OLD
  `analyse_diffusion_sptPALM` (correct but slow). Downstream diffusion numbers
  flow through the OLD path. The bug would have gone live the moment the OLD
  function is retired (see §3.2).

### 2.2b Faster startup via lazy imports (done 2026-06-27, commit `6f88b5b`)

`sptPALM_main` imported the whole pipeline at module top, pulling in trackpy
(~1.7s), matplotlib, scipy and skimage just to show the menu (~2.6s before the
prompt). Each step's import was moved into the menu `case` that uses it. Python's
`match` runs only the chosen case, and every case imports the name it uses in the
same block, so order/skipping is irrelevant and the module is cached after first
use. Launch-to-menu is now ~0.04s; heavy deps load only when their option is
chosen (e.g. trackpy on first Analyse, once per session).

Note: `simulation_main.py` likely has the same heavy-top-import pattern and could
get the same treatment if used regularly.

## 3. Planned work (in priority order)

### 3.1 External JSON config + remove hardcoded paths — DONE (2026-06-27)

Commits: `fa921ca` (main change), `65efb28` (untrack build/OS artifacts).

- DONE: analysis parameters now save/load as **human-readable JSON**
  (`helper_functions.save_parameters` / `load_parameters`). Derived
  `tracklengths_steps` is dropped on save and recomputed on load; legacy `.pkl`
  parameter files still load (backward compatible). GUI Save/Load switched to
  JSON.
- DONE: removed the hardcoded absolute `data_dir` in `set_parameters_sptPALM.py`;
  the default now resolves relative to the repo (bundled `experimental_data`), so
  the example works on any machine after cloning. (Johannes's commented dataset
  presets were intentionally kept for quick source-edit switching.)
- DONE: removed the `os.chdir()` side effect in `analyse_movies_sptPALM.py` (all
  file I/O already uses absolute paths).
- DONE: added `.gitignore`; untracked `__pycache__` and `.DS_Store`.
- NOT YET (deferred sub-task): `sim_input` (simulation parameters) still uses
  pickle — its nested numpy arrays (per-species `diff_quot`, 2D `rates_lb_ub`,
  etc.) need explicit reconstruction on load. Convert in a focused later step.

### 3.2 Retire the OLD diffusion function

- `analyse_diffusion_sptPALM` (fixed first-N-steps estimator) is to be **replaced**
  by `diff_coeffs_from_tracks_fast` (track-length-resolved, all-steps estimator).
- **Note these are different estimators**, not just fast vs slow:
  - OLD averages MSD over only the first `diff_avg_steps_min` steps (fixed count).
  - FAST bins tracks by exact length and averages over all steps of the track.
  - They also filter different track populations.
- **Decision:** keep FAST as the foundation — it is the track-length-resolved form
  the MCDDA / anaDDA machinery consumes, and the right approach given the
  exponential track-length distribution (photobleaching).
- **Prerequisite before deleting OLD:** confirm the fast outputs
  (`D_coeff` / `diff_coeffs_filtered_list`) are what downstream steps
  (`single_cell_analysis`, combine, MCDDA) expect. Remove the now-redundant manual
  `sort_values(['track_id','frame'])` in `MC_diffusion_distribution_analysis_sptPALM.py`.

### 3.3 Untangle the `para` god-dict + documentation

- Separate *settings* (and file references) from *data* (raw DataFrames, results).
  Functions should declare what they consume and return, rather than mutating one
  shared dict.
- Add docstrings/comments aimed at external users; consistent naming; remove
  commented-out debug path blocks scattered through several files.
- Fix `row_index` inconsistency in `set_parameters_sptPALM_GUI.py` (it is
  incremented but several rows use hardcoded literal row numbers).

### 3.4 Sub-track / moving-average diffusion (new, optional feature)

For very long tracks (organic fluorophores, many localisations), split a single
track into consecutive sub-tracks and report diffusion coefficients along the
track — a moving-average view that can reveal within-track diffusional state
changes. Basis: Uphoff lab, *J. Phys. Chem. B* 2024,
<https://pubs.acs.org/doi/full/10.1021/acs.jpcb.4c01454>.

**Design (resolved 2026-06-27):**

- **Data model:** add a `sub_track_id` column alongside `track_id`. Generalise the
  diffusion calc from "one D per `track_id`" to "one D per grouping key", where the
  key is `track_id` (whole-track, current) or `(track_id, sub_track_id)`
  (sub-track mode). Whole-track is the degenerate case — **one code path serves
  both.**
- **Windows:** fixed, **non-overlapping**, exactly *N* localisations
  (**default N = 4**), walking each track from the start. **Drop the remainder**
  (the leftover 1…N-1 locs at the track end). Justification: track lengths are
  exponentially distributed, so orphan remainders are a negligible data fraction
  in the long-track regime where this mode is used. *N* is a config parameter.
- **Consequence (intended, must be logged — never silent):** tracks shorter than
  *N* produce zero sub-tracks and are excluded from sub-track analysis. By the same
  exponential distribution these short tracks are the majority by count — fine,
  because whole-track analysis still uses ALL tracks and is unaffected. Log the
  count of too-short tracks excluded and remainder locs dropped.
- **Output:** a **separate diagnostic** (e.g. D-vs-time-along-track). Does NOT feed
  the main track-length histogram or MCDDA.
- **Scope note:** a single window still assumes the molecule is quasi-stationary
  within it (smaller window = finer state resolution but noisier D). A fully
  rigorous treatment of state switching would be a hidden-Markov approach
  (e.g. vbSPT) — out of scope here.

## 4. Cross-cutting design principles

- **Flexible yet stringent:** all parameters live in the JSON config (flexible),
  with validated defaults that **reproduce current behaviour when a new mode is
  off** (no silent change to existing results).
- **No silent data loss:** guards and logged counts wherever data is excluded
  (e.g. sub-track needs ≥2 locs to yield a D; too-short tracks reported, not
  dropped quietly).
- **Single code path** for whole-track and sub-track diffusion to avoid two
  implementations drifting apart.
- **Small, verified, isolated changes** over large rewrites; explain reasoning in
  plain terms and point to specific files/lines.
