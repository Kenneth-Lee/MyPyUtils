#this is the helper class to plot data 

import numpy as np
import matplotlib.pyplot as plt

__all__ = ["plot_data", "plot_cs"]

def mean(data):
    return float(sum(data)) / len(data)

def plt_show(filename):
    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def plot_data(data, name=None, filename=None):
    plt.xlabel("sequence")
    if name:
        plt.ylabel(name)
    plt.title(name + "sequence")
    plt.plot(np.arange(0, len(data), 1), data)
    plt.axhline(mean(data), 0, len(data), color='r')

    plt_show(filename)


def plot_cs(cp, filename=None):
    "cp is a CsParser Object"

    bar_len=10
    bar_gap=5

    if not len(cp.cpus):
        return

    plt.xlabel("time(ms)")
    plt.ylabel("cpu")
    plt.title("context switch chart")

    for cpu in cp.cpus:
        xy=cp.get_cpu_xy(cpu)
        plt.plot(xy[0], xy[1])

    plt_show(filename)
