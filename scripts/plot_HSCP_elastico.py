from .run_simplified_HSCP import sim_HSCP
from .run_simplified_elastico import sim_elastico

import numpy as np
import matplotlib.pyplot as plt

c = 50
k = 2
T = 15
s_hscp = np.array([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
s_elastico = 2 * s_hscp
n = s_elastico * 50
t_elastico = np.zeros(len(s_hscp))
t_hscp = np.zeros(len(s_elastico))

for i, s in enumerate(s_hscp):
    print(f"HSCP : s = {s}, k = {k}, c = {c}")
    t = sim_HSCP(s, k, c, T)
    if t is not None:
        t_hscp[i] = t
    print(f"t = {t}")

for i, s in enumerate(s_elastico):
    print(f"ELASTICO : s = {s}, c = {c}")
    t = sim_elastico(s, c, T)
    if t is not None:
        t_elastico[i] = t
    print(f"t = {t}")

plt.plot(n, t_elastico, '-o', label="ELASTICO")
plt.plot(n, t_hscp, '-x', label="HSCP")
plt.legend(loc="upper left")
plt.title(f"Average Elastico and HSCP consensus time for c = {c} and k = {k}")
plt.ylabel("Average consensus time (ms)")
plt.xlabel("Number of nodes")
plt.show()