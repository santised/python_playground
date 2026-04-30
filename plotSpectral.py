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

OLD_SPECTRAL_CHANNELS = [
    ("A", 410, 20),
    ("B", 435, 20),
    ("C", 460, 20),
    ("D", 485, 20),
    ("F", 510, 20),
    ("G", 535, 20),
    ("H", 560, 20),
    ("R", 585, 20),
    ("I", 610, 20),
    ("S", 645, 20),
    ("J", 680, 20),
    ("T", 705, 20),
    ("T", 730, 20),
    ("U", 760, 20),
    ("V", 810, 20),
    ("W", 860, 20),
    ("K", 900, 20),
    ("L", 940, 20),
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
    # This part is EOL already?
    for name, peak, fwhm in TCS3448_CHANNELS:
        y = plot_guass(wavelengths, peak, fwhm)
        plt.plot(wavelengths, y, label=name, color="blue")

        # Tricolor 1931 CIE color sensor
    # for name, peak, fwhm in TCS3430_CHANNELS:
    #    y = plot_guass(wavelengths, peak, fwhm)
    #    plt.plot(wavelengths, y, label=name, color="red")

    for name, peak, fwhm in OLD_SPECTRAL_CHANNELS:
        y = plot_guass(wavelengths, peak, fwhm)
        plt.plot(wavelengths, y, label=name, color="red")

    # Replacement part
    # for name, peak, fwhm in TCS3530_CHANNELS:
    #     y = plot_guass(wavelengths, peak, fwhm)
    #     plt.plot(wavelengths, y, label=name, color="blue")

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Normalized Responsivity")
    plt.title("Spectral Responsivity")
    plt.legend(loc="upper right", fontsize=7)
    plt.xlim(350, 1000)  # this keeps the graph from floating
    plt.ylim(0, 1.1)  # this keeps the graph from floating
    plt.xticks(np.arange(350, 1001, 25))
    plt.show()
