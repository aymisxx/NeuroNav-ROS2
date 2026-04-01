# Day 26: Estimation Pipeline Demo

## Objective
Integrate the estimation-related ROS2 nodes into a single launchable pipeline and verify that the full estimation graph runs correctly.

---

## What I Did

- Confirmed that the `nn_estimation` package exposed all expected executables:
  - `drift_analysis`.
  - `imu_vision_fusion`.
  - `pose_chaining`.
  - `pose_graph`.
  - `visual_odometry`.

- Launched the full estimation stack using:
  - `camera_publisher`.
  - `imu_publisher`.
  - `imu_vision_fusion`.
  - `visual_odometry`.
  - `pose_chaining`.
  - `multi_object_tracker`.
  
- Verified active runtime nodes using `ros2 node list`.

- Generated and captured the ROS computation graph using `rqt_graph`.

## Key Result

The Day 26 estimation pipeline demo ran successfully as a launchable multi-node ROS2 system. All major nodes  started correctly, remained active, and showed the expected topic-level connectivity.

## Observed ROS Graph

Verified connections included:

- `/camera_publisher -> /camera/image_raw`.
- `/imu_publisher -> /imu/data`.
- `/visual_odometry_node <- /camera/image_raw`.
- `/pose_chaining_node <- /vo_delta`.
- `/fusion_node <- /camera/image_raw`.
- `/fusion_node <- /imu/data`.

## Issue Faced

`rqt_graph` initially opened as a blank window under the default Qt/Wayland setup on Pop!\_OS 24.04.

## Fix Applied

Launched `rqt_graph` with:

```bash
QT_QPA_PLATFORM=xcb rqt_graph
```

This resolved the display issue and showed the active node/topic graph correctly.

## Artifact

Saved graph screenshot:

`assets/day26/estimation_pipeline_graph.png`

## Outcome

Day 26 completed successfully.  
The estimation stack is now launchable, visually verified, and ready for transition into the mapping phase.

---