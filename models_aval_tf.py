import optuna
import warnings
import scipy.signal
from joblib import dump, load
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from SantaClaraPack.Models.PreProcessors import *
from SantaClaraPack.Banco.Dados import Dados
from SantaClaraPack.Optimizer.Optimizer import OptimizerTf
from SantaClaraPack.Features.Features import Features

if __name__ == '__main__':

    warnings.filterwarnings('ignore')
    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 100)

    # Feature Eng
    fe = Features()

    # Numero de dias de previsão
    n_outs = 7

    dao = Dados()
    df_vazao = dao.get_vazao(posto=1, classe='Vazao', data_inicial='2000-01-01', data_final='2016-12-31')
    df_vazao = pd.DataFrame(df_vazao.iloc[:, 1:4])
    df_vazao.drop(columns=['num_posto'], inplace=True)
    df_vazao['dat_medicao'] = pd.to_datetime(df_vazao['dat_medicao'])
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
    X = pd.DataFrame(
        pd.concat(
            objs=[df_vazao[['val_vaz_natr']], df_chuva_transform],
            sort=True,
            axis=1
        )
    )
    y = df_vazao[['val_vaz_natr']]


    # Feature Eng de dados de vazao
    d_vazao, d2_vazao = fe.derivative(data=df_vazao['val_vaz_natr'].values)
    X['d_vazao'] = d_vazao
    X['d2_vazao'] = d2_vazao


    # Normalização dos dados
    x_scaler = MinMaxScaler()
    X_scaled = pd.DataFrame(
        data=x_scaler.fit_transform(X=X),
        columns=X.columns,
        index=X.index
    )
    y_scaler = MinMaxScaler()
    y_scaled = pd.DataFrame(
        data=y_scaler.fit_transform(X=y),
        index=X.index,
        columns=['val_vaz_natr']
    )

    '''Separação sequencial por ser um time series'''
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y_scaled,
        test_size=0.20,
        stratify=None,
        shuffle=False
    )

    # Avaliacao do modelo modelo com hyper-tunning
    optimize = OptimizerTf()

    study = optuna.create_study(
        storage='sqlite:///Optimizer/optimize_tests.db',
        direction='minimize',
        study_name='optimize',
        load_if_exists=True
    )

    optimize.get_data(X=X_scaled, y=y_scaled, X_test=X_scaled, y_test=y_scaled, n_outs=n_outs, y_scaler=y_scaler)
    #study.optimize(optimize, n_trials=20, n_jobs=1)

    window = WindowProcessor()
    X_test_lag, y_test_lag = window.transform(
        X=X_test,
        y=y_test,
        n_in=study.best_params['window_neg'],
        n_out=n_outs
    )

    # Cria e salva melhor configuração
    optimize.n_outs = n_outs
    model = optimize.create_best_model(params=study.best_params, X=X_train, y=y_train)
    print('Criação do modelo com os melhores parametros pesquisados:')

    # Invertendo MinMaxScaler do output y_test_lag e y_hat
    y_hat = model.predict(X_test_lag.values)
    y_hat = y_scaler.inverse_transform(X=y_hat)
    df_y_hat = pd.DataFrame(data=y_hat, index=X_test_lag.index)
    y_test_lag = y_scaler.inverse_transform(X=y_test_lag)

    df_previsao = pd.DataFrame()
    for i, row in df_y_hat.iterrows():
        aux = pd.DataFrame(
                data=dict(
                    dat_reference=[i]*n_outs,
                    dat_previsao=pd.date_range(start=i, freq='D', periods=n_outs),
                    val_vaz_prevista=row.values,
                    num_termo=[i for i in range(1, n_outs + 1)],
                    val_vaz_natr=df_vazao.loc[pd.date_range(start=i, freq='D', periods=n_outs), 'val_vaz_natr']
                )
        )

        df_previsao = pd.concat(objs=[df_previsao, aux])

    df_previsao.to_csv(path_or_buf=r'Fig/previsao_posto_1_oneshot.csv', sep=';', decimal=',', index=False)

    # Scores
    print('MAE test: {:}'.format(mean_absolute_error(y_true=y_test_lag, y_pred=df_y_hat)))
    print('R2 test: {:}'.format(r2_score(y_true=y_test_lag, y_pred=df_y_hat)))