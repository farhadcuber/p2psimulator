import os
import pytest
import logging

from p2psimulator import Node, Simulator, Message

class Sender(Node):
    def start(self):
        msg = Message(self.id, None, "Hello", {"content" : "Hello world!"}, 0)
        self.send(msg)

class Receiver(Node):
    def process(self, msg, t):
        if msg.type == "Hello":
            self.logger.info("Received successfully")

@pytest.fixture
def sim():
    config = {
        "time_step": 1,
        "start_time": 0,
        "stop_time": 1000,
        "bandwidth": 1
    }

    sim = Simulator(config, "helloworld.log", log_level=logging.DEBUG)
    sim.add_nodes(Sender, 1)
    sim.add_nodes(Receiver, 1)
    sim.start()
    yield sim
    os.remove("helloworld.log")

def test_helloworld(sim):
    with open('helloworld.log', 'r') as f:
        log = f.read()
    
    assert "Received successfully" in log

