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
    plt.plot(np.arange(0, len(data), 1), data)
    ave=mean(data)
    plt.axhline(ave, 0, len(data), color='r')
    plt.title(name + " sequence (max=%f, min=%f, ave=%f)"%(max(data), min(data), ave))

    plt_show(filename)


cmap = ['w', 'r', 'y', 'g']
def plot_cs(cp, filename=None):
    "cp is a CsParser Object"

    bar_len=10
    bar_gap=5

    if not len(cp.cpus):
        return

    plt.xlabel("time(ns)")
    plt.ylabel("cpu")
    plt.title("context switch chart")

    axd=cp.get_axis()
    plt.axis(axd)

    for cpu in cp.cpus:
        xy=cp.get_cpu_xy(cpu)
        lx, ly = 0, 0
        for x, y in xy:
            if lx != 0:
                plt.axhspan(cpu*3+0.1, (cpu+1)*3-0.1, xmin=float(lx)/float(axd[1]), xmax=float(x)/float(axd[1]), 
                        facecolor=cmap[ly], alpha=0.5)
            lx, ly = x, y

    plt_show(filename)
