# Santa-Clara

Santa-clara é um mecanismo para tomada de decisão a partir da previsão da vazão natural. 

## Colocando as credenciais

Para leitura dos dados é necessário completar os campos de user e password, que estão no arquivo SantaClaraPack/Config/Config.py .

```python
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
```

## Lendo os dados

Função que acesa o serviço da Amazon e devolve os dados do período selecionado.

```python
import pandas as pd
from Banco.Dados import Dados
from Config.Config import Config

dados = Dados()
df_vazao = dados.get_vazao(
    data_inicial='2017-01-01',
    data_final='2017-01-31',
    posto=1
)

config = Config()


print(df_vazao)
```

## Variáveis
Link de onde as informações foram extraidas<br/>
-[Chuva](http://ftp.cptec.inpe.br/modelos/io/produtos/MERGE/)<br/>
-[Vazão Natural](http://www.ons.org.br/)<br/>
-[Soil Moisture](https://www.esrl.noaa.gov/psd/data/gridded/data.cpcsoil.html)<br/>
-[Air Temperature](https://climatedataguide.ucar.edu/climate-data/global-surface-temperatures-best-berkeley-earth-surface--temperatures)<br/>
-[Maximum Air Temperature](https://climatedataguide.ucar.edu/climate-data/global-surface-temperatures-best-berkeley-earth-surface-temperatures)<br/>
-[Minimum Air Temperature](https://climatedataguide.ucar.edu/climate-data/global-surface-temperatures-best-berkeley-earth-surface-temperatures)<br/>
-[SST - sea surface temperature](https://climatedataguide.ucar.edu/climate-data/global-surface-temperatures-best-berkeley-earth-surface-temperatures)<br/>
