import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from atmosphere import atm_depth
from heitler import X0, cascade_profile

# create grids mapping altitude to depth using atm_depth from atmosphere.py
h_grid = np.linspace(0, 85000, 1000)
depth_grid = np.array([atm_depth(h) for h in h_grid])


def depth_to_alt(depth):
    """Take a depth (or array of depths) in g/cm^2 and return the
    corresponding altitude(s) in meters. interp1d needs a monotonic
    increasing first argument, and depth decreases as altitude increases,
    so both grids are reversed."""
    f = interp1d(depth_grid[::-1], h_grid[::-1])
    return f(depth)


def cascade_vs_alt(E0):
    depth_gcm2, particles = cascade_profile(E0)
    altitude_m = depth_to_alt(depth_gcm2)
    return altitude_m, particles, depth_gcm2


def plotter():
    E0 = 1e7
    alt, N, X = cascade_vs_alt(E0)
    fig, (ax1, ax2) = plt.subplots(1, 2, layout="constrained")
    ax1.plot(X, N)
    ax1.set_yscale("log")
    ax1.set_xlabel("Atmospheric Depth [gm/$cm^2$]")
    ax1.set_ylabel("Number of Particles")
    ax2.invert_xaxis()
    ax2.plot(alt, N)
    ax2.set_yscale("log")
    ax2.set_xlabel("Altitude [km]")
    ax2.set_ylabel("Number of Particles")
    plt.tight_layout()
    fig.savefig("figures/depth_and_altitude_cascade.png")
    plt.clf()


def main():
    plotter()


if __name__ == "__main__":
    main()
