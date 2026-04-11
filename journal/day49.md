# Day 49: Logging and Diagnostics

---

## What I built

Implemented a minimal diagnostics logger inside:

`nn_planning`

New node:

`diagnostics_logger_node`

## What the node does

The node subscribes to:

`/cmd_vel_safe` (`geometry_msgs/msg/Twist`)

And publishes:

`/diagnostics_status` (`std_msgs/msg/String`)

## Diagnostics logic

The node classifies command magnitude into simple status bands:

- `OK` for low command values.
- `WARN` for moderate command values.
- `ALERT` for high command values.

Threshold logic:

- `ALERT` when `|linear.x| >= 0.25` or `|angular.z| >= 0.80`.
- `WARN` when `|linear.x| >= 0.15` or `|angular.z| >= 0.50`.
- otherwise `OK`.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# created diagnostics_logger_node.py
# updated setup.py with new console script

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning diagnostics_logger_node

ros2 topic pub --once /cmd_vel_safe geometry_msgs/msg/Twist "{
  linear:  {x: 0.25, y: 0.0, z: 0.0},
  angular: {x: 0.0, y: 0.0, z: 0.80}
}"

ros2 topic echo /diagnostics_status --once
```

## Result

The diagnostics logger correctly classified the test command.

Observed test:

- input `linear.x = 0.25`.
- input `angular.z = 0.80`.
- output status: `ALERT`.

This confirms the node acts as a lightweight diagnostics/status layer for motion commands.

## Asset

`assets/day49_diagnostics_threshold_bands.png`

## Summary

Day 49 completed a minimal logging and diagnostics layer for NeuroNav-ROS2.

The planning package now includes a tiny command-health monitor that converts safe velocity commands into readable status labels.

---