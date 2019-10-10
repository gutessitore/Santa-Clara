import pandas as pd
from Banco.Dados import Dados
from Config.Config import Config
import matplotlib.pyplot as plt
from scipy.spatial import distance
import numpy as np

dados = Dados()
config = Config()
rio = dados.get_rio_path()
postos = dados.get_posto()

# print(rio.describe())

# lat_lon = list(zip(rio.val_lat, rio.val_lon))

# dist = list()
# for index in range(len(lat_lon)-1):
# 	distancia = distance.euclidean(lat_lon[index], lat_lon[index+1])
# 	if distancia < 0.08: #remove outliers
# 		dist.append(distancia)

# print(np.mean(dist)) #0.01624116767780382

# print(distance.euclidean(lat_lon[0], lat_lon[1])) #0.013315404612704994

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.scatter(rio.val_lon, rio.val_lat, s=2, c='b')
ax1.scatter(postos.num_lon ,postos.num_lat, s=5, c='r', marker="v")
plt.show()