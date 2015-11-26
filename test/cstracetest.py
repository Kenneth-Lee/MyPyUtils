import sys
sys.path.append("..")

from MyParser import CsParser
from MyPlot import plot_data

cp = CsParser("cs.data")
print cp.cpus
#plot_cs(cp.items, "latency")
