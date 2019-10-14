import numpy as np
import sklearn
import optuna

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.utils import parallel_backend

from sklearn.metrics import mean_absolute_error, median_absolute_error
from Models.Models import *
from Models.PreProcessors import WindowProcessor

class Optimizer(object):
    def __init__(self):
        pass


    def get_data(self, X, y, X_test, y_test):
        self.X = X
        self.y = y
        self.X_test = X_test
        self.y_test = y_test


    def __call__(self, trial):

        models = [classe.__name__ for classe in Models.__subclasses__()]

        classifier_name = trial.suggest_categorical('classifier', models)

        window = WindowProcessor()
        n_in = trial.suggest_int('window_neg', -50, -1)
        X_lag, y_lag = window.transform(
            X=self.X,
            y=self.y,
            n_in=n_in,
            n_out=0
        )

        X_test_lag, y_test_lag = window.transform(
            X=self.X_test,
            y=self.y_test,
            n_in=n_in,
            n_out=0
        )


        if classifier_name == 'MultiLayerPerceptron':

            regressor = MultiLayerPerceptron()

            layers = list()

            # Determinando Numero de camadas
            n_layers = trial.suggest_int(
                'n_layers',
                regressor.search_space['num_layer'][0],
                regressor.search_space['num_layer'][1]
            )
            # Determinando quantidade de neuronios por camada
            for layer in range(n_layers):
                layers.append(
                    trial.suggest_int(
                        'layer_{:}'.format(layer),
                        regressor.search_space['hidden_layer_sizes'][0],
                        regressor.search_space['hidden_layer_sizes'][1]
                    )
                )

            # Determinando penalidade L2 - alpha
            alpha = trial.suggest_loguniform(
                'alpha',
                regressor.search_space['alpha'][0],
                regressor.search_space['alpha'][1]
            )

            # Determinando random state
            random_state = trial.suggest_int(
                'random_state',
                regressor.search_space['random_state'][0],
                regressor.search_space['random_state'][1]
            )


            param_grid = {
                'Mlp__hidden_layer_sizes': [tuple(layers)],
                'Mlp__alpha': [alpha],
                'Mlp__random_state': [random_state],
            }

        print('-'*100)
        with parallel_backend('threading'):

            grid = GridSearchCV(
                verbose=1,
                scoring=['neg_mean_absolute_error'],
                estimator=regressor.pipeline,
                param_grid=param_grid,
                cv=TimeSeriesSplit(n_splits=5),
                n_jobs=-1,
                refit='neg_mean_absolute_error'
            )

            grid.fit(X=X_lag, y=np.ravel(y_lag))

        y_hat_test = grid.predict(X_test_lag)
        print('Score cross-val: {:}'.format(grid.best_score_))
        print('Score Test - MAE: {:}'.format(mean_absolute_error(y_true=y_test_lag, y_pred=y_hat_test)))
        print('Score Test - MedAE: {:}'.format(median_absolute_error(y_true=y_test_lag, y_pred=y_hat_test)))

        print('-'*100)

        return grid.best_score_
