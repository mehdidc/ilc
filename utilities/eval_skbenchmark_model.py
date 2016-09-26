import numpy as np

class EnsembleRegressor(object):
    def __init__(self, regs=None):
        self.regs = regs

    def fit(self, X, y):
        return self

    def predict(self, X, return_std=False):
        if return_std:
            means = []
            stds = []
            for r in self.regs:
                m, s = r.predict(X, return_std=True)
                means.append(m)
                stds.append(s)
            means = np.vstack(means).T
            stds = np.vstack(stds).T
            return np.mean(means, axis=1), (np.sqrt((stds**2).sum(axis=1)) / stds.shape[1])
        else:
            preds = np.vstack([r.predict(X) for r in self.regs]).T
            return np.mean(preds, axis=1)

if __name__ == '__main__':
    from docopt import docopt
    import pickle
    doc = """
    Usage: eval NAME DATA
    """
    args = docopt(doc)
    models = pickle.load(open(args['NAME']))
    model = EnsembleRegressor(models)
    data = np.load(args['DATA'])
    X = data['X']
    y = data['y']
    X = X.reshape((X.shape[0], -1))
    print(np.sqrt(((model.predict(X) - y)**2).mean()))
