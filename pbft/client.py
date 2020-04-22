import random
import numpy
import math
import logging

from p2psimulator import Simulator, Node, Message

class ReqGenerator(Node):
    def __init__(self, node_id, bandwidth, msg_queue, N, mean_wait_time):
        super().__init__(node_id, bandwidth, msg_queue)
        self.mean_wait_time = mean_wait_time
        self.N = N
        self.client_id = 0
        self.log = []
        self.received_msg = []
        self.logger = logging.getLogger('p2psim')
        
    def start(self):
        self.req_send(0)
    
    def process(self, msg, time):
        if msg.type == "REPLY":
            self.reply_recv(msg, time)
        
    def req_send(self, time):
        # signed <REQUEST, o, t, c> : o(operation), t(timestmap), c(client)
        data = ("REQUEST", 0, time, self.client_id)
        req = Message(self.id, 0, "REQUEST", data, 16, time)
        self.send(req)
        
        ## wait for next time
        wait = numpy.random.exponential(self.mean_wait_time, 1)
        self.setTimeout(time + wait[0], self.req_send)
        
        ## Increase client_id to have unique messages
        self.client_id = self.client_id + 1
    
    def reply_recv(self, msg, time):
        ## Add to stack until f+1 of them
        self.log.append(msg.data)
        
        cnt = 0
        for _msg in self.log:
            if _msg[3] == msg.data[3]:
                cnt += 1
        
        if cnt >= math.floor(self.N / 3) + 1 and \
            msg.data[3] not in self.received_msg:
            self.logger.info(f'client: msg {msg.data[3]} is commited')
            self.received_msg.append(msg.data[3])
        