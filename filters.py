import numpy
from scipy import signal

ir_order = 4
f_cut = 50
output_data_rate = 120

if __name__ == "__main__":
    [b, a] = signal.butter(ir_order, f_cut / (output_data_rate / 2), "low")
