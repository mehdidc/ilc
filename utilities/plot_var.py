import sys
import numpy as np
from root_numpy import root2array
from collections import defaultdict
import scipy.stats
from vars import get_vars, get_raw_values, get_other_values

#filename = 'ECalReconstruction.root'
#tree = 'TestTree'
filename, tree = '../rootfiles/Secondaries.root', 'MCParticles'


all_variables = sys.argv[1:]
raw_variables, other_variables = get_vars(all_variables)
all_variables = raw_variables + other_variables

array = root2array(filename, tree, branches=raw_variables)
values = get_raw_values(array, raw_variables)
values = get_other_values(values, other_variables)

# text save

vars_to_save = raw_input("what do you want to save?").split()
for var in vars_to_save:
    if var not in values:
        continue 
    np.savetxt(var+".txt", values[var])

# plot

vars_to_plot = raw_input("what do you want to plot?").split()

import matplotlib.pyplot as plt
eps=10E-6
distribs = [
        "lognorm",
        "norm",
]
for i, var in enumerate(vars_to_plot):
    if var not in values:
        continue
    plt.subplot(1, len(vars_to_plot), i + 1)
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
