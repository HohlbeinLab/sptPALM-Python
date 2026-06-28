# sptPALM-Python — Refactoring Plan & Design Decisions

Status: living document. Captures decisions made while modernising the analysis
pipeline so they travel with the code (collaborators, future maintainers, and the
original author). Last updated: 2026-06-27.

Progress: MSD bug fix done; **Step 1 done** (§3.1); faster startup done (§2.2b);
terminal/macOS runtime fixes done (§2.3); **Step 2 done** (§3.2, incl. gap
correction 3.2a). Next: Step 3 (§3.3, untangle the `para` god-dict).

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

### 2.3 Terminal / macOS runtime fixes (done 2026-06-27)

Surfaced when running from a plain terminal (the code was originally designed for
Spyder, where an integrated Tk/event loop hid these issues).

- Non-blocking plots (commit `d2fa3e7`): every `plt.show()` is now
  `plt.show(block=False)` + `plt.pause(0.1)`. With the `macosx` backend a plain
  `plt.show()` blocks until the window is closed by hand, which stalled the
  pipeline right after the tracking figure. Fixed in `tracking_sptPALM.py`,
  `plot_single_cell_analysis_sptPALM.py`, `plot_combined_data_sptPALM.py` (x2),
  `initiate_simulation.py`.
- Parameter GUI behaviour + macOS teardown (commits `56a7920`, `ea3f20a`):
  `set_parameters_sptPALM_GUI` was missing `root.mainloop()` in its body, so it
  returned immediately — the menu reappeared at once AND the user's edits were
  discarded (it returned the pre-edit defaults). Now it blocks until closed and
  returns the edited values. exit_GUI uses `root.quit()` (destroy-in-callback
  hangs/beachballs on macOS); after `mainloop()` the window is
  `withdraw()`+`update()`+`destroy()`-ed so it doesn't linger as a beachball
  before control returns to the blocking CLI prompt. Same fix applied to
  `set_parameters_simulation_GUI` (which also gained the missing
  `WM_DELETE_WINDOW` protocol).
- Stopped tracking generated outputs (commit `9bd8526`):
  `experimental_data/output_python/` and locally-saved `input_parameter.json` are
  gitignored; previously-tracked outputs were untracked.

Underlying takeaway: tkinter + a blocking terminal `input()` loop is fragile on
macOS. Spyder remains the smoother interactive environment; a browser-based GUI
(see §3.x ideas) would remove this fragility for good.

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

### 3.2 Retire the OLD diffusion function — DONE (2026-06-28)

Commits: `f94fbf6` (drop redundant MCDDA sort), `31b669d` (add
`diff_coeffs_per_track`), `6cc1215` (rewrite single_cell + wire in + delete OLD).
Plus sub-task 3.2a `d99a1d6` (gap correction).

- DONE: `analyse_diffusion_sptPALM` (fixed first-N-steps estimator) replaced by
  `diff_coeffs_from_tracks_fast.diff_coeffs_per_track` and the file deleted. These
  are different estimators (OLD = first `diff_avg_steps_min` steps; FAST =
  gap-corrected mean single-frame MSD over the first `min(locs, locs_max)`
  localisations); FAST kept as the foundation (track-length-resolved form the
  MCDDA/anaDDA machinery consumes; right given the exponential track-length
  distribution).
- DONE (Option B, chosen by Johannes): the per-cell/combined analyses use a higher
  minimum (`locs > diff_avg_steps_min`) than the track-length-resolved histogram
  (locs 2-8), keeping per-cell averages robust; long tracks are truncated to the
  first `tracklength_locs_max` localisations (kept, not dropped). `diff_coeffs_per_track`
  takes optional `locs_min`/`locs_max` overrides for this.
- DONE: `single_cell_analysis_sptPALM` rewritten to assign tracks to cells by a
  direct `track_id -> cell_id` lookup + groupby, replacing the fragile positional
  alignment (which silently broke if the diffusion list and cumulative per-cell
  track counts were filtered/ordered differently, and mismatched lengths once
  `number_tracks_per_cell` excluded cells).
- DONE: removed the redundant manual `sort_values(['track_id','frame'])` in
  `MC_diffusion_distribution_analysis_sptPALM.py`.
- VALIDATION (Cas12aScrambled_part1, reconstructed from `_py_out.csv`): new cell_id
  100% correct; per-cell avg D == groupby mean; Option B reproduces the OLD
  population exactly (2558 tracks, 273 kept cells) with per-cell D essentially
  unchanged (mean 0.612 -> 0.615, r=0.977, median |delta|=0.028).
- NOT YET re-verified through the live GUI pipeline end-to-end (case 2 -> combine ->
  plot). Worth a manual run to confirm plots render.

- **Sub-task 3.2a — port the track-memory / frame-gap correction into the FAST
  function (prerequisite).** The OLD function normalises a step that spans `con`
  frames (a localisation missing but bridged by `track_memory`) by dividing its
  squared displacement by `con`
  (`analyse_diffusion_sptPALM.py:45-51`, condition `0 < con <= track_memory+1`).
  The FAST `calculate_MSD` dropped this — it ignores the `frame` column entirely
  and treats every consecutive pair as 1 frame apart; the correction is only a
  commented TODO (`diff_coeffs_from_tracks_fast.py:158-160`, and even that stub
  only handled `con == 2`). With the current default `track_memory = 0` there are
  no gaps so the two agree, but enabling `track_memory > 0` would make FAST
  **overestimate** D on gapped steps. Fix: vectorise it — reshape the `frame`
  column too, `np.diff` to get per-step `con`, and divide the squared
  displacements by `con` where `0 < con <= track_memory+1` (raw otherwise).
  Read `track_memory` via `para.get('track_memory', 0)` since the simulation
  caller's `sim_input` has no such key (simulated tracks have no gaps).
  Verify: (a) regression — identical output to before when `track_memory = 0`;
  (b) synthetic — a deliberate frame gap divides that step's displacement by the
  gap. NOTE: OLD vs FAST still differ as estimators (first-N vs all-steps); this
  sub-task is only about the gap correction, not making the two numerically equal.

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
