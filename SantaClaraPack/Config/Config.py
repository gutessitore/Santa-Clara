#!/usr/bin/env python

class Config(object):
    def __init__(self):
        self.config = dict(

            merge=dict(
                data_inicial='1998-01-01',

                variable_name=dict(
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

            soil=dict(

                variables_name=dict(
                    lon='lon',
                    lat='lat',
                    soil='soilw',
                    tempo='time'
                ),

                sub_set=dict(
                    lat=dict(ini=-22.5, fim=-17.5, obs='graus N'),
                    lon=dict(ini=127.5, fim=140.0, ob='graus leste'),
                )

            ),

            temperature=dict(

                variable_names=dict(
                    lon='longitude',
                    lat='latitude',
                    temp='temperature',
                    clima='climatology',
                    day='day',
                    month='month',
                    year='year',
                    day_of_year='day_of_year'
                ),

                sub_set=dict(
                    lat=dict(ini=-23.5, fim=-16.5, obs='graus N'),
                    lon=dict(ini=-53.5, fim=-39.0, ob='graus leste'),
                ),
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


