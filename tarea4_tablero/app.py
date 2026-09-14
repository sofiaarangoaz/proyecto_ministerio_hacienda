import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


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

app.layout = html.Div(children=[
    html.H1(children='Contratación del Ministerio de Hacienda y Crédito Público'),

    html.Div(children='''
        ¿Cuánta plata contrató el Ministerio cada año, y en qué tipo de contratos se concentra?
    '''),

    html.Div(children='''
        Tablero interactivo para analizar la evolución y concentración de la contratación.
    '''),

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


if __name__ == '__main__':
    app.run(debug=True)