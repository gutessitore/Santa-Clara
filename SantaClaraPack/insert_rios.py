import pandas as pd
from SantaClaraPack.Banco.Dados import Dados

df_rios = pd.read_excel(
    io=r'../Data/Bacia_Rio_Grande.xlsx',
)
dao = Dados()

dao.insert_rios(df=df_rios)


