import os
import pytest
import logging

from pbft import Replica, ReqGenerator
from p2psimulator import Simulator

LOG_FILE = 'pbft.log'

@pytest.fixture
def sim(N):
    config = {
        "time_step": 1,
        "start_time": 0,
        "stop_time": 10000,
        "bandwidth": 1
    }

    sim = Simulator(config, LOG_FILE, log_level=logging.DEBUG)

    # Replicas should be added first
    sim.add_nodes(Replica, N, N)
    # N = number of replicas, mean_req_time = 20ms
    sim.add_nodes(ReqGenerator, 1, N, 2000)

    sim.start()
    yield sim
    os.remove(LOG_FILE)

@pytest.mark.parametrize('N', [4, 10])
def test_N_replica(sim):
    with open(LOG_FILE, 'r') as f:
        log = f.read()

    assert 'client: msg' in log