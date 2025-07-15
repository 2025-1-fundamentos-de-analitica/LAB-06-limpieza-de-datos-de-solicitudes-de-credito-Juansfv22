"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import pandas as pd
    import os

    # Cargar el archivo CSV
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)
    
    # Eliminar filas con datos faltantes
    df.dropna(inplace=True)

    # Dar formato a los valores monetarios
    df["monto_del_credito"] = df["monto_del_credito"].str.strip(" $").str.replace(r"\.00$", "", regex=True).str.replace(r"[,.]", "", regex=True).astype(int)
    
    # Dar formato a las columnas de texto
    for col in df.select_dtypes(include=['object']):
            df[col] = df[col].str.strip(" .,-_").str.lower().str.replace(r"[-,.; ]", '_', regex=True)

    # Dar formato a las fechas  
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).combine_first(
        pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    )

    # Eliminar registros duplicados
    df.drop_duplicates(inplace=True)

    # CORREGIR ERRORES DEL EJERCICIO
    df.iloc[[3586, 4293, 9806], df.columns.get_loc("barrio")] = "san_jose_de_la_cima_no_"
    df.iloc[[5312, 7615], df.columns.get_loc("barrio")] = "el_salado_"

    # Crear el directorio de salida si no existe
    os.makedirs("files/output", exist_ok=True)

    # Guardar el DataFrame limpio en un nuevo archivo CSV
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=';', index=False)

    return df

if __name__ == "__main__":
    pregunta_01()