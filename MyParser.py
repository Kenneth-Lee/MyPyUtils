import sys
import re

class PingParser:
    """parse latency data from ping output, e.g.:
    64 bytes from 192.168.201.1: icmp_seq=1 ttl=255 time=1.21 ms
    """

    items=[]

    def __init__(self, filename):
        lines = open(filename).readlines()
        for line in lines:
            las = re.findall("time=(\d+.\d+) ms", line)
            if las and len(las)==1:
                self.items.append(float(las[0]))
            else:
                sys.stderr.write("ignore line: "+line)

