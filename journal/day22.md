# Day 22: Visual Odometry Basics

## Overview

Today’s goal was to complete the **Visual Odometry Basics** milestone from the NeuroNav-ROS2 roadmap, specifically under the **Estimation and Sensor Fusion** phase. Day 22 in the project plan is explicitly allocated to visual odometry basics, with Day 23 reserved for pose chaining, so the objective today was not full trajectory estimation yet, but a correct and modular first layer of visual motion estimation from camera frames. 

The work was carried out inside the existing `nn_estimation` package in keeping with the repository’s systems-oriented structure, where each day should produce a working feature, a launchable ROS2 node or pipeline, a visual artifact, and a journal entry. 

---

## Objective

Build a first-pass monocular visual odometry node that:

1. subscribes to the live camera stream,
2. extracts visual features from each frame,
3. matches features between consecutive frames,
4. computes a basic frame-to-frame pixel displacement estimate, and
5. publishes that motion estimate as a ROS2 topic for future downstream use.

This was treated as a **foundational visual odometry stage**, not yet full metric odometry. The target was a clean ROS2 estimation component that could later support pose accumulation and drift analysis on subsequent days.

## What Was Implemented

A new node, `visual_odometry_node.py`, was added inside `ws/src/nn_estimation/nn_estimation/`. The final implementation subscribes to `/camera/image_raw`, uses OpenCV ORB features, performs brute-force Hamming-distance matching with cross-checking, filters matches by distance, computes mean 2D pixel displacement between consecutive frames, and publishes the resulting motion estimate on `/vo_delta` as a `geometry_msgs/msg/Vector3`.

In parallel, the package configuration was updated so the new node could be launched properly through ROS2. Specifically:

- `setup.py` was updated to register the `visual_odometry` console script entry point.
- `package.xml` was updated to include `geometry_msgs` as a runtime dependency so the node could publish `Vector3` motion outputs.

## Pipeline Logic

The final Day 22 visual odometry pipeline worked as follows:

### 1. Image subscription
The node subscribes to the existing camera topic:

- `/camera/image_raw`

Each incoming ROS image message is converted into an OpenCV BGR frame using `cv_bridge`.

### 2. Grayscale conversion
Each frame is converted to grayscale before feature extraction. This reduces computation and is standard for classical feature-based vision pipelines.

### 3. ORB feature extraction
ORB was used with `nfeatures=500`, providing a classical, lightweight feature detector-descriptor pair suitable for real-time frame-to-frame matching.

### 4. Consecutive-frame matching
A brute-force matcher with Hamming distance and `crossCheck=True` was used to match descriptors from the previous frame to the current frame. Matches were sorted by distance, and only matches with distance below 50 were retained as “good matches.”

### 5. Pixel-space motion estimation
For the retained good matches, the matched 2D keypoint coordinates were extracted from the previous and current frames. Their displacement vectors were computed, and the node estimated:

- `mean_dx`
- `mean_dy`
- `mean_pixel_motion`

where `mean_pixel_motion` was the mean Euclidean norm of the displacement vectors.

### 6. ROS2 topic publication
The node publishes motion output on:

- `/vo_delta`

with message type:

- `geometry_msgs/msg/Vector3`

using the convention:

- `x = mean_dx`
- `y = mean_dy`
- `z = mean_pixel_motion` 

## Commands and Validation Flow

The session followed a clean validation-first progression:

1. Verified ROS2 Jazzy workspace and package visibility.
2. Confirmed OpenCV availability.
3. Verified the camera publisher and camera topics.
4. Confirmed topic message types for `/camera/image_raw` and `/camera/camera_info`.
5. Added the new visual odometry node.
6. Registered the node in `setup.py`.
7. Added `geometry_msgs` dependency in `package.xml`.
8. Built `nn_estimation` successfully.
9. Ran the node and confirmed ORB keypoint extraction.
10. Extended the node to perform frame-to-frame matching.
11. Extended the node again to compute pixel-space displacement.
12. Added ROS2 publication of the motion estimate on `/vo_delta`.
13. Verified topic existence, topic type, live output, and publication rate.

This made Day 22 a complete implementation cycle rather than only a coding exercise.

## Observations

### Initial feature extraction
The first version of the node successfully detected large numbers of ORB keypoints per frame, typically near the configured 500-feature budget. This confirmed that the camera stream contained enough texture and contrast for feature-based tracking.

### Feature matching stage
Once consecutive-frame matching was added, the node produced a strong number of valid frame-to-frame correspondences, often in the hundreds of matches. This was a good sign that the visual stream was stable enough for temporal association.

### Pixel motion behavior
After motion estimation was added, the published values showed smooth variation over time instead of noisy random jumps. In practice, this means the node was capturing coherent frame-to-frame visual displacement rather than just generating arbitrary statistics.

A clean single sample from `/vo_delta` was:

- `x: 2.399013042449951`
- `y: 1.3544840812683105`
- `z: 3.249187707901001`

This demonstrates that the node was indeed emitting usable numerical motion estimates.

### Topic frequency
The `/vo_delta` topic was measured at approximately **10 Hz**, with small timing variation, which matched the camera stream rate well and indicated a stable lightweight processing loop.

## Final Result

By the end of Day 22, the `nn_estimation` package contained a working ROS2 visual odometry starter node with the following capabilities:

- live image subscription,
- ORB keypoint extraction,
- descriptor matching across consecutive frames,
- frame-to-frame 2D displacement estimation,
- ROS2 publication of motion deltas on `/vo_delta`.

This is a proper **visual odometry basics** milestone because it establishes the core temporal vision logic required before pose accumulation. It is not yet full odometry in the geometric sense, but it is the correct modular precursor for the next stage.

## Artifact

**Artifact name:** `day22_vo_delta_stream.png`

The artifact captures the live `/vo_delta` stream in the terminal, showing the visual odometry node publishing frame-to-frame motion estimates in real time.

## Files Modified

- `ws/src/nn_estimation/nn_estimation/visual_odometry_node.py`
- `ws/src/nn_estimation/setup.py`
- `ws/src/nn_estimation/package.xml` 

## Key Takeaway

Today established the first real bridge between raw camera imagery and motion estimation inside the NeuroNav-ROS2 estimation stack. Instead of treating visual odometry as a black-box future step, Day 22 built the classical bones manually: features, matches, displacements, and a ROS topic. That makes tomorrow’s pose chaining step feel less like magic and more like engineering.

## Next Step

The natural continuation for **Day 23** is **pose chaining**:

- subscribe to `/vo_delta`,
- integrate consecutive visual deltas into a running 2D pose estimate,
- publish accumulated pose over time,
- and begin observing drift behavior before formal drift analysis on Day 24.

---