if __name__ == '__main__':
    from docopt import docopt
    import numpy as np
    doc = """
    Usage: split.py FILE TRAIN TEST TRAIN_SIZE
    """
    args = docopt(doc)
    
    data = np.load(args['FILE'])
    X = data['X']
    y = data['y']
    
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    
    train_size = int(args['TRAIN_SIZE'])
    print('Train size:{} Test size:{}'.format(train_size, len(X)-train_size))
    X_train = X[0:train_size]
    y_train = y[0:train_size]
    X_test = X[train_size:]
    y_test = y[train_size:]

    np.savez(args['TRAIN'], X=X_train, y=y_train)
    np.savez(args['TEST'], X=X_test, y=y_test)
