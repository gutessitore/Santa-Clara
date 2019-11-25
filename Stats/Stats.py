import pandas as pd
import statsmodels.tsa.stattools as tsa

class Stats(object):
    def __init__(self):
        pass

    def calc_autocorr(self, df, x, plot=False):

        pass

    def calc_corr(self, df, x, y, plot=False):

        pass

    def check_stacionarity(self, df, feature):

        adfuller = tsa.adfuller(x=df[feature])

        df_adfuller = pd.DataFrame(
            data=adfuller[0:4],
            columns=['value'],
            index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used']
        )


        df_crit_values = pd.DataFrame.from_dict(data=adfuller[4], orient='index')
        df_crit_values.rename(columns={0: 'value'}, inplace=True)
        df_adfuller = pd.concat(objs=[df_adfuller, df_crit_values])


        for i, v in df_crit_values.iterrows():

            if df_adfuller.loc['Test Statistic', 'value'] > v['value']:
                print('Para o valor de {:} - Serie nao estacionaria'.format(i))

            else:
                print('Para o valor de {:} - Serie estacionaria'.format(i))

        return adfuller