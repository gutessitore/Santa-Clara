import pandas as pd
from Config.Config import Config
from Banco.Dados import Dados

config = Config().config

df = pd.read_csv(
    filepath_or_buffer=config['paths']['vazao']['cad_usinas'],
    sep=';',
    decimal=',',
    encoding='latin1'
)

dados = Dados()
dados.insert_cad_usinas(df=df)
