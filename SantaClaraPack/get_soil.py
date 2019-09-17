import requests
import os
import netCDF4
import numpy as np
import pandas as pd
from SantaClaraPack.Config.Config import Config
from SantaClaraPack.Banco.Dados import Dados


config = Config().config
df = pd.DataFrame()

soil_path = "soilw.mon.mean.v2.nc"

raw_data = netCDF4.MFDataset(soil_path)

lats = raw_data.variables['lat'][:]
lons = raw_data.variables['lon'][:]
soils = raw_data.variables['soilw'][:]
temps = raw_data.variables["time"][:]

temps = netCDF4.num2date(
    times=raw_data.variables[config['soil']['variables_name']['tempo']][:],
    units=raw_data.variables['time'].units
)

# Recorta os dados para o subset estipulado
lat_inds = np.where(
    (lats >= config['soil']['sub_set']['lat']['ini']) &
    (lats <= config['soil']['sub_set']['lat']['fim'])
)

lon_inds = np.where(
    (lons >= config['soil']['sub_set']['lon']['ini']) &
    (lons <= config['soil']['sub_set']['lon']['fim'])
)

latf=[]
lonf=[]

lats = raw_data.variables['lat'][lat_inds]
lons = raw_data.variables['lon'][lon_inds]
soils = raw_data.variables['soilw'][:, lat_inds[0], lon_inds[0]]

for i, tempo in enumerate(temps):

    for j, lat in enumerate(lats):
        aux = dict(
            dat_medicao=[tempo] * len(lons),
            val_lat=[lat] * len(lons),
            val_lon=lons[:],
            val_soil=soils[i, j, :]
        )
        aux = pd.DataFrame.from_dict(data=aux, orient='columns')
        df = pd.DataFrame(pd.concat(objs=[df, aux]))


# Insere no banco de dados
dados = Dados()
dados.insert_solo(df=df)

print(df)