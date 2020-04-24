from enum import Enum
from copy import deepcopy
from hashlib import sha256

import numpy
from p2psimulator import Node, Message

# Elastico states
NONE = 0
FORMED_IDENTITY = 1
RUN_AS_DIRECTORY = 2
SHARD_MEMBER = 3
SHARD_LEADER = 4
FINAL_SHARD_MEMBER = 5
FINAL_SHARD_LEADER = 6

# Consensus is modeled like this:
# 1. Leader broadcasts proposed block as SHARD_CONSENSUS_PRE_PREPARE
# 2. Members validate block and send SHARD_CONSENSUS_PREPARE to leader
# 3. When leader received 2/3 of PREPARE msgs, it broadcasts SHARD_CONSENSUS_COMMIT
# 4. Members receiving COMMIT, consider block as committed.

# Message formats
# type - data format - size
# POW - (identity) - 32 bytes

class ElasticoNode(Node):
    def __init__(self, node_id, bandwidth, msg_queue, config):
        super().__init__(node_id, bandwidth, msg_queue)
        self.state = ElasticoNode.NONE
        self.dir_nodes = []
        self.shards = dict()

        self.pow_time = config['pow_time'] # mean time to wait for pow
        self.c = config['c'] # num of shard members
        self.s = config['s'] # 2^s is number of shards 
    
    def start(self):
        # generate a random number to wait for pow
        # wait time for pow has exponential distribution with mean 100ms
        pow_time = numpy.floor(numpy.random.exponential(self.pow_time, 1)[0])

        # set callback
        self.setTimeout(pow_time, self.pow_done, args={})

    def process(self, msg, time):
        # pow and shard formation phase
        if msg.type == "POW" and self.state == NONE:
            self.add_to_dir_nodes(msg, time)
        elif msg.type == "POW" and self.state == RUN_AS_DIRECTORY:
            self.form_shards(msg, time)
        elif msg.type == "SHARD_MEMBERS" and self.state in [FORMED_IDENTITY, RUN_AS_DIRECTORY]:
            self.identify_own_shard(msg, time)

        # Intra-shard consensus phase
        elif msg.type == "SHARD_CONSENSUS_PRE_PREPARE" and self.state == SHARD_MEMBER:
            self.prepare_consensus(msg, time)
        elif msg.type == "SHARD_CONSENSUS_PREPARE" and self.state == SHARD_LEADER:
            self.commit_consensus(msg, time)
        elif msg.type == "SHARD_CONSENSUS_COMMIT" and self.state == SHARD_MEMBER:
            self.send_to_final_shard(msg, time)

        # Final shard consensus
        # Microblock is a term, I use for shard consensus results
        elif msg.type == "MICROBLOCK" and self.state == FINAL_SHARD_LEADER:
            self.recv_microblock(msg, time)
        elif msg.type == "FINAL_CONSENSUS_PRE_PREPARE" and self.state == FINAL_SHARD_MEMBER:
            self.prepare_consensus(msg, time)
        elif msg.type == "FINAL_CONSENSUS_PREPARE" and self.state == FINAL_SHARD_LEADER:
            self.commit_consensus(msg, time)
        elif msg.type == "FINAL_CONSENSUS_COMMIT" and self.state == FINAL_SHARD_MEMBER:
            self.broadcast_final_block(msg, time)
          
    def add_to_dir_nodes(self, msg, time):
        if len(self.dir_nodes) < self.c:
            self.logger.debug(f'Node {self.id} added {msg.sender} to it\'s dir_nodes')
            self.dir_nodes.append(msg.sender)
            self.form_shards(msg, time)

    def form_shards(self, msg, time):
        shard_id = self.get_shard_id(msg.data[0])
        if shard_id not in self.shards:
            self.shards[shard_id] = []
        self.shards[shard_id].append(msg.sender)

    def identify_own_shard(self, msg, time):
        pass

    def prepare_consensus(self, msg, time):
        pass

    def commit_consensus(self, msg, time):
        pass

    def send_to_final_shard(self, msg, time):
        pass

    def recv_microblock(self, msg, time):
        pass

    def broadcast_final_block(self, msg, time):
        pass

    # Functions that not called by process
    def pow_done(self):
        self.logger.debug(f'Node {self.id} POW calculated.')
        msg = Message(self.id, None, "POW", (sha256(self.id)), 32)
        if len(self.dir_nodes) < self.c:
            self.logger.debug(f'Node {self.id} running as directory.')
            self.state = RUN_AS_DIRECTORY
            self.send(msg)
        else:
            self.state = FORMED_IDENTITY
            for node_id in self.dir_nodes:
                new_msg = deepcopy(msg)
                new_msg.receiver = node_id
                self.send(new_msg)
    
    def get_shard_id(self, x):
        ''' x is a sha256 object
            returns s most significant bits of x
        '''
        d = x.digest()
        if x <= 8:
            return d[0] >> (8 - self.s)
        else:
            self.logger.error('Not implented.')
            raise NotImplementedError