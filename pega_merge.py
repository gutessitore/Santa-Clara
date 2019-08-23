#!/usr/bin/env python
import os
import glob2
from datetime import datetime
import pandas as pd
import numpy as np
from Observada.Cptec import Merge
from Handler.Handler import Handler
from Config.Config import Config

if __name__ == '__main__':

    #  Verifica pasta export para pegar último arquivo
    config = Config().config
    files = glob2.glob(pathname=os.path.join(config['paths']['merge']['export'], '*.ctl'))
    '''
    if len(files) == 0:  # usa como ponto de referencia a data passada no config

        datas = dict(
            data_inicial=config['merge']['data_inicial'],
            data_final='{:%Y-%m-%d}'.format(datetime.now())
        )
        print(
            'Dados serão puxados a partir de {data_inicial:} até {data_final:}'.format(
                data_inicial=datas['data_inicial'],
                data_final=datas['data_final']
            )
        )

    else:

        ultima = max([datetime.strptime(x[-12:-4], '%Y%m%d') for x in files])
        datas = dict(
            data_inicial='{:%Y-%m-%d}'.format(ultima),
            data_final='{:%Y-%m-%d}'.format(datetime.now())
        )

        print(
            'Dados serão puxados a partir de {data_inicial:} até {data_final:}'.format(
                data_inicial=datas['data_inicial'],
                data_final=datas['data_final']
            )
        )
    
    # Faz lista com datas a serem pegadas
    datas = pd.date_range(start=datas['data_inicial'], end=datas['data_final'])

    # Pega arquivos com pool - multiprocessado
    handler = Handler()
    handler.execute_pool(function=Merge().get_file, values=datas)
    '''

    files = glob2.glob(
        pathname=os.path.join(config['paths']['merge']['export'], '*.nc')
    )

    merge = Merge()
    merge.get_data(paths=files, chunk=1)
