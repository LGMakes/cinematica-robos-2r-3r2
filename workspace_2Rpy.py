# Animação do robô 2R com a área de trabalho (nuvem de pontos)

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

a1, a2 = 2, 1.5

# Cinemática direta 2R
def forward_kinematics_2r(theta1, theta2):
    x1 = a1*np.cos(theta1)
    y1 = a1*np.sin(theta1)
    x2 = x1 + a2*np.cos(theta1+theta2)
    y2 = y1 + a2*np.sin(theta1+theta2)
    return (0,0), (x1,y1), (x2,y2)

# Espaço de trabalho (nuvem de pontos)
def workspace_points_2r(n=100):
    θ1 = np.linspace(0, 2*np.pi, n)
    θ2 = np.linspace(0, 2*np.pi, n)
    X, Y = [], []
    for t1 in θ1:
        for t2 in θ2:
            x = a1*np.cos(t1) + a2*np.cos(t1+t2)
            y = a1*np.sin(t1) + a2*np.sin(t1+t2)
            X.append(x)
            Y.append(y)
    return X, Y

X, Y = workspace_points_2r()

# Figura
fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-4,4)
ax.set_ylim(-4,4)
ax.set_aspect('equal')
ax.scatter(X, Y, s=1, alpha=0.2, color="gray")  # área de trabalho marcada
line, = ax.plot([], [], 'o-', lw=2, color="blue")

theta1_vals = np.linspace(0, 2*np.pi, 100)
theta2_vals = np.linspace(0, np.pi, 100)

def init():
    line.set_data([], [])
    return line,

def update(frame):
    t1 = theta1_vals[frame % len(theta1_vals)]
    t2 = theta2_vals[frame % len(theta2_vals)]
    p0, p1, p2 = forward_kinematics_2r(t1, t2)
    xs = [p0[0], p1[0], p2[0]]
    ys = [p0[1], p1[1], p2[1]]
    line.set_data(xs, ys)
    return line,

ani = FuncAnimation(fig, update, frames=200, init_func=init, blit=True, interval=50)
plt.title("Robô 2R com área de trabalho")
plt.show()