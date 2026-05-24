# Heitler Cascade Simulator

import math
import numpy as np
import matplotlib.pyplot as plt

# Assuming an EM shower only
# The primary particle splits into 2 particles of half energy each
# The subparticles traverse some distance and split again
# Photons undergo pair production
# Electrons/positrons undergo brehmstrahlung (aka braking radiation)
# The distance travelled for both types is assumed equal
# 
# === Defining Physical Constants ===

X0 = 37.0 # radiation length in air [g/cm**2] the mean distance an electron travels before losing 1/e energy due to braking radiation

EC = 85.0 # critical energy [MeV] the particle energy below which ionization losses start to dominate

# ===================================

# The number of particle generations is dictated by how many times we can split our primary particle energy.
def n_generations(E0):
    # After each splitting step n, there are 2**n particles
    # Splitting stops when E0 = EC
    return math.log2(E0/EC)

# Calculates the Atmospheric depth traversed with each generation and the number of particles at each generation step
def cascade_profile(E0):
    # create an array of steps from 0 to the n_th generation
    n = np.arange(int(n_generations(E0) + 1))
    
    # Depth d [g/cm**2] is the depth of the shower in units of the radiation length X0
    # create an array of the depth for each generation
    d = X0 * n
    
    # The number of particles after n steps is 2**n
    num_particles = np.power(2.0, n)
    return d, num_particles

# Returns the number of particles at shower maximum - how many times can we split the primary energy
def n_max(E0):
    return E0 / EC

# Returns the max shower depth - the point in the atmospheric depth where the shower begins to die out
def x_max(E0):
    return X0 * math.log2(E0/EC)


def main():
    energies = [1e4, 1e6, 1e8] #MeV (1e10, 1e15, 1e20 in eV)
    # cascade_profile=cascade_profile(energy_ranges)

    fig, ax = plt.subplots()

    styles = [("-", 4), ("--", 3), (":", 2)]

    for E0, (ls, lw) in zip(energies, styles):
        depth, particles = cascade_profile(E0)
        line, = ax.plot(depth, particles, label=f"E0 = {E0:.0e} MeV", linestyle=ls, linewidth=lw)
        ax.axvline(x_max(E0), color=line.get_color(), linestyle="--", alpha=0.5)

    # for E0 in energies:
    #     depth, particles = cascade_profile(E0)
    #     line, = ax.plot(depth, particles, label=f"E0 = {E0:.0e} MeV")
    #     ax.axvline(x_max(E0), color=line.get_color(), linestyle="--", alpha=0.5)
    #
    ax.set_yscale('log')
    ax.set(xlabel='Atmospheric Depth [in X_0]')
    ax.set(ylabel='Number of Particles')
    ax.set(title='Heitler Model of EM Cascade')
    ax.legend()
    
    fig.savefig("figures/heitler_cascade.png")
    plt.show()

if __name__ == "__main__":
    main()
