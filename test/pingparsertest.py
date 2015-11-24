import sys
sys.path.append("..")

from MyParser import PingParser
from MyPlot import plot_data

pp = PingParser("ping.data")
plot_data(pp.items, "latency")
