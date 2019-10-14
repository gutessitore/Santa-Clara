import pandas as pd
import numpy as np
import optuna
from SantaClaraPack.Models.PreProcessors import *
from SantaClaraPack.Banco.Dados import Dados
from SantaClaraPack.Models.Optimizer import Optimizer


if __name__ == '__main__':
    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 100)


    dao = Dados()
    df_vazao = dao.get_vazao(posto=1, classe='Vazao', data_inicial='2000-01-01', data_final='2016-12-31')
    df_vazao = pd.DataFrame(df_vazao.iloc[:, 1:4])
    df_vazao.set_index(keys=['dat_medicao'], inplace=True)

    df_chuva = dao.get_gridded_data(
        classe='Chuva',
        data_inicial='2000-01-01',
        data_final='2016-12-31',
        lat_inicial=-22.4,
        lat_final=-21.2,
        lon_inicial=-44.6,
        lon_final=-44.2,
    )

    pre = PreProcessors()
    gridded = GriddedDataProcessor()

    df_chuva_transform = gridded.transform(
        df=df_chuva,
        index='dat_medicao',
        cols=['val_lat', 'val_lon'],
        value='val_precip',
        var_name='chuva',
        agg='sum',
    )

    # Formando X e y
    X = pd.concat(objs=[df_vazao[['val_vaz_natr']], df_chuva_transform], sort=True, axis=1)
    y = df_vazao[['val_vaz_natr']]

    # Normalização dos dados

    # Separação nos arquivos de treino e teste
    '''Separação sequencial por ser um time series'''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=None, shuffle=False)

    # Avaliacao do modelo modelo com hyper-tunning
    optimize = Optimizer()
    optimize.get_data(X=X_train, y=y_train, X_test=X_test, y_test=y_test)
    study = optuna.create_study(
        storage='sqlite:///Models/example.db',
        direction='maximize',
        study_name='test',
        load_if_exists=True
    )
    study.optimize(optimize, n_trials=10)


    print(study.best_trial)
    print(study.best_params)
    df = study.trials_dataframe()
    print(study.trials_dataframe())
    print('d')