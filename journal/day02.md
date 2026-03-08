# Day 02: Camera Publisher Pipeline

## Objective

Implement a ROS2 camera pipeline using a publisher and subscriber node.

---

## Nodes Implemented

camera_publisher  
image_viewer  

## Topic

/camera/image_raw

## Data Flow

Camera → Publisher → ROS Topic → Subscriber → OpenCV Viewer

## Concepts Learned

- ROS2 publishers
- ROS2 subscribers
- sensor_msgs/Image
- cv_bridge integration
- OpenCV + ROS2 interoperability
- Topic-based perception pipelines

## Validation

Successfully streamed webcam frames from publisher node to subscriber node.

## Artifacts

- Camera feed display window
- ROS topic communication verified

---