# Day 01: ROS2 + Gazebo + RViz2 Validation, Workspace Setup, and Bringup Package

## Objective

Install and validate the full ROS2 development stack on Pop!\_OS 24.04,
then initialize the NeuroNav-ROS2 repository and first bringup package.

---

## Tasks Completed

-   Installed ROS2 Jazzy.
-   Verified ROS2 CLI using `ros2`.
-   Verified DDS communication using `demo_nodes_cpp` talker/listener.
-   Installed and validated RViz2.
-   Resolved RViz2 Wayland/GLX issue using:
    -   `QT_QPA_PLATFORM=xcb rviz2`
-   Installed Gazebo Harmonic.
-   Verified Gazebo using `gz sim`.
-   Installed development tools:
    -   `python3-colcon-common-extensions`
    -   `python3-rosdep`
    -   `python3-vcstool`
    -   `build-essential`
-   Initialized `rosdep`.
-   Created workspace: `ws/`.
-   Created first package: `nn_bringup`.
-   Created repository structure:
    -   `journal/`
    -   `assets/`
    -   `ws/src/`
    -   `ws/launch/`
    -   `ws/config/`
    -   `ws/worlds/`

## Key Commands Used

``` bash
ros2
ros2 run demo_nodes_cpp talker
ros2 run demo_nodes_cpp listener
QT_QPA_PLATFORM=xcb rviz2
gz sim
colcon build
ros2 pkg create nn_bringup --build-type ament_python
```

## Issues Faced

### RViz2 failed under default launch

Error: - `Invalid parentWindowHandle (wrong server or screen)` -
`Unable to create the rendering window after 100 tries`

### Fix

Used X11 compatibility mode:

``` bash
QT_QPA_PLATFORM=xcb rviz2
```

Added alias in `.bashrc` for convenience.

## Outcome

The NeuroNav-ROS2 repository now has a validated ROS2 + RViz2 + Gazebo
development environment and a clean workspace structure ready for
perception development.

## Artifact

Add an RViz or Gazebo screenshot to: `assets/day01_rviz.png`

## Status

Day 01 complete.

---