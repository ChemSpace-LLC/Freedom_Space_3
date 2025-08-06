
# Freedom 3 paper

This repository contains data and tools used in the **Freedom 3** project to evaluate chemical diversity, enumerate compounds, assess synthetic accessibility (RA & SA scores), and analyze physicochemical properties.

---

## 📁 Folder Structure

```
Freedom_3_paper/
├── README.md
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
├── enumeration_example/
│   ├── enumeration.ipynb
│   └── enumeration_results_test.tsv
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
└── synthons_example/
    ├── Freedom_3_0_reactions_example.tsv
    └── Freeedom 3_0_synthons_example.tsv

```


## SA/RA Scoring
📦 Install requirements for scoring:

Navigate to `RAscore_and_SAscore/` and install:

```bash
cd synthetic_accessibility/RAscore_and_SAscore/
pip install -r requirements.txt
```
> ⚠️ Note: TensorFlow 2.5.0 (CPU or GPU) is required for the legacy RA model.  

Open in Jupyter:

```bash
jupyter notebook Scoring_pipeline.ipynb
```

This notebook:
- Loads SMILES from `1K_SMILES.csv`
- Computes:
  - **RA score** via pretrained NN model
  - **SA score** using RDKit-based scoring
- Saves result to `1K_SMILES_SA_RA.csv`

---

##  Synthetic Accessibility (AiZynthFinder)

To assess synthetic accessibility of compounds using **AiZynthFinder**, follow these steps:

1. **Install AiZynthFinder**  
   Installation was done following the official documentation:  
   🔗 https://github.com/MolecularAI/aizynthfinder

2. **Run retrosynthetic planning**  
   From the `synthetic_accessibility/AiZynthFinder_Score/` directory:

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


