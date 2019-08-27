#!/usr/bin/env python

class Config(object):
    def __init__(self):
        self.config = dict(

            merge=dict(
                data_inicial='1998-01-01',

                variables_name=dict(
                    lon='lon',
                    lat='lat',
                    chuva='prec',
                    tempo='time'
                ),

                sub_set=dict(
                    lat=dict(ini=-22.5, fim=-17.5, obs='graus N'),
                    lon=dict(ini=-52.5, fim=-40.0, ob='graus leste'),
                )

            ),

            paths=dict(

                merge=dict(
                    bin=r'http://ftp.cptec.inpe.br/modelos/io/produtos/MERGE/{data:%Y}/prec_{data:%Y%m%d}.bin',
                    ctl=r'http://ftp.cptec.inpe.br/modelos/io/produtos/MERGE/{data:%Y}/prec_{data:%Y%m%d}.ctl',
                    export=r'C:\Users\anderson\Desktop\merge',
                ),

                vazao=dict(
                    vazao_historica=r'C:\Users\anderson\Desktop/Vazões_Diárias_1931_2017.csv',
                    cad_usinas=r'C:\Users\anderson\Desktop/tbl_posto.csv',
                    acomph=r''
                ),

                gfs=dict(),

                gefs=dict(),

                cfsv2=dict(),

            )

        )

        self.config_banco = dict(
            string_engine=r'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}',

            credentials=dict(
                user='',
                password='',
                host='',
                database='',
                port=3306,
                # raise_on_warnings=True,
                # get_warnings=True,
            ),

        )


        pass


