# Day 50: Testing Automation

---

## What I built

Implemented a minimal test automation node inside:

`nn_planning`

New node:

`test_automation_node`

## What the node does

The node publishes:

`/sim_pose` (`geometry_msgs/msg/Pose2D`)

The node subscribes to:

`/behavior_state` (`std_msgs/msg/String`)

And publishes:

`/test_status` (`std_msgs/msg/String`)

## Test logic

The node performs a tiny automated regression check:

- publish a known test pose.
- expect the behavior logic node to classify it as `CRUISE`.
- publish `PASS` if the observed state matches.
- otherwise publish `FAIL`.

Test pose used:

- `x = 0.6`
- `y = 0.2`

Expected behavior state:

`CRUISE`

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# created test_automation_node.py
# updated setup.py with new console script

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning behavior_logic_node
ros2 run nn_planning test_automation_node
```

## Result

The automated test completed successfully.

Observed output:

- test pose sent: `(0.6, 0.2)`.
- expected behavior: `CRUISE`.
- test result: `PASS`.

This confirms the behavior logic can be checked automatically with a lightweight ROS2 test-style node.

## Asset

`assets/day50_test_automation_flow.png`

## Summary

Day 50 completed a minimal testing automation layer for NeuroNav-ROS2.

The planning stack now includes a tiny regression-test node that automatically validates behavior-state output.

---