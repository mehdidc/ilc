import sys
import numpy as np
from root_numpy import root2array
from collections import defaultdict
import scipy.stats

#filename = 'ECalReconstruction.root'
#tree = 'TestTree'
filename, tree = 'Secondaries.root', 'MCParticles'



variables = sys.argv[1:]
array = root2array(filename, tree, branches=variables)

values = defaultdict(list)
for i, event in enumerate(array):
    for value, var in zip(event, variables):
        if hasattr(value, "__iter__"):
            values[var].extend(value)
        else:
            values[var].append(value)


for var in variables:
    np.savetxt(var+".txt", values[var])

import matplotlib.pyplot as plt
eps=10E-6
distribs = [
        "lognorm",
        "norm",
        "invgauss",
        "beta",
]
for i, var in enumerate(variables):
    plt.subplot(1, len(variables), i + 1)
    plt.xlabel(var)

    plt.hist(values[var], bins=max(5, len(values[var])/100), normed=True, histtype='stepfilled', label='histogram')

    vals=np.array(values[var]) 
    V = np.arange(min(vals)+eps, max(vals)-eps, 0.01)

    for distrib in distribs:
        obj = eval("scipy.stats.%s"% (distrib,))
        params = obj.fit(vals)
        fit_V = obj.pdf(V, *params)
        score = np.sum(np.log(obj.pdf(vals, *params)))
        plt.plot(V, fit_V, label='%s fit'%(distrib,),lw=3)
    plt.legend()

plt.show()
