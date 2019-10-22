import pandas as pd
from Banco.Dados import Dados
from Config.Config import Config

dados = Dados()
df_vazao = dados.get_vazao(
    data_inicial='2017-01-01',
    data_final='2017-01-31',
    posto=1
)

config = Config()


print(df_vazao)