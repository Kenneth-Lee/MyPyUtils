import sys
sys.path.append("..")

from MyParser import CsParser
from MyPlot import plot_cs

cp = CsParser("cs.data")
plot_cs(cp)
