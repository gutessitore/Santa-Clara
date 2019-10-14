import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor

class Models(object):

    def __init__(self):
        pass

class MultiLayerPerceptron(Models):

    def __init__(self):
        super().__init__()

        self.search_space = {
            'num_layer': [1, 50],
            'hidden_layer_sizes': [50, 400],
            'alpha': [1e-10, 1e2],
            'random_state': [42, 10000],
            #'learning_rate': [1e-5, 1]
        }

        self.pipeline = Pipeline(
            verbose=False,
            steps=[
                ('scale', MinMaxScaler()),
                ('Mlp', MLPRegressor(
                    verbose=False,
                    early_stopping=True,
                    n_iter_no_change=10,
                    learning_rate='constant',
                    max_iter=1000,

                )
                 ),
            ]
        )