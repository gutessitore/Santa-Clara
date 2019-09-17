import pandas as pd
import numpy as np
import glob
import os
import netCDF4
import datetime

from SantaClaraPack.Config.Config import Config
from SantaClaraPack.Banco.Dados import Dados


config = Config().config
paths = glob.glob('../Data/temperature/*.nc')

batches = [[i, i+100] for i in np.arange(0, 3650, 100)]

for batch in batches:
    df_final = pd.DataFrame()
    dfs = list()
    print(batch)

    # Itera sobre os todos os arquivos:
    for arqv in paths:
        df_aux = pd.DataFrame()
        file = netCDF4.Dataset(filename=arqv)
        var_name = os.path.basename(arqv)[9:13].lower()
        #print(os.path.basename(arqv))

        if var_name == 'tavg':
            var_name = 'val_temp_med'

        elif var_name == 'tmin':
            var_name = 'val_temp_min'

        elif var_name == 'tmax':
            var_name = 'val_temp_max'

        lats = file.variables[config['temperature']['variable_names']['lat']][:]
        lons = file.variables[config['temperature']['variable_names']['lon']][:]
        days = file.variables[config['temperature']['variable_names']['day']][:]
        months = file.variables[config['temperature']['variable_names']['month']][:]
        years = file.variables[config['temperature']['variable_names']['year']][:]
        days_of_year = file.variables[config['temperature']['variable_names']['day_of_year']][:]

        datas = [datetime.datetime(year=int(years[i]), month=int(months[i]), day=int(days[i])) for i in range(days.size)]

        # Recorta os dados para o subset estipulado
        lat_inds = np.where(
            (lats >= config['temperature']['sub_set']['lat']['ini']) &
            (lats <= config['temperature']['sub_set']['lat']['fim'])
        )

        lon_inds = np.where(
            (lons >= config['temperature']['sub_set']['lon']['ini']) &
            (lons <= config['temperature']['sub_set']['lon']['fim'])
        )

        lats = file.variables[config['temperature']['variable_names']['lat']][lat_inds]
        lons = file.variables[config['temperature']['variable_names']['lon']][lon_inds]
        temperatures = file.variables[config['temperature']['variable_names']['temp']][:, lat_inds[0], lon_inds[0]]
        climatologias = file.variables[config['temperature']['variable_names']['clima']][:, lat_inds[0], lon_inds[0]]

        # Itera para formar dataframe
        for i, tempo in enumerate(datas[batch[0]:batch[1]]):

            for j, lat in enumerate(lats):
                aux = {
                    'dat_medicao': [tempo] * len(lons),
                    'val_lat': [lat] * len(lons),
                    'val_lon': lons[:],
                    '{:}'.format(var_name): temperatures[i, j, :] + climatologias[int(days_of_year[i]) - 1, j, :],

                }
                aux = pd.DataFrame.from_dict(data=aux, orient='columns')
                df_aux = pd.DataFrame(pd.concat(objs=[df_aux, aux]))


        dfs.append(df_aux)
        del temperatures, climatologias, lats, lons, days, months, years, days_of_year



    df_final = pd.DataFrame(pd.concat(objs=[dfs[0], dfs[1]]))
    df_max = pd.DataFrame(pd.concat(objs=[dfs[2], dfs[3]]))
    df_min = pd.DataFrame(pd.concat(objs=[dfs[4], dfs[5]]))

    df_final['val_temp_min'] = df_min['val_temp_min']
    df_final['val_temp_max'] = df_max['val_temp_max']
    df_final.dropna(inplace=True)

    #print('Criacao dos registros')

