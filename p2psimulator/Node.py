import copy
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
		self.msgs.append(msg)

	def __eq__(self, other):
		return self.id == other.id

	def setTimeout(self, time, callback):
		''' set a timer to call callback
		time should be the time that callback should run
		'''
		msg = Message(self.id, self.id, "CALLBACK", {
			'callback': callback}, 0, time)
		self.send(msg)

	def proceed(self, t):
		bw = self.bandwidth
		while len(self.msgs) and self.msgs[0].time < t and bw > self.msgs[0].size:
			new_msg = self.msgs[0]
			self.logger.debug(f'Node {self.id}: processing {new_msg.type}')

			if new_msg.type == "CALLBACK":
				new_msg.data['callback']()
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

