import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

"""
Define the gaisser-hillas function
We must ensure that the base of the function, i.e. (X - X0) / (Xmax - X0) does
not = 0. We clip those entries and return 0 instead. However, we might still 
have 0^0 which would then == 1 and cause a jump. That case is removed in the return statement"""


def gaisser_hillas(X, Nmax, X0, Xmax, lam):
    base = np.clip((X - X0) / (Xmax - X0), 0, None)
    exponent = (Xmax - X0) / lam
    profile = Nmax * base**exponent * np.exp((Xmax - X) / lam)
    return np.where(X > X0, profile, 0.0)


"""
# We can calculate the Gaisser-Hillas distribution for a set of paramenters
# Then using a numpy random number generator, we can create sample noise for
# an array of the same size, normalize the variance per array element according
# to the signal strength, and add that to the original distribution to simulate
# real data."""


def noise_generator(true_parameters, noise_fraction=0.05, seed=42):
    X = np.linspace(1, 1200, 120)
    profile = gaisser_hillas(X, *true_parameters)
    rng = np.random.default_rng(seed)
    noise_to_add = rng.normal(0, noise_fraction * profile)
    noisy_profile = profile + noise_to_add
    return X, noisy_profile


def main():
    X = np.linspace(0.0, 1200.0, 500)
    for Nmax, Xmax in [(1e8, 500), (1e9, 625), (1e10, 750)]:
        plt.plot(
            gaisser_hillas(X, Nmax, 0.0, Xmax, 70.0),
            label=f"Nmax={Nmax:.0e}, Xmax={Xmax}",
        )
    plt.xlabel("Depth [g/cm$^2$]")
    plt.ylabel("N")
    plt.title("Gaisser-Hillas Profiles")
    plt.legend()
    plt.savefig("figures/gaisser_hillas_test.png", dpi=150)
    plt.clf()

    true_parameters = [1e9, 0.0, 650.0, 70.0]
    guess_parameters = [8e8, 0.0, 600.0, 60.0]

    X, noisy_profile = noise_generator(true_parameters)
    popt, pcov = curve_fit(gaisser_hillas, X, noisy_profile, p0=guess_parameters)
    perr = np.sqrt(np.diag(pcov))
    best_fit = gaisser_hillas(X, *popt)

    fig, axs = plt.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [3, 1]})

    axs[0].scatter(X, noisy_profile, s=10, alpha=0.5, label="noise", marker="+")
    axs[0].plot(X, best_fit, "r-", label="best fit")
    axs[0].set_ylabel("N")
    axs[0].legend()
    axs[0].set_title("Gaisser-Hillas Fit")

    axs[1].scatter(X, noisy_profile - best_fit, marker="x")
    axs[1].axhline(0, color="k", lw=0.5)
    axs[1].set_xlabel("Depth [g/cm$^2$]")
    axs[1].set_ylabel("Residual")
    plt.tight_layout()
    plt.savefig("figures/gh_fit.png", dpi=150)
    plt.clf()

    names = ["Nmax", "X0", "Xmax", "lambda"]
    for name, t, f, e in zip(names, true_parameters, popt, perr):
        print(f"{name:12s}:  true={t:13.2f}  fit={f:13.2f}  +/- {e:13.2f}")

    energies = [1e7, 1e8, 1e9, 1e10]
    xmax_values = []
    for i, E0 in enumerate(energies):
        tp = [E0 / 0.085, 0.0, 450.0 + 70.0 * np.log10(E0 / 1e7), 70.0]
        dX, dY = noise_generator(tp, seed=i)
        po, _ = curve_fit(gaisser_hillas, dX, dY, p0=tp)
        xmax_values.append(po[2])
        print(
            f"E0={E0:.0e}, guess Xmax={tp[2]:.1f}, fitted Xmax={po[2]:.1f}, fitted lam={po[3]:.1f}"
        )
    slope, intercept = np.polyfit(np.log10(energies), xmax_values, 1)
    print(f"Elongation rate: {slope:.1f} g/cm$^2$ per decade")


if __name__ == "__main__":
    main()
