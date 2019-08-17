#!/usr/bin/env python
import requests
import os
import pandas as pd

path_bin = r'http://ftp.cptec.inpe.br/modelos/io/produtos/MERGE/2019/prec_{:%Y%m%d}.bin'
path_ctl = r'http://ftp.cptec.inpe.br/modelos/io/produtos/MERGE/2019/prec_{:%Y%m%d}.ctl'
path_export = r'C:\Users\anderson\Desktop\merge'

data_inicial = '2019-08-15'
data_final = '2019-08-17'


for data in pd.date_range(start=data_inicial, end=data_final):
    print(data)
    print(
        path_bin.format(data)
    )
    pass
    r = requests.get(url=path_bin.format(data))

    # Arquivo bin
    arquivo_bin = open(os.path.join(path_export, 'prec_{:%Y%m%d}.bin'.format(data)), 'wb')
    arquivo_bin.write(r.content)
    arquivo_bin.close()



    '''
    r = requests.get(url=path_bin)

    # Arquivo bin
    arquivo_bin = open(os.path.join(path_export, 'prec_20190101.bin'), 'wb')
    arquivo_bin.write(r.content)
    arquivo_bin.close()
    
    # Arquivo ctl
    r = requests.get(url=path_ctl)
    arquivo_ctl = open(os.path.join(path_export, 'prec_20190101.ctl'), 'wb')
    arquivo_ctl.write(r.content)
    arquivo_ctl.close()
    '''