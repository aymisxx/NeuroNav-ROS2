# Day 28 - Map update pipeline

## Goal
Extend the static occupancy grid publisher into a minimal map update pipeline.

---

## What I built

Updated `occupancy_grid_node.py` so the published 5x5 occupancy grid changes over time.
A moving unknown cell (`-1`) sweeps across the middle row while fixed occupied cells remain in place.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_mapping
source install/setup.bash
ros2 run nn_mapping occupancy_grid_node
ros2 topic echo /map --once
```

## Result

The `/map` topic published a valid `nav_msgs/OccupancyGrid`, and repeated samples confirmed that the map contents updated over time.

## Asset
- `assets/day28_map_update.png`
- `assets/day28_map_update_output.txt`

## Notes
This is a minimal synthetic update pipeline, but it establishes the core idea of time-varying map publication for later mapping stages.

---