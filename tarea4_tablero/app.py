import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
df = pd.read_csv("../tarea2_ingenieria_datos/datos_limpios.csv")


resumen_anual = (
    df
    .groupby("anio")["valor_del_contrato"]
    .agg(["count", "sum", "mean", "median", "max"])
    .reset_index()
)

resumen_anual.columns = [
    "anio",
    "numero_contratos",
    "valor_total",
    "valor_promedio",
    "valor_mediano",
    "valor_maximo"
]


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

resumen_tipo["porcentaje_valor"] = (
    resumen_tipo["valor_total"]
    / resumen_tipo["valor_total"].sum()
    * 100
)

resumen_tipo["porcentaje_contratos"] = (
    resumen_tipo["numero_contratos"]
    / resumen_tipo["numero_contratos"].sum()
    * 100
)

resumen_tipo = resumen_tipo.sort_values(
    "valor_total",
    ascending=False
)

resumen_anual["valor_total_miles_millones"] = resumen_anual["valor_total"] / 1e9


fig_anio = px.bar(
    resumen_anual,
    x="anio",
    y="valor_total_miles_millones",
    title="Valor total contratado por año",
    labels={
        "anio": "Año",
        "valor_total_miles_millones": "Valor contratado (miles de millones de pesos)",
        "numero_contratos": "Número de contratos"
    },
    hover_data={
        "numero_contratos": True,
        "valor_total_miles_millones": ":.2f"
    }
)

resumen_tipo["valor_total_miles_millones"] = resumen_tipo["valor_total"] / 1e9


fig_tipo = px.bar(
    resumen_tipo,
    x="valor_total_miles_millones",
    y="tipo_de_contrato",
    orientation="h",
    title="Valor contratado por tipo de contrato",
    labels={
        "valor_total_miles_millones": "Valor contratado (miles de millones de pesos)",
        "tipo_de_contrato": "Tipo de contrato",
        "numero_contratos": "Número de contratos",
        "porcentaje_valor": "Porcentaje del valor (%)",
        "porcentaje_contratos": "Porcentaje de contratos (%)"
    },
    hover_data={
        "numero_contratos": True,
        "porcentaje_valor": ":.2f",
        "porcentaje_contratos": ":.2f",
        "valor_total_miles_millones": ":.2f"
    }
)
valor_total = df["valor_del_contrato"].sum()
valor_total_miles_millones = valor_total / 1e9


numero_contratos = len(df)


tipo_mayor_valor = resumen_tipo.iloc[0]["tipo_de_contrato"]

tipo_mas_frecuente = (df["tipo_de_contrato"].value_counts().idxmax())


dfm = df[df["valor_del_contrato"] > 0].copy()

resumen_modalidad = (
    dfm
    .groupby("modalidad_de_contratacion")["valor_del_contrato"]
    .agg(["count", "sum", "median"])
    .reset_index()
)

resumen_modalidad.columns = [
    "modalidad_de_contratacion",
    "numero_contratos",
    "valor_total",
    "valor_mediano"
]

resumen_modalidad["valor_total_miles_millones"] = resumen_modalidad["valor_total"] / 1e9

resumen_modalidad = resumen_modalidad.sort_values("valor_total", ascending=True)


fig_modalidad = px.bar(
    resumen_modalidad,
    x="valor_total_miles_millones",
    y="modalidad_de_contratacion",
    orientation="h",
    title="Valor total contratado por modalidad",
    labels={
        "valor_total_miles_millones": "Valor contratado (miles de millones de pesos)",
        "modalidad_de_contratacion": "Modalidad de contratación",
        "numero_contratos": "Número de contratos",
        "valor_mediano": "Valor mediano"
    },
    hover_data={
        "numero_contratos": True,
        "valor_mediano": ":.0f",
        "valor_total_miles_millones": ":.2f"
    }
)

dfm["log_valor"] = np.log1p(dfm["valor_del_contrato"])

top_modalidades = dfm["modalidad_de_contratacion"].value_counts().head(5).index

fig_box_modalidad = px.box(
    dfm[dfm["modalidad_de_contratacion"].isin(top_modalidades)],
    x="log_valor",
    y="modalidad_de_contratacion",
    orientation="h",
    points=False,
    title="Distribución del valor por modalidad (escala logarítmica)",
    labels={
        "log_valor": "Log(1 + valor del contrato)",
        "modalidad_de_contratacion": "Modalidad de contratación"
    }
)

pct_contratos_directa = (dfm["es_directa"] == 1).mean() * 100

pct_valor_directa = (
    dfm.loc[dfm["es_directa"] == 1, "valor_del_contrato"].sum()
    / dfm["valor_del_contrato"].sum()
    * 100
)

correlacion_valor_duracion = (
    dfm[["valor_del_contrato", "duracion_dias"]]
    .corr(method="spearman")
    .iloc[0, 1]
)


df["valor_valido"] = df["valor_del_contrato"].where(~df["valor_contrato_cero"], np.nan)
df["pct_ejecucion"] = (df["valor_pagado"] / df["valor_valido"]) * 100

df_ejec = df[df["pct_ejecucion"].notna()].copy()

fig_hist_ejecucion = px.histogram(
    df_ejec[df_ejec["pct_ejecucion"] <= 200],
    x="pct_ejecucion",
    nbins=50,
    title="Distribución del porcentaje de ejecución presupuestal",
    labels={"pct_ejecucion": "Porcentaje de ejecución (%)"}
)
fig_hist_ejecucion.add_vline(x=100, line_dash="dash", line_color="black")

fig_box_ejecucion = px.box(
    df_ejec,
    x="es_pyme",
    y="pct_ejecucion",
    points=False,
    title="Porcentaje de ejecución según condición PyME",
    labels={
        "es_pyme": "¿Es PyME?",
        "pct_ejecucion": "Porcentaje de ejecución (%)"
    }
)

ejecucion_mediana = df_ejec["pct_ejecucion"].median()

ejecucion_mediana_pyme = df_ejec.loc[df_ejec["es_pyme"] == "Si", "pct_ejecucion"].median()

ejecucion_mediana_nopyme = df_ejec.loc[df_ejec["es_pyme"] == "No", "pct_ejecucion"].median()

contratos_con_ejecucion = len(df_ejec)


app.layout = html.Div(children=[
    html.H1(children='Contratación del Ministerio de Hacienda y Crédito Público'),

    html.Div(children='''
        Tablero interactivo para analizar la contratación del Ministerio desde tres perspectivas.
    '''),

    html.Hr(),

    html.H2(children='1. ¿Cuánta plata contrató el Ministerio cada año, y en qué tipo de contratos se concentra?'),

html.Div(children=[

    html.Div(children=[
        html.Label("Seleccione un año:"),

        dcc.Dropdown(
            id="filtro-anio",
            options=[
                {"label": "Todos", "value": "Todos"}
            ] + [
                {"label": str(anio), "value": anio}
                for anio in sorted(df["anio"].dropna().unique())
            ],
            value="Todos",
            clearable=False
        )
    ], style={
        "width": "48%",
        "display": "inline-block"
    }),

    html.Div(children=[
        html.Label("Seleccione un tipo de contrato:"),

        dcc.Dropdown(
            id="filtro-tipo",
            options=[
                {"label": "Todos", "value": "Todos"}
            ] + [
                {"label": tipo, "value": tipo}
                for tipo in sorted(df["tipo_de_contrato"].dropna().unique())
            ],
            value="Todos",
            clearable=False
        )
    ], style={
        "width": "48%",
        "display": "inline-block",
        "marginLeft": "2%"
    })

]),

html.Div(children=[

    html.Div(children=[
        html.H4("Valor total contratado"),
        html.H2(
            f"${valor_total_miles_millones:,.2f} mil millones",
            id="kpi-valor"
        )
    ], style={
    "width": "21%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),

    html.Div(children=[
        html.H4("Número de contratos"),
        html.H2(
            f"{numero_contratos:,}",
            id="kpi-numero"
        )
    ], style={
    "width": "21%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),

    html.Div(children=[
        html.H4("Tipo con mayor valor contratado"),
        html.H2(
            tipo_mayor_valor,
            id="kpi-mayor-valor"
        )
    ], style={
    "width": "21%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),

    html.Div(children=[
        html.H4("Tipo de contrato más frecuente"),
        html.H2(
            tipo_mas_frecuente,
            id="kpi-mas-frecuente"
        )
    ], style={
    "width": "21%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),
]),
dcc.Graph(
    id="grafica-anio",
    figure=fig_anio
),

dcc.Graph(
    id="grafica-tipo",
    figure=fig_tipo
),

    html.Hr(),

    html.H2(children='2. ¿Por qué modalidades contrata el Ministerio y cómo se relaciona la modalidad con el valor y la duración?'),

html.Div(children=[

    html.Div(children=[
        html.Label("Seleccione una modalidad:"),

        dcc.Dropdown(
            id="filtro-modalidad",
            options=[
                {"label": "Todas", "value": "Todas"}
            ] + [
                {"label": modalidad, "value": modalidad}
                for modalidad in sorted(dfm["modalidad_de_contratacion"].dropna().unique())
            ],
            value="Todas",
            clearable=False
        )
    ], style={
        "width": "48%",
        "display": "inline-block"
    })

]),

html.Div(children=[

    html.Div(children=[
        html.H4("Contratos por contratación directa"),
        html.H2(f"{pct_contratos_directa:,.1f}%")
    ], style={
    "width": "31%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),

    html.Div(children=[
        html.H4("Valor por contratación directa"),
        html.H2(f"{pct_valor_directa:,.1f}%")
    ], style={
    "width": "31%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),

    html.Div(children=[
        html.H4("Correlación valor - duración"),
        html.H2(f"{correlacion_valor_duracion:,.2f}")
    ], style={
    "width": "31%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),
]),
dcc.Graph(
    id="grafica-modalidad",
    figure=fig_modalidad
),

dcc.Graph(
    id="grafica-box-modalidad",
    figure=fig_box_modalidad
),

dcc.Graph(
    id="grafica-dispersion"
),

    html.Hr(),

    html.H2(children='3. ¿Difiere el porcentaje de ejecución presupuestal según si el contratista es PyME, consorcio, o el género de su representante legal?'),

html.Div(children=[

    html.Div(children=[
        html.Label("Compare la ejecución según:"),

        dcc.Dropdown(
            id="filtro-grupo",
            options=[
                {"label": "Condición PyME", "value": "es_pyme"},
                {"label": "Consorcio / grupo", "value": "es_grupo"},
                {"label": "Género del representante legal", "value": "g_nero_representante_legal"}
            ],
            value="es_pyme",
            clearable=False
        )
    ], style={
        "width": "48%",
        "display": "inline-block"
    })

]),

html.Div(children=[

    html.Div(children=[
        html.H4("Ejecución mediana"),
        html.H2(f"{ejecucion_mediana:,.1f}%")
    ], style={
    "width": "23%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),

    html.Div(children=[
        html.H4("Ejecución mediana PyME"),
        html.H2(f"{ejecucion_mediana_pyme:,.1f}%")
    ], style={
    "width": "23%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),

    html.Div(children=[
        html.H4("Ejecución mediana no PyME"),
        html.H2(f"{ejecucion_mediana_nopyme:,.1f}%")
    ], style={
    "width": "23%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),

    html.Div(children=[
        html.H4("Contratos con ejecución"),
        html.H2(f"{contratos_con_ejecucion:,}")
    ], style={
    "width": "23%",
    "display": "inline-block",
    "textAlign": "center",
    "verticalAlign": "top",
    "border": "1px solid #ddd",
    "margin": "0.5%",
    "padding": "10px"
}),
]),
dcc.Graph(
    id="grafica-hist-ejecucion",
    figure=fig_hist_ejecucion
),

dcc.Graph(
    id="grafica-box-ejecucion",
    figure=fig_box_ejecucion
)

])
@app.callback(
    Output("grafica-tipo", "figure"),
    Input("filtro-anio", "value")
)
def actualizar_grafica_tipo(anio):

    if anio == "Todos":
        df_filtrado = df
    else:
        df_filtrado = df[df["anio"] == anio]

    resumen_filtrado = (
        df_filtrado
        .groupby("tipo_de_contrato")["valor_del_contrato"]
        .agg(["count", "sum"])
        .reset_index()
    )

    resumen_filtrado.columns = [
        "tipo_de_contrato",
        "numero_contratos",
        "valor_total"
    ]

    resumen_filtrado["porcentaje_valor"] = (resumen_filtrado["valor_total"]
        / resumen_filtrado["valor_total"].sum()
        * 100
    )

    resumen_filtrado["porcentaje_contratos"] = (
        resumen_filtrado["numero_contratos"]
        / resumen_filtrado["numero_contratos"].sum()
        * 100
    )

    resumen_filtrado["valor_total_miles_millones"] = (
        resumen_filtrado["valor_total"] / 1e9
    )

    resumen_filtrado = resumen_filtrado.sort_values(
        "valor_total",
        ascending=True
    )

    fig = px.bar(
        resumen_filtrado,
        x="valor_total_miles_millones",
        y="tipo_de_contrato",
        orientation="h",
        title="Valor contratado por tipo de contrato",
        labels={
            "valor_total_miles_millones": "Valor contratado (miles de millones de pesos)",
            "tipo_de_contrato": "Tipo de contrato",
            "numero_contratos": "Número de contratos",
            "porcentaje_valor": "Porcentaje del valor (%)",
            "porcentaje_contratos": "Porcentaje de contratos (%)"
        },
        hover_data={
            "numero_contratos": True,
            "porcentaje_valor": ":.2f",
            "porcentaje_contratos": ":.2f",
            "valor_total_miles_millones": ":.2f"
        }
    )

    return fig

@app.callback(
    Output("grafica-anio", "figure"),
    Input("filtro-tipo", "value")
)
def actualizar_grafica_anio(tipo):

    if tipo == "Todos":
        df_filtrado = df
    else:
        df_filtrado = df[df["tipo_de_contrato"] == tipo]

    resumen_filtrado = (
        df_filtrado
        .groupby("anio")["valor_del_contrato"]
        .agg(["count", "sum"])
        .reset_index()
    )

    resumen_filtrado.columns = [
        "anio",
        "numero_contratos",
        "valor_total"
    ]

    resumen_filtrado["valor_total_miles_millones"] = (
        resumen_filtrado["valor_total"] / 1e9
    )

    fig = px.bar(
        resumen_filtrado,
        x="anio",
        y="valor_total_miles_millones",
        title="Valor total contratado por año",
        labels={
            "anio": "Año",
            "valor_total_miles_millones": "Valor contratado (miles de millones de pesos)",
            "numero_contratos": "Número de contratos"
        },
        hover_data={
            "numero_contratos": True,
            "valor_total_miles_millones": ":.2f"
        }
    )

    return fig
@app.callback(
    Output("kpi-valor", "children"),
    Output("kpi-numero", "children"),
    Output("kpi-mayor-valor", "children"),
    Output("kpi-mas-frecuente", "children"),
    Input("filtro-anio", "value"),
    Input("filtro-tipo", "value")
)
def actualizar_kpis(anio, tipo):

    df_filtrado = df.copy()

    if anio != "Todos":
        df_filtrado = df_filtrado[df_filtrado["anio"] == anio]

    if tipo != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    valor_total = df_filtrado["valor_del_contrato"].sum()
    valor_total_miles_millones = valor_total / 1e9

    numero_contratos = len(df_filtrado)

    resumen_valor = (
        df_filtrado
        .groupby("tipo_de_contrato")["valor_del_contrato"]
        .sum()
    )

    tipo_mayor_valor = resumen_valor.idxmax()

    tipo_mas_frecuente = (
        df_filtrado["tipo_de_contrato"]
        .value_counts()
        .idxmax()
    )

    return (
        f"${valor_total_miles_millones:,.2f} mil millones",
        f"{numero_contratos:,}",
        tipo_mayor_valor,
        tipo_mas_frecuente
    )
@app.callback(
    Output("grafica-dispersion", "figure"),
    Input("filtro-modalidad", "value")
)
def actualizar_dispersion(modalidad):

    df_filtrado = dfm[dfm["duracion_dias"].notna() & (dfm["duracion_dias"] >= 0)].copy()

    if modalidad != "Todas":
        df_filtrado = df_filtrado[df_filtrado["modalidad_de_contratacion"] == modalidad]

    df_filtrado["log_valor"] = np.log1p(df_filtrado["valor_del_contrato"])

    fig = px.scatter(
        df_filtrado,
        x="duracion_dias",
        y="log_valor",
        color="modalidad_de_contratacion",
        title="Relación entre duración y valor del contrato",
        labels={
            "duracion_dias": "Duración del contrato (días)",
            "log_valor": "Log(1 + valor del contrato)",
            "modalidad_de_contratacion": "Modalidad de contratación"
        },
        opacity=0.5
    )

    return fig
@app.callback(
    Output("grafica-box-ejecucion", "figure"),
    Input("filtro-grupo", "value")
)
def actualizar_box_ejecucion(grupo):

    etiquetas = {
        "es_pyme": "¿Es PyME?",
        "es_grupo": "¿Es consorcio / grupo?",
        "g_nero_representante_legal": "Género del representante legal"
    }

    fig = px.box(
        df_ejec,
        x=grupo,
        y="pct_ejecucion",
        points=False,
        title="Porcentaje de ejecución presupuestal por grupo",
        labels={
            grupo: etiquetas[grupo],
            "pct_ejecucion": "Porcentaje de ejecución (%)"
        }
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
