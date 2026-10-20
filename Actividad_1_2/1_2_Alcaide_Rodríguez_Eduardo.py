from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import requests
import pymongo
import pandas as pd

# Paso 3.- Codificar la petición en Python
url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/25171"
respuesta = requests.get(url)
data_json = respuesta.json()

# Paso 4.- Guardado del JSON en Mongo
client = pymongo.MongoClient("mongodb://root:secreta@localhost:27018/")
db = client["ine_database"]
collection = db["ipv_raw"]

# Limpio la colección por si lo he ejecutado antes y así evito los duplicados
collection.delete_many({})

# Como data_json es una lista de diccionarios, desde mi punto de vista sería mejor usar insert_many
result = collection.insert_many(data_json)
print(f"Documentos insertados en MongoDB: {len(result.inserted_ids)}")

# Paso 5.- Filtrar la información
filas_filtradas = []

for serie in data_json:
    # Al campo Nombre tener el formato: "Lugar. Tipo de vivienda. Tipo de dato. "
    partes_nombre = [p.strip() for p in serie["Nombre"].split(".") if p.strip()]

    if len(partes_nombre) >= 3:
        lugar = partes_nombre[0]
        tipo_vivienda = partes_nombre[1]
        tipo_dato = partes_nombre[2]

        # Filtro solo los datos "General" y de tipo "Índice"
        if tipo_vivienda == "General" and tipo_dato == "Índice":
            for registro in serie["Data"]:
                # Descarto posibles registros sin valor numérico
                if registro.get("Valor") is not None:
                    fecha = datetime.fromtimestamp(
                        registro["Fecha"] / 1000,
                        ZoneInfo("Europe/Madrid")
                    )
                    periodo = f"T{(fecha.month - 1) // 3 + 1}"
                    filas_filtradas.append({
                        "Lugar": lugar,
                        "Año": registro["Anyo"],
                        "Periodo": periodo,
                        "IPV": registro["Valor"]
                    })

# Paso 6.- Creación de un Dataframe de Pandas y asignación de los tipos
df = pd.DataFrame(filas_filtradas)

df["Lugar"] = df["Lugar"].astype(str)
df["Año"] = df["Año"].astype(int)
df["Periodo"] = df["Periodo"].astype(str)
df["IPV"] = df["IPV"].astype(float)

print("\nPrimeras filas del DataFrame:")
print(df.head())
print("\nTipos de las columnas:")
print(df.dtypes)

# Paso 7.- Guardado local del Dataframe con formato CSV
tiempo_unix = datetime.now(timezone.utc).timestamp()
nombre_csv = f"IPV_{tiempo_unix}.csv"

df.to_csv(nombre_csv, index=False, encoding="utf-8")
print(f"\nArchivo guardado correctamente como: {nombre_csv}")