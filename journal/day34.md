# Day 34: Semantic Segmentation Node

Today I implemented a lightweight **semantic segmentation node** in `nn_perception` for the NeuroNav-ROS2 pipeline.

---

## What I built

- Added `semantic_segmentation_node.py` inside the `nn_perception` package.
- Subscribed to `/camera/image_raw`.
- Converted incoming frames from ROS image messages to OpenCV format using `CvBridge`.
- Performed simple color-based semantic segmentation in HSV space.
- Isolated a **green-class mask** using `cv2.inRange(...)`.
- Published the resulting binary mask to `/camera/segmentation_mask`.

## Integration work

- Made the node executable.
- Registered it in `setup.py` as:
  - `semantic_segmentation_node = nn_perception.semantic_segmentation_node:main`
- Rebuilt the package with `colcon build --packages-select nn_perception`.
- Verified the executable was visible through ROS2.

## Validation

- Ran the semantic segmentation node successfully.
- Confirmed `/camera/segmentation_mask` existed and had type `sensor_msgs/msg/Image`.
- Used `static_image_publisher` to feed a test image into `/camera/image_raw`.
- Visualized the segmentation output in RViz2.
- Saved the visual artifact as:
  - `assets/day34_semantic_segmentation_mask.png`

## Result
The node successfully produced a valid segmentation mask from the input image. The current implementation is intentionally simple and sparse, since it uses a threshold-based green-region extractor rather than a learned semantic model. Still, it establishes the full ROS2 semantic-perception flow:

**image input → segmentation logic → ROS image output → visualization**

## Tiny takeaway
Day 34 pushed the project from detection into segmentation territory.  
Not fancy yet, but the pipe is real now.

---