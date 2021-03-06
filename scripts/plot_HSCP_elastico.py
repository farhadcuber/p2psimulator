from .run_simplified_HSCP import sim_HSCP
from .run_simplified_elastico import sim_elastico

import numpy as np
import matplotlib.pyplot as plt

def calc(c, k):
    # c = 50
    # k = 2
    T = 15
    s_hscp = np.ceil(100 / (c * k) * np.array([2, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]))
    # s_hscp = 100 / (c * k) * np.array([2, 10])
    s_elastico = k * s_hscp
    n = s_elastico * c
    t_elastico = np.zeros(len(s_hscp))
    t_hscp = np.zeros(len(s_elastico))

    for i, s in enumerate(s_hscp):
        print(f"HSCP : s = {int(s)}, k = {k}, c = {c}")
        t = sim_HSCP(int(s), k, c, T)
        if t is not None:
            t_hscp[i] = t
        print(f"t = {t}")

    # with open(f'res_{c}_{k}_HSCP.txt', 'w') as f:
    #     f.write(str(n) + '\n' + str(t_hscp))

    for i, s in enumerate(s_elastico):
        print(f"ELASTICO : s = {int(s)}, c = {c}")
        t = sim_elastico(int(s), c, T)
        if t is not None:
            t_elastico[i] = t
        print(f"t = {t}")
    
    with open(f'res_{c}_{k}.txt', 'w') as f:
        f.write(str(n) + '\n' + str(t_elastico) + '\n' + str(t_hscp))        

# plt.plot(n, t_elastico, '-o', label="ELASTICO")
# plt.plot(n, t_hscp, '-x', label="HSCP")
# plt.legend(loc="upper left")
# plt.title(f"Average Elastico and HSCP consensus time for c = {c} and k = {k}")
# plt.ylabel("Average consensus time (ms)")
# plt.xlabel("Number of nodes")
# plt.show()

values = [(100,16)]

for c, k in values:
    calc(c, k)