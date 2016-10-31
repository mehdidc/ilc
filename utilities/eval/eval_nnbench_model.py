from common import EnsembleRegressor, load_data, to_csv
import time

if __name__ == '__main__':
    from docopt import docopt
    from keras.models import model_from_json
    import sys
    import pandas as pd
    doc = """
    Usage: eval_nnbench_model.py FOLDER DATA CSV
    """
    args = docopt(doc)
    folder = args['FOLDER']
    model = model_from_json(open(folder+'/model.json').read())
    model.load_weights(folder+'/model.pkl')
    X, y = load_data(args['DATA'])
    X = X.transpose((0, 3, 1, 2))

    t = time.time()
    pred = model.predict(X)[:, 0]
    print(time.time() - t)
    print(X.shape)
    to_csv(X, pred, y[:, 0], args['CSV'])
