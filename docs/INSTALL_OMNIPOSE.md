# Installing Omnipose for the sptPALM pipeline

This guide covers installing [Omnipose](https://github.com/kevinjohncutler/omnipose)
so it can be used as a cell-segmentation option inside the sptPALM analysis
pipeline (as an alternative to the ImageJ/Fiji Watershed macro).

Omnipose runs in its **own conda environment**, separate from the environment you
use to run `sptPALM_main.py`. The pipeline launches it as a subprocess (see
[`OmniposeFromMain.py`](../OmniposeFromMain.py)).

> **Status:** verified against Omnipose **1.1.4** (Jan 2026) and the official
> install docs on 2026-07-19. The Quick-install path below was confirmed working
> on macOS via the standard `conda create` (no Apple-Silicon environment file
> needed) — the `omnipose` GUI launched successfully. If you install and something
> differs, please update this file — see
> [Keeping this future-proof](#keeping-this-future-proof).

---

## 1. Prerequisites

- An **Anaconda / Miniconda** installation of Python.
- (Optional) An NVIDIA GPU + driver if you want GPU-accelerated segmentation.
  Omnipose runs fine on CPU, just slower.

---

## 2. Quick install (recommended)

The current release of Omnipose installs cleanly with `pip` — no special
workarounds are needed. Follow the official docs
([installation guide](https://omnipose.readthedocs.io/installation.html),
[GitHub](https://github.com/kevinjohncutler/omnipose)); the steps below mirror them.

Open the **Anaconda Prompt** (it starts in the `(base)` environment) and run:

**1. Create a dedicated environment named `omnipose`:**

```bash
# CPU only
conda create -n omnipose 'python==3.10.12' pytorch
```

```bash
# With an NVIDIA GPU (CUDA 11.8)
conda create -n omnipose 'python==3.10.12' pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia
```

> The environment **must be called `omnipose`**, because that name is hardcoded in
> [`OmniposeFromMain.py`](../OmniposeFromMain.py). If you use a different name,
> change the `conda run -n omnipose ...` line in that file to match.

**2. Activate it:**

```bash
conda activate omnipose
```

The prompt changes from `(base)` to `(omnipose)`.

**3. Install Omnipose:**

```bash
pip install omnipose
```

This pulls in everything the sptPALM Omnipose scripts need — including
`scikit-image` (used for the cell-area / `regionprops` measurements) and
`torch`/`torchvision`.

**4. Verify it works** — from inside the `(omnipose)` environment, launch the
built-in Omnipose GUI:

```bash
omnipose
```

If the GUI opens, the install is good. You can close it again — the sptPALM
pipeline uses its own custom GUI, not this one.

---

## 3. Using Omnipose from the sptPALM pipeline

Once installed, you do **not** activate the `omnipose` environment yourself when
running the analysis. Run `sptPALM_main.py` from your usual sptPALM environment,
and in the **Set Parameters GUI**:

- Set **Segmentation method** to `Cellpose/Omnipose`.
- Leave **Already segmented (Omnipose only)** unchecked to launch the custom
  Omnipose segmentation GUI, or check it if masks already exist on disk.
- Optionally tick **Additional processing (Omnipose)** to average/pre-process raw
  brightfield stacks before segmentation.

The pipeline then launches Omnipose in its own environment via subprocess. See
README section 5 ("Omnipose: set-up + segmentation") for the full workflow, the
custom-GUI parameters, and the output filenames (`*_cp_masks.tif`,
`*_cp_masks_table.csv`).

---

## 4. Troubleshooting

### `ImportError: cannot import name 'ifft' from 'scipy'`

This was a well-known bug on **older** Omnipose installs. It came from an archived
third-party dependency (`peakdetect`) that imported `ifft` from the top-level
`scipy`, which broke with `scipy >= 1.12`.

**The current Omnipose release (1.1.4) no longer depends on `peakdetect`, so a
fresh `pip install omnipose` should not hit this at all.** If you do see it, you
are almost certainly installing an **old, pinned version** of Omnipose. Fixes, in
order of preference:

1. **Install the current release** (don't pin an old commit): `pip install -U omnipose`.
2. If you must use an old version, patch the one offending line in
   `.../site-packages/peakdetect/peakdetect.py` to read
   `from scipy.fft import fft, ifft` (confirmed working by multiple users).
3. Or pin `scipy < 1.12` inside the `omnipose` environment.

> ⚠️ **Do not** follow older install recipes that pin `python==3.9.18` together
> with a frozen Omnipose git commit (e.g. `...@bf456e47...`) and `aicsimageio`.
> Those exist only to work around this bug on the old code and will *reintroduce*
> the problem by installing outdated Omnipose on purpose.

### Apple Silicon (M1/M2/M3)

The official docs provide a dedicated environment file for Apple Silicon; if the
standard `conda create` above gives you trouble on an ARM Mac, use:

```bash
conda env create -f <path_to_apple_silicon_environment_file>
```

(See the [official installation guide](https://omnipose.readthedocs.io/installation.html).)

### GPU not being used

Segmentation falls back to CPU if no compatible GPU/driver is found (the scripts
print which one is in use). Make sure your PyTorch build matches your NVIDIA
driver/CUDA version.

---

## 5. Keeping this future-proof

- **Prefer the plain `pip install omnipose`** over any recipe that pins a specific
  old Omnipose commit — pinned SHAs and CUDA/wheel URLs go stale fast and are the
  main reason people still hit the `ifft` bug.
- Version pins in this doc (Python 3.10.12, CUDA 11.8) come from the official docs
  as of the date at the top. When you next install, check the
  [official installation guide](https://omnipose.readthedocs.io/installation.html)
  for the current recommendation and update the `Status` line above if it changed.
- The only sptPALM-specific requirement is that the environment is named
  `omnipose` (or that [`OmniposeFromMain.py`](../OmniposeFromMain.py) is edited to
  match your chosen name).
