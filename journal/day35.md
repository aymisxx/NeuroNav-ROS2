# Day 35: Semantic Map Creation

## Summary
Implemented a semantic mapping node that converts segmentation masks into a structured Occupancy Grid representation.

---

## Pipeline

/camera/image_raw → /camera/segmentation_mask → /semantic_map

## Implementation Details

- Created `semantic_map_node` in `nn_mapping`.
- Subscribes to segmentation mask and resizes it to a grid.
- Converts semantic pixels into occupancy values (100).
- Publishes to `/semantic_map`.

## Validation

- Verified topic flow across all nodes.
- Confirmed non-zero semantic pixels (~174k in mask).
- Verified semantic map occupancy cells (~39 active cells after resizing).
- Observed stable publishing behavior.

## Issues & Fixes

- Encountered NumPy incompatibility (NumPy 2.x vs ROS cv_bridge).
- Resolved by downgrading to NumPy 1.26.4 in virtual environment.
- Adjusted HSV thresholds for better segmentation.

## Result
End-to-end semantic perception pipeline is functional and producing structured map outputs.

## Asset
Terminal log showing semantic_map_node publishing dynamic semantic_cells values (39 ↔ 1738)

---