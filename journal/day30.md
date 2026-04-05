# Day 30: Scan Processing

## Objective

Build a ROS2 scan-processing node on top of the Day 29 LiDAR simulation pipeline, verify end-to-end LaserScan flow.

---

## What I did

- Inspected the existing Day 29 LiDAR simulation setup.
- Added a new Day 30 node: `scan_processing_node.py` inside `nn_mapping`.
- Registered the new executable in `setup.py`.
- Corrected `package.xml` by adding the missing `sensor_msgs` dependency.
- Rebuilt `nn_mapping` and verified the new executable was exported correctly.
- Ran the LiDAR publisher and scan-processing node together.
- Visualized the processed scan pipeline in RViz2.

## Files changed

- `ws/src/nn_mapping/nn_mapping/scan_processing_node.py`.
- `ws/src/nn_mapping/setup.py`.
- `ws/src/nn_mapping/package.xml`.

## New node added

### `scan_processing_node`

This node:

- subscribes to `/scan`.
- filters invalid LaserScan ranges.
- republishes the cleaned scan to `/scan_processed`.
- computes live scan statistics:
  - total beams.
  - valid beams.
  - minimum range.
  - maximum range.
  - average range.

## Key implementation idea

The Day 30 pipeline is purely LiDAR-based and does **not** depend on any camera node.

The synthetic LiDAR publisher from Day 29 directly publishes `sensor_msgs/msg/LaserScan` messages on `/scan`, and the Day 30 processing node consumes those messages. This keeps the perception stream modular:

- camera pipeline = image messages.
- LiDAR pipeline = range-over-angle scan messages.

So the scan-processing system works independently of image topics.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

colcon build --symlink-install
colcon build --symlink-install --packages-select nn_mapping

ros2 pkg executables nn_mapping
ros2 run nn_sensors lidar_publisher
ros2 run nn_mapping scan_processing_node
ros2 topic list | sort
ros2 topic info /scan -v
ros2 topic echo /scan_processed --once

export QT_QPA_PLATFORM=xcb
rviz2
```

## Verification

### Build verification

- `nn_mapping` exported both executables:
  - `occupancy_grid_node`.
  - `scan_processing_node`.

### Runtime verification

- `lidar_publisher` successfully published live `/scan` data.
- `scan_processing_node` successfully subscribed to `/scan`.
- Processed output was published on `/scan_processed`.
- `ros2 topic echo /scan_processed --once` showed a valid `LaserScan` message.
- Live logs from `scan_processing_node` confirmed changing scan statistics over time.

Example runtime log:

```text
[INFO] [scan_processing_node]: Scan stats | total=181 valid=181 min=2.294 m max=4.799 m avg=3.600 m
```

## Issues faced

### False-positive topic presence

`/scan` appeared in `ros2 topic list`, but no data was arriving.

**Cause:**
The topic existed because `scan_processing_node` was subscribing to it, not because any publisher was active.

**Fix:**
Confirmed with:
```bash
ros2 topic info /scan -v
```
and then launched the real LiDAR source:
```bash
ros2 run nn_sensors lidar_publisher
```

### Missing package dependency

The new node used `sensor_msgs.msg.LaserScan`, but `sensor_msgs` was not declared in `nn_mapping/package.xml`.

**Fix:**
Added:

```xml
<depend>sensor_msgs</depend>
```

## Result

Day 30 successfully extended the mapping stack with a working scan-processing stage.

The repository now supports this verified live pipeline:

```text
LiDAR Publisher (/scan) -> Scan Processing Node -> /scan_processed
```

This completes the Day 30 objective of introducing a dedicated LaserScan processing layer on top of the Day 29 LiDAR simulation base.

## Asset

**Recommended asset filename:**
`day30_scan_processing_rviz.png`

This RViz2 screenshot shows the Day 30 LaserScan processing pipeline visually.

---