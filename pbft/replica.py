import math

from p2psimulator import Simulator, Node, Message

class Replica(Node):
    def __init__(self, node_id, bandwidth, msg_queue, num_replicas):
        super().__init__(node_id, bandwidth, msg_queue)
        self.N = num_replicas
        self.view_num = 0
        self.seq_num = 0
        self.log = []
        self.msg_status = {}
    
    def is_primary(self):
        return self.id == (self.view_num % self.N)
    
    def process(self, msg, time):
        if msg.type == "REQUEST":
            self.req_recv(msg, time)
        elif msg.type == "PRE_PREPARE":
            self.pre_prepare_recv(msg, time)
        elif msg.type == "PREPARE":
            self.prepare_recv(msg, time)
        elif msg.type == "COMMIT":
            self.commit_recv(msg, time)
            
    def req_recv(self, msg, time):
        if self.is_primary():
            ## Pre-Prepare <signed <PRE-PREPARE, v, n, d>, m>
            ## v(view num), d(digest of m), n(seq num), m(message)
            data = (("PRE_PREPARE", self.view_num, self.seq_num, \
                hash(msg.data))
                    , msg.data)
            new_msg = Message(self.id, None, "PRE_PREPARE", data, 30)
            self.send(new_msg)
            
            ## Append to log
            self.log.append(msg.data)
            self.log.append(data[0])
            
            ## Increase seq num
            self.seq_num = self.seq_num + 1
        
        else:
            ## Send to primary replica
            pass

    def pre_prepare_recv(self, msg, time):
        ## Check if seq_num is used for another msg
        pass
    
        ## Check if in same view
        if msg.data[0][1] != self.view_num:
            return
    
        ## Check h < seq_num < H
        pass
        
        ## Check if signatures in msg are correct
        pass

        ## Send signed <PREPARE, v, n, d, i>
        ## v(view_num), n(seq_num), d(digest of m), i(replica id)
        data = ("PREPARE", self.view_num, msg.data[0][2], msg.data[0][3], \
             self.id)
        new_msg = Message(self.id, None, "PREPARE", data, 20)
        self.send(new_msg)
        
        ## Append to log
        self.log.append(msg.data[0])
        self.log.append(msg.data[1])
        self.prepare_recv(new_msg, time)
    
    def prepare_recv(self, msg, time):
        ## Check Signature, view_num, seq_num
        pass

        ## Append to log
        self.log.append(msg.data)

        ## Check if msg is prepared
        if self.prepared(msg.data[1], msg.data[2], msg.data[3]) and \
            (msg.data[2], 'prepared') not in self.log:
            
            self.log.append((msg.data[2], 'prepared'))

            ## send signed <COMMIT, v, n, d, i>
            data = ("COMMIT", msg.data[1], msg.data[2], msg.data[3], self.id)
            
            if data in self.log:
                ## we send it before
                return
            else:
                new_msg = Message(self.id, None, "COMMIT", data, 20)
                self.send(new_msg)
                self.commit_recv(new_msg, time)
    
    def prepared(self, view_num, seq_num, digest):
        ## check if client msg is in log
        _client_msg = digest in [hash(x) for x in self.log]
        
        ## check if pre-prepare is exist
        _pre_prepare = ("PRE_PREPARE", view_num, seq_num, digest) in self.log
        
        ## check if 2f prepare exist
        num = math.floor(self.N / 3) * 2
        cnt = 0
        for msg in self.log:
            if msg[0] == "PREPARE" and msg[1] == view_num \
                and msg[2] == seq_num and msg[3] == digest:
                cnt += 1
            
        return cnt >= num and _pre_prepare and _client_msg

    def commit_recv(self, msg, time):
        ## Check Signature, view_num, seq_num
        pass

        ## Append to log
        self.log.append(msg.data)
        
        ## check if msg is commited-local
        if self.commited_local(msg.data[1], msg.data[2], msg.data[3]) and \
            (msg.data[2], 'commited') not in self.log:

            self.log.append((msg.data[2], 'commited'))
            
            ## Send reply to client
            client_msg = self.get_client_msg(msg.data[3])
            data = ("REPLY", msg.data[1], client_msg[2], client_msg[3],
                    self.id, 0)
            self.send(Message(self.id, self.N, "REPLY", data, 21, time))
    
    def commited_local(self, view_num, seq_num, digest):
        if self.prepared(view_num, seq_num, digest):
            cnt = 0
            for msg in self.log:
                if msg[0] == "COMMIT" and msg[1] == view_num \
                    and msg[2] == seq_num and msg[3] == digest:
                    cnt += 1
            
            if cnt >= math.floor(self.N / 3) * 2 + 1:
                return True
        return False
        
    def get_client_msg(self, digest):
        for msg in self.log:
            if hash(msg) == digest:
                return msg
        return None        
                
            