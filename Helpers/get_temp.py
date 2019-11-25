import pandas as pd
import numpy as np
import glob
import os
import netCDF4
import datetime
from SantaClaraPack.Config.Config import Config
from SantaClaraPack.Banco.Dados import Dados
files = ['tavg', 'tmin', 'tmax']
config = Config().config
df_finais = dict()

# Abertura dos arquivos
for c, file in enumerate(files):
    print(file)
    df_variavel = pd.DataFrame()
    arqvs = glob.glob('../Data/temperature/*{:}*.nc'.format(file))

    for arqv in arqvs:
        var_name = os.path.basename(arqv)[9:13].lower()
        df_aux = pd.DataFrame()

        file_nc = netCDF4.Dataset(filename=arqv)

        if var_name == 'tavg':
            var_name = 'val_temp_med'

        elif var_name == 'tmin':
            var_name = 'val_temp_min'

        elif var_name == 'tmax':
            var_name = 'val_temp_max'


        #Le variaveis
        lats = file_nc.variables[config['temperature']['variable_names']['lat']][:]
        lons = file_nc.variables[config['temperature']['variable_names']['lon']][:]
        days = file_nc.variables[config['temperature']['variable_names']['day']][:]
        months = file_nc.variables[config['temperature']['variable_names']['month']][:]
        years = file_nc.variables[config['temperature']['variable_names']['year']][:]
        days_of_year = file_nc.variables[config['temperature']['variable_names']['day_of_year']][:]
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

        lats = file_nc.variables[config['temperature']['variable_names']['lat']][lat_inds]
        lons = file_nc.variables[config['temperature']['variable_names']['lon']][lon_inds]
        temperatures = file_nc.variables[config['temperature']['variable_names']['temp']][:, lat_inds[0], lon_inds[0]]
        climatologias = file_nc.variables[config['temperature']['variable_names']['clima']][:, lat_inds[0], lon_inds[0]]
        t_2 = 1
        # Itera nos dias
        for i, tempo in enumerate(datas):
            if tempo.year != t_2:
                print(tempo.year, var_name)
                t_2 = tempo.year

            for j, lat in enumerate(lats):
                aux = {
                    'dat_medicao': [tempo] * len(lons),
                    'val_lat': [lat] * len(lons),
                    'val_lon': lons[:],
                    '{:}'.format(var_name): temperatures[i, j, :] + climatologias[int(days_of_year[i]) - 1, j, :],
                }

                aux = pd.DataFrame.from_dict(data=aux, orient='columns')
                df_aux = pd.DataFrame(pd.concat(objs=[df_aux, aux]))

        df_variavel = pd.concat(objs=[df_variavel, df_aux])
        df_variavel.dropna(inplace=True)

    # Joga no df final
    if c <= 0:
        df_finais = df_variavel
        print(df_finais.info())

    else:
       df_finais = df_finais.merge(right=df_variavel, on=['dat_medicao', 'val_lat', 'val_lon'])
       print(df_finais.info())


#df_finais.dropna(inplace=True)
# Insercao dos dados no banco - em chunks
n = 5000  # chunk row size
list_df = [df_finais[i:i + n] for i in range(0, df_finais.shape[0], n)]
dados = Dados()
for df in list_df:
    dados.insert_temperature(df=df)
