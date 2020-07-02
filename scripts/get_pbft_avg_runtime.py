import os
import pytest
import logging
import json
import uuid
import sys

import numpy as np
import matplotlib.pyplot as plt

from pbft import Replica, ReqGenerator
from p2psimulator import Simulator


def sim(N, d, overall):
    LOG_FILE = str(uuid.uuid4())
    if os.path.isfile(LOG_FILE):
        os.remove(LOG_FILE)

    config = {
        "time_step": 1,
        "start_time": 0,
        "stop_time": overall*1000,
        "bandwidth": 6.25 / 1024 #50Kb/s
    }

    sim = Simulator(config, LOG_FILE, log_level=logging.DEBUG)

    # Replicas should be added first
    sim.add_nodes(Replica, N, N)
    # N = number of replicas, mean_req_time = 20ms
    sim.add_nodes(ReqGenerator, 1, N, d)

    sim.start()

    with open(LOG_FILE, 'r') as f:
        log = f.read()
    
    calc_avg_time(log, N, d, overall)
    os.remove(LOG_FILE)

def calc_avg_time(log, N, d, overall):

    lines = log.split('\n')
    t = 0
    msgs = {}
    for line in lines:
        if line.startswith("[p2psim][INFO] - sim: t ="):
            t = int(line.split()[-1])
        elif line.startswith("[p2psim][DEBUG] - msg"):
            msg_id = int(line.split()[3])
            msgs[msg_id] = {"start_time": t}
        elif line.startswith("[p2psim][INFO] - client: msg"):
            msg_id = int(line.split()[4])
            msgs[msg_id]["end_time"] = t
            msgs[msg_id]["duration"] = t - msgs[msg_id]["start_time"]

    with open(f"result_pbft_c{N}_{d}ms_{overall}s.json", 'w') as f:
        json.dump(msgs, f)

if __name__ == '__main__':
    sim(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))