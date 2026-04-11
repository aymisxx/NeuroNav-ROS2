# Day 47: Lifecycle Nodes

---

## What I built

Implemented a minimal lifecycle manager inside:

`nn_planning`

New node:

`lifecycle_manager_node`

## What the node does

The node publishes:

`/lifecycle_state` (`std_msgs/msg/String`)

## Lifecycle logic

The node simulates a tiny lifecycle progression:

- start in `unconfigured`.
- move to `inactive`.
- move to `active`.
- remain in `active` afterward.

A timer publishes the current lifecycle state every 2 seconds.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# created lifecycle_manager_node.py
# updated setup.py with new console script

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning lifecycle_manager_node
```

## Result

The lifecycle manager published the expected sequence:

- `unconfigured`.
- `inactive`.
- `active`.

After reaching `active`, it stayed there on subsequent timer callbacks.

## Asset

`assets/day47_lifecycle_state_progression.png`

## Summary

Day 47 completed a minimal lifecycle-state demo for NeuroNav-ROS2.

The planning package now also contains a lightweight lifecycle progression node for bringup-style state signaling.

---