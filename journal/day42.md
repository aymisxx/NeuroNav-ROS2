# Day 42: Perception-to-Planning Interface

---

## What I built

Started Phase 4 by creating the first bridge from perception output to planning input.

Created a new ROS2 package:

`nn_planning`

Created a new node:

`perception_to_planning_node`

## What the node does

The node subscribes to:

`/semantic_map` (`nav_msgs/msg/OccupancyGrid`)

And publishes:

`/planning/goal` (`geometry_msgs/msg/PoseStamped`)

Logic used:

- scan the semantic map.
- find the best valid cell.
- apply a small center-distance penalty.
- convert grid cell to world coordinates.
- publish a planning goal in the `map` frame.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws
source install/setup.bash

ros2 pkg create --build-type ament_python nn_planning --dependencies rclpy std_msgs nav_msgs geometry_msgs
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning perception_to_planning_node
ros2 run nn_sensors camera_publisher
ros2 run nn_perception semantic_segmentation_node
ros2 run nn_mapping semantic_map_node

ros2 topic echo /planning/goal --once
```

## Result

The full pipeline worked:

- camera stream published.
- semantic segmentation ran.
- semantic map was generated.
- planning goal was published from semantic-map input.

Example observed goal:

- `x ≈ 0.275`
- `y ≈ 0.475`

Later runtime logs showed multiple goal updates as the map kept updating.

## Issue faced

Initially tried:
```bash
ros2 run nn_sensors static_image_publisher
```

That executable did not exist.

Resolved by checking available executables and using:

```bash
ros2 run nn_sensors camera_publisher
```

## Asset

`assets/day42_perception_to_planning_interface.png`

---