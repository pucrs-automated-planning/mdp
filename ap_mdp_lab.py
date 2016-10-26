# The line below is to be used if you have pymdptoolbox installed with setuptools
# import mdptoolbox.example
# Whereas the line below obviate the need to install that
import sys
sys.path.insert(0, 'pymdptoolbox/src')
import mdptoolbox.example

import numpy as _np
from gen_scenario import *


"""
(Y,X)
| 00 01 02 ... 0X-1
| 10  .         .
| 20    .       .
| .       .     .
| .         .   .
| .           . .
| Y-1,0 . . .   Y-1X-1
""" 


shape = [3,4]
rewards = [[0,3,100],[1,3,-100]]
obstacles = [[1,1]]
terminals = [[0,3],[1,3]]
P, R = mdp_grid(shape=shape, terminals=terminals, r=-3, rewards=rewards, obstacles=obstacles)
vi = mdptoolbox.mdp.ValueIterationGS(P, R, discount=0.99, epsilon=0.001, max_iter=1000, skip_check=True)
# vi.verbose = True # Uncomment this for question 2
vi.run()
#You can check the quadrant values using print vi.V
print_policy(vi.policy, shape, obstacles=obstacles, terminals=terminals)
