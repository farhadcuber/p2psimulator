from enum import Enum
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

class ElasticoNode(Node):
    def __init__(self, node_id, bandwidth, msg_queue):
        super().__init__(node_id, bandwidth, msg_queue)
        self.state = ElasticoNode.NONE
        self.dir_nodes = []
    
    def start(self):
        pass

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
        pass

    def form_shards(self, msg, time):
        pass

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

