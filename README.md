# CCI: Cross-Class Information Pipeline
Author: Pieter Barkema

This repository contains the reference implementation for Cross-Class Information (CCI), a novel statistical metric I developed as part of the Kietzmann Lab (https://www.kietzmannlab.org/) to investigate the functional role of cortical noise in class recognition. I designed CCI to quantify information from human brain data about what object category a human participant is viewing, in a unique way. Unlike standard methods, CCI distills object category information from the variability of brain responses, that are typically seen as noise.

# 🧠 Scientific Context: Cortical Noise & Class Recognition
The objective of this pipeline is to investigate the functional role of cortical noise in the human brain. Specifically, the analysis tests the hypothesis that neural "noise" is not merely stochastic interference but is actively useful for class recognition ('noise is a feature not a bug'), and aids in one-shot learning.

By  Contrasted-Class Information (CCI) metrics, this pipeline quantifies how much information about an object category is carried within the variability of neural states, helping to understand how variability in neural firing may not be deterimental to - but is actually necessary for - robust object recognition.

# MEG Analysis Pipeline: Informative Variance & CCI
This repository contains code for a high-performance neuroimaging pipeline used to analyze Magnetoencephalography (MEG) (300-dimensional time-series) data.

🚀 Key Features
Distributed Processing: A bash-driven grid-engine interface for parallelizing analysis across massive datasets.

Statistical Analysis: Custom Python implementation of Cross-Condition Information (CCI) metrics.

Production Ready: Independent codebase currently being used for upcoming scientific publications.

🛠 Tech Stack
Language: Python (NumPy, SciPy, MNE-Python)

HPC: Shell scripting for distributed grid computing.

Domain: Multivariate Pattern Analysis (MVPA), Neuroimaging, Statistics.

📁 Architecture
cci_functions_publ.py: The analytical engine containing statistical functions.

grid_cci_publ.py: The wrapper for session-level data injection.

informative_variance_grid_bash.sh: The job scheduler for cluster-wide distribution.
