import os
import pytest

from p2psimulator import Node, Simulator, Message

class Sender(Node):
    def start(self):
        msg = Message(self.id, None, "Hello", {"content" : "Hello world!"}, 0)
        self.send(msg)

class Receiver(Node):
    def process(self, msg, t):
        if msg.type == "Hello":
            print(f"received: {msg.data['content']}")

@pytest.fixture
def init_simulator():
    config = {
        "time_step": 1,
        "start_time": 0,
        "stop_time": 1000,
        "bandwidth": 1
    }

    sim = Simulator(config, "hellowolrd.log")
    sim.add_nodes(Sender, 1)
    sim.add_nodes(Receiver, 1)
    sim.start()
    yield sim
    os.remove("helloworld.log")

def test_helloworld(init_simulator):
    print("hello")

