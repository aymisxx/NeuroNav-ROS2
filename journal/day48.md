# Day 48: Parameter Tuning

---

## What I built

Updated the local planner in:

`nn_planning`

Node used:

`local_planner_node`

## What changed

The planner was upgraded from fixed constants to ROS2 parameters.

Exposed parameters:

- `max_linear`
- `max_angular`
- `k_linear`
- `k_angular`
- `goal_tolerance`

The node now reads parameter values on startup and prints them for verification.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# patched local_planner_node.py to use ROS2 parameters

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning local_planner_node --ros-args \
  -p max_linear:=0.30 \
  -p max_angular:=0.70 \
  -p k_linear:=0.40 \
  -p k_angular:=0.90 \
  -p goal_tolerance:=0.10

ros2 topic pub --once /planning/goal geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {
    position: {x: 1.0, y: 0.5, z: 0.0},
    orientation: {w: 1.0}
  }
}"

ros2 topic echo /cmd_vel --once
```

## Result

The tuned parameter set loaded correctly:

- `max_linear = 0.30`
- `max_angular = 0.70`
- `k_linear = 0.40`
- `k_angular = 0.90`
- `goal_tolerance = 0.10`

Observed command output for the test goal:

- `linear.x = 0.30`
- `angular.z ≈ 0.417`

This confirms the planner behavior now changes through runtime parameter tuning.

## Asset

`assets/day48_local_planner_parameter_tuning.png`

## Summary

Day 48 completed a minimal parameter-tuning upgrade for NeuroNav-ROS2.

The local planner is now cleaner, configurable, and better aligned with real ROS2 workflows.

---