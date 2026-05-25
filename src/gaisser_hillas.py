import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# define the gaisser-hillas function
def gaisser_hillas(X, Nmax, X0, Xmax, lam):
    base = np.clip( (X - X0)/(Xmax - X0), 0, None)
    exponent = (Xmax - X0) / lam
    profile = Nmax * base ** exponent * np.exp( (Xmax - X) / lam )
    return np.where(X > X0, profile, 0.0) # for edge case where exponent == 0 -> 0^0 = 1, instead of returning 0

def main():
    X = np.linspace(0.0, 1200.0, 500)
    # Nmax_set = [1e6, 1e7, 1e8]
    # Xmax_set = [1e3, 2e3, 4e3]
    # lam ~ 70.0
    #
    for Nmax, Xmax in [(1e8, 500), (1e9, 625), (1e10, 750)]:
        plt.plot(gaisser_hillas(X, Nmax, 0.0, Xmax, 70.0), label=f'Nmax={Nmax:.0e}, Xmax={Xmax}')
    plt.xlabel("Depth [g/cm$^2$]")
    plt.ylabel("N")
    plt.title("Gaisser-Hillas Profiles")
    plt.legend()
    plt.savefig("figures/gaisser_hillas_test.png", dpi=150)
    plt.clf()

if __name__ == "__main__":
    main()
