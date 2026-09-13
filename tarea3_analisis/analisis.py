######################################################################
#Sofía
#Importar librerías necesarias
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # guarda las graficas como PNG en vez de abrir ventanas
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy import stats
import seaborn as sns
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
print("-------------------------------------------------------------------------------------------------------------")
print("Análisis Sofía - ¿Cuánta plata contrató el Ministerio cada año y en qué tipo de contratos se concentra?:")
print("-------------------------------------------------------------------------------------------------------------")
#Cargar los datos
df = pd.read_csv("../tarea2_ingenieria_datos/datos_limpios.csv")

print("Dimensión de los datos originales:")
print(df.shape)

#Se hace un análisis descriptivo de la variable valor_del_contrato 
print("\nEstadísticas descriptivas del valor de los contratos:")
print(df["valor_del_contrato"].describe())

#Histograma para visualizar la distribución original del valor de los contratos
plt.figure(figsize=(10, 6))
plt.hist(
    df["valor_del_contrato"],
    bins=30,
    edgecolor="black"
)

plt.title("Distribución del valor de los contratos")
plt.xlabel("Valor del contrato")
plt.ylabel("Frecuencia")

plt.tight_layout()
plt.savefig("grafica_01.png", dpi=120, bbox_inches="tight"); plt.close()

#Se aplica una transformación logarítmica para visualizar mejor valores extremos
plt.figure(figsize=(10, 6))

plt.hist(
    np.log1p(df["valor_del_contrato"]),
    bins=30,
    edgecolor="black"
)

plt.title("Distribución del valor de los contratos (escala logarítmica)")
plt.xlabel("Log(1 + valor del contrato)")
plt.ylabel("Frecuencia")

plt.tight_layout()
plt.savefig("grafica_02.png", dpi=120, bbox_inches="tight"); plt.close()


#Boxplot para identificar dispersión y valores atípicos
plt.figure(figsize=(10, 5))

plt.boxplot(
    np.log1p(df["valor_del_contrato"]),
    vert=False
)

plt.title("Diagrama de caja del valor de los contratos")
plt.xlabel("Log(1 + valor del contrato)")

plt.tight_layout()
plt.savefig("grafica_03.png", dpi=120, bbox_inches="tight"); plt.close()


#Ahora se busca saber cuanta plata contrató el ministerio cada año, 
#para esto se agrupa por cada año y de ahí calculan estadísticas descriptivas del valor de los contratos.
resumen_anual = (
    df
    .groupby("anio")["valor_del_contrato"]
    .agg(["count", "sum", "mean", "median", "max"])
    .reset_index()
)

#Cambiar nombres de columnas
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

#Visualización de cuánto dinero se contrató en cada año
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
plt.savefig("grafica_04.png", dpi=120, bbox_inches="tight"); plt.close()


#Se analizaron en que tipo de contratos se concentra el dinero contratado por el ministerio, 
#Se agrupa por tipo de contrato y se calculan estadísticas descriptivas del valor de los contratos.
resumen_tipo = (
    df
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

#Porcentaje del valor total
resumen_tipo["porcentaje_valor"] = (
    resumen_tipo["valor_total"]
    / resumen_tipo["valor_total"].sum()
    * 100
)

#Porcentaje de contratos
resumen_tipo["porcentaje_contratos"] = (
    resumen_tipo["numero_contratos"]
    / resumen_tipo["numero_contratos"].sum()
    * 100
)

#Ordenar de mayor a menor valor contratado
resumen_tipo = resumen_tipo.sort_values(
    "valor_total",
    ascending=False
)

print("\nContratación por tipo de contrato:")
print(resumen_tipo.to_string(index=False))


#Visualización de qué tipos de contrato concentran mayor cantidad de dinero
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
plt.savefig("grafica_05.png", dpi=120, bbox_inches="tight"); plt.close()

#Relación entre año y tipo de contrato, 
#Se agrupa por año y tipo de contrato y se calcula el valor total contratado.
resumen_anio_tipo = (
    df
    .groupby(
        ["anio", "tipo_de_contrato"]
    )["valor_del_contrato"]
    .sum()
    .reset_index()
)

print("\nValor contratado por año y tipo de contrato:")
print(resumen_anio_tipo.to_string(index=False))


#Mostrar los registros con mayor valor para cada año
resumen_ordenado = resumen_anio_tipo.sort_values(
    ["anio", "valor_del_contrato"],
    ascending=[True, False]
)

tipo_principal_anio = resumen_ordenado.drop_duplicates(
    subset="anio"
)

print("\nTipo de contrato con mayor valor en cada año:")
print(tipo_principal_anio.to_string(index=False))

#Seleccionar los 6 tipos de contrato con mayor valor total
#y crear tabla para comparar el valor contratado por año y tipo de contrato
principales = (
    df
    .groupby("tipo_de_contrato")["valor_del_contrato"]
    .sum()
    .sort_values(ascending=False)
    .head(6)
    .index
)

datos_mapa = df[
    df["tipo_de_contrato"].isin(principales)
]

tabla = datos_mapa.pivot_table(
    index="tipo_de_contrato",
    columns="anio",
    values="valor_del_contrato",
    aggfunc="sum",
    fill_value=0
)

#Convertir a miles de millones de pesos
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
plt.savefig("grafica_06.png", dpi=120, bbox_inches="tight"); plt.close()

#Diagrama de violin para comparar la distribución del valor de los contratos
#para los tipos más frecuentes

tipos = df["tipo_de_contrato"].value_counts().head(5).index

datos = []

for tipo in tipos:
    valores = df[
        df["tipo_de_contrato"] == tipo
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
plt.savefig("grafica_07.png", dpi=120, bbox_inches="tight"); plt.close()


#Diagrama de dispersión para ver la relación entre el año y el valor de los contratos

plt.figure(figsize=(10, 6))

plt.scatter(
    df["anio"],
    np.log1p(df["valor_del_contrato"]),
    alpha=0.4
)

plt.title("Valor de los contratos según el año")
plt.xlabel("Año")
plt.ylabel("Log(1 + valor del contrato)")

plt.tight_layout()
plt.savefig("grafica_08.png", dpi=120, bbox_inches="tight"); plt.close()


#Correlación entre el año y el valor del contrato

correlacion, p_valor = pearsonr(
    df["anio"],
    df["valor_del_contrato"]
)

print("\nCorrelación entre año y valor del contrato:")
print("Correlación:", correlacion)
print("P-valor:", p_valor)
if p_valor < 0.05:
    print("Existe una relación significativa entre el año y el valor de los contratos.")
else:
    print("No existe una relación significativa entre el año y el valor de los contratos.")


######################################################################
print("-----------------------------------------------------------------------------------------------------------------------------------")
print("Análisis Juan - ¿Difiere el porcentaje de ejecución presupuestal (pagado / contratado) al momento del corte según si el contratista es PyME, consorcio, o el género de su representante legal?:")
print("-----------------------------------------------------------------------------------------------------------------------------------")
#JSQO
# % de ejecución = pagado / contratado * 100 (excluye contratos con valor 0)
valor_valido = df["valor_del_contrato"].where(~df["valor_contrato_cero"], np.nan)
df["pct_ejecucion"] = (df["valor_pagado"] / valor_valido) * 100

# Estadísticas descriptivas
print(df["pct_ejecucion"].describe().round(2))
 
for grupo in ["es_pyme", "es_grupo", "g_nero_representante_legal"]:
    print(f"\n% de ejecución por {grupo}")
    print(df.groupby(grupo)["pct_ejecucion"].agg(["count", "mean", "median", "std"]).round(2))
 
pivot = df.pivot_table(index="es_pyme", columns="g_nero_representante_legal",
                        values="pct_ejecucion", aggfunc="mean").round(2)
print("\n% de ejecución promedio: PyME x Género")
print(pivot)

# --- Visualizaciones ---
fig, ax = plt.subplots(figsize=(7, 5))
sns.histplot(df["pct_ejecucion"].dropna(), bins=50, kde=True, ax=ax, color="#4C72B0")
ax.axvline(100, color="black", linestyle="--", linewidth=1, label="100% ejecutado")
ax.legend()
ax.set_title("Distribución del % de ejecución presupuestal")
fig.tight_layout()
plt.savefig("grafica_09.png", dpi=120, bbox_inches="tight"); plt.close()
 
fig, ax = plt.subplots(figsize=(6, 5))
sns.boxplot(data=df, x="es_pyme", y="pct_ejecucion", ax=ax, showfliers=False)
ax.set_title("% de ejecución según condición PyME")
fig.tight_layout()
plt.savefig("grafica_10.png", dpi=120, bbox_inches="tight"); plt.close()
 
fig, ax = plt.subplots(figsize=(6, 5))
sns.boxplot(data=df, x="es_grupo", y="pct_ejecucion", ax=ax, showfliers=False)
ax.set_title("% de ejecución según si es consorcio/grupo")
fig.tight_layout()
plt.savefig("grafica_11.png", dpi=120, bbox_inches="tight"); plt.close()
 
fig, ax = plt.subplots(figsize=(7, 5))
orden = ["Hombre", "Mujer", "No definido"]
sns.boxplot(data=df, x="g_nero_representante_legal", y="pct_ejecucion", order=orden, ax=ax, showfliers=False)
ax.set_title("% de ejecución según género del representante legal")
fig.tight_layout()
plt.savefig("grafica_12.png", dpi=120, bbox_inches="tight"); plt.close()
 
fig, ax = plt.subplots(figsize=(9, 6))
sns.violinplot(
    data=df[df["g_nero_representante_legal"] != "No definido"],
    x="g_nero_representante_legal", y="pct_ejecucion",
    hue="es_pyme", split=True, cut=0, ax=ax
)
ax.set_title("% de ejecución: Género x Condición PyME")
fig.tight_layout()
plt.savefig("grafica_13.png", dpi=120, bbox_inches="tight"); plt.close()
 
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
ax.set_title("% de ejecución promedio: PyME x Género")
fig.tight_layout()
plt.savefig("grafica_14.png", dpi=120, bbox_inches="tight"); plt.close()

# --- Pruebas estadísticas ---
y = df["pct_ejecucion"].dropna()
stat_norm, p_norm = stats.normaltest(y)
print(f"\nNormalidad (D'Agostino): p-valor = {p_norm:.4g}")
 
g1 = df.loc[df["es_pyme"] == "Si", "pct_ejecucion"].dropna()
g2 = df.loc[df["es_pyme"] == "No", "pct_ejecucion"].dropna()
u, p = stats.mannwhitneyu(g1, g2, alternative="two-sided")
print(f"\nPyME vs No PyME: Mann-Whitney p-valor = {p:.4g} "
      f"(mediana PyME = {g1.median():.2f}%, No PyME = {g2.median():.2f}%)")
 
g1 = df.loc[df["es_grupo"] == "Si", "pct_ejecucion"].dropna()
g2 = df.loc[df["es_grupo"] == "No", "pct_ejecucion"].dropna()
u, p = stats.mannwhitneyu(g1, g2, alternative="two-sided")
print(f"Consorcio vs individual: Mann-Whitney p-valor = {p:.4g} "
      f"(mediana Grupo = {g1.median():.2f}%, Individual = {g2.median():.2f}%)")
 
grupos_genero = [
    df.loc[df["g_nero_representante_legal"] == g, "pct_ejecucion"].dropna()
    for g in df["g_nero_representante_legal"].unique()
]
h, p = stats.kruskal(*grupos_genero)
print(f"Género (Kruskal-Wallis): p-valor = {p:.4g}")
 
g1 = df.loc[df["g_nero_representante_legal"] == "Hombre", "pct_ejecucion"].dropna()
g2 = df.loc[df["g_nero_representante_legal"] == "Mujer", "pct_ejecucion"].dropna()
u, p = stats.mannwhitneyu(g1, g2, alternative="two-sided")
print(f"Hombre vs Mujer: Mann-Whitney p-valor = {p:.4g} "
      f"(mediana Hombre = {g1.median():.2f}%, Mujer = {g2.median():.2f}%)")
 
datos_validos = df[df["g_nero_representante_legal"] != "No definido"].copy()
modelo = ols("pct_ejecucion ~ C(es_pyme) * C(g_nero_representante_legal)", data=datos_validos).fit()
tabla_anova = anova_lm(modelo, typ=2)
print("\nANOVA de dos vías (PyME x Género):")
print(tabla_anova.round(4))

######################################################################
#  JJ
# Trabajo con los contratos de valor > 0
dfm = df[df["valor_del_contrato"] > 0].copy()

# --- Descriptivo: número de contratos y valor por modalidad ---
resumen = (
    dfm.groupby("modalidad_de_contratacion")["valor_del_contrato"]
    .agg(n="count", valor_total="sum", valor_mediano="median")
    .sort_values("valor_total", ascending=False)
)
resumen["pct_valor"] = (resumen["valor_total"] / resumen["valor_total"].sum() * 100).round(1)
resumen["pct_contratos"] = (resumen["n"] / resumen["n"].sum() * 100).round(1)
print("\nContratación por modalidad:")
print(resumen.to_string())

print("\nDirecta vs competitiva (es_directa):")
print(dfm.groupby("es_directa")["valor_del_contrato"].agg(n="count", valor_total="sum", valor_mediano="median"))

# --- Duración mediana por modalidad ---
print("\nDuración mediana (días) por modalidad:")
print(dfm.groupby("modalidad_de_contratacion")["duracion_dias"].median().sort_values(ascending=False))

# Gráfica 1: valor total por modalidad
plt.figure(figsize=(10, 6))
datos = resumen.sort_values("valor_total")
plt.barh(datos.index, datos["valor_total"] / 1e9, edgecolor="black")
plt.title("Valor total contratado por modalidad")
plt.xlabel("Miles de millones de pesos")
plt.tight_layout()
plt.savefig("grafica_15.png", dpi=120, bbox_inches="tight"); plt.close()

# Gráfica 2: distribución del valor por modalidad 
top = dfm["modalidad_de_contratacion"].value_counts().head(5).index
dt = dfm[dfm["modalidad_de_contratacion"].isin(top)].copy()
dt["log_valor"] = np.log1p(dt["valor_del_contrato"])
plt.figure(figsize=(10, 6))
sns.boxplot(data=dt, y="modalidad_de_contratacion", x="log_valor", showfliers=False)
plt.title("Distribución del valor por modalidad (escala logarítmica)")
plt.xlabel("Log(1 + valor del contrato)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("grafica_16.png", dpi=120, bbox_inches="tight"); plt.close()

#Relación valor - duración: correlación y su mapa de calor 
dfd = dfm[dfm["duracion_dias"].notna() & (dfm["duracion_dias"] >= 0)].copy()
corr = dfd[["valor_del_contrato", "duracion_dias", "dias_adicionados"]].corr(method="spearman")
plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlación (Spearman) entre valor, duración y días adicionados")
plt.tight_layout()
plt.savefig("grafica_17.png", dpi=120, bbox_inches="tight"); plt.close()

rho, p = stats.spearmanr(dfd["valor_del_contrato"], dfd["duracion_dias"])
print(f"\nCorrelación valor-duración (Spearman): rho = {rho:.3f}, p = {p:.3g}")

# regresión lineal del (log) valor
dfd["log_valor"] = np.log1p(dfd["valor_del_contrato"])
modelo = ols("log_valor ~ duracion_dias + es_directa", data=dfd).fit()
print("\nRegresión: log(1 + valor) ~ duración + es_directa")
print(modelo.summary().tables[1])
print(f"R2 = {modelo.rsquared:.3f}")