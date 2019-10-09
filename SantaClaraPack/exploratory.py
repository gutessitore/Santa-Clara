import pandas as pd
from SantaClaraPack.Banco.Dados import Dados
from SantaClaraPack.Stats.Stats import Stats
from SantaClaraPack.Plot.Plot import Plot

# Leitura dos dados
dao = Dados()
plot = Plot()


df_vazao = dao.get_vazao(data_inicial='1998-01-01', data_final='2018-12-31', posto=6, classe='Vazao')
df_vazao['dat_medicao'] = pd.to_datetime(df_vazao['dat_medicao'])
df_vazao.set_index(keys=['dat_medicao'], inplace=True)

df_vazao_mensal = df_vazao.resample(rule='M').mean()
df_vazao_mensal['mes'] = df_vazao_mensal.index.month

stats = Stats()
adfuller = stats.check_stacionarity(df=df_vazao, feature='val_vaz_natr')

# plot
plot.plot_time_series(df=df_vazao, x='index', y='val_vaz_natr')
plot.plot_time_series(df=df_vazao_mensal, x='index', y='val_vaz_natr')

# Plot Distribuition
plot.plot_distribuition(df=df_vazao_mensal, x='mes', y='val_vaz_natr')

#
plot.plot_autocorr(df=df_vazao_mensal, x='val_vaz_natr', lags=60, mode='autocorr')
plot.plot_autocorr(df=df_vazao_mensal, x='val_vaz_natr', lags=60, mode='pcorr')
