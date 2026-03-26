# Day 20: rosbag2 Recording & Replay

## Objective

Implement data recording and playback for the perception pipeline using
rosbag2, enabling offline debugging and reproducibility.

------------------------------------------------------------------------

## What Was Built

-   Recorded full pipeline topics:
    -   /camera/image_raw
    -   /camera/camera_info
    -   /imu/data
    -   /fusion/state
    -   /tracking/objects
-   Generated rosbag dataset: `rosbag2_2026_03_26-10_11_18`

------------------------------------------------------------------------

## Replay Validation

-   Replayed recorded data using:

    ``` bash
    ros2 bag play rosbag2_2026_03_26-10_11_18
    ```

-   Verified:

    -   Topics published correctly during replay.
    -   System operates independent of live sensors.

------------------------------------------------------------------------

## Key Learnings

-   rosbag acts as a data abstraction layer.

-   Enables:

    -   Offline debugging.
    -   Reproducible experiments.
    -   Dataset generation for ML.

-   Important distinction:

    -   rosbag = publisher.
    -   processing nodes must run separately.

------------------------------------------------------------------------

## Observations

-   Replay alone does not trigger processing nodes.
-   Correct workflow:

    1.  Launch system.
    2.  Replay rosbag.

------------------------------------------------------------------------

## Artifact

-   Terminal logs showing successful rosbag recording and playback.

------------------------------------------------------------------------

## Outcome

The system now supports:

- Full pipeline recording.
- Offline replay.
- Deterministic debugging.

Foundation for:

- Benchmarking (Day 21).
- Visual odometry.
- Dataset-driven development.

------------------------------------------------------------------------