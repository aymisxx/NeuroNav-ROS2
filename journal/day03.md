# Day 03: OpenCV Integration and Edge Detection

## Objective

Integrate OpenCV into the ROS2 perception pipeline and implement real‑time Canny edge detection on the camera stream.

---

## Pipeline Implemented

```
camera_publisher → edge_detector → image_viewer
```

1. `camera_publisher` publishes raw frames on `/camera/image_raw`.
2. `edge_detector` subscribes to `/camera/image_raw`.
3. OpenCV converts frame → grayscale.
4. Canny edge detection applied.
5. Processed image published on `/camera/edges`.
6. `image_viewer` subscribes to `/camera/edges`.

## Concepts Learned

- ROS2 image topics.
- `sensor_msgs/Image`.
- `cv_bridge` conversion between ROS images and OpenCV.
- Canny edge detection.
- ROS2 node parameter usage.
- Image encoding handling (`8UC1`, `mono8`, passthrough).

## Issues Faced

### Viewer node hardcoded topic

`image_viewer` was originally subscribing to `/camera/image_raw`.

**Fix**

Added parameter support:

```
self.declare_parameter('image_topic', '/camera/image_raw')
image_topic = self.get_parameter('image_topic').value
```

### Encoding mismatch

Canny output produced `8UC1` images causing conversion failure when forcing `mono8`.

**Fix**
Used passthrough encoding:

```
frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
```

## Result

Real‑time edge detection successfully visualized.

The system now performs **basic feature extraction**, which is the first stage in most robotic vision pipelines.

## Artifact

Saved screenshot:

assets/day03_canny_edges.png

## Final Working Stack

camera_publisher
      ↓
/camera/image_raw
      ↓
edge_detector (OpenCV + Canny)
      ↓
/camera/edges
      ↓
image_viewer

## Next Step (Day 04)

- Hough Line Detection
- ORB Feature Extraction

---