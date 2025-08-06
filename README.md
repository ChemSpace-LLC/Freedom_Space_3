
# Freedom 3 – Enumeration, Synthetic Accessibility & Diversity Analysis

This repository contains data and tools used in the **Freedom 3** project to evaluate chemical diversity, enumerate compounds, assess synthetic accessibility (RA & SA scores), and analyze physicochemical properties.

---

## 📁 Folder Structure

```
Freedom_3_paper/
│
├── diversity_and_physchem_analysis/        # Chemical diversity and phys-chem analysis
│   ├── datasets/                           # Raw CSV datasets used in analysis
│   ├── physicochemical_properties/         # XLSX data and plots
│   └── UMAP/                               # UMAP dimensionality reduction (scripts)
│
├── enumeration_example/                    # Example of compound enumeration
│   ├── enumeration.ipynb                   # Jupyter notebook for enumeration
│   └── enumeration_results_test.tsv        # Output file with enumeration results
│
├── synthetic_accessibility/                # Synthetic accessibility evaluation
│   ├── AiZynthFinder_Score/                # AiZynthFinder output, config, and script
│   ├── RAscore_and_SAscore/                # SA & RA scoring code and data
│   │   ├── 1K_SMILES.csv                   # Input SMILES
│   │   ├── 1K_SMILES_SA_RA.csv             # Output scores
│   │   ├── RAscore/                        # RAscore model code and weights
│   │   ├── SAscore/                        # SAscore scoring script and pickle
│   │   ├── Scoring_pipeline.ipynb          # Main notebook for scoring
│   │   └── requirements.txt                # Environment dependencies
│   └── Scored_Data/                        # Archived results (.tar.xz)
│
├── synthons_example/                       # Synthons and reaction examples
│   ├── Freedom_3_0_reactions_example.tsv
│   └── Freeedom 3_0_synthons_example.tsv
│
└── README.md                               # This file
```

---

## 🚀 Quick Start

### 1. 🧪 Create and activate a Conda environment:

```bash
conda create -n freedom3 python=3.8
conda activate freedom3
```

### 2. 📦 Install requirements for scoring:

Navigate to `RAscore_and_SAscore/` and install:

```bash
cd synthetic_accessibility/RAscore_and_SAscore/
pip install -r requirements.txt
```

> ⚠️ Note: TensorFlow 2.5.0 (CPU or GPU) is required for the legacy RA model.  
> Make sure `model.h5` is used instead of `.tf` format due to Keras 3 compatibility.

---

## 🧠 Notebooks

### ▶️ Run SA/RA Scoring

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

## 🧪 Synthetic Accessibility (AiZynthFinder)

To score via AiZynthFinder:

```bash
cd synthetic_accessibility/AiZynthFinder_Score/
bash process_with_Aizynthfinder.sh
```

This runs `aizynthcli` on `1K_SMILES.smi` using a custom config and logs progress.

To post-process results:

```bash
python process_log_file.py
```

---

## 📊 Diversity & Physchem Analysis

- All supporting datasets, UMAP embeddings, and plots are located in `diversity_and_physchem_analysis/`
- Launch UMAP scripts using:
```bash
cd UMAP
bash run_umap.sh
```

---

## 🧱 Enumeration & Synthons

- Use `enumeration_example/enumeration.ipynb` for compound enumeration.
- Synthons and reaction mappings are available under `synthons_example/`.

---

## 📬 Contact

For questions or collaboration: **Serhii Hlotov**

---

## ✅ License

This project is for research and academic purposes only. License TBD.
