import random
import math
import logging
import copy
from queue import Queue

import progressbar as pb
from .LatencyModel import KingLatencyModel

class Simulator:
	def __init__(self, config, log_file, log_level=logging.INFO):
		
		self.time_step = config['time_step']
		self.start_time = config['start_time']
		self.stop_time = config['stop_time']
		self.bandwidth = config['bandwidth'] * self.time_step * (1024 ** 2)
		
		self.nodes = []
		self.msg_queue = Queue()

		self._init_logger(log_file, log_level)

		self.latency_model = KingLatencyModel()
	
	def _init_logger(self, log_file, log_level):
		self.logger = logging.getLogger('p2psim')
		self.logger.setLevel(log_level)
		
		handler = logging.FileHandler(log_file)
		handler.setLevel(log_level)

		log_format = logging.Formatter('[%(name)s][%(levelname)s] - %(message)s')
		handler.setFormatter(log_format)
		
		self.logger.addHandler(handler)

	def add_nodes(self, node_type, num, *args):
		for i in range(num):
			node_id = len(self.nodes)
			self.nodes.append(node_type(node_id, self.bandwidth, \
				self.msg_queue, *args))

	def start(self):
		for node in self.nodes:
			node.start()

		widgets = ['Processed: ', pb.Counter()*self.time_step, ' ms (', pb.Timer(), ')']
		pbar = pb.ProgressBar(widgets=widgets)

		for t in pbar((t for t in range(self.start_time, self.stop_time, \
			self.time_step))):
			self.logger.info(f'sim: t = {t}')
			
			while not self.msg_queue.empty():
				msg = self.msg_queue.get()
				if msg.receiver == None:
					for node in self.nodes:
						if msg.sender == node.id:
							continue
						new_msg = copy.deepcopy(msg)
						new_msg.time = t + self.latency_model.get_latency()
						node.recv(new_msg)
				else:
					if msg.type != "CALLBACK":
						msg.time = t + self.latency_model.get_latency()
					self.nodes[msg.receiver].recv(msg)

			for node in self.nodes:
				node.proceed(t)
