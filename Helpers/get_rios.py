import fiona
import pandas as pd

#shapes = fiona.open(r"C:\Users\anderson\Desktop\shapefle/Subbacias_Hidrográficas_DNAEE.shp")
shapes = fiona.open(r"C:\Onedrive\Middle Office\Middle\Hidrologia\ShapeFiles\Rio_Parana/Sub_bacias.shp")
rios = fiona.open(r"C:\Onedrive\Middle Office\Middle\Hidrologia\ShapeFiles\Rio_Parana/Hidrografia 250000.shp")
df = pd.DataFrame()
aux = dict(
    nom_bacia=list(),
    lat=list(),
    lon=list(),
    ponto=list()
)
df = pd.DataFrame()
for i, rio in enumerate(rios):
    print(rio['properties']['NOME'])

    if rio['properties']['NOME'] in [
        'Rio Grande',
        #'Rio Pardo',
        'Rio Mogi-Guaçú',
        'Rio Sarapuí'
    ]:
        df_coords = pd.DataFrame(
            data=rio['geometry']['coordinates'],
            columns=['lon', 'lat']
        )
        df_coords['nom_bacia'] = rio['properties']['NOME']
        df_coords['ponto'] = range(len(rio['geometry']['coordinates']))
        df_coords['hidroarc_i'] = rio['properties']['HIDROARC_']
        df_coords['tipo'] = rio['properties']['TIPO']

        df = pd.concat(objs=[df, df_coords])

df.to_csv(path_or_buf='bacia_grande.csv', sep=';', decimal=',', index=False)