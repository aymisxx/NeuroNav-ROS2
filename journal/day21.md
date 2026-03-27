# Day 21: Time Synchronization Benchmark Metric

## Artifact
**Suggested asset name:** `day21_time_sync_metric_node.png`

## Summary

Today was not just a "run the node and clap" day. It turned into a proper debug-and-upgrade pass.

The original `nn_time_sync/time_sync_node.py` was successfully launching and performing approximate time synchronization between `/imu/data` and `/camera/image_raw`, but it was only logging synchronization quality to the terminal. It was **not publishing any synchronized metric** that other nodes or tools could consume.

That meant the synchronization logic existed, but the pipeline stopped at human-readable logs.

So the real work for Day 21 became:

1. verify the node behavior end-to-end,
2. identify whether the missing output was a runtime bug or a design gap,
3. modify the node to publish a benchmark metric,
4. rebuild and validate the updated graph.

---

## What I verified first
I started from a clean workspace and confirmed that the expected packages were present:

- `nn_bringup`
- `nn_estimation`
- `nn_perception`
- `nn_sensors`
- `nn_time_sync`

Then I confirmed that `nn_time_sync` exposed the executable:
- `time_sync_node`

The node launched successfully and printed:
- `Approximate Time Sync Node Started`

So startup itself was not broken.

## First issue discovered

After checking the graph, I found that `/camera/image_raw` and `/imu/data` had subscribers but **zero publishers**.

That meant the synchronization node was waiting correctly, but no upstream sensor streams were active. In other words, the synchronizer was not the problem. The inputs were simply not being fed.

## Bringing the pipeline alive

I launched:
- `camera_publisher`
- `imu_publisher`

Once both were running, `time_sync_node` started reporting synchronized message pairs.

Typical synchronization logs looked like this:
- delta around **10.7 to 10.9 ms** initially.
- quality consistently reported as **GOOD**.

This confirmed that approximate time matching was functioning correctly.

## Second issue discovered
Even though synchronization was working, there was still **no new output topic** in the ROS graph.

Checks using:
- `ros2 topic list`
- `ros2 node info /time_sync_node`

showed that the node only had:
- subscribers to `/imu/data` and `/camera/image_raw`
- default publishers like `/rosout` and `/parameter_events`

There was **no benchmark output topic at all**.

At that point, I inspected the source code of `time_sync_node.py` directly.

## Root cause
The code confirmed the exact behavior seen at runtime:
- it subscribed to IMU and image topics,
- synchronized them using `ApproximateTimeSynchronizer`,
- computed time difference `dt`,
- classified quality (`EXCELLENT`, `GOOD`, `FAIR`, `POOR`),
- and only **logged** the result.

There was no publisher in the implementation.

So this was **not** a ROS runtime failure.
It was a **design gap** in the node.

## Fix implemented
I upgraded the node by adding a publisher:
- topic: `/time_sync/delta`
- type: `std_msgs/msg/Float32`

Now, each synchronized callback does two things:
1. logs the synchronization quality,
2. publishes the measured time offset `dt` as a float.

This converted the node from a passive debug monitor into a minimal benchmark metric producer.

## Rebuild and validation
After editing the file, I rebuilt only the relevant package:
- `colcon build --packages-select nn_time_sync`

The build completed successfully.

Then I relaunched the node and verified that:
- synchronization logs still appeared correctly,
- delta remained stable,
- `/time_sync/delta` now appeared in the ROS graph.

## Duplicate-node issue
During validation, I discovered another problem: **two instances of `/time_sync_node` were running simultaneously**.

This caused confusing graph introspection, where ROS would sometimes show the old logger-only node and sometimes the updated one.

Using process inspection, I found both process chains still alive and killed them manually. After that, I relaunched a single clean instance and verified that the graph contained exactly:
- `/camera_publisher`
- `/imu_publisher`
- `/time_sync_node`

This cleanup mattered because otherwise the verification would stay polluted by stale processes.

## Final verified result
The final clean node graph confirmed that `/time_sync_node` now has:
- subscribers:
  - `/camera/image_raw`
  - `/imu/data`
- publishers:
  - `/time_sync/delta`
  - `/rosout`
  - `/parameter_events`

I then verified the output directly:
- `ros2 topic echo /time_sync/delta --once`

Sample value:
- **0.011495113372802734 s**

That is approximately:
- **11.50 ms**

## Benchmark behavior

Observed runtime behavior after the fix:
- synchronization delta stayed around **11.4 to 11.7 ms**.
- synchronization quality stayed **GOOD**.
- publish rate of `/time_sync/delta` stayed at approximately **10 Hz**.
- timing jitter remained low.

This means the benchmark signal is now:
- stable,
- machine-readable,
- suitable for downstream monitoring, plotting, or future performance evaluation.

## Technical outcome of Day 21
Day 21 produced a real functional upgrade, not just a visual demo.

### Before today
- synchronization existed only as terminal logs.
- no benchmark topic was available for downstream use.

### After today
- synchronization still works correctly.
- time offset is now published as `/time_sync/delta`.
- output rate is verified at ~10 Hz.
- process graph has been cleaned and validated.

## Why this matters
A robotics system becomes far more useful when timing quality is available as a topic instead of living only in console text.

Publishing synchronization delta makes it possible to later:
- log timing statistics automatically,
- plot latency drift over time,
- trigger warnings if synchronization degrades,
- compare sensor timing quality across runs,
- feed benchmarking or diagnostics pipelines.

So this is a small code change, but architecturally it is a meaningful move toward observability.

## Closing note
Today began as a synchronization check and ended as a clean instrumentation upgrade.

The best part is that the final result is not ambiguous anymore:
**the node now publishes a measurable synchronization metric, and that metric has been verified live in ROS2.**

---