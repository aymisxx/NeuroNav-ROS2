# Day 51: Stress Testing

---

## What I built

Implemented a minimal stress test node inside:

`nn_planning`

New node:

`stress_test_node`

## What the node does

The node publishes:

`/cmd_vel` (`geometry_msgs/msg/Twist`)

And publishes a summary on:

`/stress_status` (`std_msgs/msg/String`)

## Stress-test logic

The node performs a tiny burst-style load test:

- publish 20 velocity commands.
- vary `linear.x` and `angular.z` over time.
- stop after the fixed burst length.
- publish a completion summary.

Configured burst:

- `total_steps = 20`.
- timer period = `0.1 s`.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# created stress_test_node.py
# updated setup.py with new console script

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning stress_test_node
```

## Result

The stress test completed successfully.

Observed output:

- startup message confirmed burst publishing.
- final summary: `COMPLETE: published 20 commands`.

This confirms the node can generate a small burst workload for downstream planning and control components.

## Asset

`assets/day51_stress_test_command_burst.png`

## Summary

Day 51 completed a minimal stress-testing layer for NeuroNav-ROS2.

The planning package now includes a tiny burst-command generator for lightweight load testing.

---