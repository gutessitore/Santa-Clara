import pandas as pd
import numpy as np
from scipy.interpolate import griddata

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

df_solo = dao.get_gridded_data(
    classe='Solo',
    data_inicial='1998-01-01',
    data_final='2019-12-31',
    lat_inicial=-90.0,
    lat_final=90.0,
    lon_inicial=0,
    lon_final=360
)
df_solo['val_lon'] = df_solo['val_lon'] - 180.0

df_solo = pd.pivot_table(
    data=df_solo,
    values='val_soil',
    index='dat_medicao',
    columns=['val_lat', 'val_lon'],
    aggfunc='sum'
)

grid_lat, grid_lon = np.meshgrid(df_chuva.columns.levels[0], df_chuva.columns.levels[1])
lat_chuva, lon_chuva = df_chuva.columns.levels[0].size, df_chuva.columns.levels[1].size

df_interpolado = pd.DataFrame()
for date, values in df_solo.iterrows():
    print(date)
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
                val_soil=v
            )
        )

        df_interpolado = pd.concat(objs=[df_interpolado, aux], ignore_index=True)

df_interpolado.to_csv(path_or_buf=r'../Data/df_soil_interpolado.csv', sep=',', decimal='.', index=False)

