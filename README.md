# Cross-Condition Information (CCI) Analysis Pipeline

**Lead Researcher & Developer:** Pieter Barkema  
**Status:** Reference Implementation (Research in Prep)

A high-performance Python pipeline for **Distributed Neuroimaging Analysis**. This repository implements **CCI**, a novel statistical framework I developed to investigate whether cortical noise in the human brain carries functional information for object recognition.

---

## 🚀 Executive Summary
* **The Problem:** Standard neuroimaging metrics (like RSA or Decoding) often treat trial-by-trial variance as "nuisance noise," potentially ignoring functional neural dynamics.
* **The Solution:** I invented **Cross-Condition Information (CCI)** to quantify the shared variance between a stable "class manifold" and stochastic neural noise.
* **The Engineering:** A modular, distributed pipeline built to scale across High-Performance Computing (HPC) clusters, processing multi-terabyte MEG datasets.

---

## 🔬 Technical Specifications (The CCI Framework)

### 1. Manifold Extraction (Signal)
The pipeline defines the "ideal" neural representation for a stimulus using **Class-Averaged Principal Component Analysis (PCA)**. 
* **Process:** Extraction of eigenvectors from class-averaged responses to identify the primary axes of the object-representation space.
* **Input:** High-dimensional MEG sensor data transformed into a lower-dimensional signal manifold.

### 2. Subspace Alignment (Noise Analysis)
CCI measures the **alignment** between individual "noisy" trials and the signal manifold defined above.
* **Hypothesis:** If trial-specific noise is co-linear with the class-level principal components, the variance is "informative" rather than stochastic.
* **Implementation:** Optimized covariance calculations to determine the shared information density between latent class archetypes and observational noise.

---

## 🛠 Engineering & Scalability
This project is designed for **Research Engineering** at scale:
* **Distributed Backend:** `informative_variance_grid_bash.sh` handles job scheduling and resource allocation for parallel processing across cluster nodes.
* **Optimized Compute:** `grid_cci_publ.py` manages memory-efficient data injection, allowing for the analysis of massive cohorts.
* **Vectorized Math:** Core logic in `cci_functions_publ.py` utilizes NumPy/SciPy for high-speed linear algebra operations.

---

## 📖 Related Literature & Frameworks
CCI bridges the gap between cognitive neuroscience and established Machine Learning concepts:
* **Manifold Learning:** Treating neural states as points on a low-dimensional manifold.
* **Probabilistic PCA:** Modeling the structure of noise relative to latent variables.
* **Signal-to-Noise Subspaces:** Quantifying how the brain's internal "noise" correlates with external stimulus categories.

---

## 📂 Repository Structure
* **`cci_functions_publ.py`**: The analytical engine containing the original CCI mathematical implementation.
* **`grid_cci_publ.py`**: The session-level wrapper for data injection and pipeline orchestration.
* **`informative_variance_grid_bash.sh`**: The cluster-orchestration script for distributed computing environments.

---

## 🎓 Impact
This pipeline is currently used in the **Kietzmann Lab** (Donders Institute) for MEG-analysis. The results provide evidence that cortical variance is structured and functionally relevant to how the human brain recognizes object classes.
