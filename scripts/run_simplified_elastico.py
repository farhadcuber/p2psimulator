import os
import logging
import uuid
import sys


from elastico import SimpleElasticoNode
from p2psimulator import Simulator

def sim_elastico(s, c, t):
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
    N = c * s
    sim.add_nodes(SimpleElasticoNode, N , {"c": c, "s": s})

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
        elif line.startswith("[p2psim][INFO] - Received enough microblocks"):
            cnt += 1
            if cnt > 2 * c / 3:
                return t  

    return None
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Wrong input. S, C, T')
        exit(-1)
    
    t = sim_elastico(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    print(f"Consensus finished at t = {t}.")
