import matplotlib.pyplot as plt
import numpy as np
import json
from math import pow, sqrt

def plot_f(c, k):
    with open(f'res_{c}_{k}.json', 'r') as f:
        values = json.load(f)
    
    # Theorical threshold
    t_pbft = 4596
    d_net = 961
    a = t_pbft + d_net
    th = a + 2 * c + 4 * sqrt(pow(c, 2) + a * c)
    
    N = np.array(values['n'])
    t_elastico = np.array(values["elastico"])
    t_hscp = np.array(values["hscp"])

    f_elastico = t_elastico + 2 * t_pbft
    f_hscp = t_hscp+3*t_pbft

    plt.plot(N, f_elastico, '-o', label="ELASTICO")
    plt.plot(N, f_hscp, '-x', label="HSCP")
    plt.axvline(x = th, ls=':', color='g', label="Theorical Threshold")
    plt.legend(loc="upper left")
    plt.title(f"Average Elastico and HSCP consensus time for c = {c} and k = {k}")
    plt.ylabel("Average consensus time (ms)")
    plt.xlabel("Number of nodes")
    # idx = np.argwhere(np.diff(np.sign(f_hscp - f_elastico))).flatten()
    # plt.plot(N[idx], f_hscp[idx], 'ro')
    plt.show()

plot_f(100, 16)