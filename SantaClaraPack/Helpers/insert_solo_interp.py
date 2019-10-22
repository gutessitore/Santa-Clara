from SantaClaraPack.Banco.Dados import Dados
import pandas as pd

dao = Dados()

df = pd.read_csv(
    filepath_or_buffer=r'C:\Users\anderson\PycharmProjects\StaClara\Data/df_soil_interpolado.csv',
    sep=',',
    decimal='.',
    #dtype=[]
)
df['dat_medicao'] = pd.to_datetime(df['dat_medicao'])

dao.insert_solo(df=df)
