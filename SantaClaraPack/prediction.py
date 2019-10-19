from datetime import datetime
import optuna
from joblib import dump, load
from sklearn.metrics import mean_absolute_error, median_absolute_error, r2_score
from SantaClaraPack.Models.PreProcessors import *
from SantaClaraPack.Banco.Dados import Dados
from SantaClaraPack.Optimizer.Optimizer import Optimizer
from SantaClaraPack.Plot.Plot import Plot

if __name__ == '__main__':
    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 100)

    # Avaliacao do modelo modelo com hyper-tunning
    dao = Dados()
    optimize = Optimizer()
    pre = PreProcessors()
    gridded = GriddedDataProcessor()
    window = WindowProcessor()

    study = optuna.create_study(
        storage='sqlite:///Optimizer/optimize_tests.db',
        direction='maximize',
        study_name='optimize',
        load_if_exists=True
    )

    # Load do modelo
    model = load(filename=r'Models/mlp_posto_1.joblib')

    df_resultados = pd.DataFrame()
    df_vaz_true = dao.get_vazao(
        data_inicial='2013-01-01',
        data_final='2017-12-30'
    )

    df_vaz_true.drop(columns=['id', 'num_posto'], inplace=True)
    df_vaz_true['dat_medicao'] = pd.to_datetime(df_vaz_true['dat_medicao'])
    df_vaz_true.set_index(keys=['dat_medicao'], inplace=True)

    df_chuva_true = dao.get_gridded_data(
        classe='Chuva',
        data_inicial='2013-01-01',
        data_final='2017-12-30',
        lat_inicial=-22.4,
        lat_final=-21.2,
        lon_inicial=-44.6,
        lon_final=-44.2,
    )

    df_chuva_true['dat_medicao'] = pd.to_datetime(df_chuva_true['dat_medicao'])
    df_chuva_true = gridded.transform(
        df=df_chuva_true,
        index='dat_medicao',
        cols=['val_lat', 'val_lon'],
        value='val_precip',
        var_name='chuva',
        agg='sum',
    )

    #for data in pd.date_range(start='2013-08-17', end='2017-12-30', freq='7D'):
    for data in pd.date_range(start='2013-08-17', end='2017-12-01', freq='7D'):

        data_inicial = datetime.strftime(
            data + pd.to_timedelta(arg=study.best_params['window_neg'], unit='D'),
            '%Y-%m-%d'
        )

        data_final_vazao = data + pd.to_timedelta(arg=study.best_params['window_neg'], unit='D') + \
                           pd.to_timedelta(arg=-study.best_params['window_neg'], unit='D')

        data_final = datetime.strftime(
            data + pd.to_timedelta(arg=10, unit='D'),
            '%Y-%m-%d'
        )

        df_vazao = df_vaz_true.loc[data_inicial:data_final_vazao]

        df_chuva_transform = df_chuva_true.loc[data_inicial:data_final]

        # Formando X e y
        X = pd.concat(objs=[df_vazao[['val_vaz_natr']], df_chuva_transform], sort=True, axis=1)

        i = 1
        # Gera previsões para t+1 a t+7 para cada data do loop anterior
        for data_previsao in pd.date_range(start=data, freq='1D', periods=10):

            X_test_lag = window.transform_predict(
                X=X,
                n_in=study.best_params['window_neg'],
                n_out=0
            )

            X_test_lag = pd.DataFrame(data=[X_test_lag.loc[data_previsao]], columns=X_test_lag.loc[data_previsao].index)
            y_hat = model.predict(X=X_test_lag)


            # Atualiza na base de dados
            X.loc[data_previsao, 'val_vaz_natr'] = y_hat

            # Atualiza log de resultados
            aux = pd.DataFrame(
                data=dict(
                    dat_reference=data,
                    dat_previsao=data_previsao,
                    num_termo=i,
                    val_vaz_pred=y_hat,
                    val_vaz_true=df_vaz_true.loc[data_previsao, 'val_vaz_natr']
                )
            )

            df_resultados = pd.concat(objs=[df_resultados, aux], ignore_index=True)
            i += 1

        # Scores
        #print('MAE test: {:}'.format(mean_absolute_error(y_true=, y_pred=X_test_lag[1:, 'val_vaz_natr'])))
        #print('MedAE test: {:}'.format(median_absolute_error(y_true=y_test_lag, y_pred=y_hat)))
        #print('R2 test: {:}'.format(r2_score(y_true=y_test_lag, y_pred=y_hat)))


    df_resultados.to_csv(path_or_buf=r'Fig/resultados_posto_1.csv', sep=';', decimal=',')

    # plot
    #plot = Plot()
    #plot.plot_prediction_compararison(y_true=y_test_lag['val_vaz_natr'].values, y_pred=y_hat, times=y_test_lag.index)