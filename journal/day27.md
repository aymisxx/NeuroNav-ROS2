# Day 27: Occupancy Grid Basics

## What I built

Created a minimal ROS2 Python package `nn_mapping` with a node that publishes a toy `nav_msgs/OccupancyGrid` message on `/map`.

---

## Node

- `occupancy_grid_node`.
- topic: `/map`.
- message type: `nav_msgs/msg/OccupancyGrid`.

## Map setup

- resolution: `1.0`.
- width: `5`.
- height: `5`.
- frame: `map`.

## Cell meaning used

- `0` = free.
- `100` = occupied.
- `-1` = unknown.

## Validation

- Built package successfully with `colcon build --packages-select nn_mapping`.
- Ran node with `ros2 run nn_mapping occupancy_grid_node`.
- Verified `/map` topic exists.
- Verified message contents using `ros2 topic echo /map --once`.

## Asset

`assets/day27_map_echo.png`

## Outcome

Completed the Day 27 basics milestone for occupancy grid publishing in ROS2.

---