# Day 24: Drift Analysis

## Objective
Today’s goal was to extend the visual odometry pipeline by adding a basic drift analysis node.  
The focus was not on correcting drift yet, but on **measuring how pose error accumulates over time** from chained visual odometry estimates.

---

## What I Built

I implemented a new ROS2 node inside `nn_estimation`:

- **Node:** `drift_analysis_node.py`.
- **Executable:** `drift_analysis`.

This node subscribes to:

`/vo_pose` from the Day 23 pose chaining pipeline.

and computes a simple drift metric:

**drift magnitude** = `sqrt(x^2 + y^2)`

It also tracks:

- current pose estimate `(x, y)`.
- current drift magnitude.
- maximum observed drift.
- cumulative motion from pose chaining.

## Implementation Summary

### 1. Added Drift Analysis Node

Created a new node:

`src/nn_estimation/nn_estimation/drift_analysis_node.py`

Core logic:

- subscribe to `/vo_pose`.
- compute Euclidean distance of the current accumulated pose from the origin.
- track `max_drift`.
- log drift progression sample-by-sample.

### 2. Registered Node in `setup.py`

Updated `nn_estimation/setup.py` to expose the executable:

```python
'drift_analysis = nn_estimation.drift_analysis_node:main',
```

### 3. Rebuilt Package

Built only the estimation package:

```bash
cd ~/GitHub/NeuroNav-ROS2/ws
colcon build --packages-select nn_estimation
source install/setup.bash
```

### 4. Verified Executable Registration

Confirmed the package exports:

```bash
ros2 pkg executables nn_estimation
```

Output included:

```bash
nn_estimation drift_analysis
nn_estimation imu_vision_fusion
nn_estimation pose_chaining
nn_estimation visual_odometry
```

## Pipeline Validation

To validate the Day 24 pipeline, I launched the estimation stack in separate terminals:

### Terminal 1
```bash
cd ~/GitHub/NeuroNav-ROS2/ws
source install/setup.bash
ros2 run nn_sensors camera_publisher
```

### Terminal 2
```bash
cd ~/GitHub/NeuroNav-ROS2/ws
source install/setup.bash
ros2 run nn_estimation visual_odometry
```

### Terminal 3
```bash
cd ~/GitHub/NeuroNav-ROS2/ws
source install/setup.bash
ros2 run nn_estimation pose_chaining
```

### Terminal 4
```bash
cd ~/GitHub/NeuroNav-ROS2/ws
source install/setup.bash
ros2 run nn_estimation drift_analysis
```

This produced live drift logs from the accumulated VO pose.

## Sample Drift Output

Example output from the drift analysis node:

```text
[INFO] [drift_analysis_node]: Drift sample 8: x=12.42, y=63.10, drift=64.31, max_drift=64.31, cumulative_motion=1113.12
[INFO] [drift_analysis_node]: Drift sample 9: x=9.88, y=63.06, drift=63.83, max_drift=64.31, cumulative_motion=1116.05
[INFO] [drift_analysis_node]: Drift sample 10: x=5.73, y=63.78, drift=64.03, max_drift=64.31, cumulative_motion=1120.73
```

Later in the run, drift increased further, with the terminal capture showing:

- **current drift** around `62 to 64`
- **max drift** reaching `104.83`
- **cumulative motion** exceeding `3000`

## Topic Snapshot

I also captured one live `/vo_pose` sample:

```bash
ros2 topic echo /vo_pose --once
```

Output:

```yaml
x: -5.477253565331921
y: 57.453302227309905
z: 2420.759958267212
```

This confirms that:

- the pose chaining node is publishing accumulated pose,
- the drift analysis node is receiving meaningful pose values,
- cumulative motion continues to grow over time.

## Artifact

Saved validation screenshot as:

```text
assets/day24_drift_analysis_validation.png
```

## Key Observation

This experiment clearly shows the core weakness of naive visual odometry chaining:

- even if frame-to-frame motion estimates look reasonable,
- small pixel-level errors accumulate over time,
- and the chained pose gradually drifts away from the origin.

So Day 24 successfully demonstrates **drift emergence** in a simple VO pipeline.

## What I Learned

Today reinforced a very important estimation concept:

> local motion estimates may be usable in the short term, but repeated integration without correction leads to drift.

This sets up the motivation for future topics like:

- pose graph concepts.
- loop closure.
- global optimization.
- corrected state estimation pipelines.

## Files Added / Modified

### Added

`src/nn_estimation/nn_estimation/drift_analysis_node.py`

### Modified

`src/nn_estimation/setup.py`

## Result

Day 24 successfully added a working **drift analysis node** to the existing visual odometry and pose chaining pipeline.

The pipeline now supports:

- visual odometry delta estimation.
- pose accumulation.
- drift monitoring.

This makes the estimation stack more complete and also gives a clean bridge into Day 25: **Pose Graph Concepts**.

---