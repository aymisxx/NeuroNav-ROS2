# Day 11: RGB–Depth Synchronization

## Objective
Establish a synchronized perception pipeline by aligning RGB and depth streams into a unified callback for downstream robotics applications.

---

## System Setup

### Active Nodes
- `/camera_publisher`
- `/depth_publisher`
- `/rgb_depth_sync`

### Topics
- `/camera/image_raw` (RGB)
- `/camera/depth/image_raw` (Depth)
- `/camera/camera_info`

---

## Key Development

### 1. Depth Pipeline Fix
- Identified resource conflict: both RGB and depth nodes were attempting to access `/dev/video0`
- Refactored `depth_publisher`:
  - Removed direct camera access
  - Subscribed to `/camera/image_raw`
  - Generated synthetic depth from grayscale intensity

---

### 2. Multi-Stream Synchronization

Implemented a new perception node:

**`rgb_depth_sync.py`**

- Uses:
  - `message_filters.Subscriber`
  - `ApproximateTimeSynchronizer`
- Inputs:
  - RGB stream
  - Depth stream
- Output:
  - Unified synchronized callback

---

## 📊 Runtime Behavior

Example output:

SYNC OK | RGB: 640x480 | Depth: 640x480 |
Depth[min=0.22, mean=2.40, max=4.98] |
RGB stamp=... | Depth stamp=...

### Observations
- Consistent synchronization achieved across streams
- Occasional timestamp offsets due to approximate sync window (`slop=0.1`)
- Depth statistics stable and within expected synthetic range (0–5 m)

---

## ⚠️ System Insight

Observed duplicate node instances:

/camera_publisher
/camera_publisher
/depth_publisher
/depth_publisher

### Cause
- Multiple launches without proper shutdown

### Impact
- Potential ambiguity in message sources
- ROS warning regarding node name conflicts

---

## What Was Achieved

- Transitioned from independent sensor streams → **synchronized multi-modal perception**
- Established **temporal coherence** between RGB and depth
- Built foundation for:
  - RGB-D SLAM
  - Visual navigation
  - Semantic mapping (VLMaps integration)

---

## Takeaway

Day 11 marks the shift from:
> "Publishing sensor data"

to:
> **"Fusing sensor modalities in time-consistent perception pipelines"**

This is the first step toward real robotic understanding of the environment.

---

## Assets

- `rgb_depth_sync_pipeline_live.png`
- `ros2_node_graph_duplicate_state.png`

---