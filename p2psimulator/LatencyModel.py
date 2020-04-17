import random
import bisect
import os

class KingLatencyModel:
	def __init__(self):
		path_to_cdf = os.path.abspath(__file__).rsplit('/', 1)[0] + "/king_delay_cdf"
		self.cdf = []
		with open(path_to_cdf, 'r') as rfile:
			for line in rfile:
				if line != "":
					self.cdf.append(int(line))

	def get_latency(self):
		rand = random.randint(0, self.cdf[-1])
		return bisect.bisect(self.cdf, rand)



		