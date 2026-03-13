# Day 07: Camera Model Concepts

## Objective

Understand how camera geometry is represented in ROS2 and extend the
camera publisher to provide camera model metadata along with the raw
image stream.

---

## Work Done

The existing camera publisher node was extended to publish both:

```
/camera/image_raw
/camera/camera_info
```

The node now publishes `sensor_msgs/Image` together with
`sensor_msgs/CameraInfo`, allowing the camera stream to include
intrinsic calibration parameters.

The following improvements were implemented:

-   Added timestamp synchronization using ROS.
-   Added `frame_id = camera_link`.
-   Implemented CameraInfo publisher.
-   Included intrinsic camera matrix (K).
-   Included rectification matrix (R).
-   Included projection matrix (P).
-   Added placeholder distortion model (`plumb_bob`).

## Camera Model Parameters

Resolution:

```
640 × 480
```

Intrinsic matrix K:

```
    fx  0  cx
K = 0  fy  cy
    0   0   1
```

Current placeholder values used:

```
fx = 525
fy = 525
cx = 320
cy = 240
```

These represent a simple pinhole camera approximation.

Actual calibration will be performed in Day 08.

## Verification

Camera topics confirmed:

```
/camera/image_raw
/camera/camera_info
```

Verified message type:

```
sensor_msgs/msg/CameraInfo
```

Camera parameters successfully published and visible via:

```
ros2 topic echo /camera/camera_info --once
```

## Key Concepts Learned

-   Pinhole camera model.
-   Camera intrinsic parameters.
-   Projection matrices in ROS.
-   Relationship between image stream and camera geometry.
-   Role of `sensor_msgs/CameraInfo` in perception pipelines.

## Outcome

The camera publisher now provides both image data and camera model
metadata, enabling downstream perception algorithms to correctly
interpret image geometry.

---