import pandas as pd
import numpy as np
import scipy
import tensorflow as tf
from sklearn.model_selection import TimeSeriesSplit, train_test_split

class PreProcessors(object):

    def __init__(self):
        pass

    def fit(self):
        pass

    def transform(self):
        pass

    def reverse_transform(self):
        pass

    def generate_window(self, df, n_lags):
        pass


class GriddedDataProcessor(PreProcessors):
    def __init__(self):
        super().__init__()

    def transform(self, df, index, cols, value, var_name,  agg='sum'):

            df = df.pivot_table(
                values=value,
                index=index,
                columns=cols,
                aggfunc=agg
            )
            df.columns = [
                '{var_name:}_{lat:}_{lon:}'.format(var_name=var_name, lat=i[0], lon=i[1])
                for i in df.columns.to_flat_index()
            ]
            return df


class LSTMProcessor(PreProcessors):
        def __init__(self):
            super().__init__()

        def transform(self, dataset, target, start_index, end_index, history_size, target_size, step, single_step=False):
            data = []
            labels = []

            start_index = start_index + history_size
            if end_index is None:
                end_index = len(dataset) - target_size

            for i in range(start_index, end_index - 1):
                if i == 365:
                    print('d')

                indices = range(i - history_size, i, step)
                data.append(dataset[indices])

                if single_step:
                    labels.append(target[i + target_size])
                else:
                    labels.append(target[i:i + target_size])

            return np.array(data), np.array(labels)


class WindowProcessor(PreProcessors):
    def __init__(self):
        super().__init__()

    def transform(self, X, y, n_in=1, n_out=1, dropnan=True, y_name='val_vaz_natr'):
        X = pd.DataFrame(X)
        y = pd.DataFrame(y)

        cols, names = list(), list()
        # input sequence (t-n_in, ... t-1, t+0, t+1, t+2 ... t+n_out)
        for i in range(n_in, n_out+1, 1):
            cols.append(X.shift(-i))
            names += ['{var:}_(t{lag:+d})'.format(var=var, lag=i) for var in X.columns]

        # Label sequence (t-n_in, ... t-1, t+0, t+1, t+2 ... t+n_out)
        y_lag = y.shift(-n_in)
        y_lag = y_lag.shift(n_out)

        # put it all together
        X_lag = pd.concat(cols, axis=1)
        X_lag.columns = names

        # Remove t+0, t+1 ... t+n da variável y_name
        for i in range(n_out + 1):
            X_lag.drop(columns=['{var:}_(t{lag:+d})'.format(var=y_name, lag=i)], inplace=True)

        # drop rows with NaN values
        if dropnan:
            X_lag.dropna(inplace=True)
            y_lag.dropna(inplace=True)

        return X_lag, y_lag


    def transform_predict(self, X, n_in=1, n_out=1, dropnan=True, y_name='val_vaz_natr'):
        X = pd.DataFrame(X)


        cols, names = list(), list()
        # input sequence (t-n_in, ... t-1, t+0, t+1, t+2 ... t+n_out)
        for i in range(n_in, n_out+1, 1):
            cols.append(X.shift(-i))
            names += ['{var:}_(t{lag:+d})'.format(var=var, lag=i) for var in X.columns]

        # Label sequence (t-n_in, ... t-1, t+0, t+1, t+2 ... t+n_out)
        #y_lag = y.shift(-n_in)
        #y_lag = y_lag.shift(n_out)

        # put it all together
        X_lag = pd.concat(cols, axis=1)
        X_lag.columns = names

        # Remove t+0, t+1 ... t+n da variável y_name
        for i in range(n_out + 1):
            X_lag.drop(columns=['{var:}_(t{lag:+d})'.format(var=y_name, lag=i)], inplace=True)

        # drop rows with NaN values
        if dropnan:
            X_lag.dropna(inplace=True)


        return X_lag
