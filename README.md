# 🚀 **NeuroNav-ROS2** ⚙️
### **(59-Day Mastery Plan)**

**NeuroNav-ROS2** is a 59-day deep dive into **robot perception and
autonomy using ROS2**. The goal of this challenge is to build a **complete perception-to-navigation pipeline** while maintaining a **professional ROS2 repository structure** rather than a tutorial-style project.

------------------------------------------------------------------------

The challenge begins on **March 3** and ends on **April 30**.

------------------------------------------------------------------------

By the end of the challenge the repository evolves into a **modular robotics perception stack** including:

-   Sensor pipelines.
-   Computer vision processing.
-   Sensor fusion.
-   State estimation.
-   Mapping.
-   Semantic perception.
-   Perception-driven navigation.

------------------------------------------------------------------------

# Philosophy of the Challenge

Many learning projects follow a **day-wise folder structure**:

```
    day01/
    day02/
    day03/
```

While this is good for tutorials, it is **not how real robotics systems
are built**.

Instead, this challenge follows a **systems-engineering approach**:

-   One ROS2 workspace
-   Modular robotics packages
-   Continuous integration of components
-   Git commits track day-wise progress
-   A daily journal documents learning

This ensures the repository resembles a **real robotics autonomy stack**
rather than a collection of experiments.

------------------------------------------------------------------------

# Repository Structure

```
    NeuroNav-ROS2
    │
    ├── README.md
    ├── requirements.txt
    │
    ├── journal/
    │ ├── day01.md
    │ ├── day02.md
    │ └── ...
    │
    ├── ws/
    │ ├── src/
    │ │ ├── nn_sensors/
    │ │ ├── nn_perception/
    │ │ ├── nn_estimation/
    │ │ ├── nn_mapping/
    │ │ ├── nn_planning/
    │ │ └── nn_bringup/
    │ │
    │ ├── launch/
    │ ├── config/
    │ └── worlds/
    │
    └── assets/
```

### Folder Explanation

- **journal/**\
Daily learning logs including commands used, concepts learned, issues
faced, and results.

- **ws/**\
The ROS2 workspace for the entire project.

- **src/**\
ROS2 packages containing system modules.

- **nn_sensors**\
Sensor interfaces (camera, depth, lidar, IMU).

- **nn_perception**\
Vision pipelines including feature extraction, detection, and
segmentation.

- **nn_estimation**\
Tracking, filtering, and sensor fusion algorithms.

- **nn_mapping**\
Mapping systems such as occupancy grids and semantic maps.

- **nn_planning**\
Planning and decision layers using perception outputs.

- **nn_bringup**\
Launch files and integration of the entire stack.

- **launch/**\
Launch configurations for subsystems.

- **config/**\
YAML parameter configurations.

- **worlds/**\
Gazebo simulation environments.

- **assets/**\
GIFs, screenshots, graphs, and demo media.

------------------------------------------------------------------------

# Daily Workflow

Each day must produce:

1.  One working feature.
2.  One launchable ROS2 node or pipeline.
3.  One visual artifact (GIF, screenshot, or RViz capture).
4.  One journal entry documenting the process.

Example commit format:

```
    Day 01: ROS2 + Gazebo installation and validation
    Day 02: Workspace initialization and bringup package
    Day 03: Camera publisher node
```

------------------------------------------------------------------------

# Theoretical Foundations

This challenge is structured around the **core pillars of robot
perception systems**.

### Perception

Robots must transform raw sensor data into meaningful information.

Key topics:
- image processing.
- feature extraction.
- object detection.
- semantic understanding.

### State Estimation

Robots must estimate their own state and the state of objects around
them.

Key topics:
- Kalman filters.
- Extended Kalman filters.
- sensor fusion.
- tracking systems.

### Mapping

Robots must construct a representation of the environment.

Key topics:
- occupancy grids.
- lidar processing.
- semantic maps.

### Navigation

Robots must use perception outputs to move intelligently.

Key topics:
- obstacle detection.
- goal selection.
- planning.

------------------------------------------------------------------------

# Challenge Timeline

- **First Date:** March 3.
- **Final Date:** April 30.
- **Duration:** 59 Days.

------------------------------------------------------------------------

# Phase 1: ROS2 Perception Foundations

```
  Day   Date     Task
  ----- -------- -------------------------------------------------
  1     Mar 3    Install ROS2, Gazebo, RViz2 and validate setup
  2     Mar 4    Initialize workspace and create bringup package
  3     Mar 5    Camera publisher node
  4     Mar 6    Image subscriber pipeline
  5     Mar 7    OpenCV integration node
  6     Mar 8    Canny edge detection
  7     Mar 9    Hough line detection
  8     Mar 10   ORB feature extraction
  9     Mar 11   Feature matching
  10    Mar 12   TF2 fundamentals
  11    Mar 13   Camera model concepts
  12    Mar 14   Camera calibration
  13    Mar 15   Distortion correction
  14    Mar 16   Depth image processing
```

------------------------------------------------------------------------

# Phase 2: Estimation and Sensor Fusion

```
  Day   Date     Task
  ----- -------- -------------------------------
  15    Mar 17   RGB-depth synchronization
  16    Mar 18   Basic object tracking
  17    Mar 19   Centroid tracker
  18    Mar 20   Kalman filter tracking
  19    Mar 21   Extended Kalman filter
  20    Mar 22   IMU data simulation
  21    Mar 23   IMU + vision fusion
  22    Mar 24   Time synchronization concepts
  23    Mar 25   Multi-object tracking
  24    Mar 26   rosbag2 recording
  25    Mar 27   Benchmark metrics
  26    Mar 28   Visual odometry basics
  27    Mar 29   Pose chaining
  28    Mar 30   Drift analysis
  29    Mar 31   Pose graph concepts
  30    Apr 1    Estimation pipeline demo
```

------------------------------------------------------------------------

# Phase 3: Mapping and Semantic Perception

```
  Day   Date     Task
  ----- -------- ----------------------------
  31    Apr 2    Occupancy grid basics
  32    Apr 3    Map update pipeline
  33    Apr 4    LiDAR simulation
  34    Apr 5    Scan processing
  35    Apr 6    Mapping demo
  36    Apr 7    PyTorch ROS2 wrapper
  37    Apr 8    Object detection node
  38    Apr 9    Semantic segmentation node
  39    Apr 10   Semantic map creation
  40    Apr 11   Map query service
  41    Apr 12   Language-conditioned goals
  42    Apr 13   Multi-sensor fusion
  43    Apr 14   Robustness testing
  44    Apr 15   Performance optimization
  45    Apr 16   Semantic perception demo
```

------------------------------------------------------------------------

# Phase 4: Perception Driven Navigation

```
  Day   Date     Task
  ----- -------- ----------------------------------
  46    Apr 17   Perception-to-planning interface
  47    Apr 18   Local planner implementation
  48    Apr 19   Navigation simulation
  49    Apr 20   Safety layer
  50    Apr 21   Behavior logic
  51    Apr 22   Lifecycle nodes
  52    Apr 23   Parameter tuning
  53    Apr 24   Logging and diagnostics
  54    Apr 25   Testing automation
  55    Apr 26   Stress testing
  56    Apr 27   Full system bringup
  57    Apr 28   Demo recording
  58    Apr 29   Repository documentation
  59    Apr 30   Final NeuroNav-ROS2 release
```

------------------------------------------------------------------------

# Final Outcome

After 59 days the repository will contain:

-   A complete ROS2 perception stack.
-   Vision processing pipelines.
-   Sensor fusion and tracking.
-   Mapping and semantic understanding.
-   Integration with navigation.
-   Full system demonstration.

------------------------------------------------------------------------