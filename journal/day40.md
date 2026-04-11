# Day 40: Performance Optimization

## Objective

Performed a minimal runtime optimization on the semantic mapping pipeline by reducing unnecessary per-frame logging.

---

## What I changed

- Updated `semantic_map_node.py`.
- Removed the repeated per-frame info log: `Published semantic map | semantic_cells=...`.
- Kept the startup log intact.

## Why

Per-frame console logging adds unnecessary runtime overhead and clutters terminal output during continuous publishing. For this stage, reducing log spam improves cleanliness and slightly lightens execution.

## Validation

- Rebuilt `nn_mapping`.
- Relaunched `semantic_map_node`.
- Confirmed:
  - startup log still appears.
  - node runs successfully.
  - per-frame spam no longer appears.

## Files involved

`ws/src/nn_mapping/nn_mapping/semantic_map_node.py`

## Asset

`assets/day40_performance_optimization.png`

---