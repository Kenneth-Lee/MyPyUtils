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

	return items as a list of time in ms
	"""


	def __init__(self, filename):
	        self.items=[]
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

	the input looks like:
	<idle>-0     [001] d... 139464.058332: sched_switch: prev_comm=swapper/1 prev_pid=0 prev_prio=120 prev_state=R ==> next_comm=rcu_sched next_pid=7 next_prio=120

	get the parse result from get_cpu_xy, it result the xy list [times, status-es]
	status can be 0-idle, 1-irq, 2-softirq, 3-thread

	the self.cpus return a list of cpus
	"""

	def __init__(self, filename):
                self.items=[]
                self.cpus=[]

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
		item[3] = int(float(item[3][0:-1])*1000000)
		item[4] = item[4][0:-1]

		if self.checkitem(item):
			self.items.append(item)
		else:
			self.ignoreline(2, line)


	def get_axis(self, cpu_height=3):
		return [0, self.items[-1][3] - self.items[0][3],
			0, max(self.cpus) * cpu_height]

	def get_cpu_xy(self, cpu):
		xy=[]
		prev=0
		cur=0
		time_begin = self.items[0][3]
		for item in self.items:
			if int(item[1])==cpu:
				if item[4]=='sched_switch':
					next_pid = int(re.findall("next_pid=(\d+)", item[5])[0])

					if next_pid==0:
						cur=0
					else:
						cur=3
					prev=cur
				elif item[4]=='irq_handler_entry':
					cur = 1
				elif item[4]=='irq_handler_exit':
					cur = prev
				elif item[4]=='softirq_entry':
					cur = 2
				elif item[4]=='softirq_exit':
					cur = prev

				xy.append([item[3] - time_begin, cur])
		return xy
