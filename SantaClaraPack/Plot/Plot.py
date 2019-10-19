import plotly.graph_objects as go
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as stats

import pandas as pd
import numpy as np
import plotly.express as px

import chart_studio.plotly as chart
import plotly.graph_objects as go
import plotly as py
import plotly.io as pio


class Plot(object):
    def __init__(self):
        pass

    def plot_time_series(self, df, x='index', y='val_vaz_natr'):

        if x == 'index':
            df.reset_index(inplace=True)
            x = 'dat_medicao'


        fig = px.line(
            data_frame=df,
            x=x,
            y=y,
            line_shape='spline',
            render_mode='svg'
        )
        fig.show()
        pass


    def plot_distribuition(self, df, x, y):

        if x == 'index':
            df.reset_index(inplace=True)
            x = 'dat_medicao'

        fig = px.box(
            data_frame=df,
            x=x,
            y=y,
            points='all',
            notched=True,

        )

        fig.show()

        pass


    def plot_autocorr(self, df, x, lags, mode='autocorr'):
        df = pd.DataFrame(df)
        if mode == 'autocorr':
            coefs, conf_interval = stats.acf(x=df[x], fft=False, nlags=lags, alpha=0.05)

        elif mode == 'pcorr':
            coefs, conf_interval = stats.pacf(x=df[x], nlags=lags, alpha=0.05)


        lower = [conf_interval[i][0] for i, v in enumerate(conf_interval)]
        upper = [conf_interval[i][1] for i, v in enumerate(conf_interval)]

        fig = go.Figure()

        fig.add_trace(

            go.Bar(
                x=[i for i in range(len(coefs))],
                y=coefs,
                width=[0.05 for i in range(coefs.shape[0])],
                marker_color='blue',
                name=mode,

                #showlegend=False,
            )
        )

        fig.add_trace(

            go.Scatter(
                x=[i for i in range(len(coefs))],
                y=coefs,
                mode='markers',
                marker_color='blue',
                showlegend=False
            )
        )

        fig.add_trace(

            go.Scatter(
                x=[i for i in range(len(coefs))],
                y=upper,
                mode='lines',
                fill=None,
                line_color='rgba(0,176,246,0.2)',
                showlegend=False,
                name='upper'
            )
        )

        fig.add_trace(

            go.Scatter(
                x=[i for i in range(len(coefs))],
                y=lower,
                mode='lines',
                fill='tonexty',
                #fillcolor='red',
                line_color='rgba(0,176,246,0.2)',
                fillcolor='rgba(0,176,246,0.2)',
                showlegend=False,
                #stackgroup='one',
                name='lower'
            )
        )



        fig.update_layout(legend_orientation="h")
        pio.write_html(fig=fig, file=r'Fig/{:}.html'.format(mode))
        fig.show()


    def plot_fft(self, df, x='val_vaz_natr'):
        #print(df.head())

        t = df.index
        s = df[x]

        df_fft = np.fft.fft(a=df[x])
        df_psd = np.abs(df_fft) ** 2

        # 1/T = frequency
        f = np.fft.fftfreq(len(df_psd), 1.0 / 30)
        i = f > 0

        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        ax.plot(fftfreq[i], 10 * np.log10(temp_psd[i]))
        ax.set_xlim(0, 5)
        ax.set_xlabel('Frequency (1/year)')
        ax.set_ylabel('PSD (dB)')
        pass


    def plot_prediction_compararison(self, y_pred, y_true, times, auto_open=False):

        trace_pred = go.Scatter(
            x=times,
            y=y_pred,
            name='Previsão',
            mode='lines',
            line=dict(color='green')

        )

        trace_true = go.Scatter(
            x=times,
            y=y_true,
            fillcolor='green',
            name='Observado',
            mode='lines',
            line=dict(color='red')
        )


        fig = go.Figure(data=[trace_pred, trace_true])
        pio.write_html(fig=fig, file=r'Fig/comparacao_test_mlp.html', auto_open=auto_open)
        pass