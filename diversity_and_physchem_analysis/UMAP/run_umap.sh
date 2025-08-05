#!/bin/bash

# ---------------- SETTINGS ----------------
PYTHON_SCRIPT="umap_jaccard.py"

# List your datasets
DATASETS=(
    "Freedom_2_unique_scaffolds.csv"
    "Freedom_3_unique_scaffolds.csv"
    "chembl_cutted_smi_unique_scaffolds.csv"
)

# Legends for each dataset (must match order and count of DATASETS)
LEGENDS=(
    "Freedom 2.0"
    "Freedom 3.0"
    "ChEMBL"
)

# Colors for each dataset (hex codes, same order)
COLORS=(
    "#E76254"
    "#1E466E"
    "#0e959a"
)

# Optional: path to cache directory
CACHE_DIR="output_2025-06-30_0217"  # e.g., "./umap_cache" or leave as ""

# UMAP parameters
N_NEIGHBORS=50
MIN_DIST=0.1

# Set to true to enable threadpool control in UMAP (recommended on shared CPUs)
USE_THREADPOOL=true
# ---------------- END SETTINGS ----------------

# Build command
CMD=(python "$PYTHON_SCRIPT")

# Add datasets
CMD+=(--datasets)
for dataset in "${DATASETS[@]}"; do
    CMD+=("$dataset")
done

# Add legends
CMD+=(--legends)
for legend in "${LEGENDS[@]}"; do
    CMD+=("$legend")
done

# Add colors
CMD+=(--colors)
for color in "${COLORS[@]}"; do
    CMD+=("$color")
done

# Add cache dir if provided
if [[ -n "$CACHE_DIR" ]]; then
    CMD+=(--cache_dir "$CACHE_DIR")
fi

# Add threadpool flag if enabled
if [[ "$USE_THREADPOOL" == true ]]; then
    CMD+=(--use_threadpool)
fi

# Add UMAP parameters
CMD+=(--n_neighbors "$N_NEIGHBORS")
CMD+=(--min_dist "$MIN_DIST")

# Run the command
echo "Running command:"
echo "${CMD[@]}"
"${CMD[@]}"

