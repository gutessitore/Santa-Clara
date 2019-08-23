import pandas as pd
from Config.Config import Config
from Banco.Dados import Dados

config = Config().config
raw = pd.read_csv(
    filepath_or_buffer=config['paths']['vazao']['vazao_historica'],
    encoding='latin1',
    sep=';',
    decimal=',',
)

raw['data'] = pd.to_datetime(raw['data'])
df = pd.DataFrame()

for i, col in enumerate(raw.columns):

    if col != 'data':
        aux = pd.DataFrame.from_dict(
            data=dict(
                dat_medicao=raw['data'].values,
                num_posto=[int(col[str(col).find('(') + 1:str(col).find(')')])] * len(raw['data']),
                val_vazao_natr=raw[col].values
            )
        )

        df = pd.concat(objs=[df, aux])

df = pd.DataFrame(df.loc[df['num_posto'].isin([1, 2, 211, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18])])
df = df.loc[df['dat_medicao'] >= '19980102']
df.sort_values(by=['num_posto', 'dat_medicao'], ascending=True, inplace=True)
dados = Dados()
dados.insert_vazao(df=df)
