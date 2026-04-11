# Day 45: Safety Layer

---

## What I built

Implemented a minimal safety layer inside:

`nn_planning`

New node:

`safety_layer_node`

## What the node does

The node subscribes to:

`/cmd_vel` (`geometry_msgs/msg/Twist`)

And publishes:

`/cmd_vel_safe` (`geometry_msgs/msg/Twist`)

## Safety logic

The safety layer applies simple command clamping:

- limit forward speed to a safe maximum.
- limit angular speed to a safe maximum.
- pass through safe values unchanged.
- publish the bounded command for downstream use.

Configured limits:

- `max_linear = 0.25`
- `max_angular = 0.80`

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# created safety_layer_node.py
# updated setup.py with new console script

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning safety_layer_node

ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{
  linear:  {x: 0.8, y: 0.0, z: 0.0},
  angular: {x: 0.0, y: 0.0, z: 1.5}
}"

ros2 topic echo /cmd_vel_safe --once
```

## Result

The safety layer correctly clamped an unsafe command.

Observed behavior:

- input `linear.x = 0.8` -> output `linear.x = 0.25`.
- input `angular.z = 1.5` -> output `angular.z = 0.8`.

This confirms the node is acting as a lightweight safety filter before command execution.

## Asset

`assets/day45_safety_layer_clamp_demo.png`

## Summary

Day 45 completed a minimal safety layer for NeuroNav-ROS2.

The pipeline now supports:

- planning goal -> velocity command.
- velocity command -> safety-filtered velocity command.
- safety-filtered command ready for downstream execution.

---