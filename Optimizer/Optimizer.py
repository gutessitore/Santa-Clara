import numpy as np
import sklearn
import optuna
import tensorflow as tf
import time
from datetime import datetime
from joblib import load
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit, train_test_split
from sklearn.utils import parallel_backend
from sklearn.metrics import mean_absolute_error, r2_score

from SantaClaraPack.Models.Models import *
from SantaClaraPack.Models.PreProcessors import WindowProcessor

class Optimizer(object):
    def __init__(self):
        pass


    def get_data(self, X, y, X_test, y_test, y_scaler, n_outs=7):
        self.X = X
        self.y = y
        self.X_test = X_test
        self.y_test = y_test
        self.n_outs = n_outs
        self.y_scaler = y_scaler


    def create_best_model(self, params):

        window = WindowProcessor()
        X_lag, y_lag = window.transform(
            X=self.X,
            y=self.y,
            n_in=params['window_neg'],
            n_out=7
        )

        if params['classifier'] == 'MultiLayerPerceptron':
            param_grid = {
                'Mlp__hidden_layer_sizes': [tuple([params['layer_{:}'.format(i)] for i in range(params['n_layers'])])],
                'Mlp__alpha': [params['alpha']],
                'Mlp__random_state': [params['random_state']],
                'Mlp__learning_rate_init': [params['learning_rate']]
            }

        else:
            pass

        grid = GridSearchCV(
            estimator=globals()[params['classifier']]().pipeline,
            scoring='neg_mean_absolute_error',
            param_grid=param_grid,
            n_jobs=-1,
            verbose=1,
            return_train_score=True,
            cv=TimeSeriesSplit(n_splits=5),
            refit='neg_mean_absolute_error'
        )

        with parallel_backend('threading'):
            grid.fit(X=X_lag.values, y=y_lag)

        print(grid.best_score_)
        return grid


    def load_model(self, path):
        model = load(
            filename=path
        )
        return model


    def __call__(self, trial):

        models = [classe.__name__ for classe in Models.__subclasses__()]

        classifier_name = trial.suggest_categorical('classifier', models)
        #n_in = trial.suggest_int('window_neg', -90, -1)
        n_in = trial.suggest_int('window_neg', -7, -7)

        window = WindowProcessor()
        X_lag, y_lag = window.transform(
            X=self.X,
            y=self.y,
            n_in=n_in,
            n_out=self.n_outs
        )

        '''Separação sequencial por ser um time series'''
        X_lag, X_test_lag, y_lag, y_test_lag = train_test_split(
            X_lag,
            y_lag,
            test_size=0.20,
            stratify=None,
            shuffle=False
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

            learning_rate_init = trial.suggest_loguniform(
                'learning_rate',
                regressor.search_space['learning_rate_init'][0],
                regressor.search_space['learning_rate_init'][1]
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
                'Mlp__learning_rate_init': [learning_rate_init]
            }
        print('Window Neg: {:}'.format(n_in))
        print('Window Forecast: {:}'.format(self.n_outs))

        [print(k, v) for k, v in param_grid.items()]
        with parallel_backend('threading'):

            grid = GridSearchCV(
                verbose=1,
                scoring='neg_mean_absolute_error',
                estimator=regressor.pipeline,
                param_grid=param_grid,
                cv=TimeSeriesSplit(n_splits=5),
                n_jobs=-1,
                refit='neg_mean_absolute_error'
            )

            grid.fit(X=X_lag, y=y_lag)

        y_hat_test = grid.predict(X_test_lag)
        y_hat_test = self.y_scaler.inverse_transform(y_hat_test)
        y_test_lag = self.y_scaler.inverse_transform(y_test_lag)

        print('Score cross-val: {:}'.format(grid.best_score_))
        print('Score Test - MAE: {:}'.format(mean_absolute_error(y_true=y_test_lag, y_pred=y_hat_test)))
        print('R2 test: {:}'.format(r2_score(y_true=y_test_lag, y_pred=y_hat_test, multioutput='uniform_average')))
        print('-'*100)
        print('\n')
        return mean_absolute_error(y_true=y_test_lag, y_pred=y_hat_test)




class OptimizerTf(object):
    def __init__(self):
        pass


    def get_data(self, X, y, X_test, y_test, y_scaler, n_outs=7):
        self.X = X
        self.y = y
        self.X_test = X_test
        self.y_test = y_test
        self.n_outs = n_outs
        self.y_scaler = y_scaler


    def create_best_model(self, params, X, y):
        strategy = tf.distribute.MirroredStrategy()
        window = WindowProcessor()
        X_lag, y_lag = window.transform(
            X=X,
            y=y,
            n_in=params['window_neg'],
            n_out=self.n_outs
        )

        # Inicialização do modelo
        with strategy.scope():
            model = tf.keras.models.Sequential()
            model.add(tf.keras.layers.Dense(name='l_input', units=X_lag.shape[1], input_shape=[len(X_lag.keys())]))

            # Determinando quantidade de neuronios nas hidden layers
            for layer in range(params['n_layers']):
                model.add(
                    tf.keras.layers.Dense(
                        name='l_{:}'.format(layer),
                        units=params['layer_{:}'.format(layer)],
                        activation=tf.nn.relu,
                        kernel_regularizer=tf.keras.regularizers.l2(params['l_2'])
                    )
                )
                model.add(tf.keras.layers.Dropout(params['dropout']))

            # Camada de saída dos dados
            model.add(tf.keras.layers.Dense(units=self.n_outs, activation=tf.keras.activations.linear))

            # tensorboard
            tensorboard = tf.keras.callbacks.TensorBoard(
                log_dir=r'C:\Users\anderson\PycharmProjects\StaClara\SantaClaraPack\logs\best_{:%Y-%m-%d_%H_%M_%S}'.format(
                    datetime.now()
                ),
                #histogram_freq=1
            )

            model.compile(
                optimizer=tf.keras.optimizers.Adadelta(),
                loss=tf.keras.losses.mean_absolute_percentage_error,
                metrics=['mse', 'mae', 'mape']
            )
            #print(model.summary())

            history = model.fit(
                X_lag.values,
                y_lag.values,
                epochs=int(1e5),
                validation_split=0.1,
                verbose=0,
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(
                        monitor='val_mape',
                        verbose=True,
                        patience=int(50),
                        min_delta=2e-3
                    ),

                    tf.keras.callbacks.TensorBoard(
                        log_dir=r'C:\Users\anderson\PycharmProjects\StaClara\SantaClaraPack\logs\F_{:%Y-%m-%d_%H_%M_%S}'.format(
                            datetime.now()
                        ),
                        #histogram_freq=1
                        write_images=True
                    )
                ]
            )

            # Avaliacao no X_test
            #loss, mse, mae, mape = model.evaluate(X_test_lag.values, y_test_lag.values, verbose=1)
            #print(loss, mse, mae)

            print('*'*100)
            model.save(r'Optimizer/model_tf.h5')

        return model


    def load_model(self, path):
        model = load(
            filename=path
        )
        return model


    def __call__(self, trial):

        models = [classe.__name__ for classe in Models.__subclasses__()]
        strategy = tf.distribute.MirroredStrategy()

        classifier_name = trial.suggest_categorical('classifier', models)
        n_in = trial.suggest_int('window_neg', -90, -1)
        #n_in = trial.suggest_int('window_neg', -7, -7)

        window = WindowProcessor()
        X_lag, y_lag = window.transform(
            X=self.X,
            y=self.y,
            n_in=n_in,
            n_out=self.n_outs
        )

        '''Separação sequencial por ser um time series'''
        X_lag, X_test_lag, y_lag, y_test_lag = train_test_split(
            X_lag,
            y_lag,
            test_size=0.20,
            stratify=None,
            shuffle=False
        )

        # Determinando Numero de camadas
        n_layers = trial.suggest_int(name='n_layers', low=2, high=15)

        # Determinando penalidade L2 - alpha
        l_2 = trial.suggest_loguniform(
            name='l_2',
            low=5e-4,
            high=5e-1
        )

        #learning_rate = trial.suggest_loguniform(
        #    name='learning_rate',
        #    low=5e-4,
        #    high=5e-1
        #)

        dropout = trial.suggest_loguniform(
            name='dropout',
            low=0.05,
            high=0.50
        )

        layers = list()
        # Inicialização do modelo
        with strategy.scope():
            model = tf.keras.models.Sequential()
            model.add(tf.keras.layers.Dense(name='l_input', units=X_lag.shape[1], input_shape=[len(X_lag.keys())]))

            # Determinando quantidade de neuronios nas hidden layers
            for layer in range(n_layers):
                neurons = trial.suggest_int(name='layer_{:}'.format(layer), low=16, high=128)
                model.add(
                    tf.keras.layers.Dense(
                        name='l_{:}'.format(layer),
                        units=neurons,
                        activation=tf.keras.activations.relu,
                        kernel_regularizer=tf.keras.regularizers.l2(l_2)
                    )
                )
                layers.append(neurons)

                model.add(tf.keras.layers.Dropout(dropout))


            # Camada de saída dos dados
            model.add(tf.keras.layers.Dense(units=self.n_outs, activation=tf.keras.activations.linear))
            model.compile(
                optimizer=tf.keras.optimizers.Adadelta(),
                loss=tf.keras.losses.mean_absolute_percentage_error,
                metrics=['mse', 'mae', 'mape']
            )

            print('''
            n_layers: {:}
            neurons: {:}
            l_2: {:}
            dropout: {:}
                '''.format(n_layers, layers, l_2, dropout)
            )


            history = model.fit(
                X_lag.values,
                y_lag.values,
                epochs=int(1e5),
                validation_split=0.1,
                verbose=0,
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(
                        monitor='val_mape',
                        verbose=True,
                        patience=int(50),
                        min_delta=2e-3
                    ),
                    tf.keras.callbacks.TensorBoard(
                        log_dir=r'C:\Users\anderson\PycharmProjects\StaClara\SantaClaraPack\logs\t_{:%Y-%m-%d_%H_%M_%S}'.format(
                            datetime.now()
                        ),
                        #histogram_freq=1
                        write_images=True
                    )
                ]
            )

            # Avaliacao no X_test
            loss, mse, mae, mape = model.evaluate(X_test_lag.values, y_test_lag.values, verbose=1)
            #print(loss, mse, mae)

            print('*'*100)

        return loss
