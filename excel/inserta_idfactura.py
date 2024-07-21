import pandas as pd

# Ruta al archivo Excel
ARCHIVO_EXCEL = 'factura_prueba.xlsx'

# Lee el archivo Excel
df = pd.read_excel(ARCHIVO_EXCEL, sheet_name='Factura')
df2 = pd.read_excel(ARCHIVO_EXCEL, sheet_name='Detalle')

list_factura_id = df['idfactura']
idfactura_detalle = df2['idventadetalle'].tolist()

for id_factura in list_factura_id:
    for index, row in enumerate(idfactura_detalle):
        if idfactura_detalle[index] == id_factura:
            # modificar las celdas de la columna
            df2.loc[index, 'idfactura'] = id_factura

    with pd.ExcelWriter(ARCHIVO_EXCEL) as writer:
        df.to_excel(writer, sheet_name='Factura', index=False)
        df2.to_excel(writer, sheet_name='Detalle', index=False)
