import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
from scipy import signal
path = r'Fig/previsao_posto_1_oneshot.csv'

df = pd.read_csv(
    filepath_or_buffer=path,
    sep=';',
    decimal=',',
)

df['dat_reference'] = pd.to_datetime(df['dat_reference'])
df['dat_previsao'] = pd.to_datetime(df['dat_previsao'])

# Pega previsao aos sabados
datas = pd.date_range(start='2013-08-17', end='2016-12-24', freq='7D')
df = df[df['dat_reference'].isin(datas)]
df['smooth'] = signal.savgol_filter(x=df['val_vaz_prevista'], window_length=7, polyorder=2, deriv=0)

df_semanal = df.copy()
df_semanal = df_semanal.groupby(by=pd.Grouper(freq='W', key='dat_reference')).mean()
df_semanal['dat_previsao'] = df_semanal.index


# Criação da figura

fig = make_subplots(
    rows=4,
    cols=2,
    shared_xaxes=False,
    shared_yaxes=False,
    specs=[
        [{"colspan": 2}, None],
        [{"colspan": 2}, None],
        [{}, {}],
        [{"colspan": 2}, None]
    ],
    subplot_titles=(
        'Comparativo Diário',
        'Comparativo Semanal',
        'Scatter y_true x y_pred',
        'Distribuição dos Resíduos',
        'Análise de Fourier'
    )
)


fig.add_trace(
    row=1,
    col=1,
    trace=go.Scatter(
        x=df['dat_previsao'],
        y=df['val_vaz_prevista'],
        name='previsao',
        legendgroup='previsao',
        mode='lines',
        marker=dict(
            color='blue',
        ),
        connectgaps=True
    )
)

fig.add_trace(
    row=1,
    col=1,
    trace=go.Scatter(
        x=df['dat_previsao'],
        y=df['val_vaz_natr'],
        name='true',
        legendgroup='true',
        mode='lines',
        marker=dict(
            color='green',
        ),
        connectgaps=True
    )
)

fig.add_trace(
    row=1,
    col=1,
    trace=go.Scatter(
        x=df['dat_previsao'],
        y=df['smooth'],
        name='smooth',
        showlegend=True,
        legendgroup='smooth',
        mode='lines',
        marker=dict(
            color='red',
        ),
        connectgaps=True
    )
)


# Grafico semanal
fig.add_trace(
    row=2,
    col=1,
    trace=go.Scatter(
        x=df_semanal['dat_previsao'],
        y=df_semanal['val_vaz_prevista'],
        name='previsao',
        showlegend=False,
        legendgroup='previsao',
        mode='lines',
        marker=dict(
            color='blue',
        ),
        connectgaps=True
    )
)

fig.add_trace(
    row=2,
    col=1,
    trace=go.Scatter(
        x=df_semanal['dat_previsao'],
        y=df_semanal['val_vaz_natr'],
        name='true',
        showlegend=False,
        legendgroup='true',
        mode='lines',
        marker=dict(
            color='green',
        ),
        connectgaps=True
    )
)

fig.add_trace(
    row=2,
    col=1,
    trace=go.Scatter(
        x=df_semanal['dat_previsao'],
        y=df_semanal['smooth'],
        name='smooth',
        showlegend=False,
        legendgroup='smooth',
        mode='lines',
        marker=dict(
            color='red',
        ),
        connectgaps=True
    )
)





fig.add_trace(
    row=3,
    col=1,
    trace=go.Scatter(
        #x=np.log1p(df['smooth']),
        #y=np.log1p(df['val_vaz_natr']),
        x=df['smooth'],
        y=df['val_vaz_natr'],
        mode='markers',
        showlegend=False,
        marker=dict(
            color='red',
        ),
        connectgaps=False

    )
)

fig.add_trace(
    row=3,
    col=1,
    trace=go.Scatter(
        #x=np.log1p([i for i in range(20, 450)]),
        #y=np.log1p([i for i in range(20, 450)]),
        x=[i for i in range(20, 450)],
        y=[i for i in range(20, 450)],
        line=dict(dash='dot', width=3),
        mode='lines',
        marker=dict(
            color='black',

        ),
        showlegend=False,
        connectgaps=True
    )
)

fig.add_trace(
    row=3,
    col=2,
    trace=go.Histogram(
        x=df['smooth'] - df['val_vaz_natr'],
        histnorm='probability',
        showlegend=False,
        name='Distribuição Resíduos'
    )
)

f, Pxx_den = signal.periodogram(x=2*np.sqrt(2) * df['val_vaz_natr'], fs=86400,)
fig.add_trace(
    row=4,
    col=1,
    trace=go.Scatter(
        x=f[0:50],
        y=Pxx_den[0:50],
        name='Vazao Natural',
        showlegend=False,
        line=dict(dash='solid', width=3),
        mode='lines',
        marker=dict(
            color='red',

        ),

    ),
)

mape = np.mean(np.abs(df['val_vaz_natr'] - df['smooth']) / df['val_vaz_natr'])
mae = np.mean(np.abs(df['val_vaz_natr'] - df['smooth']))

mape_semanal = np.mean(np.abs(df_semanal['val_vaz_natr'] - df_semanal['smooth']) / df_semanal['val_vaz_natr'])
mae_semanal = np.mean(np.abs(df_semanal['val_vaz_natr'] - df_semanal['smooth']))

fig.update_layout(
    dict1=dict(
        autosize=False,
        height=1396,
        width=1280,
        annotations=[],
        title=go.layout.Title(
            text='MAPE Diário: {:.2%} - MAE Diário: {:.0f} m³/s<Br>MAPE Semanal: {:.2%} - MAE Semanal: {:.0f} m³/s'.format(
                mape,
                mae,
                mape_semanal,
                mae_semanal
            ),

            x=0.10,
            y=0.95
        ),
        legend=go.layout.Legend(
            orientation='h',
            x=0.70,
            y=1.05,
        ),
    ),
)




fig.update_xaxes(patch=dict(title_text='Tempo'), row=1, col=1)
fig.update_xaxes(patch=dict(title_text='Y pred smooth'), row=3, col=1)

fig.update_yaxes(patch=dict(title_text='Vazao'), row=1, col=1)
fig.update_yaxes(patch=dict(title_text='Y true'), row=3, col=1)

pio.write_html(fig=fig, file=r'Fig/Comparativo_resultados.html', )

pass