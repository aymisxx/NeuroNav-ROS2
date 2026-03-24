# Day 18: Time Synchronization Analysis in ROS2

## Objective
To analyze temporal alignment between heterogeneous sensor streams (IMU and Camera) in a ROS 2 pipeline and implement synchronization strategies for reliable multi-sensor fusion.

---

## System Setup
- IMU Publisher → `/imu/data` (~10 Hz).
- Camera Publisher → `/camera/image_raw` (~10 Hz).
- New package: `nn_time_sync`.

## Naive Timestamp Comparison

### Approach
- Subscribed independently to IMU and Camera topics.
- Extracted timestamps from message headers.
- Computed: $Δt = ||t_{imu} - t_{image}||$.

### Observation
- Delta oscillated between:
  - ~0.044 sec.  
  - ~0.056 sec.  

### Interpretation
- Streams are active and stable.
- However, comparison was between **latest received messages**, not temporally aligned pairs.
- Result: alternating mismatch due to asynchronous callbacks.

## Approximate Time Synchronization

### Approach
- Implemented `ApproximateTimeSynchronizer` (ROS `message_filters`).
- Parameters:
  - `queue_size = 10`.
  - `slop = 0.1 sec`.

### Result
- Consistent synchronized pairing achieved.
- Observed: $Δt ≈ 0.045 sec (stable)$.

### Interpretation
- Synchronizer successfully pairs closest timestamps.
- Remaining offset is **systematic**, not random.

## Sync Quality Classification

### Criteria

| Delta (sec) | Quality |
|------------|--------|
| < 0.01     | EXCELLENT |
| < 0.03     | GOOD |
| < 0.05     | FAIR |
| ≥ 0.05     | POOR |

### Observed Output
- Consistently:
  - `Delta ≈ 0.045 sec`.
  - `Quality: FAIR`.

## Key Insights

1. **Stable but Offset Streams**
   - Both sensors operate reliably at ~10 Hz.
   - Fixed temporal offset (~45 ms) observed.

2. **Naive vs Synced Comparison**
   - Naive method reveals asynchronous callback effects.
   - Synchronization filters produce meaningful pairing.

3. **Deterministic Timing Error**
   - Offset is consistent → likely due to:
     - publisher timing differences.  
     - processing delay.  
     - timestamp assignment strategy.  

4. **Practical Implication**
   - Approximate synchronization is sufficient for many fusion pipelines.
   - For high-precision systems, further correction (e.g., timestamp alignment or delay compensation) is required.

## Asset

`day18_time_sync_quality.png`  

→ Visualization of synchronized timestamp delta and quality classification.

## Conclusion

Successfully implemented and analyzed time synchronization in a ROS 2 multi-sensor setup. Demonstrated the limitations of naive timestamp comparison and validated the effectiveness of approximate synchronization techniques. Identified a consistent inter-sensor delay (~45 ms), laying the groundwork for future delay compensation and fusion strategies.

## Next Steps

- Publish `/time_sync/delta` as a ROS topic.  
- Implement delay compensation (time offset correction).  
- Integrate synchronized data into fusion pipeline (e.g., EKF / state estimation).

---