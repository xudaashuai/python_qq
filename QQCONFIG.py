import re
import threading,queue
from socket import *

ADDR = ('202.114.196.97', 21558)

s = socket(AF_INET, SOCK_DGRAM)

name_re = re.compile(r"[^:#]+")

q=queue.Queue(1)
class ReceiveThread(threading.Thread):
	result = None

	def run(self):
		self.result, _ = s.recvfrom(100000)
		q.put_nowait(self.result)
		print(self.result)

