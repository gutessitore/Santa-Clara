import pandas as pd

# Ler os dados
path = r'C:\Users\anderson\Desktop\Vazões_Diárias_1931_2017.csv'

df = pd.read_csv(
    filepath_or_buffer=path,
    sep=';',
    decimal=',',
    encoding='latin1'
)

# Pegar range de datas que me interessam - 1998 e 2000
df = df.loc[
    (df['data'] >= '1998-01-01') &
    (df['data'] <= '2000-01-01')
    #df['data'].day == 1
]



df_vazao = pd.DataFrame()

for i, col in enumerate(df.columns):

    if col != 'data':
        num_posto = int(str(col)[str(col).find('(') + 1:str(col).find(')')])

    df_aux = pd.DataFrame(
        data=dict(
            val_vaz_natr=df[col].values,
            num_posto=[num_posto] * len(df[col]),
            dat_medicao=df['data'].values
        )
    )

    df_vazao = pd.concat(objs=[df_vazao, df_aux])


df_vazao.to_csv(
    path_or_buf='tbl_vazao_bd.csv',
    sep=';',
    decimal='.',
    index=False
)