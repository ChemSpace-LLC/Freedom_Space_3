import pandas as pd
import plotly.graph_objects as go
import os
import argparse
import logging
from datetime import datetime
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
import scipy.sparse as sp
from joblib import Parallel, delayed, dump, load
import umap
from PIL import Image
import multiprocessing
from threadpoolctl import threadpool_limits

# ---------- Utilities ----------

def smiles_to_fingerprint(smiles, radius=2, n_bits=2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=n_bits)
        return sp.csr_matrix(np.array(fp))
    else:
        return None

def generate_fingerprints(file_path, chunk_size, num_cores):
    fps = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        logging.info(f"Processing chunk of size {len(chunk)} from {file_path}")
        results = Parallel(n_jobs=num_cores)(delayed(smiles_to_fingerprint)(smi) for smi in chunk['smiles'])
        valid = [fp for fp in results if fp is not None]
        fps.extend(valid)
    return sp.vstack(fps)

def save_sparse_matrix(path, matrix):
    dump(matrix, path)

def load_sparse_matrix(path):
    return load(path)

def save_umap(path, coords):
    pd.DataFrame(coords, columns=['Component1', 'Component2']).to_csv(path, index=False)

def load_umap(path):
    return pd.read_csv(path).to_numpy()

def sanitize(name):
    return name.replace(" ", "_").replace(".", "_").replace(",", "_")

def save_plot(fig, filename_base, output_dir):
    png_path = os.path.join(output_dir, f"{filename_base}.png")
    tiff_path = os.path.join(output_dir, f"{filename_base}.tiff")
    fig.write_image(png_path, scale=2)
    img = Image.open(png_path)
    img.save(tiff_path, format='TIFF')

# ---------- Plotting ----------

def plot_umap_single(data, label, color, output_dir, filename):
    fig = go.Figure()
    fig.add_trace(go.Scattergl(
        x=data[:, 0], y=data[:, 1],
        mode='markers',
        marker=dict(size=6, color=color, opacity=0.5),
        name=label
    ))
    fig.update_layout(
        title=label,
        showlegend=False,
        xaxis=dict(title='UMAP1', showgrid=True, gridcolor='white', scaleanchor='y'),
        yaxis=dict(title='UMAP2', showgrid=True, gridcolor='white'),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Arial', size=30, color='black'),
        width=2000, height=2000
    )
    save_plot(fig, filename, output_dir)

def plot_umap_combined(coords1, coords2, label1, label2, color1, color2, output_dir, filename):
    fig = go.Figure()
    fig.add_trace(go.Scattergl(
        x=coords1[:, 0], y=coords1[:, 1],
        mode='markers',
        marker=dict(size=6, color=color1, opacity=0.2),
        name=label1
    ))
    fig.add_trace(go.Scattergl(
        x=coords2[:, 0], y=coords2[:, 1],
        mode='markers',
        marker=dict(size=6, color=color2, opacity=0.2),
        name=label2
    ))
    x_min = min(coords1[:, 0].min(), coords2[:, 0].min())
    x_max = max(coords1[:, 0].max(), coords2[:, 0].max())
    y_min = min(coords1[:, 1].min(), coords2[:, 1].min())
    y_max = max(coords1[:, 1].max(), coords2[:, 1].max())
    margin = 0.05
    x_range = [x_min - (x_max - x_min) * margin, x_max + (x_max - x_min) * margin]
    y_range = [y_min - (y_max - y_min) * margin, y_max + (y_max - y_min) * margin]
    fig.update_layout(
        showlegend=False,
        xaxis=dict(title="UMAP1", showgrid=True, gridcolor='white', scaleanchor='y', range=x_range),
        yaxis=dict(title="UMAP2", showgrid=True, gridcolor='white', range=y_range),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="Arial", color="black", size=30),
        autosize=False,
        width=2000,
        height=2000
    )
    save_plot(fig, filename, output_dir)

# ---------- Main ----------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datasets', nargs='+', required=True)
    parser.add_argument('--legends', nargs='+', required=True)
    parser.add_argument('--colors', nargs='+', required=True)
    parser.add_argument('--cache_dir', default=None)
    parser.add_argument('--use_threadpool', action='store_true', help="Use threadpool-limited UMAP")
    parser.add_argument('--n_neighbors', type=int, default=50, help="Number of neighbors for UMAP")
    parser.add_argument('--min_dist', type=float, default=0.1, help="Minimum distance for UMAP")
    args = parser.parse_args()

    # Validate lengths
    if not (len(args.datasets) == len(args.legends) == len(args.colors)):
        raise ValueError(f"Mismatch: {len(args.datasets)} datasets, {len(args.legends)} legends, {len(args.colors)} colors")

    now = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = f"output_{now}"
    os.makedirs(output_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(output_dir, "log.txt")),
            logging.StreamHandler()
        ]
    )

    chunk_size = 100_000
    num_cores = max(1, multiprocessing.cpu_count() // 2)

    all_fps = []
    lengths = []
    base_names = []

    for dataset in args.datasets:
        base = sanitize(os.path.splitext(os.path.basename(dataset))[0])
        base_names.append(base)
        cache = args.cache_dir if args.cache_dir else output_dir
        fp_path = os.path.join(cache, f"fp_{base}.pkl")

        if os.path.exists(fp_path):
            logging.info(f"Loading fingerprints: {fp_path}")
            fps = load_sparse_matrix(fp_path)
        else:
            logging.info(f"Generating fingerprints for {dataset}")
            fps = generate_fingerprints(dataset, chunk_size, num_cores)
            save_sparse_matrix(fp_path, fps)

        all_fps.append(fps)
        lengths.append(fps.shape[0])

    combined_fp = sp.vstack(all_fps)

    umap_path = os.path.join(args.cache_dir if args.cache_dir else output_dir, "umap_combined.csv")
    if os.path.exists(umap_path):
        logging.info(f"Loading combined UMAP: {umap_path}")
        combined_coords = load_umap(umap_path)
    else:
        logging.info(f"Running UMAP (n_neighbors={args.n_neighbors}, min_dist={args.min_dist})")
        reducer = umap.UMAP(
            n_neighbors=args.n_neighbors,
            min_dist=args.min_dist,
            metric='jaccard',
            random_state=42
        )

        if args.use_threadpool:
            with threadpool_limits(limits=1):
                combined_coords = reducer.fit_transform(combined_fp)
        else:
            combined_coords = reducer.fit_transform(combined_fp)

        save_umap(umap_path, combined_coords)

    # Split and plot
    start = 0
    coords_list = []
    for i, (length, legend, color, base) in enumerate(zip(lengths, args.legends, args.colors, base_names)):
        end = start + length
        coords = combined_coords[start:end]
        coords_list.append(coords)
        plot_umap_single(coords, legend, color, output_dir, f"umap_{base}")
        start = end

    # Overlays (all ordered pairs)
    for i in range(len(coords_list)):
        for j in range(len(coords_list)):
            if i != j:
                plot_umap_combined(
                    coords_list[i], coords_list[j],
                    args.legends[i], args.legends[j],
                    args.colors[i], args.colors[j],
                    output_dir,
                    f"umap_overlay_{base_names[i]}_{base_names[j]}"
                )

if __name__ == '__main__':
    main()
