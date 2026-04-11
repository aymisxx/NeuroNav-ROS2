# Day 46: Behavior Logic

---

## What I built

Implemented a minimal behavior logic node inside:

`nn_planning`

New node:

`behavior_logic_node`

## What the node does

The node subscribes to:

`/sim_pose` (`geometry_msgs/msg/Pose2D`)

And publishes:

`/behavior_state` (`std_msgs/msg/String`)

## Behavior logic

The node selects a simple discrete state from robot distance to origin:

- `IDLE` when radius < `0.20`.
- `CRUISE` when `0.20 <= radius < 1.00`.
- `RECOVER` when radius >= `1.00`.

This creates a tiny behavior layer on top of the navigation simulation.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# created behavior_logic_node.py
# updated setup.py with new console script

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning behavior_logic_node

ros2 topic pub --once /sim_pose geometry_msgs/msg/Pose2D "{
  x: 0.6,
  y: 0.2,
  theta: 0.0
}"

ros2 topic echo /behavior_state --once
```

## Result

The behavior logic node correctly mapped a simulated pose to a behavior state.

Observed test:

- input pose: `(x=0.6, y=0.2)`.
- radius: about `0.63`.
- output state: `CRUISE`.

## Asset

`assets/day46_behavior_logic_thresholds.png`

## Summary

Day 46 completed a minimal behavior-selection layer for NeuroNav-ROS2.

The pipeline now includes:

- planning goal -> velocity command.
- velocity command -> simulated pose.
- simulated pose -> behavior state.

---