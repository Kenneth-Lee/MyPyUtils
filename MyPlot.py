#this is the helper class to plot data 

import numpy as np
import matplotlib.pyplot as plt

__all__ = ["plot_data"]

def mean(data):
    return float(sum(data)) / len(data)

def plot_data(data, name=None, filename=None):
    plt.xlabel("sequence")
    if name:
        plt.ylabel(name)
    plt.title(name + "sequence")
    plt.plot(np.arange(0, len(data), 1), data)
    plt.axhline(mean(data), 0, len(data), color='r')
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
