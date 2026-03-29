# Day 23: Pose Chaining

## Objective
Today’s goal was to extend the Day 22 visual odometry pipeline by chaining frame-to-frame motion estimates into a cumulative pose estimate.

This marks the first step from **instantaneous visual motion** toward a **running trajectory estimate**, even if still in a simplified pixel-space form.

---

## What I Implemented

### Reviewed the Day 22 visual odometry node

The existing `visual_odometry_node.py` was already publishing frame-to-frame motion estimates on:

`/vo_delta`

Message type:

`geometry_msgs/Vector3`

Published interpretation:

- `x` → mean pixel displacement in x.
- `y` → mean pixel displacement in y.
- `z` → mean per-frame pixel motion magnitude.

This provided the exact input required for pose chaining.

### Added a new pose chaining node

Created:

`src/nn_estimation/nn_estimation/pose_chaining_node.py`

This node:

- subscribes to `/vo_delta`.
- accumulates incoming visual odometry deltas over time.
- publishes the chained pose on `/vo_pose`.

Message type:

`geometry_msgs/Vector3`

Current interpretation:
- `x` → cumulative x displacement.
- `y` → cumulative y displacement.
- `z` → cumulative pixel motion.

This is a minimal but valid pose chaining implementation built directly on top of the Day 22 output.

### Registered the node in the estimation package

Updated:

`src/nn_estimation/setup.py`

Added console script:
`pose_chaining = nn_estimation.pose_chaining_node:main`

After rebuilding `nn_estimation`, the node was successfully recognized by ROS2.

### Integrated pose chaining into system bringup

Updated:

`src/nn_bringup/launch/full_system.launch.py`

Added:
- `visual_odometry`.
- `pose_chaining`.

This made Day 23 reproducible through the main bringup pipeline rather than relying only on manual multi-terminal execution.

## Validation Procedure

### Manual node-by-node validation

The following nodes were launched individually:

1. `camera_publisher`.
2. `visual_odometry`.
3. `pose_chaining`.

Observed behavior:

- camera frames were published successfully.
- visual odometry produced stable frame-to-frame deltas.
- pose chaining accumulated those deltas into a running pose estimate.

Example behavior:

- `visual_odometry_node` logged per-frame `mean_dx`, `mean_dy`, and `mean_pixel_motion`.
- `pose_chaining_node` logged cumulative values increasing over time.

### Topic-level validation

Verified:

- `/vo_pose`

The topic echoed successfully and showed accumulated values, confirming that the chaining pipeline was functioning end-to-end.

### Full bringup validation

Launched the updated full system using:

```bash
ros2 launch nn_bringup full_system.launch.py
```

Confirmed that the following estimation chain was active:

- camera publisher.
- visual odometry node.
- pose chaining node.

This validated that Day 23 is now integrated into the broader NeuroNav-ROS2 stack.

## Files Added / Modified

### Added

- `src/nn_estimation/nn_estimation/pose_chaining_node.py`.

### Modified

- `src/nn_estimation/setup.py`.
- `src/nn_bringup/launch/full_system.launch.py`.

## Key Result

A working **pose chaining node** was added to the system.

The pipeline now supports:

**camera stream → visual odometry delta → chained cumulative pose**

This is still a simplified representation in image/pixel space, but it establishes the structural transition from local motion estimation to trajectory accumulation.

## Limitations

This implementation is intentionally minimal and has several known limitations:

- The chained pose is **not metric**.
- Motion is accumulated in **pixel space**, not world coordinates.
- No camera calibration or geometric scale recovery is used.
- Drift is expected to accumulate rapidly.
- The `z` field currently represents cumulative pixel motion, not physical height or orientation.
- No orientation estimate is included.

These limitations are acceptable for Day 23 because the purpose was to demonstrate the **concept of chaining odometry increments into a running pose estimate**

## Artifact

Validation screenshot captured:

`day23_pose_chaining_validation.png`

This artifact shows the full estimation-related terminal activity during system bringup, including:

- IMU publisher.
- IMU-vision fusion.
- visual odometry.
- pose chaining.

## Reflection

Today was partly a recovery day because the system had to be rebuilt after a full OS reinstall. Even so, the day ended with a meaningful step forward in the estimation pipeline.

The important outcome is not just the new node itself, but the fact that the repository now contains a working bridge between:

- frame-to-frame motion estimation.
- cumulative pose construction.

That makes Day 24 naturally set up for **drift analysis**, since the current chained pose is expected to diverge over time.

## Next Step

**Day 24: Drift Analysis**

Planned focus:
- observe cumulative drift behavior over longer runs.
- quantify instability in chained pixel-space odometry.
- analyze how frame noise and matching errors accumulate over time.

---