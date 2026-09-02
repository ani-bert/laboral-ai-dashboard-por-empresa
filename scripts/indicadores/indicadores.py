import pandas as pd
import plotly.express as px


# ============================================================
# FUNCIONES MODULARES PARA INDICADORES
# ============================================================


def calcular_total_unico(df, columna):
    """
    Calcula el total de registros únicos de una columna.

    Puede reutilizarse para contar:
    - Empresas
    - Empleos
    - Postulaciones
    """

    return df[columna].nunique()


def contar_categorias(df, columna, etiqueta_nulos=None):
    """
    Cuenta la cantidad de registros de cada categoría.

    Si se proporciona una etiqueta para los valores nulos,
    estos serán reemplazados antes de realizar el conteo.
    """

    datos = df[columna].copy()

    if etiqueta_nulos is not None:
        datos = datos.fillna(etiqueta_nulos)

    return datos.value_counts()


def generar_ranking(df, columna, top_n=10):
    """
    Genera un ranking de los valores más frecuentes
    de una columna.

    top_n indica la cantidad máxima de resultados.
    """

    return (
        df[columna]
        .dropna()
        .value_counts()
        .head(top_n)
    )


def contar_condicion(df, columna, valor):
    """
    Cuenta la cantidad de registros que cumplen
    una condición determinada.

    Ejemplo:
    contar_condicion(jobs_clean, "isExternalOffer", True)
    """

    return df[columna].eq(valor).sum()


def contar_por_mes(df, columna_fecha):
    """
    Cuenta la cantidad de registros agrupados por mes
    utilizando una columna de fecha.
    """

    datos = df.copy()

    datos[columna_fecha] = pd.to_datetime(
        datos[columna_fecha],
        errors="coerce"
    )

    datos = datos.dropna(
        subset=[columna_fecha]
    )

    datos["mes"] = datos[columna_fecha].dt.to_period("M")

    return (
        datos["mes"]
        .value_counts()
        .sort_index()
    )


def crear_grafico_barras(
    df,
    x,
    y,
    titulo,
    color="#0a99ac"
):
    """
    Crea un gráfico de barras reutilizable
    utilizando Plotly.
    """

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=titulo,
        text=y
    )

    fig.update_traces(
        marker_color=color,
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        hovermode="x unified"
    )

    return fig

# ============================================================
# ESTANDARIZAR MODALIDADES PARA VISUALIZACIÓN
# ============================================================

def normalizar_modalidades(serie):
    """
    Unifica las modalidades sin modificar el dataset original.
    Conserva las categorías desconocidas y etiqueta los nulos.
    """

    modalidades = (
        serie.astype("string")
        .str.strip()
        .str.lower()
    )

    return (
        modalidades
        .replace({
            "hibrido": "Híbrido",
            "híbrido": "Híbrido",
            "presencial": "Presencial",
            "remoto": "Remoto",
            "": "Sin especificar"
        })
        .fillna("Sin especificar")
    )


# ============================================================
# KPIS DE LA VISTA SELECCIONADA
# ============================================================

def calcular_kpis_empresa(
    ofertas,
    postulaciones,
    columna_id_postulacion="_id_application"
):
    """
    Recibe las ofertas y postulaciones previamente filtradas.

    Cuenta identificadores únicos para evitar que los cruces
    incrementen artificialmente los totales.

    No elimina filas ni modifica las tablas recibidas.
    """

    total_ofertas = ofertas["_id"].nunique()

    estados = (
        ofertas["status"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    ofertas_abiertas = ofertas.loc[
        estados.eq("OPEN").fillna(False),
        "_id"
    ].nunique()

    if postulaciones.empty:
        total_postulaciones = 0
    else:
        if columna_id_postulacion not in postulaciones.columns:
            raise ValueError(
                "Falta la columna identificadora de postulaciones: "
                f"{columna_id_postulacion}"
            )

        total_postulaciones = (
            postulaciones[columna_id_postulacion].nunique()
        )

    return {
        "total_ofertas": int(total_ofertas),
        "ofertas_abiertas": int(ofertas_abiertas),
        "total_postulaciones": int(total_postulaciones)
    }