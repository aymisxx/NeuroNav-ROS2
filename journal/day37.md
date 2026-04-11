# Day 37: Language-Conditioned Goals

## Objective

Built a minimal language-conditioned goal node that maps simple text queries to fixed navigation goals.

---

## What I implemented

- Added `language_goal_node.py` inside `nn_mapping`.
- Subscribed to `/language_query` using `std_msgs/String`.
- Published `geometry_msgs/PoseStamped` goals to `/language_goal`.
- Implemented a minimal label-to-goal lookup:
  - `plant -> (2.0, 1.0)`
  - `chair -> (4.0, 2.0)`
  - `table -> (6.0, 3.0)`

## Validation

- Started `language_goal_node`.
- Published query:
  - `plant`
- Confirmed goal output on `/language_goal`.
- Observed published goal:
  - `frame_id = map`
  - `position = (2.0, 1.0)`

## Files involved

- `ws/src/nn_mapping/nn_mapping/language_goal_node.py`
- `ws/src/nn_mapping/setup.py`

## Notes

This is a minimal prototype for language-conditioned navigation goals. It does not yet query the semantic map dynamically and instead uses a fixed lookup table for fast validation.

## Asset

`assets/day37_language_conditioned_goals.png`

---