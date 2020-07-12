import os
import logging
import uuid
import sys


from HSCP import SimpleHSCP
from p2psimulator import Simulator

def sim_HSCP(s, k, c, t):
    LOG_FILE = str(uuid.uuid4())
    if os.path.isfile(LOG_FILE):
        os.remove(LOG_FILE)

    config = {
        "time_step": 1,
        "start_time": 0,
        "stop_time": t * 1000,
        "bandwidth": 6.25 / 1024 #50Kb/s
    }

    sim = Simulator(config, LOG_FILE, log_level=logging.DEBUG)

    # add nodes
    N = s * k * c
    sim.add_nodes(SimpleHSCP, N , {"c": c, "s": s, "k": k})

    sim.start()

    with open(LOG_FILE, 'r') as f:
        log = f.read()
    os.remove(LOG_FILE)
    
    lines = log.split('\n')
    t = 0
    cnt = 0
    for line in lines:
        if line.startswith("[p2psim][INFO] - sim: t ="):
            t = int(line.split()[-1])
        elif line.startswith("[p2psim][INFO] - Received enough blocks"):
            cnt += 1
            if cnt > 2 * c / 3:
                return t
    
    return None

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('Wrong input. S, K, C, T')
        exit(-1)
    
    t = sim_HSCP(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    print(f"Consensus finished at t = {t}.")
