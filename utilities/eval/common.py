import numpy as np
import pandas as pd

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

def rmse(pred, true):
    return np.sqrt(((pred - true)**2).mean())

def load_data(filename):
    data = np.load(filename)
    X = data['X']
    y = data['y']
    return X, y

def to_csv(pred, true, filename):
    pd.DataFrame({'y_pred': pred, 'y_true': true}).to_csv(filename)
