
#Importar librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

#cargar los datos
df = pd.read_csv("../tarea2_ingenieria_datos/Datos_MinisterioHacienda.csv")

print("Dimensión de los datos originales:")
print(df.shape)


#Preparar las variables necesarias para responder la pregunta: ¿Cuánta plata contrató el Ministerio cada año, 
# y en qué tipo de contratos se concentra?
df = df[df["valor_del_contrato"] < 1e12].copy()

#Convertir las fechas a formato datetime
df["fecha_de_firma"] = pd.to_datetime(df["fecha_de_firma"],errors="coerce")

df["fecha_de_inicio_del_contrato"] = pd.to_datetime(df["fecha_de_inicio_del_contrato"],errors="coerce")

#Usar la fecha de firma y, si no existe, la fecha de inicio
df["fecha_analisis"] = df["fecha_de_firma"].fillna(df["fecha_de_inicio_del_contrato"])

# Crear variable año
df["anio"] = df["fecha_analisis"].dt.year

# Organizar los nombres de los tipos de contrato
df["tipo_de_contrato"] = (df["tipo_de_contrato"].str.strip().str.capitalize())

# Conservar los contratos que tienen un año identificado
df_analisis = df[df["anio"].notna()].copy()

print("\nDimensión de los datos utilizados en el análisis:")
print(df_analisis.shape)




#Se hace un análisis descriptivo de la variable valor_del_contrato, 
print("\nEstadísticas descriptivas del valor de los contratos:")
print(df_analisis["valor_del_contrato"].describe())

#Histograma para visualizar la distribución original del valor de los contratos
plt.figure(figsize=(10, 6))

plt.hist(
    df_analisis["valor_del_contrato"],
    bins=30,
    edgecolor="black"
)

plt.title("Distribución del valor de los contratos")
plt.xlabel("Valor del contrato")
plt.ylabel("Frecuencia")

plt.tight_layout()
plt.show()

#Se aplica una transformación logarítmica para visualizar mejor valores extremos
plt.figure(figsize=(10, 6))

plt.hist(
    np.log1p(df_analisis["valor_del_contrato"]),
    bins=30,
    edgecolor="black"
)

plt.title("Distribución del valor de los contratos (escala logarítmica)")
plt.xlabel("Log(1 + valor del contrato)")
plt.ylabel("Frecuencia")

plt.tight_layout()
plt.show()


#Boxplot para identificar dispersión y valores atípicos
plt.figure(figsize=(10, 5))

plt.boxplot(
    np.log1p(df_analisis["valor_del_contrato"]),
    vert=False
)

plt.title("Diagrama de caja del valor de los contratos")
plt.xlabel("Log(1 + valor del contrato)")

plt.tight_layout()
plt.show()


#Ahora se busca saber cuanta plata contrató el ministerio cada año, 
# para esto se agrupa por cada año y de ahí calculan estadísticas descriptivas del valor de los contratos.
resumen_anual = (
    df_analisis
    .groupby("anio")["valor_del_contrato"]
    .agg(["count", "sum", "mean", "median", "max"])
    .reset_index()
)

# Cambiar nombres de columnas
resumen_anual.columns = [
    "anio",
    "numero_contratos",
    "valor_total",
    "valor_promedio",
    "valor_mediano",
    "valor_maximo"
]
print("\nResumen de contratación por año:")
print(resumen_anual)

#visualización de cuánto dinero se contrató en cada año
plt.figure(figsize=(11, 6))

plt.bar(
    resumen_anual["anio"].astype(str),
    resumen_anual["valor_total"] / 1e9,
    edgecolor="black"
)

plt.title("Valor total contratado por año")
plt.xlabel("Año")
plt.ylabel("Valor contratado (miles de millones de pesos)")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


#Se analizaron en que tipo de contratos se concentra el dinero contratado por el ministerio, 
# Se agrupa por tipo de contrato y se calculan estadísticas descriptivas del valor de los contratos.
resumen_tipo = (
    df_analisis
    .groupby("tipo_de_contrato")["valor_del_contrato"]
    .agg(["count", "sum", "mean", "median"])
    .reset_index()
)

resumen_tipo.columns = [
    "tipo_de_contrato",
    "numero_contratos",
    "valor_total",
    "valor_promedio",
    "valor_mediano"
]

# Porcentaje del valor total
resumen_tipo["porcentaje_valor"] = (
    resumen_tipo["valor_total"]
    / resumen_tipo["valor_total"].sum()
    * 100
)

# Porcentaje de contratos
resumen_tipo["porcentaje_contratos"] = (
    resumen_tipo["numero_contratos"]
    / resumen_tipo["numero_contratos"].sum()
    * 100
)

# Ordenar de mayor a menor valor contratado
resumen_tipo = resumen_tipo.sort_values(
    "valor_total",
    ascending=False
)

print("\nContratación por tipo de contrato:")
print(resumen_tipo.to_string(index=False))




#visualización de qué tipos de contrato concentran mayor cantidad de dinero
datos_tipo = resumen_tipo.sort_values("valor_total")

plt.figure(figsize=(11, 7))

plt.barh(
    datos_tipo["tipo_de_contrato"],
    datos_tipo["valor_total"] / 1e9,
    edgecolor="black"
)

plt.title("Valor contratado por tipo de contrato")
plt.xlabel("Valor contratado (miles de millones de pesos)")
plt.ylabel("Tipo de contrato")

plt.tight_layout()
plt.show()

#Relación entre año y tipo de contrato, 
#Se agrupa por año y tipo de contrato y se calcula el valor total contratado.
resumen_anio_tipo = (
    df_analisis
    .groupby(
        ["anio", "tipo_de_contrato"]
    )["valor_del_contrato"]
    .sum()
    .reset_index()
)

print("\nValor contratado por año y tipo de contrato:")
print(resumen_anio_tipo.to_string(index=False))


# Mostrar los registros con mayor valor para cada año
resumen_ordenado = resumen_anio_tipo.sort_values(
    ["anio", "valor_del_contrato"],
    ascending=[True, False]
)

tipo_principal_anio = resumen_ordenado.drop_duplicates(
    subset="anio"
)

print("\nTipo de contrato con mayor valor en cada año:")
print(tipo_principal_anio.to_string(index=False))

# Seleccionar los 6 tipos de contrato con mayor valor total
# y crear tabla para comparar el valor contratado por año y tipo de contrato
principales = (
    df_analisis
    .groupby("tipo_de_contrato")["valor_del_contrato"]
    .sum()
    .sort_values(ascending=False)
    .head(6)
    .index
)

datos_mapa = df_analisis[
    df_analisis["tipo_de_contrato"].isin(principales)
]

tabla = datos_mapa.pivot_table(
    index="tipo_de_contrato",
    columns="anio",
    values="valor_del_contrato",
    aggfunc="sum",
    fill_value=0
)

# Convertir a miles de millones de pesos
tabla = tabla / 1e9

plt.figure(figsize=(12, 6))

plt.imshow(
    tabla,
    aspect="auto"
)

plt.colorbar(
    label="Miles de millones de pesos"
)

plt.xticks(
    range(len(tabla.columns)),
    tabla.columns
)

plt.yticks(
    range(len(tabla.index)),
    tabla.index
)

plt.title("Valor contratado por año y tipo de contrato")
plt.xlabel("Año")
plt.ylabel("Tipo de contrato")

plt.tight_layout()
plt.show()

# Diagrama de violin para comparar la distribución del valor de los contratos
# para los tipos más frecuentes

tipos = df_analisis["tipo_de_contrato"].value_counts().head(5).index

datos = []

for tipo in tipos:
    valores = df_analisis[
        df_analisis["tipo_de_contrato"] == tipo
    ]["valor_del_contrato"]

    datos.append(np.log1p(valores))

plt.figure(figsize=(11, 6))

plt.violinplot(datos)

plt.xticks(
    range(1, len(tipos) + 1),
    tipos,
    rotation=45
)

plt.title("Distribución del valor por tipo de contrato")
plt.xlabel("Tipo de contrato")
plt.ylabel("Log(1 + valor del contrato)")

plt.tight_layout()
plt.show()


# Diagrama de dispersión para ver la relación entre el año y el valor de los contratos

plt.figure(figsize=(10, 6))

plt.scatter(
    df_analisis["anio"],
    np.log1p(df_analisis["valor_del_contrato"]),
    alpha=0.4
)

plt.title("Valor de los contratos según el año")
plt.xlabel("Año")
plt.ylabel("Log(1 + valor del contrato)")

plt.tight_layout()
plt.show()


# Correlación entre el año y el valor del contrato

correlacion, p_valor = pearsonr(
    df_analisis["anio"],
    df_analisis["valor_del_contrato"]
)

print("\nCorrelación entre año y valor del contrato:")
print("Correlación:", correlacion)
print("P-valor:", p_valor)
if p_valor < 0.05:
    print("Existe una relación significativa entre el año y el valor de los contratos.")
else:
    print("No existe una relación significativa entre el año y el valor de los contratos.")