
# Freedom 3 paper

This repository contains data and tools used in the **Freedom 3** paper to evaluate chemical diversity, enumerate compounds, assess synthetic accessibility (RA & SA scores), and analyze physicochemical properties.

---

## 📁 Folder Structure

```
Freedom_3_paper/
│ 
├── diversity_and_physchem_analysis/
│   ├── datasets/
│   │   ├── ChEMBL35_for_scaffolds.csv.gz
│   │   ├── ChEMBL_unique_scaffolds.csv.gz
│   │   ├── Freedom_2_1M_random_compounds.csv.gz
│   │   ├── Freedom_2_1M_random_compounds_unique_scaffolds.csv.gz
│   │   ├── Freedom_3_1M_random_compounds.csv.gz
│   │   └── Freedom_3_1M_random_compounds_unique_scaffolds.csv.gz
│   ├── physicochemical_properties/
│   │   ├── phys_chem_prop.xlsx
│   │   └── plots.pptx
│   └── UMAP/
│       ├── run_umap.sh
│       └── umap_jaccard.py

├── synthetic_accessibility/
│   ├── AiZynthFinder_Score/
│   │   ├── 1K_SMILES.log
│   │   ├── 1K_SMILES.smi
│   │   ├── 1K_SMILES_with_AiZynthFinder_Score.csv
│   │   ├── custom_config.yml
│   │   ├── process_log_file.py
│   │   └── process_with_Aizynthfinder.sh
│   ├── RAscore_and_SAscore/
│   │   ├── 1K_SMILES.csv
│   │   ├── 1K_SMILES_SA_RA.csv
│   │   ├── Scoring_pipeline.ipynb
│   │   ├── requirements.txt
│   │   ├── RAscore/
│   │   └── SAscore/
│   └── Scored_Data/
│       ├── 2_comp.tar.xz
│       ├── 3_comp.tar.xz
│       └── random_1M.tar.xz
│ 
├── enumeration_example/
│   ├── enumeration.ipynb
│   └── enumeration_results_test.tsv
│      
└── synthons_example/
    ├── Freedom_3_0_reactions_example.tsv
    └── Freeedom 3_0_synthons_example.tsv

```
## Synthetic accessibility

### SA/RA Scoring

To assess synthetic accessibility and retrosynthetic tractability via RA and SA scores:

1. **Installation**  
   Navigate to the scoring module and install the required packages:

   ```bash
   cd synthetic_accessibility/RAscore_and_SAscore/
   pip install -r requirements.txt
    ```
> ⚠️ Note: TensorFlow 2.5.0 (CPU or GPU) is required for the legacy RA model.  

2. **Launch Scoring Pipeline**

Open in Jupyter:

```bash
jupyter notebook Scoring_pipeline.ipynb
```
The notebook performs the following steps:

- Loads SMILES from `1K_SMILES.csv`
- Computes:
    - **RA score** using a pretrained neural network model from [RAscore (reymond-group)](https://github.com/reymond-group/RAscore.git)
    - **SA score** using a fragment-based RDKit scoring approach from [SAscore (GeauxEric)](https://github.com/GeauxEric/SAscore.git)
- Saves result to `1K_SMILES_SA_RA.csv`

---
##  AiZynthFinder evaluation

To assess synthetic accessibility of compounds using **AiZynthFinder**, follow these steps:

1. **Installation**  
   AiZynthFinder was installed following the official documentation:  
   🔗 https://github.com/MolecularAI/aizynthfinder
   
2. **Retrosynthetic Planning**  
   To compute synthetic accessibility, the retrosynthesis pipeline was executed from:

   ```bash
   cd synthetic_accessibility/AiZynthFinder_Score/
   bash process_with_Aizynthfinder.sh
   ```

3. **Post-process the output**
    
    After computation is complete, results are parsed using:
    
    ```bash
    python process_log_file.py
    ```
    This generates 1K_SMILES_with_AiZynthFinder_Score.csv, which includes SMILES and their Solved_with_AiZynthFinder status.

## Scored Data

This directory contains all precomputed synthetic accessibility scores used to generate the plots and figures presented in the paper
```
synthetic_accessibility/Scored_Data/
├── 2_comp.tar.xz
├── 3_comp.tar.xz
└── random_1M.tar.xz+]
```
Each archive contains corresponding CSV files with computed SA/RA/AiZynthFinder scores used in the analysis.

---
## 📊 Diversity & Physchem Analysis

- All supporting datasets, UMAP embeddings, and plots are located in `diversity_and_physchem_analysis/`
- Launch UMAP scripts using the files in `diversity_and_physchem_analysis/UMAP/`:
  - `run_umap.sh`
  - `umap_jaccard.py`

---

### 📦 Requirements

This module has been tested with the following packages and Python version:

- `Python 3.13.0`
- `rdkit 2024.9.2`
- `pandas 2.2.3`
- `umap 0.1.1`



---
## Enumeration & Synthons

- Use `enumeration_example/enumeration.ipynb` for compound enumeration.
- Synthons and reaction mappings are available under `synthons_example/`.

---

### 📦 Requirements

This module has been tested with the following packages and Python version:

- `Python 3.13.0`
- `rdkit 2024.9.2`
- `pandas 2.2.3`
---


