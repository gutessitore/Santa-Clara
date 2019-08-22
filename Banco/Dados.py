# !/usr/bin/env python
# *- coding: utf-8 -*-
import pandas as pd
from Banco.Banco import *
from Config.Config import Config
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func

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