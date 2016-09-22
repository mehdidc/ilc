import os

import numpy as np
import pandas as pd

import ROOT
from root_numpy import root2array, root2rec, tree2rec, list_branches
from root_numpy.testdata import get_filepath
from root_numpy.testdata import get_filepath


def vectorize_point(E, X, Y, Z):
    v = np.zeros((18, 18, 30))
    for e, x, y, z in zip(E, X, Y, Z):
        v[x, y, z] = e
    return v

def vectorize_dataset(dataset):
    n = len(array)
    data = []
    for point in dataset:
        energy = point['energy']
        posx = point['posx']
        posy = point['posy']
        posz = point['posz']
        datapoint = vectorize_point(energy, posx, posy, posz)
        data.append(datapoint)
    data = np.array(data)
    return data

def array_to_dict(array, keys):
    n = len(array)
    data = []
    for i in range(n):
        point = {}
        for key, value in zip(keys, array[i]):
            point[key] = value
        data.append(point)
    return data

if __name__ == '__main__':
    from docopt import docopt

    doc = """
    Usage: generate_vectorized_data.py [--output=OUTPUT] [--tree=TREE] [--branches=BRANCHES] INPUT [OUTPUT]
    
    Arguments:
        INPUT input filename
        OUTPUT output filename[data.npz]

    Options:
        --tree=TREE root tree name [default: Stats]
        --branches=BRANCHES root branches list [default: nhits,interaction,posx,posy,posz,energy,MCParticleMomentum]
        --output=OUTPUT output branch names [default: MCParticleMomentum]
    """
    args = docopt(doc)
    filename = args['INPUT']
    output_filename = args['OUTPUT']
    tree = args['--tree'] if args['--tree'] else 'Stats'
    branches = args['--branches'] if args['--branches'] else 'nhits,interaction,posx,posy,posz,energy,MCParticleMomentum'
    branches = branches.split(',')
    output = args['--output'] if args['--output'] else 'MCParticleMomentum'
    output = output.split(',')
    array = root2array(filename, tree, branches=branches)
    data = array_to_dict(array, branches)
    X = vectorize_dataset(data)
    y = pd.DataFrame(data)[output].values
    print(X.shape, y.shape, type(X), type(y))
    np.savez(output_filename, X=X, y=y)
