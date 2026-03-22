# Day 16: IMU Data Simulation

## Objective
Implement a simulated IMU data publisher in ROS2 and integrate it into the NeuroNav sensor pipeline.

---

## What I Built

Today I implemented a **synthetic IMU publisher node** inside the `nn_sensors` package.  
The node publishes standard `sensor_msgs/Imu` messages on the `/imu/data` topic.

The goal was to simulate inertial measurements that can later be used for:
- sensor fusion,
- state estimation,
- and vision-inertial pipelines.

## Implementation Details

### Node: imu_publisher.py

- ROS2 Python node using `rclpy`
- Publish rate: **10 Hz**
- Topic: `/imu/data`
- Frame: `imu_link`

### Simulated Signals

Angular velocity:
- sinusoidal variation across all axes.

Linear acceleration:
- sinusoidal motion in X and Y.
- constant **9.81 m/s²** in Z (gravity).

### Key Design Choice

Orientation was **intentionally left undefined**:

```python
msg.orientation_covariance[0] = -1.0
```

This reflects real-world scenarios where:
- raw IMU does not directly provide orientation,
- orientation must be estimated using filtering (e.g., EKF).

## Integration Steps

1. Created `imu_publisher.py` inside `nn_sensors`
2. Added executable entry in `setup.py`:
   ```
   imu_publisher = nn_sensors.imu_publisher:main
   ```
3. Rebuilt workspace:
   ```
   colcon build
   source install/setup.bash
   ```
4. Verified executable:
   ```
   ros2 pkg executables nn_sensors
   ```
5. Ran node:
   ```
   ros2 run nn_sensors imu_publisher
   ```

## Validation

### Topic Check
```
ros2 topic list
```
Confirmed `/imu/data` is active.

### Message Inspection
```
ros2 topic echo /imu/data
```
Verified:
- timestamps updating correctly.
- angular velocity varies smoothly.
- linear acceleration behaves as expected.
- gravity present on Z-axis.
- orientation marked invalid.

### Rate Verification
```
ros2 topic hz /imu/data
```

Observed:
- ~10.00 Hz stable publishing
- minimal timing jitter (≈0.0003s std dev)

## Key Learnings

- ROS2 message standards (`sensor_msgs/Imu`) and proper usage.
- Importance of **frame_id consistency**.
- Difference between:
  - raw sensor data.
  - estimated states (orientation not directly available).
- ROS2 executable registration via `setup.py`.
- Validation workflow:
  - topic → message → rate

## Outcome

A fully functional IMU simulation node is now part of the NeuroNav sensor stack.

This completes the **Day 16 milestone: IMU data simulation**.

The system now has:
- camera stream,
- depth pipeline,
- and IMU data,

forming the foundation for upcoming **sensor fusion (Day 17)**.

## Asset

`assets/day16_imu_wavefield.png`

---