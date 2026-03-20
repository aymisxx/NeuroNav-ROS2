# Day 14: Kalman-Based Object Tracking in ROS2

## Overview
Day 14 focused on adding **state estimation** to the perception pipeline using a **Kalman Filter**. The goal was to move beyond raw centroid measurements and build a tracker that can **predict** and **smooth** object motion in real time.

A fresh rebuild was also required because the operating system had been reinstalled and the repository was cloned again into the same workspace path:

---

`/home/twilightpriest/GitHub/NeuroNav-ROS2/`

## Objective

Build a ROS2 perception node that:
- subscribes to the RGB camera feed from `/camera/image_raw`.
- detects the green object using HSV thresholding.
- measures object centroid from the detected contour.
- runs a **Kalman Filter** for prediction and correction.
- visualizes:
  - **Measured** position
  - **Predicted** position
  - **Estimated** position

## Workspace Recovery

Because the OS was reinstalled, the workspace had to be rebuilt from scratch.

### Recovery steps completed

- verified workspace structure under `ws/src`.
- confirmed all ROS2 package manifests were present.
- reinstalled build dependencies.
- initialized and updated `rosdep`.
- rebuilt the workspace with `colcon`.
- re-sourced the overlay and verified package discovery.

## Packages Verified

The following packages were confirmed and rebuilt successfully:
- `learning_tf2_py`
- `nn_bringup`
- `nn_perception`
- `nn_sensors`

## Files Added / Updated

### New file

- `ws/src/nn_perception/nn_perception/kalman_tracker.py`

### Updated file

- `ws/src/nn_perception/setup.py`

A new console entry point was added:

- `kalman_tracker = nn_perception.kalman_tracker:main`

## Kalman Filter Design

The tracker uses OpenCV's Kalman filter with:

- **State vector:** `[x, y, vx, vy]^T`
- **Measurement vector:** `[x, y]^T`

### State transition model

The motion model assumes constant velocity:

```text
[x_k]   [1 0 1 0][x_{k-1}]
[y_k] = [0 1 0 1][y_{k-1}]
[vx_k]  [0 0 1 0][vx_{k-1}]
[vy_k]  [0 0 0 1][vy_{k-1}]
```

### Measurement model

Only position is directly measured from the image:

```text
[z_k] = [x_k, y_k]^T
```

## Detection Pipeline

The perception pipeline for Day 14 is:

```text
Camera Publisher -> /camera/image_raw -> HSV thresholding -> contour extraction -> centroid measurement -> Kalman prediction/correction
```

### Detection steps

- convert RGB image to HSV.
- threshold for green color range.
- apply median blur.
- apply erosion and dilation for noise cleanup.
- extract contours.
- select largest contour above area threshold.
- compute centroid.
- feed centroid measurement into Kalman correction step.

## Runtime Validation

### Camera publisher

The camera publisher in `nn_sensors` was required to stream frames before the tracker could function.

Node used:
- `ros2 run nn_sensors camera_publisher`

### Kalman tracker
Node used:
- `ros2 run nn_perception kalman_tracker`

## Build and Run Commands

### Rebuild perception package
```bash
cd /home/twilightpriest/GitHub/NeuroNav-ROS2/ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select nn_perception
```

### Source workspace
```bash
cd /home/twilightpriest/GitHub/NeuroNav-ROS2/ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

### Run camera publisher
```bash
ros2 run nn_sensors camera_publisher
```

### Run Kalman tracker
```bash
ros2 run nn_perception kalman_tracker
```

## Result
The Day 14 pipeline worked successfully in live testing.

### Observed outputs
- green object correctly segmented in the mask.
- bounding box tightly enclosed the object.
- measured centroid displayed correctly.
- predicted state displayed correctly.
- estimated state displayed correctly.
- tracker remained visually coherent during motion.

This marks the first integration of **state estimation** into the NeuroNav-ROS2 perception stack.

## Asset
Suggested asset filename:
- `day14_kalman_object_tracking_ros2.png`

## Why this matters
This step is important because it upgrades the system from raw frame-by-frame detection into a perception pipeline that reasons over time. That is the bridge between basic computer vision and robotics-grade tracking.

Day 14 therefore represents a move from:
- **detection only**

to:
- **detection + prediction + estimation**

---