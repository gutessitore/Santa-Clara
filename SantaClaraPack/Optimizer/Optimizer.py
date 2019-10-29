from joblib import load

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.utils import parallel_backend
from sklearn.metrics import mean_absolute_error, r2_score

from SantaClaraPack.Models.Models import *
from SantaClaraPack.Models.PreProcessors import WindowProcessor

class Optimizer(object):
    def __init__(self):
        pass


    def get_data(self, X, y, X_test, y_test, n_outs=7):
        self.X = X
        self.y = y
        self.X_test = X_test
        self.y_test = y_test
        self.n_outs = n_outs

    def __call__(self, trial):

        models = [classe.__name__ for classe in Models.__subclasses__()]

        classifier_name = trial.suggest_categorical('classifier', models)
        n_in = trial.suggest_int('window_neg', -20, -1)

        window = WindowProcessor()
        X_lag, y_lag = window.transform(
            X=self.X,
            y=self.y,
            n_in=n_in,
            n_out=self.n_outs
        )

        X_test_lag, y_test_lag = window.transform(
            X=self.X_test,
            y=self.y_test,
            n_in=n_in,
            n_out=self.n_outs
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
        print('Numero Layers: {:}'.format(n_layers))
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

        mape = np.mean(np.abs((y_test_lag - y_hat_test) / y_hat_test))
        print('Score cross-val: {:}'.format(grid.best_score_))
        print('Score Test - MAE: {:.2f}'.format(mean_absolute_error(y_true=y_test_lag, y_pred=y_hat_test)))
        print('Score Test - MAPE: {:.2%}'.format(mape.mean()))
        print('R2 test: {:}'.format(r2_score(y_true=y_test_lag, y_pred=y_hat_test, multioutput='uniform_average')))
        print('-'*100)
        print('\n')
        return mape.mean()


    def create_best_model(self, params):

        window = WindowProcessor()
        X_lag, y_lag = window.transform(
            X=self.X,
            y=self.y,
            n_in=params['window_neg'],
            n_out=self.n_outs
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

