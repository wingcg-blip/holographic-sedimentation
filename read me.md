# Holographic Sedimentation: Experimental Data & Analysis

This repository contains the quantum circuits, raw hardware counts, and analysis scripts for the study: **"Observation of Geometric Dark Matter Sedimentation on a 133-Qubit Superconducting Processor"**.

## Abstract
We propose dark matter as a geometric "sedimentation" effect arising from non-unitary holographic dynamics. Using the 133-qubit **IBM Torino** processor, we observe a $\mathbb{Z}_4$ topologically protected state at a cooling factor of $\gamma_c = 0.25$. This repository provides the data to verify the $0.018$ renormalization gap between laboratory results and Planck 2018 cosmological observations.

## Data Provenance
All experimental data were executed on the `ibm_torino` (Heron r1) backend.
- **Sniper Scan (Fig S2/S3):** Job ID `d59q2qjht8fs73a50kpg`
- **Finite-Size Scaling (Fig S4):** Job ID `d59q7e1smlfc739ksb3g`

## Repository Structure
- `/Data`: Raw JSON counts from IBM Quantum.
- `/Scripts`: Python scripts for Zero-Noise Extrapolation (ZNE) and Data Collapse.
- `/Circuits`: OpenQASM 3.0 representations of the sedimentation protocol.

## How to Cite
If you use this data or code in your research, please cite:
> Wangfujia et al., "Observation of Geometric Dark Matter Sedimentation...", (2025). [[(https://doi.org/10.5281/zenodo.18108172)]
