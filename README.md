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

## 📊 Output Example (May 4, 2026)

| NODE | CLASS | PARTITION | CPUS | TOTAL_NODES | TOTAL_CPUS | MEMORY[GB/node] | MEMORY[GB/cpu] | CPU_MNF | CPU_GEN | CPU_SKU | CPU_FRQ | GPU_SKU | GPU_MEM |
|------|-------|------------|------|--------------|-------------|-----------------|----------------|----------|---------|----------|----------|---------|--------|
| sh03-08n49 | SH3_CBASE.1 | serc | 32 | 96 | 3072 | 250 | 7.81 | AMD | MLN | 7543 | 2.75GHz |  |  |
| sh03-17n01 | SH3_G8TF64.1 | serc | 128 | 4 | 512 | 1000 | 7.81 | AMD | MLN | 7763 | 2.45GHz | A100_SXM4 | 80GB |
| sh03-18n11 | SH3_G4TF64.1 | serc | 64 | 2 | 128 | 500 | 7.81 | AMD | MLN | 7543 | 2.75GHz | A100_SXM4 | 80GB |
| sh04-09n01 | SH4_G8TF64 | serc | 64 | 1 | 64 | 2000 | 31.25 | INTEL | SPR | 8462Y+ | 2.80GHz | H100_SXM5 | 80GB |
| sh03-14n03 | SH3_G8TF64 | serc | 128 | 6 | 768 | 1000 | 7.81 | AMD | RME | 7662 | 2.00GHz | A100_SXM4 | 40GB |
| sh03-14n17 | SH3_CPERF | serc | 128 | 8 | 1024 | 1000 | 7.81 | AMD | RME | 7742 | 2.25GHz |  |  |
| sh04-03n14 | SH4_CPERF | serc | 64 | 13 | 832 | 375 | 5.86 | AMD | GEN | 9384X | 3.10GHz |  |  |
| sh04-06n13 | SH4_CSCALE | serc | 256 | 4 | 1024 | 1500 | 5.86 | AMD | BGM | 9754 | 2.25GHz |  |  |
| sh02-10n61 |  | serc | 24 | 12 | 288 | 375 | 15.62 | INTEL | SKX | 5118 | 2.30GHz |  |  |
| sh02-16n08 |  | serc | 24 | 2 | 48 | 186.5 | 7.77 | INTEL | SKX | 5118 | 2.30GHz | V100_PCIE | 32GB |
| sh03-04n41 | SH3_CBASE | serc | 32 | 104 | 3328 | 250 | 7.81 | AMD | RME | 7502 | 2.50GHz |  |  |
| sh04-05n17 | SH4_CBASE | serc | 24 | 97 | 2328 | 187.5 | 7.81 | AMD | SIE | 8224P | 2.55GHz |  |  |

---

## ⚙️ Usage
- Login to Sherlock
- Run main.py
