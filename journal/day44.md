# Day 44: Navigation Simulation

---

## What I built

Implemented a minimal navigation simulator inside:

`nn_planning`

New node:

`navigation_sim_node`

## What the node does

The node subscribes to:

`/cmd_vel` (`geometry_msgs/msg/Twist`)

And publishes:

`/sim_pose` (`geometry_msgs/msg/Pose2D`)

## Simulator logic

The simulator uses a very lightweight 2D kinematic update:

- receive linear and angular velocity.
- integrate heading over time.
- integrate x-y motion using the current heading.
- publish the simulated pose.
- log the trajectory to CSV for plotting.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws/src/nn_planning
# created navigation_sim_node.py
# updated setup.py with new console script

cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_planning
source install/setup.bash

ros2 run nn_planning navigation_sim_node
ros2 run nn_planning local_planner_node

ros2 topic pub --once /planning/goal geometry_msgs/msg/PoseStamped "{
  header: {frame_id: 'map'},
  pose: {
    position: {x: 1.0, y: 0.5, z: 0.0},
    orientation: {w: 1.0}
  }
}"

ros2 topic echo /cmd_vel --once
ros2 topic echo /sim_pose --once
```

## Result

The minimal navigation chain worked:

- `/planning/goal` was published.
- `local_planner_node` converted it to `/cmd_vel`.
- `navigation_sim_node` integrated the motion and published `/sim_pose`.

Observed outputs 

- `linear.x = 0.5`.
- `angular.z ≈ 0.556`.
- nonzero `/sim_pose` values confirming simulated motion.

## Asset

`assets/day44_navigation_sim_trajectory.png`

---