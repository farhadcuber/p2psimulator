from copy import deepcopy
from p2psimulator import Node, Message

class SimpleElasticoNode(Node):
    def __init__(self, node_id, bandwidth, msg_queue, config):
        super().__init__(node_id, bandwidth, msg_queue)
        self.c = config['c'] # num of shard members
        self.s = config['s'] # 2^s is number of shards

        self.N = self.s * self.c
        self.received_microblocks = []
        self.finished = False

    def start(self):
        msg = Message(self.id, None, "FIRST-ROUND-CONSENSUS", None, 1)
        for i in range(self.c):
            new_msg = deepcopy(msg)
            new_msg.receiver = i
            self.send(new_msg)

    def process(self, msg, time):
        # Final shard consensus
        # Microblock is a term, I use for shard consensus results
        if msg.type == "FIRST-ROUND-CONSENSUS" and not self.finished:
            self.recv_microblock(msg)
    
    def recv_microblock(self, msg):
        self.received_microblocks.append(msg)
        if len(self.received_microblocks) > 2*self.N/3:
            self.logger.info(f"Received enough microblocks by Node {self.id}.")
            self.finished = True
