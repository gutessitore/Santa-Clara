#!/usr/bin/env python
import requests
import os
import netCDF4
import numpy as np
import pandas as pd
from Config.Config import Config
from Banco.Dados import Dados

class Merge(object):
    # '20170901' <- fazer algo

    def __init__(self):
        config = Config()
        self.config = config.config
        pass

    def get_file(self, data):
        print(data)
        # Manuseio do arquivo .bin do merge
        r = requests.get(
            url=self.config['paths']['merge']['bin'].format(data=data)
        )  # pega dados do arquivo .bin

        arquivo_bin = open(
            os.path.join(self.config['paths']['merge']['export'], 'prec_{data:%Y%m%d}.bin'.format(data=data)),
            'wb'
        )

        arquivo_bin.write(r.content)
        arquivo_bin.close()


        # Manuseio do arquivo .ctl do merge
        r = requests.get(url=self.config['paths']['merge']['ctl'].format(data=data))

        arquivo_ctl = open(
            os.path.join(self.config['paths']['merge']['export'], 'prec_{data:%Y%m%d}.ctl'.format(data=data)),
            'wb'
        )
        arquivo_ctl.write(r.content)
        arquivo_ctl.close()

        pass

    def convert_file(self, path):
        pass

    def get_data(self, paths: list, chunk=5):

        pedacos = [paths[i:i + chunk] for i in range(0, len(paths), chunk)]

        for n, pedaco in enumerate(pedacos):
            df = pd.DataFrame()
            print('Pedaco {:} de {:} -> {:}'.format(n + 1, len(pedacos) + 1, pedaco))

            # leitura dos dados
            raw_data = netCDF4.MFDataset(pedaco)
            lons = raw_data.variables[self.config['merge']['variables_name']['lon']][:]
            lats = raw_data.variables[self.config['merge']['variables_name']['lat']][:]
            try:
                precip = raw_data.variables[self.config['merge']['variables_name']['chuva']][:]
            except:
                print(pedaco)
                print(raw_data.variables)

            temps = netCDF4.num2date(
                times=raw_data.variables[self.config['merge']['variables_name']['tempo']][:],
                units=raw_data.variables['time'].units
            )

            # Recorta os dados para o subset estipulado
            lat_inds = np.where(
                (lats >= self.config['merge']['sub_set']['lat']['ini']) &
                (lats <= self.config['merge']['sub_set']['lat']['fim'])
            )

            lon_inds = np.where(
                (lons >= self.config['merge']['sub_set']['lon']['ini']) &
                (lons <= self.config['merge']['sub_set']['lon']['fim'])
            )

            lats = raw_data.variables[self.config['merge']['variables_name']['lat']][lat_inds[0]]
            lons = raw_data.variables[self.config['merge']['variables_name']['lon']][lon_inds[0]]
            precip = raw_data.variables[self.config['merge']['variables_name']['chuva']][:, lat_inds[0], lon_inds[0]]

            for i, tempo in enumerate(temps):

                for j, lat in enumerate(lats):

                    aux = dict(
                        dat_medicao=[tempo] * len(lons),
                        val_lat=[lat] * len(lons),
                        val_lon=lons[:],
                        val_precip=precip[i, j, :]
                    )

                    aux = pd.DataFrame.from_dict(data=aux, orient='columns')
                    df = pd.DataFrame(pd.concat(objs=[df, aux]))


            # Insere no banco de dados
            dados = Dados()
            dados.insert_chuva(df=df)
            #df.to_csv('chuva_{:}_de_{:}.csv'.format(n + 1, len(pedacos) + 1), index=False, sep=';', decimal=',')

        return None

