import copy
import bisect
import logging

from .Message import Message

class Node:
	def __init__(self, node_id, bandwidth, msg_queue):
		self.id = node_id
		self.msgs = []
		self.msg_queue = msg_queue
		self.bandwidth = bandwidth
		self.logger = logging.getLogger('p2psim')
	
	def recv(self, msg):
		bisect.insort(self.msgs, msg)

	def __eq__(self, other):
		return self.id == other.id

	def setTimeout(self, time, callback, args={}):
		''' set a timer to call callback
		time should be the time that callback should run
		also args should be in dict with keywords
		for example for f(time) it should be like {'time':3}
		'''
		msg = Message(self.id, self.id, "CALLBACK", {
			'callback': callback,
			'args': args}, 0, time)
		self.send(msg)

	def proceed(self, t):
		bw = self.bandwidth
		# while len(self.msgs) and self.msgs[0].time < t and bw > self.msgs[0].size:
		
		# For simulating highloads we assume just one msg is processed at each
		# time step, but real condition is the line up commented.
		if len(self.msgs) and self.msgs[0].time < t:
			new_msg = self.msgs[0]
			self.logger.debug(f'Node {self.id}: processing {new_msg.type}')

			if new_msg.type == "CALLBACK":
				new_msg.data['callback'](**new_msg.data['args'])
			else:
				bw -= new_msg.size
				self.process(new_msg, t)
			self.msgs.pop(0)

	def send(self, msg):
		self.logger.debug(f'Node {self.id}: sending {msg.type}')
		self.msg_queue.put(msg)

	def process(self, msg, time):
		pass

	def start(self):
		pass

