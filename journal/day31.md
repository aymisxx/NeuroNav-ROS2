# Day 31 - Mapping Demo

## Objective
Validate a minimal scan-to-map pipeline for the mapping stage.

## What I did
- Replaced the old dummy `occupancy_grid_node` logic with a scan-driven occupancy grid update.
- Kept `scan_processing_node` as the preprocessing stage:
  - subscribes to `/scan`
  - filters valid ranges
  - publishes `/scan_processed`
- Updated `occupancy_grid_node` to:
  - subscribe to `/scan_processed`
  - project scan points into a small 2D occupancy grid
  - publish `/map`

## Files worked on
- `src/nn_mapping/nn_mapping/occupancy_grid_node.py`

## Build
```bash
cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_mapping
```

## Validation
Ran:
```bash
source install/setup.bash
ros2 run nn_mapping scan_processing_node
ros2 run nn_mapping occupancy_grid_node
```

Since no active `/scan` publisher was available locally, I validated the pipeline using a one-shot synthetic `LaserScan`:

```bash
ros2 topic pub --once /scan sensor_msgs/msg/LaserScan "{
  header: {frame_id: 'base_scan'},
  angle_min: -1.57,
  angle_max: 1.57,
  angle_increment: 0.785,
  time_increment: 0.0,
  scan_time: 0.1,
  range_min: 0.12,
  range_max: 5.0,
  ranges: [2.0, 1.5, 1.0, 0.8, 1.2],
  intensities: []
}"
```

Observed:
- `scan_processing_node` reported valid scan statistics
- `occupancy_grid_node` published `/map`
- occupied cells detected: `5`

## Result
Minimal mapping demo completed successfully:

`/scan -> /scan_processed -> /map`

## Artifact
- `assets/day31_mapping_demo.png`

## Notes
- `turtlebot3_gazebo` was not available in the current ROS environment, so today’s demo was validated with synthetic scan input instead of a simulator-driven live LiDAR stream.
- The mapping node is now meaningfully connected to scan data instead of publishing a hardcoded toy grid.
