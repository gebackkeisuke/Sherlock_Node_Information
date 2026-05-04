# Sherlock Node Information Analyzer

This repository provides a tool to extract and analyze computing node information from the Stanford Sherlock HPC cluster.

## 🚀 Features

- Extract node information from `sinfo` and `scontrol`
- Generate structured CSV files:
  - `nodes_information_all.csv`
  - `nodes_information_machine_specs.csv`
- Analyze node hardware specifications
- Compare node performance across partitions and classes
- Identify suitable nodes based on CPU, memory, and GPU availability

---

## 📊 Output Example

The generated machine specs file includes:

| Column | Description |
|--------|-------------|
| NODE | Node name |
| CLASS | Node class (e.g., SH4_CBASE, SH3_G8TF64) |
| PARTITION | Slurm partition |
| CPUS | Number of CPUs |
| MEMORY | Total memory per node |
| CPU_MNF | CPU manufacturer |
| CPU_GEN | CPU generation |
| CPU_SKU | CPU model |
| CPU_FRQ | CPU frequency |
| GPU_SKU | GPU model (if available) |
| GPU_MEM | GPU memory |

---

## ⚙️ Usage

### 1. Login to Sherlock

```bash
ssh username@sherlock.stanford.edu
