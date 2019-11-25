import fiona
import pandas as pd

#shapes = fiona.open(r"C:\Users\anderson\Desktop\shapefle/Subbacias_Hidrográficas_DNAEE.shp")
uhes = fiona.open(r"C:\Users\anderson\Downloads\output\zipfolder/Usinas_Hidrelétricas_UHE.shp")

df = pd.DataFrame()

for uhe in uhes:

    aux = pd.DataFrame.from_dict(data=[uhe['properties']], orient='columns')
    aux['val_lat'] = uhe['geometry']['coordinates'][0]
    aux['val_lon'] = uhe['geometry']['coordinates'][1]

    df = pd.concat(objs=[df, aux], ignore_index=True)

print(df.head())
df.to_csv(path_or_buf=r'../Data/coords_uhe.csv', sep=';', decimal=',')