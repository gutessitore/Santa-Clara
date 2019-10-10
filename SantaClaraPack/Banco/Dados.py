# !/usr/bin/env python
# *- coding: utf-8 -*-

import pandas as pd
import numpy as np
from Banco.Banco import *
from Config.Config import Config
from sqlalchemy.orm import Session

class Dados(object):

    def __init__(self):
        self.config = Config().config
        pass


    def get_vazao(self, data_inicial='2017-01-01', data_final='2017-01-31', posto=1, classe='Vazao'):
        cla = globals()[classe]

        session = Session(bind=engine)

        stmt = session.query(cla).\
            filter(cla.dat_medicao >= data_inicial).\
            filter(cla.dat_medicao <= data_final). \
            filter(cla.num_posto == posto)


        df = pd.read_sql(
            sql=stmt.statement,
            con=session.bind
        )

        return df


    def query_chuva(self, data_inicial, data_final):

        session = Session(bind=engine)

        session.query(Chuva).filter(Chuva.dat_medicao >= data_inicial).filter(Chuva.dat_medicao <= data_final)
        pass


    def get_gridded_data(
            self,
            classe,
            data_inicial,
            data_final,
            lat_inicial=-22.5,
            lat_final=-17.5,
            lon_inicial=-52.5,
            lon_final=-40.0
    ):
        cla = globals()[classe]
        session = Session(bind=engine)

        stmt = session.query(cla).filter(cla.dat_medicao >= data_inicial).filter(cla.dat_medicao <= data_final)\
            .filter(cla.val_lat >= lat_inicial).filter(cla.val_lat <= lat_final)\
            .filter(cla.val_lon >= lon_inicial).filter(cla.val_lon <= lon_final)

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

    
    def get_rio_path(self):

        session = Session(bind=engine)

        stmt = session.query(Rios)

        df = pd.read_sql(
            sql=stmt.statement,
            con=session.bind
        )

        return df


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


    def insert_solo(self, df):
        df = pd.DataFrame(df)

        # Remove nulls e nas
        df.replace(to_replace='', value=np.nan, inplace=True)
        df.fillna(value=0.0, inplace=True)

        session = Session(bind=engine)

        dados = list()

        for i, dado in df.iterrows():
            dados.append(
                Solo(
                    val_lat=dado['val_lat'],
                    val_lon=dado['val_lon'],
                    dat_medicao=dado.dat_medicao.to_pydatetime(),
                    val_soil=dado['val_soil'],
                )
            )

        session.bulk_save_objects(objects=dados)

        try:
            session.commit()

        except:
            input('"Press Enter to continue..."')

        pass


    def insert_temperature(self, df):
        df = pd.DataFrame(df)

        # Remove nulls e nas
        #df.replace(to_replace='', value=np.nan, inplace=True)
        #df.drop(inplace=True)
        session = Session(bind=engine)

        dados = [
            Temperature(
                val_lat=dado['val_lat'],
                val_lon=dado['val_lon'],
                dat_medicao=dado.dat_medicao.to_pydatetime(),
                val_temp_med=dado['val_temp_med'],
                val_temp_min=dado['val_temp_min'],
                val_temp_max=dado['val_temp_max'],
            ) for i, dado in df.iterrows()
        ]

        #print('Insercao na base de dados')
        session.bulk_save_objects(objects=dados)
        session.commit()


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


    def insert_rios(self, df):
        df = pd.DataFrame(df)

        postos = list()
        for i, dado in df.iterrows():

            postos.append(
                Rios(
                    val_lon=dado['val_lon'],
                    val_lat=dado['val_lat'],
                    nom_bacia=dado['nom_bacia'],
                    num_ponto=dado['num_ponto'],
                    num_hidroac=dado['num_hidroac'],
                    num_tipo=dado['num_tipo']
                )
            )

        session = Session(bind=engine)

        session.bulk_save_objects(objects=postos)
        session.commit()
