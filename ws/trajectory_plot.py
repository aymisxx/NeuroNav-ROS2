import matplotlib.pyplot as plt
import random

# Simulate same motion logic
objects = {
    0: [100, 100],
    1: [300, 200],
    2: [500, 400],
}

history = {k: [v.copy()] for k, v in objects.items()}

# simulate motion
for _ in range(50):
    for obj_id, pos in objects.items():
        dx = random.randint(-20, 20)
        dy = random.randint(-20, 20)

        pos[0] = max(0, min(640, pos[0] + dx))
        pos[1] = max(0, min(480, pos[1] + dy))

        history[obj_id].append(pos.copy())

# plot
for obj_id, traj in history.items():
    xs = [p[0] for p in traj]
    ys = [p[1] for p in traj]

    plt.plot(xs, ys, marker='o', label=f'ID {obj_id}')

plt.title("Multi-Object Tracking Trajectories")
plt.xlim(0, 640)
plt.ylim(0, 480)
plt.legend()
plt.grid()

plt.gca().invert_yaxis()  # image-style coords
plt.savefig("trajectory_day19.png")
plt.show()