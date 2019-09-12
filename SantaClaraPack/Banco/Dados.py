# !/usr/bin/env python
# *- coding: utf-8 -*-
import pandas as pd
from Banco.Banco import *
from Config.Config import Config
from sqlalchemy.orm import Session

class Dados(object):
    def __init__(self):
        self.config = Config().config
        pass

    def insert_chuva(self, df):
        df = pd.DataFrame(df)

        # Remove nulls e nas
        df.replace(to_replace='', value=np.nan, inplace=True)
        df.fillna(value=0.0, inplace=True)

        session = Session(bind=engine)

        dados = list()

        for i, dado in df.iterrows():

            dados.append(
                Chuva(
                    val_lat=dado['val_lat'],
                    val_lon=dado['val_lon'],
                    dat_medicao=dado.dat_medicao.to_pydatetime(),
                    val_precip=dado['val_precip'],
                )
            )

        session.bulk_save_objects(objects=dados)

        try:
            session.commit()

        except:
            input('"Press Enter to continue..."')

        pass

    def query_chuva(self, data_inicial, data_final):

        session = Session(bind=engine)

        session.query(Chuva).filter(Chuva.dat_medicao >= data_inicial).filter(Chuva.dat_medicao <= data_final)
        pass

    def insert_vazao(self, df):
        df = pd.DataFrame(df)
        dados = list()

        session = Session(bind=engine)
        for i, row in df.iterrows():
            dados.append(
                Vazao(
                    num_posto=row['num_posto'],
                    dat_medicao=row['dat_medicao'].to_pydatetime(),
                    val_vaz_natr=row['val_vazao_natr']
                )
            )

        session.bulk_save_objects(objects=dados)
        session.commit()
        session.close()

    def insert_cad_usinas(self, df):
        df = pd.DataFrame(df)

        postos = list()
        for i, dado in df.iterrows():

            postos.append(
                Posto(
                    num_usina=dado['num_usina'],
                    num_posto=dado['num_posto'],
                    nom_usina=dado['nom_usina'],
                    nom_posto=dado['nom_posto'],
                    #num_ordem=dado['num_ordem'],
                    num_jusante=dado['num_jusante'],
                    #val_lat=dado['val_lat'],
                    #val_lon=dado['val_lon'],
                )
            )

        session = Session(bind=engine)

        session.bulk_save_objects(objects=postos)
        session.commit()

    def get_vazao(self, data_inicial='1998-01-02', data_final='2019-08-31', posto=1):
        session = Session(bind=engine)

        stmt = session.query(
            Vazao.num_posto, Vazao.dat_medicao, Vazao.val_vaz_natr).\
            filter(Vazao.dat_medicao >= data_inicial).\
            filter(Vazao.dat_medicao <= data_final).\
            filter(Vazao.num_posto == posto)

        df = pd.read_sql(
            sql=stmt.statement,
            con=session.bind
        )

        return df

    def get_posto(self):

        session = Session(bind=engine)

        stmt = session.query(Posto)

        df = pd.read_sql(
            sql=stmt.statement,
            con=session.bind
        )

        return df