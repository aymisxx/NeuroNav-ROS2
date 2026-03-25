# Day 19: **Multi-Object Tracking**

## Objective
Extend the perception pipeline from single-object tracking to multi-object tracking with persistent identity assignment, enabling temporal consistency across frames.

---

## What I Built

Today focused on implementing a centroid-based multi-object tracking system within the nn_perception package.

### Core Components:
- CentroidTracker Class
  - Assigns unique IDs to detected objects.
  - Matches objects across frames using Euclidean distance.
  - Handles object appearance and disappearance.
  - Maintains state using:
    - objects (ID → centroid).
    - disappeared (ID → missing frames).

- MultiObjectTrackerNode (ROS2)
  - Simulates detections.
  - Updates tracker at fixed intervals.
  - Publishes tracked objects to /tracking/objects.
  - Logs persistent ID assignments.

## Key Concepts Implemented

### 1. Data Association
Used pairwise distance matrix:
- Existing objects vs new detections.
- Greedy matching via minimum distance.

### 2. Identity Persistence
Each object is assigned a unique ID that remains stable across frames unless:
- It disappears for more than a threshold.
- A new object enters the scene.

### 3. Temporal Consistency
Tracking ensures:
- Objects are not re-identified every frame.
- Motion continuity is preserved.

## Major Issue Encountered

### Problem:
Initial implementation used random detections which caused:
- Objects to teleport randomly.
- Incorrect ID assignments.
- Unrealistic tracking behavior.

### Fix:
Replaced with persistent simulated objects with incremental motion:
- Objects initialized once.
- Each frame applies small random displacement.

This transformed:

chaotic detection → structured motion → meaningful tracking

## Results & Analysis

The trajectory plot generated shows the evolution of tracked objects over time:

- Each object (ID 0, ID 1, ID 2) maintains a distinct trajectory.
- Motion is smooth and continuous, with no sudden jumps.
- No ID switching observed, indicating correct data association.

### Observations:
- ID 0: confined motion with gradual drift.
- ID 1: clear directional movement, demonstrating stable tracking under displacement.
- ID 2: localized cluster, showing robustness to small positional variations.

### Key Insight:
The tracker successfully:
- Preserves identity across time.
- Handles multiple objects simultaneously.
- Maintains stability even with noisy motion.

This validates the correctness of the centroid-based approach under controlled conditions.

## Asset Generated

- day19_multi_object_tracking_trajectories.png
  - Visualizes object trajectories.
  - Demonstrates temporal consistency.
  - Highlights ID persistence.

## System Progression

Pipeline now evolves as:

Sensor Data → Detection → Centroid Extraction → Multi-Object Tracking

This marks a transition from:

frame-based perception → stateful perception

## Next Steps

- Replace simulated detections with real camera-based detections.
- Integrate contour detection / segmentation.
- Extend tracker with:
  - velocity estimation.
  - Kalman filtering.
  - Hungarian algorithm.

## Takeaway

Today was a shift from:
“seeing objects”

to:
“understanding objects over time”

Multi-object tracking introduces memory into perception, which is fundamental for autonomous systems.

## Reflection

This implementation demonstrates how even a simple geometric approach can produce robust tracking when paired with consistent input dynamics.

The key learning:
tracking quality depends heavily on input consistency.

---