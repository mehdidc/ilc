import sys
import numpy as np
from root_numpy import root2array

filename = ('/mac/Users/mehdi/Documents/Projects/GenerativePhysics/ECalReconstruction.root')
array = root2array(filename, 'TestTree', branches=["energy", "posx", "posy", "posz"])

events = np.zeros(  (len(array), 30, 18, 18)  )

for i, event in enumerate(array):
    energy, posx, posy, posz = event
    for e, x, y, z in zip(energy, posx, posy, posz):
        events[i , z, y, x]  = e

np.save(sys.argv[1], events)
