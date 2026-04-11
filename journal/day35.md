# Day 35: Semantic Map Creation

## Objective
Built a semantic map creation pipeline in ROS2 by converting semantic segmentation masks into an OccupancyGrid representation.

---

## What I implemented

- Verified `semantic_map_node.py` in `nn_mapping`.
- Confirmed ROS2 executable exposure through `setup.py`.
- Ran `semantic_map_node` successfully.
- Brought up upstream pipeline:
  - `static_image_publisher` -> `/camera/image_raw`
  - `semantic_segmentation_node` -> `/camera/segmentation_mask`
  - `semantic_map_node` -> `/semantic_map`
- Verified `/semantic_map` was published as `nav_msgs/msg/OccupancyGrid`.

## Key pipeline

`/camera/image_raw` -> `/camera/segmentation_mask` -> `/semantic_map`

## Important observation

Initial CLI topic echoes looked misleading because large ROS image/message arrays were truncated. Direct validation and runtime logs confirmed the semantic mask and semantic map were producing nonzero content.

## Results

- Semantic map node launched successfully.
- OccupancyGrid publishing confirmed.
- Runtime logs showed nonzero semantic cells, e.g. `semantic_cells=1738`.
- Smol asset created: `assets/day35_semantic_map_creation.png`.

## Files involved

- `ws/src/nn_mapping/nn_mapping/semantic_map_node.py`.
- `ws/src/nn_mapping/setup.py`.
- `ws/src/nn_perception/nn_perception/semantic_segmentation_node.py`.

## Notes

This is an image-space semantic map prototype, not yet a geometrically consistent world-frame semantic mapping system. Good enough for Day 35 foundation.

---