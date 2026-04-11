# Day 53 - Demo Recording

---

## What I built

Implemented a minimal demo recorder inside:

`nn_planning`

New node:

`demo_recorder_node`

## What the node does

The node subscribes to:

- `/planning/goal` (`geometry_msgs/msg/PoseStamped`).
- `/cmd_vel_safe` (`geometry_msgs/msg/Twist`).
- `/sim_pose` (`geometry_msgs/msg/Pose2D`).
- `/behavior_state` (`std_msgs/msg/String`).
- `/diagnostics_status` (`std_msgs/msg/String`).

It writes a compact summary file to:

`/tmp/day53_demo_summary.txt`

## Demo-recording logic

The node acts as a tiny demo observer:

- count messages arriving on key stack topics.
- wait for a short recording window.
- write a compact summary text file.
- log the summary write path.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# created demo_recorder_node.py
# updated setup.py with new console script

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 launch nn_planning day52_full_system_bringup.launch.py
ros2 run nn_planning demo_recorder_node

ros2 topic pub --once /planning/goal geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {
    position: {x: 1.0, y: 0.5, z: 0.0},
    orientation: {w: 1.0}
  }
}"

cat /tmp/day53_demo_summary.txt
```

## Result

The demo recorder ran successfully and produced a real summary file.

Observed summary:

- `planning_goal_messages: 1`
- `cmd_vel_safe_messages: 0`
- `sim_pose_messages: 100`
- `behavior_state_messages: 197`
- `diagnostics_status_messages: 0`

This run captured a live bringup plus one planning-goal poke. It recorded strong activity on simulated pose and behavior-state topics, while safe-command and diagnostics traffic remained zero in this specific run.

## Asset

`assets/day53_demo_recording_summary.png`

## Summary

Day 53 completed a minimal demo-recording layer for NeuroNav-ROS2.

The planning stack now includes a tiny recorder node that watches key topics and writes a compact demo summary artifact.

---