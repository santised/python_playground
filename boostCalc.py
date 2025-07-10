from tabulate import tabulate


def boost_calc(resistor_two):
    resistor_one = resistor_two * ((12 / 1.25) - 1)
    return [resistor_one, resistor_two]


def actual_VOUT(resistor_one, resistor_two):
    out = 1.25 * (1 + (resistor_one / resistor_two))
    print("Actual VOUT is ", out, " Volts")
    return out


def iref_calc(vout):
    current_resistor = (vout - 2) / (18.75 * 0.000001)
    print(current_resistor, "Ohm Needed")


if __name__ == "__main__":
    table = []
    for i in range(1000, 5000, 100):
        temp_list = boost_calc(i)
        table.append(temp_list)

    print(tabulate(table, headers=["Resistor One", "Resistor Two"]))
    iref_calc(actual_VOUT(18000, 2100))
