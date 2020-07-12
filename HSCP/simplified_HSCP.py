from copy import deepcopy
from p2psimulator import Node, Message

class SimpleHSCP(Node):
    def __init__(self, node_id, bandwidth, msg_queue, config):
        super().__init__(node_id, bandwidth, msg_queue)
        self.c = config['c'] # num of shard members
        self.k = config['k'] # num of shards in super-shard
        self.s = config['s'] # num of super-shards

        self.N = self.s * self.c * self.k
        self.received_microblocks = []
        self.received_blocks = []
        self.first_finished = False
        self.finished = False

    def start(self):
        msg = Message(self.id, None, "FIRST-ROUND-CONSENSUS", None, 1)

        shard_id = int(self.id / (self.k * self.c))
        self.logger.info(f"Shard id is {shard_id} for Node {self.id}")
        for i in range(self.c):
            new_msg = deepcopy(msg)
            new_msg.receiver = shard_id * self.k * self.c + i
            self.send(new_msg)

    def process(self, msg, time):
        if msg.type == "FIRST-ROUND-CONSENSUS" and not self.first_finished:
            self.recv_microblock(msg)
        
        elif msg.type == "SECOND-ROUND-CONSENSUS" and not self.finished:
            self.recv_block(msg)
    
    def recv_microblock(self, msg):
        self.received_microblocks.append(msg)
        if len(self.received_microblocks) > 2 * self.k * self.c / 3:
            self.logger.info(f"Received enough microblocks by Node {self.id}.")
            self.first_finished = True

            block = Message(self.id, None, "SECOND-ROUND-CONSENSUS", None, 1)
            for i in range(self.c):
                new_msg = deepcopy(block)
                new_msg.receiver = i
                self.send(new_msg)
        
    def recv_block(self, msg):
        self.received_blocks.append(msg)
        if len(self.received_blocks) > 2 * self.s * self.c / 3:
            self.logger.info(f"Received enough blocks by Node {self.id}")
            self.finished = True
