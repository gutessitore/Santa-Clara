import numpy as np
import pandas as pd
class Scores(object):

    def mape(self, y_pred, y_true):

        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

        return mape