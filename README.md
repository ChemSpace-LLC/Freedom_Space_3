
# Freedom 3 paper

This repository contains data and tools used in the **Freedom 3** paper to evaluate chemical diversity, enumerate compounds, assess synthetic accessibility, and analyze physicochemical properties.

##  Structure

```
Freedom_3_paper/
│
├── diversity_and_physchem_analysis/
│   ├── datasets/
│   ├── physicochemical_properties/
│   └── UMAP/
│
├── synthetic_accessibility/
│   ├── AiZynthFinder_Score/
│   ├── RAscore_and_SAscore/
│   └── Scored_Data/
│
├── enumeration_example/
└── synthons_example/
```

##  Diversity & Physchem Analysis
This module provides all necessary data and code to reproduce diversity and physicochemical analyses.

### Umap
To run UMAP-based diversity projections:

```bash
cd diversity_and_physchem_analysis/UMAP/
bash run_umap.sh
```
This module has been tested with the following packages and Python version:
- `Python 3.13.0`
- `rdkit 2024.9.2`
- `pandas 2.2.3`
- `umap 0.1.1`

### physicochemical_properties
Contains precomputed molecular properties and summary plots used in the analysis:

- phys_chem_prop.xlsx # Excel file with molecular descriptors
- plots.pptx # Summary visualizations used in the article

### datasets
Includes all compound datasets and their corresponding scaffold extractions used for diversity and scaffold analyses:

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

###  AiZynthFinder evaluation

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

### Scored Data

This directory contains all precomputed synthetic accessibility scores used to generate the plots and figures presented in the paper
```
synthetic_accessibility/Scored_Data/
├── 2_comp.tar.xz
├── 3_comp.tar.xz
└── random_1M.tar.xz
```
Each archive contains corresponding CSV files with computed SA/RA/AiZynthFinder scores used in the analysis.

## Enumeration & Synthons

This module provides tools for compound enumeration.

- Use `enumeration_example/enumeration.ipynb` for compound enumeration.
- Synthons and reaction files are available under `synthons_example/`.

#### Requirements

- `Python 3.13.0`
- `rdkit 2024.9.2`
- `pandas 2.2.3`

---


