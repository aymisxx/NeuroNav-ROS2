# Day 10 --- Depth Image Processing

## Overview

Today's objective was to introduce **depth image handling** into the
NeuroNav perception pipeline. Since the development environment uses a
standard RGB webcam without a true depth sensor, a **synthetic depth
stream** was generated from grayscale intensity values to emulate depth
measurements. This allowed the perception pipeline to be extended and
validated without requiring specialized hardware.

The pipeline now processes depth images and publishes a normalized
visualization stream suitable for debugging and inspection.

------------------------------------------------------------------------

## Nodes Implemented

### 1. Depth Publisher (`nn_sensors`)

A new ROS2 node was created to publish a synthetic depth stream.

**Topic published**

`/camera/depth/image_raw`

The node captures webcam frames and converts grayscale intensity into a
floating‑point depth approximation:

`depth = grayscale_intensity / 255 * 5.0`

The resulting image is published using the ROS encoding:

`32FC1`

representing depth values in meters.

------------------------------------------------------------------------

### 2. Depth Processor (`nn_perception`)

A processing node was implemented to subscribe to the raw depth stream
and convert it into a visualizable format.

**Topic subscribed**

`/camera/depth/image_raw`

**Topic published**

`/camera/depth_visual`

Processing steps:

1.  Receive floating‑point depth image\
2.  Replace invalid values\
3.  Normalize values to `[0,255]`\
4.  Convert to `uint8`\
5.  Publish visualization stream

This produces a grayscale depth visualization where brighter pixels
correspond to closer surfaces.

------------------------------------------------------------------------

## System Pipeline

Webcam frame\
↓\
Synthetic depth publisher\
↓\
`/camera/depth/image_raw`\
↓\
Depth processing node\
↓\
`/camera/depth_visual`\
↓\
Visualization via `rqt_image_view`

------------------------------------------------------------------------

## Validation

Depth visualization was verified using:

`rqt_image_view`

Topic inspected:

`/camera/depth_visual`

Publishing frequency was confirmed using:

`ros2 topic hz /camera/depth_visual`

Observed rate:

`~10 Hz`

------------------------------------------------------------------------

## Artifact

Depth visualization screenshot:

`assets/day10_depth_visual.png`

This image shows the normalized depth output generated from the
synthetic depth pipeline.

------------------------------------------------------------------------

## Notes

The current implementation uses **synthetic depth derived from grayscale
intensity**, which does not represent true geometric depth. The purpose
of this stage is to validate the **ROS2 depth image processing
pipeline** before integrating real RGB‑D sensors or simulated depth
cameras.

Future stages will combine depth with RGB streams to support **RGB‑D
perception and synchronized processing**.

------------------------------------------------------------------------

## Outcome

Depth image processing capability has been successfully integrated into
the NeuroNav perception stack. The system now supports depth topic
publishing, processing, and visualization.
