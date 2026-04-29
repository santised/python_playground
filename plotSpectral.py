import matplotlib.pyplot as plt
import numpy as np

wavelengths = np.linspace(350, 1000, 1000)

# U2
TCS3448_CHANNELS = [
    ("F1", 407, 28),
    ("F2", 424, 29),
    ("FZ", 450, 67),
    ("F3", 473, 38),
    ("F4", 516, 48),
    ("FY", 560, 123),
    ("F5", 546, 44),
    ("FXL", 596, 93),
    ("F6", 636, 58),
    ("F7", 687, 63),
    ("F8", 748, 77),
    ("NIR", 855, 61),
]

# U4
TCS3430_CHANNELS = [
    ("X1", 437, 55),
    ("X2", 574, 93),
    ("Y", 537, 102),
    ("Z", 434, 63),
]

# U3
# TCS3430_CHANNELS = [
#    ("UVA", 437, 55),
#    ("UVB", 574, 93),
#    ("UVC", 537, 102),
# ]
# a Replacment for U2 3448
TCS3530_CHANNELS = [
    ("X1", 436, 420),
    ("X2", 594, 548),
    ("Y", 555, 508),
    ("Z", 445, 421),
    ("HgL", 519, 508),
    ("HgH", 545, 535),
]


def plot_guass(x, peak, fwhm):
    sigma = fwhm / 2.355
    return np.exp(-0.5 * ((x - peak) / sigma) ** 2)


if __name__ == "__main__":
    for name, peak, fwhm in TCS3448_CHANNELS:
        y = plot_guass(wavelengths, peak, fwhm)
        plt.plot(wavelengths, y, label=name, color="green")

    for name, peak, fwhm in TCS3430_CHANNELS:
        y = plot_guass(wavelengths, peak, fwhm)
        plt.plot(wavelengths, y, label=name, color="red")

    # Replacement part
    for name, peak, fwhm in TCS3530_CHANNELS:
        y = plot_guass(wavelengths, peak, fwhm)
        plt.plot(wavelengths, y, label=name, color="blue")

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Normalized Responsivity")
    plt.title("Spectral Responsivity")
    plt.legend(loc="upper right", fontsize=7)
    plt.xlim(350, 1000)
    plt.ylim(0, 1.1)
    plt.xticks(np.arange(350, 1001, 25))
    plt.show()
