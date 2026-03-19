# Day 13: Centroid-Based Multi-Object Tracking

## Objective
Implement a **multi-object tracking system** using centroid-based data association on top of the existing color-based detection pipeline.

---

## Key Concept
Tracking is not detection.

Detection answers:
> “What is present right now?”

Tracking answers:
> “Is this the same object as before?”

This was achieved using a **centroid tracker**, which assigns persistent IDs to objects based on spatial proximity across frames.

---

## System Pipeline

Camera → HSV Color Segmentation → Mask Cleanup → Contour Detection → Bounding Boxes  
→ Centroid Extraction → Centroid Tracker → ID Assignment → Visualization

---

## Implementation Details

### 1. Detection Layer
- Converted RGB image to HSV space  
- Applied green color threshold:  
  lower_green = [35, 80, 80]  
  upper_green = [85, 255, 255]  
- Generated binary mask using `cv2.inRange`

### 2. Noise Reduction
- Median filtering to remove noise  
- Morphological operations:
  - Erosion  
  - Dilation  

### 3. Contour Processing
- Extracted contours from mask  
- Filtered by area threshold: area > 1500  
- Converted bounding boxes to centroid coordinates  

### 4. Tracking Layer
- Implemented **CentroidTracker**:
  - Maintains object IDs  
  - Matches objects using Euclidean distance  
  - Handles registration & disappearance  

---

## Results
- Stable detection of green objects  
- Clean segmentation  
- Persistent ID tracking  
- Real-time ROS2 performance  

---

## Artifact
**assets/day13_centroid_tracking_clean_detection.png**

---

## Challenges
- Noisy masks initially  
- Lighting sensitivity  
- Parameter tuning required  

---

## Key Learnings
- Detection quality impacts tracking  
- Simple tracking works without ML  
- Identity persistence is fundamental  
- Preprocessing is critical  

---

## Next Step
**Day 14: Kalman Filter Tracking**

---

## Personal Reflection
Transition from:
“Seeing objects” → “Understanding continuity over time”

---