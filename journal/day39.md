# Day 39: Robustness Testing

## Objective

Performed a minimal robustness test on the language-conditioned goal pipeline by sending an invalid query and verifying graceful handling.

---

## What I tested

- Ran `language_goal_node`.
- Published an unknown label: `banana`.

## Validation

- Confirmed the node did not crash.
- Confirmed it rejected the unknown label safely.
- Observed warning log: `Unknown label: banana`.

## Files involved

`ws/src/nn_mapping/nn_mapping/language_goal_node.py`

## Notes

This was a lightweight robustness check focused on failure handling for invalid language inputs. The node behaved correctly by warning and ignoring the unsupported query.

## Asset

`assets/day39_robustness_testing.png`

---