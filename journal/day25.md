# Day 25: Pose Graph Concepts

## What I built

Implemented a new ROS2 node: `pose_graph_node.py` inside `nn_estimation`.

---

## What it does

- Subscribes to `/vo_pose`.
- Creates sparse pose-graph nodes every few pose samples.
- Adds graph edges between consecutive graph nodes.
- Skips redundant nodes if motion is too small.
- Shuts down cleanly on `Ctrl+C`.

## Validation

Successfully verified:

- node startup.
- graph node creation.
- edge creation (`0 -> 1`).
- distance-threshold skip logic.
- clean shutdown without traceback.

## Files changed

- `ws/src/nn_estimation/nn_estimation/pose_graph_node.py`.
- `ws/src/nn_estimation/setup.py`.

## Asset

`day25_pose_graph_node_runtime.png`

## Day 25 outcome

Pose graph concepts are now integrated as a working estimation-layer prototype in NeuroNav-ROS2.

---