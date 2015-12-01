import sys
sys.path.append("..")

from MyParser import CsParser
from MyPlot import plot_cs

cp = CsParser("cs1.data")
#plot_cs(cp, "test.svg")
plot_cs(cp)
