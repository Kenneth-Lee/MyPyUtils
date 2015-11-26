import sys
import re

class MyParser:
    def ignoreline(self, reason, line):
        sys.stderr.write("ignore line("+str(reason)+"): "+line+"\n")

    def __init__(self, filename):
        lines = open(filename).readlines()
        for line in lines:
            line=line.strip()
            if line:
                self.parseline(line.strip())

class PingParser(MyParser):
    """parse latency data from ping output, e.g.:
    64 bytes from 192.168.201.1: icmp_seq=1 ttl=255 time=1.21 ms
    """

    items=[]

    def __init__(self, filename):
        MyParser.__init__(self, filename);

    def parseline(self, line):
        las = re.findall("time=(\d+.\d+) ms", line)
        if las and len(las)==1:
            self.items.append(float(las[0]))
        else:
            self.ignoreline(1, line)

class CsParser(MyParser):
    """parse context switch event from ftrace
    to get the parse data, do:
        echo irq:* > set_event
        echo sched_switch > set_event
    then get the result from trace and give to this parser

    the result looks like:
     <idle>-0     [001] d... 139464.058332: sched_switch: prev_comm=swapper/1 prev_pid=0 prev_prio=120 prev_state=R ==> next_comm=rcu_sched next_pid=7 next_prio=120
    """

    items=[]
    cpus=[]
    def __init__(self, filename):
        MyParser.__init__(self, filename);
        self.cpus.sort()

    def checkitem(self, item):
        cpu = int(item[1])
        if not cpu in self.cpus:
            self.cpus.append(cpu)
        return True

    def parseline(self, line):
        if line.startswith('#'):
            return
        item = line.split(None, 5)
        if len(item) != 6:
            self.ignoreline(1, line)
            return

        item[1] = item[1][1:-1]
        item[3] = item[3][0:-1]
        item[4] = item[4][0:-1]

        if self.checkitem(item):
            self.items.append(item)
        else:
            self.ignoreline(2, line)

