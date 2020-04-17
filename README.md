# P2P Network Simulator
This is a network simulator that models a p2p network, so you can
implement any distributed algorithm and test that your algorithm works or not.

# Usage
You should install this package into your project.
```pip install p2psimulator```
For implementing your algorithm you should write your each node behavior, you can
see examples in tests folder.

# Network Model
For modeling network i used King dataset [[1]]. When a node send a message for another
randomly a delay is selected from this dataset.

## References
<a id="1">[1]</a> 
Gummadi, Krishna P., Stefan Saroiu, and Steven D. Gribble. "King: Estimating latency between arbitrary internet end hosts." Proceedings of the 2nd ACM SIGCOMM Workshop on Internet measurment. 2002.