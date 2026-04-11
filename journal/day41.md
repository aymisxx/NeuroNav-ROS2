# Day 41: Semantic Perception Demo

## Objective

Ran a minimal end-to-end semantic perception demo using the Day 35 semantic pipeline components.

---

## Demo pipeline

- `static_image_publisher` -> `/camera/image_raw`.
- `semantic_segmentation_node` -> `/camera/segmentation_mask`.
- `semantic_map_node` -> `/semantic_map`.

## Validation

Confirmed all three key topics were active:

- `/camera/image_raw`
  - Type: `sensor_msgs/msg/Image`
  - Publisher count: 1
  - Subscription count: 1

- `/camera/segmentation_mask`
  - Type: `sensor_msgs/msg/Image`
  - Publisher count: 1
  - Subscription count: 1

- `/semantic_map`
  - Type: `nav_msgs/msg/OccupancyGrid`
  - Publisher count: 1
  - Subscription count: 0

## Files involved

- `ws/src/nn_perception/nn_perception/static_image_publisher.py`.
- `ws/src/nn_perception/nn_perception/semantic_segmentation_node.py`.
- `ws/src/nn_mapping/nn_mapping/semantic_map_node.py`.

## Notes

This demo confirms the semantic perception chain is functioning end-to-end at a prototype level: image input, segmentation output, and semantic map generation.

## Asset

`assets/day41_semantic_perception_demo.png`

---