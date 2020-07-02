import json
import sys

import numpy as np
import matplotlib.pyplot as plt

def find_max_msg_id(msgs):
    max_id = 0
    for key, value in msgs.items():
        if "duration" in value:
            max_id = max(max_id, int(key))
    
    return max_id

def calc_avg_time(N, d, overall):
    with open(f"result_pbft_c{N}_{d}ms_{overall}s.json", 'r') as f:
        msgs = json.load(f)
    
    max_msg_id = find_max_msg_id(msgs)

    ids = np.arange(0, max_msg_id + 1)
    ds = np.zeros(np.shape(ids))
    for _id in ids:
        if str(_id) in msgs and "duration" in msgs[str(_id)]:
            ds[_id] = msgs[str(_id)]["duration"]
        elif _id > 0:
            ds[_id] = ds[_id - 1]
    
    plt.plot(ids, ds)
    plt.show()

if __name__ == '__main__':
    calc_avg_time(sys.argv[1], sys.argv[2], sys.argv[3])