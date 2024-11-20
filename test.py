OPT_MATRIX_ROWS = 4
OPT_MATRIX_COLS = 4


class sfe_color_t:
    """
    Dataclass for storing color data from the OPT4048.
    """

    red: int = 0
    green: int = 0
    blue: int = 0
    white: int = 0
    counterR: int = 0
    counterG: int = 0
    counterB: int = 0
    counterW: int = 0
    CRCR: int = 0
    CRCG: int = 0
    CRCB: int = 0
    CRCW: int = 0


cie_matrix = [
    [0.000234892992, -0.0000189652390, 0.0000120811684, 0],
    [0.0000407467441, 0.000198958202, -0.0000158848115, 0.00215],
    [0.0000928619404, -0.0000169739553, 0.000674021520, 0],
    [0, 0, 0, 0],
]

if __name__ == "__main__":
    color = sfe_color_t()

    color.red = 1
    color.green = 1
    color.blue = 1

    a = b = c = x = y = z = 0

    for row in range(OPT_MATRIX_ROWS):
        x += color.red * cie_matrix[row][0]
        y += color.green * cie_matrix[row][1]
        z += color.blue * cie_matrix[row][2]

    print(f"X: {x}, Y: {y}, Z: {z}")

    a += color.red * cie_matrix[0][0]
    a += color.green * cie_matrix[1][0]
    a += color.blue * cie_matrix[2][0]

    b += color.red * cie_matrix[0][1]
    b += color.green * cie_matrix[1][1]
    b += color.blue * cie_matrix[2][1]

    c += color.red * cie_matrix[0][2]
    c += color.green * cie_matrix[1][2]
    c += color.blue * cie_matrix[2][2]

    print(f"A: {a}, B: {b}, C: {c}")
