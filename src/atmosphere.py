import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

# Building the US Standard Atmosphere layered model and integrating to get atmospheric depth

# Define standard layer values as a tuple
# layer_example (base alitude [m], temperature [K], temperature lapse rate [K/m]) where the temperature lapse rate is the temp rate of change with altitude
G0 = 9.80665  # m/s^2
R = 8.31447  # J/mol*K
M = 0.0289644  # kg/mol
P0 = 101325.0  # Pa mean sea level

LAYERS = [
    (0.0, 288.15, -0.0065),
    (11e3, 216.65, 0.0),
    (20e3, 216.65, 0.001),
    (32e3, 228.65, 0.0028),
    (47e3, 270.65, 0.000),
    (51e3, 270.65, -0.0028),
    (71e3, 214.65, -0.002),
    (85e3, 186.95, 0.0),
]


def _layer_index(h):
    idx = 0
    for i, (hb, _, _) in enumerate(LAYERS):  # only have to compare to height to get idx
        if h >= hb:
            idx = i
    return idx


def temperature(h):
    hb, Tb, Lb = LAYERS[_layer_index(h)]
    return Tb + Lb * (h - hb)


def exponential_pressure(Pb, h, hb, Tb):
    return Pb * math.exp((-G0 * M * (h - hb)) / (R * Tb))


def power_pressure(Pb, h, hb, Tb, Lb):
    base = Tb / (Tb + Lb * (h - hb))
    power = (G0 * M) / (R * Lb)
    return Pb * math.pow(base, power)


def get_pressure_layers():
    Pb = [P0]
    for i in range(len(LAYERS) - 1):
        hb, Tb, Lb = LAYERS[i]
        h_top = LAYERS[i + 1][0]
        if Lb != 0:
            Pb.append(power_pressure(Pb[i], h_top, hb, Tb, Lb))
        else:
            Pb.append(exponential_pressure(Pb[i], h_top, hb, Tb))
    return Pb


def pressure(h):
    Pb = get_pressure_layers()
    idx = _layer_index(h)
    hb, Tb, Lb = LAYERS[idx]
    if Lb != 0:
        return power_pressure(Pb[idx], h, hb, Tb, Lb)
    else:
        return exponential_pressure(Pb[idx], h, hb, Tb)


def density(h):
    return (M * pressure(h)) / (
        R * temperature(h)
    )  # vectorizing function to work with arrays


def atm_depth(h):
    h_max = LAYERS[-1][0]
    depth, _ = integrate.quad(density, h, h_max)  # [kg/m^2]
    return depth * 0.1  # [g / cm^2]


def slant_depth(theta=60.0, h=0):
    """theta [degrees]. only valid from 0-60 deg"""
    rad = np.radians(theta)
    return atm_depth(h) / np.cos(rad)


def my_plotter(bins=120):
    """Plotting temperature, pressure and density vs altitude"""
    h_max = LAYERS[-1][0]
    altitudes = np.linspace(0, h_max, bins)
    vector_temp = np.vectorize(temperature)
    vector_pres = np.vectorize(pressure)
    vector_dens = np.vectorize(density)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 5))
    ax1.plot(altitudes, vector_temp(altitudes))
    ax1.set_title("Temperature")
    ax1.set_xlabel("Altitude (m)")
    ax2.plot(altitudes, vector_pres(altitudes))
    ax2.set_title("Pressure")
    ax2.set_yscale("log")
    ax2.set_xlabel("Altitude (m)")
    ax3.plot(altitudes, vector_dens(altitudes))
    ax3.set_title("Density")
    ax3.set_yscale("log")
    ax3.set_xlabel("Altitude (m)")
    plt.tight_layout()
    plt.savefig("figures/atmosphere_profiles.png")
    plt.clf()

    vector_dep = np.vectorize(atm_depth)
    plt.plot(vector_dep(altitudes), altitudes / 1000)
    plt.xlabel("Atmospheric Depth [g/$cm^2$]")
    plt.ylabel("Altitude [km]")
    plt.title("Atmospheric Depth")
    plt.savefig("figures/atmospheric_depth.png")
    plt.clf()

    th = np.linspace(0, 60, 120)
    vector_sl = np.vectorize(slant_depth)
    plt.plot(vector_sl(th), th)
    plt.xlabel("Slant Depth [g/$cm^2$]")
    plt.ylabel("Zenith Angle [degrees]")
    plt.title("Slant Depth")
    plt.savefig("figures/slant_depth.png")
    plt.clf()


def main():
    my_plotter()
    depth_msl = atm_depth(0)
    print(f"Atmospheric Depth at Mean Sea Level: {depth_msl}")
    print(density(0))


if __name__ == "__main__":
    main()
