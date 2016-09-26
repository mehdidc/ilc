import numpy as np
from common import EnsembleRegressor, load_data, to_csv

if __name__ == '__main__':
    from docopt import docopt
    import pickle
    doc = """
    Usage: eval MODEL DATA CSV
    """
    args = docopt(doc)
    models = pickle.load(open(args['MODEL']))
    model = EnsembleRegressor(models)
    X, y = load_data(args['DATA'])
    X = X.reshape((X.shape[0], -1))
    to_csv(model.predict(X)[:, 0], y[:, 0], args['CSV'])
