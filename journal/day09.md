# Day 09: Camera Distortion Correction

## Objective

Implement a real-time camera distortion correction node in ROS2 using
OpenCV and calibration parameters obtained earlier. The goal is to
transform the raw camera feed into a rectified stream suitable for
downstream perception tasks.

------------------------------------------------------------------------

## Motivation

Most camera lenses introduce **radial and tangential distortion**, which
bends straight lines and warps geometry. For robotics systems performing
tasks such as:

-   visual odometry.
-   SLAM.
-   object detection.
-   pose estimation.

Accurate geometric representation of the scene is critical.

Therefore the raw camera stream must be **rectified using intrinsic
calibration parameters** before further processing.

------------------------------------------------------------------------

## Calibration Parameters

The camera calibration file (`ost.yaml`) contains:

-   image resolution
-   intrinsic camera matrix
-   distortion coefficients
-   rectification matrix
-   projection matrix

Example:

``` yaml
image_width: 640
image_height: 480

camera_matrix:
  data: [616.87282, 0.0, 316.71633,
         0.0, 616.26854, 255.87024,
         0.0, 0.0, 1.0]

distortion_coefficients:
  data: [-0.151500, 0.326256, -0.002678, -0.000843, 0.000000]
```

The distortion model used is **plumb_bob**, which accounts for radial
and tangential distortion.

------------------------------------------------------------------------

## Node Architecture

A new ROS2 node was created:

`distortion_correction_node`

Pipeline:

```
    camera_publisher
          ↓
    /camera/image_raw
          ↓
    distortion_correction_node
          ↓
    /camera/image_rect
          ↓
    image_viewer
```

------------------------------------------------------------------------

## Implementation

The node performs the following steps:

1.  Subscribe to `/camera/image_raw`.
2.  Convert ROS Image → OpenCV frame using `cv_bridge`.
3.  Load calibration parameters from `ost.yaml`.
4.  Apply distortion correction using:

``` python
cv2.undistort(frame, camera_matrix, distortion_coeffs)
```

5.  Publish corrected frame to `/camera/image_rect`.

------------------------------------------------------------------------

## Key Code Snippet

``` python
frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

undistorted = cv2.undistort(
    frame,
    self.camera_matrix,
    self.dist_coeffs
)

out_msg = self.bridge.cv2_to_imgmsg(undistorted, encoding='bgr8')
self.publisher.publish(out_msg)
```

------------------------------------------------------------------------

## ROS Topics

Active topics:

```
    /camera/image_raw
    /camera/image_rect
    /camera/camera_info
```

Verification:

```
    ros2 topic list
```

------------------------------------------------------------------------

## Runtime Verification

Nodes launched:

```
    ros2 run nn_sensors camera_publisher
    ros2 run nn_sensors distortion_correction
    ros2 run nn_sensors image_viewer
```

Rectified stream verified using the image viewer.

------------------------------------------------------------------------

## Result

The system successfully produces a **real-time rectified camera stream**
suitable for robotics perception pipelines.

------------------------------------------------------------------------

## Technical Lessons

-   ROS2 nodes should publish **processed sensor streams as separate
    topics**.
-   Calibration files must be installed via `setup.py` so they can be
    located using:

```{=html}
<!-- -->
```

```
    ament_index_python.get_package_share_directory()
```

-   `cv_bridge` enables seamless conversion between ROS Image messages
    and OpenCV frames.

------------------------------------------------------------------------

## Next Step

With a rectified image stream available, the perception stack can now
progress to **feature detection and spatial understanding**, such as:

-   ArUco marker detection.
-   AprilTag localization.
-   feature tracking.
-   visual odometry.

------------------------------------------------------------------------