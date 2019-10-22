from scipy.interpolate import griddata
import pandas as pd
import numpy as np
from SantaClaraPack.Banco.Dados import Dados

dao = Dados()

df_chuva = dao.get_gridded_data(
    classe='Chuva',
    data_inicial='2017-09-02',
    data_final='2017-09-02'
)


df_chuva = pd.pivot_table(
    data=df_chuva,
    values='val_precip',
    index='dat_medicao',
    columns=['val_lat', 'val_lon'],
    aggfunc='sum'
)

df_temp = dao.get_gridded_data(
    classe='Temperature',
    data_inicial='1998-01-01',
    data_final='2000-12-31',
    lat_inicial=-90.0,
    lat_final=90.0,
    lon_inicial=-180,
    lon_final=180
)
df_temp = df_temp[['dat_medicao', 'val_lon', 'val_lat', 'val_temp_med']]
df_temp['dat_medicao'] = pd.to_datetime(df_temp['dat_medicao'])
x = df_temp[df_temp['dat_medicao'] == '2000-01-01']

df_temp_med = pd.pivot_table(
    data=df_temp,
    values='val_temp_med',
    index='dat_medicao',
    columns=['val_lat', 'val_lon'],
    aggfunc='sum'
)

print(df_temp_med.shape)
grid_lat, grid_lon = np.meshgrid(df_chuva.columns.levels[0], df_chuva.columns.levels[1])
lat_chuva, lon_chuva = df_chuva.columns.levels[0].size, df_chuva.columns.levels[1].size

df_interpolado = pd.DataFrame()

for date, values in df_temp_med.iterrows():
    points = [[lat, lon] for lat in values.index.levels[0] for lon in values.index.levels[1]]

    interp = griddata(
        points=[[lat, lon] for lat in values.index.levels[0] for lon in values.index.levels[1]],
        values=values,
        xi=(grid_lat, grid_lon),
        method='nearest'
    )

    for i, v in enumerate(interp):
        aux = pd.DataFrame(
            data=dict(
                dat_medicao=[date] * lat_chuva,
                val_lon=[df_chuva.columns.levels[1][i]] * lat_chuva,
                val_lat=df_chuva.columns.levels[0],
                val_temp_med=v
            )
        )

        df_interpolado = pd.concat(objs=[df_interpolado, aux], ignore_index=True)

df_interpolado.to_csv(path_or_buf=r'../Data/df_temp_med_interpolado.csv', sep=',', decimal='.', index=False)

