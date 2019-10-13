import pandas as pd
from Config.Config import Config
from Banco.Dados import Dados

#arquivo destinado a testes

config = Config()
dados = Dados()


# temp = dados.get_gridded_data(
#             data_inicial='2017-01-01', 
#             data_final='2017-01-31',
#             classe="Temperature",
# 			lat_inicial=-22.6,
# 			lat_final=-21.32,
# 			lon_inicial=-44.8,
# 			lon_final=-44.2
#     )

# chuva = dados.get_gridded_data(
#             data_inicial='2017-01-01', 
#             data_final='2017-01-31',
#             classe="Chuva",
# 			lat_inicial=-22.6,
# 			lat_final=-21.32,
# 			lon_inicial=-44.8,
# 			lon_final=-44.2
#     )

# umid = dados.get_gridded_data(
#             data_inicial='2017-01-01', 
#             data_final='2017-01-31',
#             classe="Solo",
# 			lat_inicial=-22.6,
# 			lat_final=-21.32,
# 			lon_inicial=-44.8,
# 			lon_final=-44.2
#     )

# vaz_natr = dados.get_vazao(data_inicial='2017-01-01', posto=1)

# print(temp.head(), chuva.head(), umid.head())

# df = chuva.iloc[:, 1:]
# df = df.merge(vaz_natr.iloc[:, 2:4], on="dat_medicao")
# df = df.merge(temp.iloc[:, 1:], on="dat_medicao")

# print(chuva.iloc[:, 1:])


data = dados.get_post_data(
			lat_inicial=-22.6,
			lat_final=-21.32,
			lon_inicial=-44.8,
			lon_final=-44.2
    )

print(data)