# Day 32: PyTorch ROS2 Wrapper with CUDA-Backed Status Publisher

---

## What I built
Today I integrated a minimal **PyTorch-enabled ROS2 node** into the NeuroNav-ROS2 perception stack. The node imports PyTorch, detects the available device, runs a tiny tensor operation on a timer, and publishes a live status message on `/nn/pytorch_status`.

## What happened
The first attempt failed because PyTorch was not installed in the system Python. I created a local workspace virtual environment, installed `torch` and `torchvision`, and verified that CUDA was available. After that, I created a wrapper node and integrated it into the existing `nn_perception` package.

There was one package-structure issue: I initially placed `nn_pytorch_wrapper` as a nested package inside `nn_perception`, which `colcon` did not discover as a separate package. I corrected this by moving the node into the main `nn_perception` Python package and registering it properly in `setup.py`.

A second issue appeared when launching the node through ROS2: `ros2 run` could not find the `torch` module because it was installed inside the local virtual environment. I fixed this by exporting the virtual environment's `site-packages` path into `PYTHONPATH` before running the node.

## Commands used

```bash
cd ~/GitHub/NeuroNav-ROS2/ws
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install torch torchvision

colcon build --packages-select nn_perception
export PYTHONPATH=$HOME/GitHub/NeuroNav-ROS2/ws/.venv/lib/python3.12/site-packages:$PYTHONPATH
source install/setup.bash
ros2 run nn_perception pytorch_wrapper_node

colcon build --packages-select nn_bringup
ros2 launch nn_bringup day32_pytorch_wrapper.launch.py
```

## Result
The wrapper node successfully ran with:
- **PyTorch version:** 2.6.0+cu124
- **Device:** CUDA
- **Published status:** `device=cuda | tensor_sum=20.00`

I also verified the node visually using `rqt_graph`, which showed:
- `/pytorch_wrapper_node`
- `/nn/pytorch_status`

## Visual asset
**Asset:** `day32_pytorch_ros2_graph.png`

This visual confirms that the new PyTorch wrapper node is publishing correctly into the ROS2 graph, so today did not end as terminal-only noise.

## Key takeaway
Today established the **foundation for deep learning inside the ROS2 perception stack**. The node is still minimal, but now the project has a working bridge between ROS2 execution and GPU-backed PyTorch inference. That sets up the next step cleanly: building an actual object detection node on top of this wrapper.

## Status
Day 32 complete.

---