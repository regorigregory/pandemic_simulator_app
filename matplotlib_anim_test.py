import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def get_initial_coordinates(width, height, n_particles):
    x_coords = np.random.random(n_particles) * width
    y_coords = np.random.random(n_particles) * height
    return np.array([x_coords, y_coords])
def get_initial_velocities(width, height, n_particles, speed_coefficient = 0.1):
    x_vel = np.random.random(n_particles) * width * speed_coefficient
    y_vel = np.random.random(n_particles) * height * speed_coefficient
    return np.array([x_vel, y_vel])
def get_new_locations(coordinates, velocities):
    return coordinates + velocities

def generate_animation_function(ax, width, height, n_particles, speed_coefficient):
    coordinates = get_initial_coordinates(width, height, n_particles)
    velocities = get_initial_velocities(width, height, n_particles, speed_coefficient=speed_coefficient)
    data_points, = ax.plot(*coordinates)



if __name__ == "__main__":
    matplotlib.use("TkAgg")

    n_particles = 100
    width = 10
    height = 10
    speed_coefficient = 0.01
    coordinates = get_initial_coordinates(width, height, n_particles)
    velocities = get_initial_velocities(width, height, n_particles, speed_coefficient=speed_coefficient)

    fig = plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))
    line, = ax.plot([], [])
    line, = ax.plot([], [], "ro")


    def init():
        line.set_data(*coordinates)
        return line,


    def animate(i):
        global coordinates, velocities
        coordinates = coordinates + velocities
        line.set_data(*coordinates)
        return line,


    anim = FuncAnimation(fig, animate, init_func=init,
                         frames=200, interval=20, blit=True)
    plt.show()