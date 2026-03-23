# Day 17: IMU + Vision Fusion

## Objective

Combine IMU and vision data streams to create a basic sensor fusion pipeline.

## System Overview

This step integrates two independent sensing modalities:

- IMU → high-frequency motion sensing (angular velocity).
- Vision → lower-frequency but stable environmental observation.

The goal is to combine both into a unified signal.

---

## Implementation

### Node

Created a new package:

nn_estimation

Implemented:

imu_vision_fusion_node.py

### Subscriptions

- /imu/data → sensor_msgs/Imu.
- /camera/image_raw → sensor_msgs/Image.

### Signal Extraction

- IMU:

  - angular_velocity.z used as motion proxy.

- Vision:

  - mean pixel intensity used as a simple visual signal proxy.

### Fusion Logic

A weighted fusion model was used:

$fused = α * vision + (1 - α) * imu$

Where:
$α = 0.6$

### Output

Published fused signal to:

/fusion/state → std_msgs/Float32

## Results

- Fusion node successfully subscribes to both IMU and camera streams.
- Real-time fused values are continuously published.
- Stable output observed (~72 range under current inputs).

## Key Insight

IMU provides fast but drifting motion data, while vision provides stable but slower observations.

Even a simple weighted fusion demonstrates:

- complementary sensor behavior.
- the necessity of combining modalities.

## Limitations

- No normalization between IMU and vision signals.
- Units are not physically meaningful.
- No time synchronization.
- Not a true state estimator (no EKF yet).

## Outcome

A working multi-sensor fusion pipeline was established, forming the foundation for future state estimation methods.

## Next Step

- Time synchronization between sensors.
- Structured state representation.
- Transition toward EKF-based fusion.

---