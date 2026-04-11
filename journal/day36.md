# Day 36: Map Query Service

## Objective

Built a minimal ROS2 service to query a cell value from the semantic occupancy grid.

---

## What I implemented

- Added `map_query_service.py` inside `nn_mapping`.
- Subscribed to `/semantic_map`.
- Exposed service `/query_semantic_map`.
- Used `example_interfaces/srv/AddTwoInts` as a lightweight query interface:
  - `a -> x`
  - `b -> y`
  - `sum -> queried cell value`

## Validation

- Confirmed service registration with:
  - `ros2 service list | grep query_semantic_map`
- Queried the semantic map with:
  - `(x, y) = (96, 54)`
- Received response:
  - `sum = 0`

## Files involved

- `ws/src/nn_mapping/nn_mapping/map_query_service.py`
- `ws/src/nn_mapping/setup.py`

## Notes

This is a minimal prototype service for fast querying and validation. It reuses a standard ROS2 service type for speed instead of defining a custom `.srv` interface.

## Asset
`assets/day36_map_query_service.png`

---