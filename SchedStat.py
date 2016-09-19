#read /proc/schedstat

import time

def sublist(list1, list2):
    list3=[]

    i=0
    for e in list1:
        if isinstance(e, list):
            list3.append(sublist(e, list2[i]))
        else:
            list3.append(int(e) - int(list2[i]))
        i+=1

    return list3


class SchedStatParser:

    def sub(self, schedstat):
        return sublist(self.cpu_stats, schedstat.cpu_stats)

    def decode(self, lines):
        if self.version == 15:
            self.timestamp=long(lines[0].split(' ')[1])
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('cpu'):
                    self.cpu_stats.append(line.split(' ')[1:])
                elif line.startswith('domain'):
                    c = line.split(' ')
                    self.domain_mask.append(c[1])
                    self.cpu_stats[-1].append(c[2:])

        else:
            raise ValueException("version")

    def __init__(self):
        self.version = -1 
        self.timestamp = -1L
        self.cpu_stats = []
        self.domain_mask = []

        f = open('/proc/schedstat')
        lines = f.readlines()
        f.close()
        if lines[0].startswith("version"):
            self.version=int(lines[0].split(' ')[1])
        self.decode(lines[1:])

sp = SchedStatParser()
time.sleep(1)
sp1 = SchedStatParser()

s = sp1.sub(sp)

print 'total cpu: ', len(s)
for i in s:
    print i[8]

