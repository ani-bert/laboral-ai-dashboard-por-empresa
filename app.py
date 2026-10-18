import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast
import re
import requests
import unicodedata

from collections import Counter
from scripts.constructor import constructor


st.set_page_config(
    page_title="Exploración por empresa | Laboral.ai",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COLORES
# ============================================================

AZUL_OSCURO = "#0B213C"
AZUL_LINEA = "#0B213C"
VERDE_BARRA = "#A6C263"
CELESTE_BARRA = "#66C7D1"
AMARILLO_BARRA = "#FFDE59"
MORADO_BARRA = "#754480"
NARANJA = "#f0901a"


PERU_GEOJSON_URL = (
    "https://raw.githubusercontent.com/"
    "juaneladio/peru-geojson/master/"
    "peru_departamental_simple.geojson"
)


# ============================================================
# 18 ÁREAS PROFESIONALES OFICIALES
# ============================================================

AREAS_OFICIALES = [
    "Administración, Contabilidad y Finanzas",
    "Aduanas y Comercio Exterior",
    "Agricultura, Ganadería y Agroindustria",
    "Arquitectura, Diseño de Interiores y Decoración",
    "Comercial, Ventas y Desarrollo de Negocios",
    "Construcción e Ingeniería Civil",
    "Diseño y Artes Gráficas",
    "Gastronomía, Hotelería y Turismo",
    "Legal y Cumplimiento",
    "Logística, Abastecimiento y Transporte",
    "Mantenimiento y Reparaciones Técnicas",
    "Marketing, Publicidad y Comunicación",
    "Minería, Petróleo, Energía y Gas",
    "Otras Ingenierías",
    "Producción, Manufactura y Operaciones",
    "Recursos Humanos y Capacitación",
    "Salud, Medicina y Farmacia",
    "Tecnología, Sistemas y Telecomunicaciones",
]


# ============================================================
# MAPEO DE CATEGORY A NOMBRE OFICIAL
# ============================================================

CATEGORIA_A_AREA = {

    "administracion-contabilidad-finanzas":
        "Administración, Contabilidad y Finanzas",

    "aduanas-comercio-exterior":
        "Aduanas y Comercio Exterior",

    "agricultura-ganaderia-agroindustria":
        "Agricultura, Ganadería y Agroindustria",

    "arquitectura-diseno-interiores-decoracion":
        "Arquitectura, Diseño de Interiores y Decoración",

    "arquitectura-diseno-de-interiores-decoracion":
        "Arquitectura, Diseño de Interiores y Decoración",

    "comercial-ventas-desarrollo-negocios":
        "Comercial, Ventas y Desarrollo de Negocios",

    "construccion-ingenieria-civil":
        "Construcción e Ingeniería Civil",

    "diseno-artes-graficas":
        "Diseño y Artes Gráficas",

    "gastronomia-hoteleria-turismo":
        "Gastronomía, Hotelería y Turismo",

    "legal-cumplimiento":
        "Legal y Cumplimiento",

    "logistica-abastecimiento-transporte":
        "Logística, Abastecimiento y Transporte",

    "mantenimiento-reparaciones-tecnicas":
        "Mantenimiento y Reparaciones Técnicas",

    "marketing-publicidad-comunicacion":
        "Marketing, Publicidad y Comunicación",

    "mineria-petroleo-energia-gas":
        "Minería, Petróleo, Energía y Gas",

    "otras-ingenierias":
        "Otras Ingenierías",

    "produccion-manufactura-operaciones":
        "Producción, Manufactura y Operaciones",

    "recursos-humanos-capacitacion":
        "Recursos Humanos y Capacitación",

    "salud-medicina-farmacia":
        "Salud, Medicina y Farmacia",

    "tecnologia-sistemas-telecomunicaciones":
        "Tecnología, Sistemas y Telecomunicaciones",
}


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {
    background:#FFFFFF !important;
    color:#172B40 !important;
}

[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] [data-testid="stText"],
[data-testid="stMain"] [data-testid="stMetricValue"],
[data-testid="stMain"] [data-testid="stMetricLabel"] {
    color:#172B40 !important;
}

[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    color:#536679 !important;
}

[data-testid="stMetric"] {
    background:#FFFFFF;
    border:1px solid #E0E5EB;
    border-radius:20px;
    padding:30px 15px;
    text-align:center;
    box-shadow:0 5px 22px rgba(11,33,60,.06);
}

[data-testid="stMetricLabel"] {
    display:flex !important;
    justify-content:center !important;
    width:100% !important;
}

[data-testid="stMetricLabel"] > div {
    width:100% !important;
    justify-content:center !important;
}

[data-testid="stMetricLabel"] p {
    width:100% !important;
    text-align:center !important;
}

[data-testid="stMain"] h3 {
    font-size:22px !important;
    font-weight:600 !important;
    color:#29333F !important;
    line-height:1.35 !important;
}

[data-testid="stMain"] [data-testid="stMetricLabel"] p {
    color:#000000 !important;
    font-weight:700;
    text-align:center;
}

[data-testid="stMain"] [data-testid="stMetricValue"] {
    color:#000000 !important;
    font-weight:700;
    text-align:center;
    font-size:44px;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color:#D3E3EA !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"],
div[data-baseweb="base-input"],
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input {
    background:#F4F9FC !important;
    color:#172B40 !important;
}

div[data-baseweb="select"] > div {
    border-color:#86ADC0 !important;
}

input {
    color:#172B40 !important;
    -webkit-text-fill-color:#172B40 !important;
}

input::placeholder {
    color:#61798A !important;
    -webkit-text-fill-color:#61798A !important;
}

[data-baseweb="popover"],
[role="listbox"],
[role="option"] {
    background:#FFFFFF !important;
    color:#172B40 !important;
}

[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background:#D9EEF7 !important;
}

[data-testid="stButton"] button {
    background:#0B213C !important;
    color:#FFFFFF !important;
    border:1px solid #0B213C !important;
    border-radius:9px;
}

[data-testid="stButton"] button p {
    color:#FFFFFF !important;
}

[data-testid="stButton"] button:hover {
    background:#245776 !important;
}

[data-testid="stNumberInput"] button {
    background:#D9EEF7 !important;
    color:#172B40 !important;
}

button[role="tab"] {
    color:#172B40 !important;
}

button[role="tab"][aria-selected="true"] {
    color:#176B91 !important;
}

[data-testid="stSidebar"] {
    background:#0B213C !important;
}

[data-testid="stSidebarContent"] {
    display:flex !important;
    flex-direction:column !important;
    justify-content:center !important;
    min-height:100vh !important;
    padding-top:18px !important;
    padding-bottom:18px !important;
    overflow-y:auto !important;
}

[data-testid="stSidebarContent"] > div {
    width:100% !important;
    margin-top:0 !important;
    margin-bottom:0 !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap:0.75rem !important;
}

[data-testid="stSidebar"] h2 {
    color:#FFFFFF !important;
    font-size:24px !important;
    font-weight:700 !important;
    margin-top:28px !important;
    margin-bottom:8px !important;
}

[data-testid="stSidebar"] h3 {
    color:#FFFFFF !important;
    font-size:20px !important;
    font-weight:700 !important;
    margin-top:10px !important;
    margin-bottom:5px !important;
}

[data-testid="stSidebar"] label {
    color:#FFFFFF !important;
    font-size:14px !important;
    font-weight:500 !important;
}

[data-testid="stSidebar"] p {
    font-size:13px !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    min-height:38px !important;
    height:38px !important;
    font-size:14px !important;
    border-radius:10px !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] input {
    padding-top:0 !important;
    padding-bottom:0 !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] span {
    font-size:14px !important;
    line-height:38px !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color:#8FA4B8 !important;
    font-size:12px !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button {
    min-height:42px !important;
    font-size:14px !important;
    border-radius:10px !important;
    padding:5px 10px !important;
    border:1px solid #90cae0 !important;
}

.tabla-scroll {
    overflow:auto;
    max-height:480px;
    border:1px solid #C1DCE8;
    border-radius:10px;
    margin-bottom:18px;
}

table.tabla-clara {
    border-collapse:collapse;
    width:100%;
    font-size:14px;
    color:#172B40;
    background:white;
}

.tabla-clara thead th {
    background:#90cae0 !important;
    color:#102C40 !important;
    position:sticky;
    top:0;
    text-align:left;
    padding:13px;
    border-bottom:2px solid #70AAC2;
}

.tabla-clara td {
    padding:12px;
    border-bottom:1px solid #DCE9F0;
    white-space:normal;
    min-width:105px;
    max-width:320px;
}

.tabla-clara td:first-child,
.tabla-clara th:first-child {
    min-width:220px;
}

.tabla-clara td:nth-child(3),
.tabla-clara th:nth-child(3) {
    min-width:230px;
}

.tabla-clara tbody tr:nth-child(even) {
    background:#EEF7FB;
}

.tabla-clara tbody tr:hover {
    background:#DCEFF7;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# IMPORTS INTERNOS
# ============================================================

from scripts.empresas import construir_directorio_empresas

from scripts.indicadores.indicadores import (
    calcular_kpis_empresa,
    normalizar_modalidades,
)


# ============================================================
# CONSTANTES
# ============================================================

TODAS = "__todas__"
SIN_EMPRESA = "__sin_empresa__"
AREA_TODAS = "__todas_areas__"
REGION_TODAS = "__todas_regiones__"


# ============================================================
# FUNCIONES GENERALES
# ============================================================

def texto_limpio(serie):

    return (
        serie
        .astype("string")
        .str.strip()
        .replace({
            "":
                pd.NA,

            "None":
                pd.NA,

            "nan":
                pd.NA,

            "<NA>":
                pd.NA
        })
    )


def fechas_utc(serie):

    return pd.to_datetime(
        serie,
        errors="coerce",
        utc=True,
        format="mixed"
    )


def asegurar_columnas(
    df,
    columnas
):

    resultado = (
        df.copy()
    )


    for columna in columnas:

        if (
            columna
            not in
            resultado.columns
        ):

            resultado[
                columna
            ] = pd.NA


    return resultado


def validar_ids(
    df,
    nombre
):

    if (
        df["_id"].isna().any()
        or
        df["_id"].duplicated().any()
    ):

        raise ValueError(
            f"{nombre}: hay identificadores "
            "vacíos o repetidos."
        )


def clasificar_tipo_oferta(
    valor
):

    if pd.isna(valor):

        return "No definido"


    texto = (
        str(valor)
        .strip()
        .lower()
    )


    if texto in [
        "true",
        "1",
        "1.0",
        "si",
        "sí",
        "yes"
    ]:

        return "Externas"


    if texto in [
        "false",
        "0",
        "0.0",
        "no"
    ]:

        return "Internas"


    return "No definido"


# ============================================================
# PREPARAR MODELO
# ============================================================

def preparar_modelo(
    companies,
    jobs,
    applications
):

    empresas = asegurar_columnas(
        companies,
        [
            "_id",
            "businessName"
        ]
    )


    ofertas = asegurar_columnas(
        jobs,
        [
            "_id",
            "companyId",
            "externalCompanyName",
            "isExternalOffer",
            "createdAt",
            "publishUntil",
            "status",
            "professionalArea",
            "category",
            "modality",
            "title",
            "jobType",
            "geographicDepartment",
            "country",
            "department",
            "requirements",
            "skills",
            "vacancies",
            "workExperience",
            "isFeatured"
        ]
    )


    postulaciones = asegurar_columnas(
        applications,
        [
            "_id",
            "job",
            "createdAt",
            "applicationStatus"
        ]
    )


    n_ofertas = len(
        ofertas
    )

    n_postulaciones = len(
        postulaciones
    )


    for datos in (
        empresas,
        ofertas,
        postulaciones
    ):

        datos[
            "_id"
        ] = texto_limpio(
            datos[
                "_id"
            ]
        )


    validar_ids(
        empresas,
        "Empresas"
    )


    validar_ids(
        ofertas,
        "Ofertas"
    )


    validar_ids(
        postulaciones,
        "Postulaciones"
    )


    ofertas[
        "createdAt"
    ] = fechas_utc(
        ofertas[
            "createdAt"
        ]
    )


    ofertas[
        "publishUntil"
    ] = fechas_utc(
        ofertas[
            "publishUntil"
        ]
    )


    ofertas[
        "tipo_oferta"
    ] = (
        ofertas[
            "isExternalOffer"
        ]
        .apply(
            clasificar_tipo_oferta
        )
    )


    marca_original = (
        ofertas[
            "isExternalOffer"
        ]
        .copy()
    )


    ofertas[
        "isExternalOffer"
    ] = (
        ofertas[
            "tipo_oferta"
        ]
        .map({
            "Externas":
                True,

            "Internas":
                False
        })
        .astype(
            "boolean"
        )
    )


    directorio, ofertas = (
        construir_directorio_empresas(
            empresas,
            ofertas
        )
    )


    ofertas[
        "isExternalOffer"
    ] = marca_original


    # ========================================================
    # EMPRESAS GENÉRICAS
    # ========================================================

    nombre = (
        texto_limpio(
            ofertas[
                "externalCompanyName"
            ]
        )
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
        .str.casefold()
    )


    genericos = {
        "confidencial",
        "empresa confidencial",
        "importante",
        "importante del sector",
        "importante empresa del sector",
        "importante empresa en el sector",
        "empresa importante en el sector",
        "empresa no especificada",
        "empresas no especificadas",
        "empresa no identificada",
        "sin especificar",
        "no especificada",
        "no especificado",
        "sin información",
        "sin informacion",
    }


    interna = (
        ofertas[
            "empresa_clave"
        ]
        .str.startswith(
            "interna:",
            na=False
        )
    )


    desconocida = (
        ofertas[
            "empresa_clave"
        ].isna()
        |
        (
            ~interna
            &
            nombre.isin(
                genericos
            )
        )
    )


    claves_genericas = set(
        ofertas.loc[
            desconocida,
            "empresa_clave"
        ]
        .dropna()
    )


    directorio = (
        directorio.loc[
            ~directorio[
                "empresa_clave"
            ]
            .isin(
                claves_genericas
            )
        ]
        .copy()
    )


    ofertas.loc[
        desconocida,
        "empresa_clave"
    ] = SIN_EMPRESA


    ofertas.loc[
        desconocida,
        "empresa_nombre"
    ] = "Empresas no especificadas"


    ofertas.loc[
        desconocida,
        "empresa_origen"
    ] = "Sin identificar"


    if desconocida.any():

        grupo = pd.DataFrame([
            {
                "empresa_clave":
                    SIN_EMPRESA,

                "empresa_nombre":
                    "Empresas no especificadas",

                "empresa_origen":
                    "Sin identificar",

                "total_ofertas":
                    int(
                        ofertas.loc[
                            desconocida,
                            "_id"
                        ]
                        .nunique()
                    ),

                "ultima_publicacion":
                    ofertas.loc[
                        desconocida,
                        "createdAt"
                    ]
                    .max()
            }
        ])


        directorio = pd.concat(
            [
                directorio,
                grupo
            ],
            ignore_index=True
        )


    directorio[
        "ultima_publicacion"
    ] = fechas_utc(
        directorio[
            "ultima_publicacion"
        ]
    )


    directorio[
        "total_ofertas"
    ] = (
        directorio[
            "total_ofertas"
        ]
        .fillna(0)
        .astype(int)
    )


    # ========================================================
    # ESTADO
    # ========================================================

    ofertas[
        "status"
    ] = (
        texto_limpio(
            ofertas[
                "status"
            ]
        )
        .str.upper()
    )


    ofertas[
        "estado_visual"
    ] = (
        ofertas[
            "status"
        ]
        .replace({
            "OPEN":
                "Abierta",

            "CLOSED":
                "Cerrada"
        })
        .fillna(
            "Sin especificar"
        )
    )


    # ========================================================
    # ÁREA PROFESIONAL FINAL
    #
    # 1. Si existe category → usar category oficial.
    # 2. Si no existe → usar professionalArea reclasificada.
    # ========================================================

    categoria = texto_limpio(
        ofertas[
            "category"
        ]
    )


    categoria_visual = (
        categoria
        .str.casefold()
        .map(
            CATEGORIA_A_AREA
        )
    )


    area_historica = (
        texto_limpio(
            ofertas[
                "professionalArea"
            ]
        )
    )


    ofertas[
        "area_visual"
    ] = (
        categoria_visual
        .fillna(
            area_historica
        )
        .fillna(
            "Otras Ingenierías"
        )
    )


    # Garantizar que el resultado pertenezca
    # a la taxonomía oficial.

    ofertas.loc[
        ~ofertas[
            "area_visual"
        ].isin(
            AREAS_OFICIALES
        ),
        "area_visual"
    ] = "Otras Ingenierías"


    # ========================================================
    # MODALIDAD Y TÍTULO
    # ========================================================

    ofertas[
        "modalidad_visual"
    ] = normalizar_modalidades(
        ofertas[
            "modality"
        ]
    )


    ofertas[
        "title"
    ] = (
        texto_limpio(
            ofertas[
                "title"
            ]
        )
        .fillna(
            "Sin título"
        )
    )


    # ========================================================
    # POSTULACIONES
    # ========================================================

    postulaciones[
        "_id"
    ] = texto_limpio(
        postulaciones[
            "_id"
        ]
    )


    postulaciones[
        "job"
    ] = texto_limpio(
        postulaciones[
            "job"
        ]
    )


    postulaciones[
        "createdAt"
    ] = fechas_utc(
        postulaciones[
            "createdAt"
        ]
    )


    postulaciones[
        "applicationStatus"
    ] = (
        texto_limpio(
            postulaciones[
                "applicationStatus"
            ]
        )
        .fillna(
            "Sin estado"
        )
    )


    postulaciones[
        "oferta_encontrada"
    ] = (
        postulaciones[
            "job"
        ]
        .isin(
            ofertas[
                "_id"
            ]
        )
    )


    if (
        len(ofertas)
        !=
        n_ofertas
        or
        len(postulaciones)
        !=
        n_postulaciones
    ):

        raise ValueError(
            "La preparación cambió "
            "la cantidad de registros."
        )


    return (
        directorio,
        ofertas,
        postulaciones
    )


# ============================================================
# FILTRAR DATOS
# ============================================================

def filtrar_datos(
    ofertas,
    postulaciones,
    empresa=TODAS,
    area=AREA_TODAS,
    region=REGION_TODAS,
    destacada="Todas",
    inicio=None,
    fin=None,
    tipo="Todas"
):

    mascara = pd.Series(
        True,
        index=ofertas.index
    )


    if tipo != "Todas":

        mascara &= (
            ofertas[
                "tipo_oferta"
            ]
            .eq(
                tipo
            )
        )


    if empresa != TODAS:

        mascara &= (
            ofertas[
                "empresa_clave"
            ]
            .eq(
                empresa
            )
        )


    if area != AREA_TODAS:

        mascara &= (
            ofertas[
                "area_visual"
            ]
            .eq(
                area
            )
        )


    if region != REGION_TODAS:

        region_oferta = (
            ofertas[
                "geographicDepartment"
            ]
            .fillna(
                "Sin especificar"
            )
            .astype(str)
            .str.strip()
            .replace({
                "":
                    "Sin especificar",

                "None":
                    "Sin especificar",

                "nan":
                    "Sin especificar",

                "<NA>":
                    "Sin especificar"
            })
        )


        mascara &= (
            region_oferta
            .eq(
                region
            )
        )


    # ========================================================
    # OFERTA DESTACADA
    # ========================================================

    if destacada != "Todas":

        destacada_oferta = (
            ofertas[
                "isFeatured"
            ]
            .astype(
                "string"
            )
            .str.strip()
            .str.lower()
        )


        es_destacada = (
            destacada_oferta
            .isin([
                "true",
                "1",
                "1.0",
                "si",
                "sí",
                "yes"
            ])
        )


        es_no_destacada = (
            destacada_oferta
            .isin([
                "false",
                "0",
                "0.0",
                "no"
            ])
        )


        if (
            destacada
            ==
            "Destacadas"
        ):

            mascara &= (
                es_destacada
            )


        elif (
            destacada
            ==
            "No destacadas"
        ):

            mascara &= (
                es_no_destacada
            )


        elif (
            destacada
            ==
            "No definido"
        ):

            mascara &= ~(
                es_destacada
                |
                es_no_destacada
            )


    # ========================================================
    # FECHAS
    # ========================================================

    if (
        inicio is not None
        and
        fin is not None
    ):

        desde = pd.Timestamp(
            inicio,
            tz="UTC"
        )


        hasta = (
            pd.Timestamp(
                fin,
                tz="UTC"
            )
            +
            pd.Timedelta(
                days=1
            )
        )


        mascara &= (
            ofertas[
                "createdAt"
            ].ge(
                desde
            )
            &
            ofertas[
                "createdAt"
            ].lt(
                hasta
            )
        )


    vista = (
        ofertas.loc[
            mascara.fillna(
                False
            )
        ]
        .copy()
    )


    sin_restricciones = (
        empresa == TODAS
        and
        area == AREA_TODAS
        and
        region == REGION_TODAS
        and
        destacada == "Todas"
        and
        inicio is None
        and
        fin is None
        and
        tipo == "Todas"
    )


    if sin_restricciones:

        solicitudes = (
            postulaciones.copy()
        )

    else:

        solicitudes = (
            postulaciones.loc[
                postulaciones[
                    "job"
                ]
                .isin(
                    vista[
                        "_id"
                    ]
                )
            ]
            .copy()
        )


    return (
        vista,
        solicitudes
    )


# ============================================================
# DETALLE DE OFERTAS
# ============================================================

def detalle_ofertas(
    ofertas,
    postulaciones
):

    detalle = (
        ofertas.copy()
    )


    conteos = (
        postulaciones
        .groupby(
            "job"
        )[
            "_id"
        ]
        .nunique()
    )


    vacantes_num = pd.to_numeric(
        detalle["vacancies"],
        errors="coerce"
    )

    detalle["Vacantes"] = vacantes_num.apply(
        lambda x: (
            int(x)
            if pd.notna(x) and x > 0
            else "No informado"
        )
)

    detalle[
        "Postulaciones"
    ] = (
        detalle[
            "_id"
        ]
        .map(
            conteos
        )
        .fillna(0)
        .astype(int)
    )


    detalle[
        "Fecha de creación"
    ] = (
        detalle[
            "createdAt"
        ]
        .dt.strftime(
            "%d/%m/%Y"
        )
        .fillna(
            "Sin fecha"
        )
    )


    detalle[
        "Vencimiento"
    ] = (
        detalle[
            "publishUntil"
        ]
        .dt.strftime(
            "%d/%m/%Y"
        )
        .fillna(
            "Sin fecha"
        )
    )


    detalle = detalle.rename(
        columns={
            "_id":
                "ID de oferta",

            "title":
                "Puesto",

            "empresa_nombre":
                "Empresa",

            "area_visual":
                "Área",

            "modalidad_visual":
                "Modalidad",

            "estado_visual":
                "Estado",

            "geographicDepartment":
                "Ubicación"
        }
    )


    return detalle[
        [
            "ID de oferta",
            "Puesto",
            "Empresa",
            "Área",
            "Modalidad",
            "Ubicación",
            "Estado",
            "Vacantes",
            "Fecha de creación",
            "Vencimiento",
            "Postulaciones"
        ]
    ]


# ============================================================
# HERRAMIENTAS / SKILLS
# ============================================================

REGLAS_REQUISITOS = {

    "Excel": [
        r"\bexcel\b",
        r"\bhojas? de calculo\b"
    ],

    "Microsoft Office": [
        r"\bmicrosoft office\b",
        r"\bms office\b",
        r"\boffice\b",
        r"\bofimatica\b"
    ],

    "Word": [
        r"\bmicrosoft word\b",
        r"\bms word\b",
        r"\bword\b"
    ],

    "PowerPoint": [
        r"\bmicrosoft powerpoint\b",
        r"\bpowerpoint\b",
        r"\bpower point\b",
        r"\bppt\b"
    ],

    "Power BI": [
        r"\bpower\s*bi\b",
        r"\bpowerbi\b"
    ],

    "Google Analytics": [
        r"\bgoogle analytics\b",
        r"\bga4\b"
    ],

    "SQL": [
        r"\bsql\b(?!\s*server)"
    ],

    "SQL Server": [
        r"\bsql\s*server\b"
    ],

    "MySQL": [
        r"\bmysql\b"
    ],

    "PostgreSQL": [
        r"\bpostgresql\b",
        r"\bpostgres\b"
    ],

    "Python": [
        r"\bpython\b"
    ],

    "Canva": [
        r"\bcanva\b"
    ],

    "SAP": [
        r"\bsap\b",
        r"\bsap business one\b"
    ],

    "ERP": [
        r"\berp\b",
        r"\berps\b",
        r"\bodoo\b"
    ],

    "Photoshop": [
        r"\bphotoshop\b"
    ],

    "Illustrator": [
        r"\billustrator\b"
    ],

    "Premiere Pro": [
        r"\bpremiere\b",
        r"\bpremiere pro\b"
    ],

    "AutoCAD": [
        r"\bautocad\b"
    ],

    "CRM": [
        r"\bcrm\b",
        r"\bhubspot\b",
        r"\bsalesforce\b"
    ],

    "Figma": [
        r"\bfigma\b"
    ],

    "Tableau": [
        r"\btableau\b"
    ],

    "Looker Studio": [
        r"\blooker studio\b"
    ],

    "Google Ads": [
        r"\bgoogle ads\b"
    ],

    "Meta Ads": [
        r"\bmeta ads\b",
        r"\bfacebook ads\b"
    ],

    "TikTok Ads": [
        r"\btiktok ads\b"
    ],

    "Power Query": [
        r"\bpower query\b"
    ],

    "Azure": [
        r"\bazure\b"
    ],

    "AWS": [
        r"\baws\b",
        r"\bamazon web services\b"
    ],

    "Git/GitHub": [
        r"\bgit\b",
        r"\bgithub\b"
    ],

    "Java": [
        r"\bjava\b"
    ],

    "JavaScript": [
        r"\bjavascript\b",
        r"\btypescript\b"
    ]
}


HERRAMIENTAS_TECNICAS = set(
    REGLAS_REQUISITOS.keys()
)


def extraer_textos_requisitos(
    valor
):

    if valor is None:
        return []


    if (
        not isinstance(
            valor,
            (
                list,
                dict
            )
        )
        and
        pd.isna(
            valor
        )
    ):
        return []


    if isinstance(
        valor,
        str
    ):

        try:

            valor = ast.literal_eval(
                valor
            )

        except (
            ValueError,
            SyntaxError
        ):

            return [
                valor
            ]


    if isinstance(
        valor,
        dict
    ):

        valor = [
            valor
        ]


    if not isinstance(
        valor,
        list
    ):

        return [
            str(
                valor
            )
        ]


    textos = []


    for requisito in valor:

        if isinstance(
            requisito,
            dict
        ):

            texto = (
                requisito.get(
                    "text"
                )
            )

        else:

            texto = requisito


        if (
            texto is not None
            and
            str(
                texto
            ).strip()
        ):

            textos.append(
                str(
                    texto
                )
            )


    return textos


def extraer_textos_skills(
    valor
):

    if valor is None:
        return []


    if (
        not isinstance(
            valor,
            (
                list,
                dict
            )
        )
        and
        pd.isna(
            valor
        )
    ):
        return []


    if isinstance(
        valor,
        str
    ):

        texto = (
            valor.strip()
        )


        if not texto:
            return []


        try:

            valor = ast.literal_eval(
                texto
            )

        except (
            ValueError,
            SyntaxError
        ):

            return [
                texto
            ]


    if isinstance(
        valor,
        dict
    ):

        for clave in [
            "name",
            "skill",
            "label",
            "title",
            "text"
        ]:

            dato = valor.get(
                clave
            )


            if (
                dato is not None
                and
                str(
                    dato
                ).strip()
            ):

                return [
                    str(
                        dato
                    ).strip()
                ]


        textos = []


        for dato in valor.values():

            textos.extend(
                extraer_textos_skills(
                    dato
                )
            )


        return textos


    if isinstance(
        valor,
        (
            list,
            tuple,
            set
        )
    ):

        textos = []


        for item in valor:

            textos.extend(
                extraer_textos_skills(
                    item
                )
            )


        return textos


    texto = str(
        valor
    ).strip()


    if texto:

        return [
            texto
        ]


    return []


def normalizar_termino(
    texto
):

    texto = unicodedata.normalize(
        "NFKD",
        str(
            texto
        )
        .casefold()
    )


    return "".join(
        letra
        for letra in texto
        if not unicodedata.combining(
            letra
        )
    )


def categorias_herramientas_desde_textos(
    textos
):

    categorias = set()


    for texto in textos:

        limpio = normalizar_termino(
            texto
        )


        for categoria in HERRAMIENTAS_TECNICAS:

            patrones = (
                REGLAS_REQUISITOS[
                    categoria
                ]
            )


            if any(
                re.search(
                    patron,
                    limpio
                )
                for patron in patrones
            ):

                categorias.add(
                    categoria
                )


    return categorias


def top_terminos_requisitos(
    ofertas,
    limite=10
):

    conteos = Counter()

    ofertas_con_requisitos = 0


    for _, oferta in ofertas.iterrows():

        # ================================================
        # FUENTE NUEVA PRINCIPAL
        # ================================================

        textos_skills = (
            extraer_textos_skills(
                oferta.get(
                    "skills"
                )
            )
        )


        if textos_skills:

            categorias_oferta = (
                categorias_herramientas_desde_textos(
                    textos_skills
                )
            )


        # ================================================
        # RESPALDO HISTÓRICO
        # ================================================

        else:

            textos_requirements = (
                extraer_textos_requisitos(
                    oferta.get(
                        "requirements"
                    )
                )
            )


            categorias_oferta = (
                categorias_herramientas_desde_textos(
                    textos_requirements
                )
            )


        if categorias_oferta:

            ofertas_con_requisitos += 1

            conteos.update(
                categorias_oferta
            )


    tabla = pd.DataFrame(
        conteos.most_common(
            limite
        ),
        columns=[
            "Término",
            "Ofertas"
        ]
    )


    return (
        tabla,
        ofertas_con_requisitos
    )

# ============================================================
# GEOJSON DEL PERÚ
# ============================================================

@st.cache_data(show_spinner=False)
def cargar_geojson_peru():

    respuesta = requests.get(
        PERU_GEOJSON_URL,
        timeout=30
    )

    respuesta.raise_for_status()

    return respuesta.json()


# ============================================================
# MAPA DE OFERTAS Y VACANTES
# ============================================================

def grafico_mapa_ofertas(ofertas):

    if ofertas.empty:

        st.info(
            "No hay ofertas para construir el mapa."
        )

        return


    departamentos = (
        texto_limpio(
            ofertas[
                "geographicDepartment"
            ]
        )
        .dropna()
    )


    if departamentos.empty:

        st.info(
            "Las ofertas seleccionadas no tienen "
            "departamento registrado."
        )

        return


    base_mapa = ofertas.copy()


    base_mapa[
        "Departamento"
    ] = (
        texto_limpio(
            base_mapa[
                "geographicDepartment"
            ]
        )
        .map(
            normalizar_termino
        )
    )


    base_mapa[
        "vacancies"
    ] = (
        pd.to_numeric(
            base_mapa[
                "vacancies"
            ],
            errors="coerce"
        )
        .fillna(0)
    )


    ofertas_dep = (
        base_mapa[
            "Departamento"
        ]
        .dropna()
        .value_counts()
        .rename_axis(
            "Departamento"
        )
        .reset_index(
            name="Ofertas"
        )
    )


    vacantes_dep = (
        base_mapa
        .dropna(
            subset=[
                "Departamento"
            ]
        )
        .groupby(
            "Departamento",
            as_index=False
        )[
            "vacancies"
        ]
        .sum()
        .rename(
            columns={
                "vacancies":
                    "Vacantes"
            }
        )
    )


    conteos = (
        ofertas_dep
        .merge(
            vacantes_dep,
            on="Departamento",
            how="left"
        )
    )


    conteos[
        "Vacantes"
    ] = (
        conteos[
            "Vacantes"
        ]
        .fillna(0)
    )


    try:

        geojson = cargar_geojson_peru()


        for feature in geojson.get(
            "features",
            []
        ):

            propiedades = (
                feature.setdefault(
                    "properties",
                    {}
                )
            )


            propiedades[
                "DEPARTAMENTO_NORMALIZADO"
            ] = normalizar_termino(
                propiedades.get(
                    "NOMBDEP",
                    ""
                )
            )


        mapa = pd.DataFrame({

            "Departamento": [
                feature
                .get(
                    "properties",
                    {}
                )
                .get(
                    "DEPARTAMENTO_NORMALIZADO",
                    ""
                )

                for feature in geojson.get(
                    "features",
                    []
                )
            ],

            "Nombre": [
                feature
                .get(
                    "properties",
                    {}
                )
                .get(
                    "NOMBDEP",
                    ""
                )

                for feature in geojson.get(
                    "features",
                    []
                )
            ]

        }).drop_duplicates(
            "Departamento"
        )


        mapa = (
            mapa.merge(
                conteos,
                on="Departamento",
                how="left"
            )
        )


        mapa[
            "Ofertas"
        ] = (
            mapa[
                "Ofertas"
            ]
            .fillna(0)
        )


        mapa[
            "Vacantes"
        ] = (
            mapa[
                "Vacantes"
            ]
            .fillna(0)
        )


        fig = px.choropleth(

            mapa,

            geojson=geojson,

            locations="Departamento",

            featureidkey=(
                "properties."
                "DEPARTAMENTO_NORMALIZADO"
            ),

            color="Ofertas",

            color_continuous_scale=[
                [
                    0.00,
                    "#EEF2F6"
                ],
                [
                    0.15,
                    "#D4F0F3"
                ],
                [
                    0.40,
                    "#66C7D1"
                ],
                [
                    0.70,
                    "#0A99AD"
                ],
                [
                    1.00,
                    "#077F8F"
                ]
            ],

            hover_name="Nombre",

            hover_data={
                "Ofertas":
                    True,

                "Vacantes":
                    True,

                "Departamento":
                    False,

                "Nombre":
                    False
            }
        )


        fig.update_traces(

            marker_line_color="#FFFFFF",

            marker_line_width=1.2,

            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Ofertas: <b>%{z}</b><br>"
                "Vacantes: <b>%{customdata[1]}</b>"
                "<extra></extra>"
            )
        )


        fig.update_geos(

            fitbounds="geojson",

            visible=False,

            showcountries=False,

            showcoastlines=False,

            showland=False,

            showframe=False,

            bgcolor=(
                "rgba(0,0,0,0)"
            )
        )


        fig.update_layout(

            height=560,

            paper_bgcolor=(
                "rgba(0,0,0,0)"
            ),

            plot_bgcolor=(
                "rgba(0,0,0,0)"
            ),

            margin=dict(
                l=0,
                r=0,
                t=55,
                b=0
            ),

            coloraxis_colorbar=dict(

                title="Ofertas",

                orientation="h",

                x=0.5,

                xanchor="center",

                y=1.02,

                yanchor="bottom",

                len=0.62,

                thickness=12,

                outlinewidth=0
            )
        )


        st.plotly_chart(

            fig,

            use_container_width=True,

            theme=None,

            key="mapa_ofertas",

            config={
                "displayModeBar":
                    False,

                "responsive":
                    True,

                "scrollZoom":
                    False
            }
        )


    except requests.RequestException:

        st.warning(
            "No se pudo cargar el mapa "
            "departamental del Perú."
        )


# ============================================================
# FUNCIONES VISUALES
# ============================================================

def formato_numero(valor):

    return (
        f"{int(valor):,}"
        .replace(
            ",",
            "."
        )
    )


def estilo_figura(
    fig,
    altura=330
):

    fig.update_layout(

        template="plotly_white",

        height=altura,

        paper_bgcolor=(
            "rgba(0,0,0,0)"
        ),

        plot_bgcolor=(
            "rgba(0,0,0,0)"
        ),

        showlegend=False,

        font=dict(
            family="Arial",
            size=12,
            color="#59636F"
        ),

        margin=dict(
            l=10,
            r=55,
            t=25,
            b=15
        ),

        xaxis_title=None,

        yaxis_title=None
    )


    fig.update_xaxes(
        zeroline=False,
        automargin=True
    )


    fig.update_yaxes(
        zeroline=False,
        automargin=True
    )


    return fig


def barras(
    datos,
    categoria,
    valor,
    color,
    key
):

    if datos.empty:

        st.info(
            "No hay datos para esta selección."
        )

        return


    fig = px.bar(

        datos,

        x=valor,

        y=categoria,

        orientation="h",

        text=valor
    )


    fig.update_traces(

        marker_color=color,

        textposition="outside",

        cliponaxis=False,

        hovertemplate=(
            "%{y}<br>"
            "%{x}"
            "<extra></extra>"
        )
    )


    estilo_figura(

        fig,

        max(
            310,
            min(
                650,
                len(datos) * 35 + 70
            )
        )
    )


    fig.update_yaxes(

        categoryorder=(
            "total ascending"
        ),

        showgrid=False
    )


    fig.update_xaxes(

        showgrid=True,

        gridcolor="#EEF1F4",

        range=[
            0,
            max(
                1,
                float(
                    datos[
                        valor
                    ].max()
                )
            )
            * 1.22
        ],

        rangemode="tozero",

        tickformat=",d"
    )


    st.plotly_chart(

        fig,

        use_container_width=True,

        key=key,

        theme=None,

        config={
            "displayModeBar":
                False
        }
    )


def grafico_categorias(
    datos,
    columna,
    color,
    key,
    top=10
):

    serie = (
        texto_limpio(
            datos[
                columna
            ]
        )
        .fillna(
            "Sin especificar"
        )
    )


    conteos = (
        serie
        .value_counts()
        .head(top)
    )


    tabla = (
        conteos
        .rename_axis(
            "Categoría"
        )
        .reset_index(
            name="Cantidad"
        )
    )


    barras(
        tabla,
        "Categoría",
        "Cantidad",
        color,
        key
    )


    if (
        serie.nunique()
        >
        top
    ):

        st.caption(
            f"Se muestran las {top} "
            "categorías con más registros."
        )


def grafico_modalidades(
    datos
):

    if datos.empty:

        st.info(
            "No hay ofertas para esta selección."
        )

        return


    tabla = (
        datos[
            "modalidad_visual"
        ]
        .value_counts()
        .rename_axis(
            "Modalidad"
        )
        .reset_index(
            name="Ofertas"
        )
    )


    fig = px.pie(

        tabla,

        names="Modalidad",

        values="Ofertas",

        color="Modalidad",

        color_discrete_map={
            "Presencial":
                "#66c7d1",

            "Híbrido":
                "#0a99ad",

            "Remoto":
                "#077f8f",

            "Sin especificar":
                "#B7BDC5"
        }
    )


    fig.update_traces(

        textposition="outside",

        textinfo=(
            "label+percent+value"
        ),

        marker=dict(
            line=dict(
                color="white",
                width=2
            )
        ),

        hovertemplate=(
            "%{label}<br>"
            "%{value} ofertas · "
            "%{percent}"
            "<extra></extra>"
        )
    )


    fig.update_layout(

        template="plotly_white",

        height=370,

        showlegend=False,

        paper_bgcolor="white",

        font=dict(
            color="#172B40",
            size=13
        ),

        margin=dict(
            l=65,
            r=65,
            t=40,
            b=40
        )
    )


    st.plotly_chart(

        fig,

        use_container_width=True,

        theme=None,

        key="modalidades",

        config={
            "displayModeBar":
                False
        }
    )


def mostrar_tabla(
    datos,
    key
):

    visible = (
        datos
        .drop(
            columns=[
                "ID de oferta"
            ],
            errors="ignore"
        )
    )


    if visible.empty:

        st.info(
            "No hay registros para mostrar."
        )

        return


    paginas = max(
        1,
        (
            len(visible)
            +
            49
        )
        //
        50
    )


    pagina = 1


    if paginas > 1:

        estado = (
            f"tabla_pagina_{key}"
        )


        st.session_state[
            estado
        ] = min(
            int(
                st.session_state.get(
                    estado,
                    1
                )
            ),
            paginas
        )


        pagina = int(

            st.number_input(

                "Página de la tabla",

                min_value=1,

                max_value=paginas,

                step=1,

                key=estado
            )
        )


        st.caption(
            f"{len(visible)} registros · "
            f"Página {pagina} de {paginas}"
        )


    html = (
        visible
        .iloc[
            (pagina - 1) * 50:
            pagina * 50
        ]
        .to_html(
            index=False,
            escape=True,
            classes="tabla-clara",
            border=0,
            na_rep="Sin especificar"
        )
    )


    st.markdown(

        '<div class="tabla-scroll">'
        +
        html
        +
        '</div>',

        unsafe_allow_html=True
    )


def grafico_mensual(
    datos,
    color,
    key,
    linea=True
):

    fechas = fechas_utc(
        datos[
            "createdAt"
        ]
    )


    validas = fechas.dropna()


    if validas.empty:

        st.info(
            "No hay fechas válidas "
            "para construir esta gráfica."
        )

        return


    meses = (
        validas
        .dt
        .tz_localize(None)
        .dt
        .to_period("M")
    )


    conteos = (
        meses
        .value_counts()
        .sort_index()
    )


    if (
        (
            meses.max()
            -
            meses.min()
        ).n
        <=
        240
    ):

        conteos = (
            conteos.reindex(

                pd.period_range(
                    meses.min(),
                    meses.max(),
                    freq="M"
                ),

                fill_value=0
            )
        )


    tabla = pd.DataFrame({

        "Mes":
            conteos.index.astype(str),

        "Cantidad":
            conteos.values
    })


    if linea:

        fig = px.line(

            tabla,

            x="Mes",

            y="Cantidad",

            markers=True
        )


        rgb = tuple(

            int(
                color
                .lstrip("#")[
                    i:
                    i + 2
                ],
                16
            )

            for i in (
                0,
                2,
                4
            )
        )


        fig.update_traces(

            line_color=color,

            fill="tozeroy",

            fillcolor=(
                f"rgba("
                f"{rgb[0]},"
                f"{rgb[1]},"
                f"{rgb[2]},"
                f"0.18)"
            )
        )

    else:

        fig = px.bar(

            tabla,

            x="Mes",

            y="Cantidad",

            text="Cantidad"
        )


        fig.update_traces(

            marker_color=color,

            textposition="outside",

            cliponaxis=False
        )


    estilo_figura(
        fig
    )


    fig.update_xaxes(

        type="category",

        showgrid=False
    )


    fig.update_yaxes(

        gridcolor="#EEF1F4",

        tickformat=",d",

        range=[
            0,
            max(
                1,
                int(
                    tabla[
                        "Cantidad"
                    ].max()
                )
            )
            *
            1.25
        ]
    )


    st.plotly_chart(

        fig,

        use_container_width=True,

        key=key,

        theme=None,

        config={
            "displayModeBar":
                False
        }
    )


# ============================================================
# CACHÉ Y CALLBACKS
# ============================================================

@st.cache_data(
    show_spinner=False
)
def cargar_datos_empresa():

    tablas = constructor()


    modelo = preparar_modelo(
        tablas[0],
        tablas[1],
        tablas[2]
    )


    return (
        *modelo,
        pd.Timestamp.now(
            tz="America/Lima"
        )
    )


def limpiar_filtros_empresa():

    st.session_state[
        "tipo_empresa_filtro"
    ] = "Todas"


    st.session_state[
        "empresa_filtro"
    ] = TODAS


    st.session_state[
        "area_filtro"
    ] = AREA_TODAS


    st.session_state[
        "region_filtro"
    ] = REGION_TODAS


    st.session_state[
        "periodo_filtro"
    ] = "Completo"


    st.session_state[
        "destacada_filtro"
    ] = "Todas"


    for clave in (
        "fecha_desde",
        "fecha_hasta"
    ):

        st.session_state.pop(
            clave,
            None
        )


    st.session_state[
        "busqueda_directorio"
    ] = ""


    st.session_state[
        "origen_directorio"
    ] = "Todas"


    st.session_state[
        "pagina_directorio"
    ] = 1


def cambiar_empresa():

    st.session_state[
        "area_filtro"
    ] = AREA_TODAS


def cambiar_tipo_empresa():

    st.session_state[
        "empresa_filtro"
    ] = TODAS


    st.session_state[
        "area_filtro"
    ] = AREA_TODAS


# ============================================================
# APP PRINCIPAL
# ============================================================

def main():

    st.title(
        "Exploración por empresa"
    )


    st.caption(
        "Laboral.ai — Ofertas laborales "
        "y postulaciones registradas"
    )


    try:

        with st.spinner(
            "Cargando empresas y ofertas "
            "desde MongoDB..."
        ):

            (
                directorio,
                ofertas,
                postulaciones,
                actualizado
            ) = cargar_datos_empresa()


    except Exception as error:

        st.error(
            "No se pudieron cargar los datos "
            "desde MongoDB. "
            f"Tipo de error: "
            f"{type(error).__name__}."
        )


        if isinstance(
            error,
            ValueError
        ):

            st.warning(
                str(error)
            )


        st.button(
            "Reintentar carga",
            on_click=(
                cargar_datos_empresa.clear
            )
        )


        st.stop()


    por_clave = (
        directorio
        .set_index(
            "empresa_clave"
        )
    )


    tipos = [
        "Todas",
        "Internas",
        "Externas",
        "No definido"
    ]


    if (
        st.session_state.get(
            "tipo_empresa_filtro"
        )
        not in
        tipos
    ):

        st.session_state[
            "tipo_empresa_filtro"
        ] = "Todas"


    tipo = (
        st.session_state[
            "tipo_empresa_filtro"
        ]
    )


    base_tipo = (

        ofertas

        if tipo == "Todas"

        else

        ofertas.loc[
            ofertas[
                "tipo_oferta"
            ].eq(
                tipo
            )
        ]
    )


    directorio_tipo = (

        directorio

        if tipo == "Todas"

        else

        directorio.loc[
            directorio[
                "empresa_clave"
            ]
            .isin(
                base_tipo[
                    "empresa_clave"
                ]
            )
        ]
    )


    nombres = {
        TODAS:
            "Todas"
    }


    for fila in (
        directorio_tipo
        .itertuples()
    ):

        nombre = str(
            fila.empresa_nombre
        )


        if (
            fila.empresa_clave
            ==
            SIN_EMPRESA
        ):

            nombre = (
                "Ofertas sin empresa "
                "identificada"
            )


        nombres[
            fila.empresa_clave
        ] = nombre


    opciones = (
        [
            TODAS
        ]
        +
        sorted(
            [
                clave
                for clave
                in nombres
                if clave != TODAS
            ],
            key=lambda clave:
                nombres[
                    clave
                ]
                .casefold()
        )
    )


    if (
        st.session_state.get(
            "empresa_filtro"
        )
        not in
        opciones
    ):

        st.session_state[
            "empresa_filtro"
        ] = TODAS


    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.markdown(
            "## Laboral.ai"
        )


        st.caption(
            "Análisis de empresas"
        )


        st.markdown(
            "### Filtros"
        )


        st.selectbox(

            "Tipo de oferta",

            tipos,

            key=(
                "tipo_empresa_filtro"
            ),

            on_change=(
                cambiar_tipo_empresa
            )
        )


        empresa = st.selectbox(

            "Empresa seleccionada",

            opciones,

            key=(
                "empresa_filtro"
            ),

            format_func=lambda clave:
                nombres[
                    clave
                ],

            on_change=(
                cambiar_empresa
            )
        )


        periodo = st.selectbox(

            "Período de creación de ofertas",

            [
                "Completo",
                "Últimos 7 días",
                "Últimos 30 días",
                "Últimos 3 meses",
                "Último año",
                "Personalizado"
            ],

            key=(
                "periodo_filtro"
            )
        )


        base_empresa = (

            base_tipo

            if empresa == TODAS

            else

            base_tipo.loc[
                base_tipo[
                    "empresa_clave"
                ].eq(
                    empresa
                )
            ]
        )


        # ====================================================
        # FILTRO ÁREA PROFESIONAL
        #
        # Mantiene el nombre "Área profesional"
        # y usa la taxonomía oficial.
        # ====================================================

        areas = [
            AREA_TODAS
        ] + AREAS_OFICIALES


        if (
            st.session_state.get(
                "area_filtro"
            )
            not in
            areas
        ):

            st.session_state[
                "area_filtro"
            ] = AREA_TODAS


        area = st.selectbox(

            "Área profesional",

            areas,

            key=(
                "area_filtro"
            ),

            format_func=lambda valor:
                (
                    "Todas"
                    if valor == AREA_TODAS
                    else valor
                )
        )
        regiones_serie = (

            base_empresa[
                "geographicDepartment"
            ]
            .fillna(
                "Sin especificar"
            )
            .astype(str)
            .str.strip()
            .replace({
                "":
                    "Sin especificar",

                "None":
                    "Sin especificar",

                "nan":
                    "Sin especificar",

                "<NA>":
                    "Sin especificar"
            })
        )


        regiones = (
            [
                REGION_TODAS
            ]
            +
            sorted(
                regiones_serie
                .unique()
                .tolist()
            )
        )


        region = st.selectbox(

            "Región",

            regiones,

            key=(
                "region_filtro"
            ),

            format_func=lambda valor:
                (
                    "Todas"
                    if valor
                    ==
                    REGION_TODAS
                    else valor
                )
        )


        destacada = st.selectbox(

            "Oferta destacada",

            [
                "Todas",
                "Destacadas",
                "No destacadas",
                "No definido"
            ],

            key=(
                "destacada_filtro"
            )
        )


        hoy = (
            pd.Timestamp
            .now(
                tz="UTC"
            )
            .normalize()
        )


        inicio = None
        fin = None


        if (
            periodo
            ==
            "Personalizado"
        ):

            minima = (
                ofertas[
                    "createdAt"
                ]
                .min()
            )


            inicial = (

                minima.date()

                if pd.notna(
                    minima
                )

                else

                hoy.date()
            )


            inicio = st.date_input(

                "Desde",

                value=inicial,

                key=(
                    "fecha_desde"
                )
            )


            fin = st.date_input(

                "Hasta",

                value=(
                    hoy.date()
                ),

                key=(
                    "fecha_hasta"
                )
            )


        elif (
            periodo
            !=
            "Completo"
        ):

            fin = hoy.date()


            if (
                periodo
                ==
                "Últimos 7 días"
            ):

                inicio = (
                    hoy
                    -
                    pd.Timedelta(
                        days=6
                    )
                ).date()


            elif (
                periodo
                ==
                "Últimos 30 días"
            ):

                inicio = (
                    hoy
                    -
                    pd.Timedelta(
                        days=29
                    )
                ).date()


            elif (
                periodo
                ==
                "Últimos 3 meses"
            ):

                inicio = (
                    hoy
                    -
                    pd.DateOffset(
                        months=3
                    )
                ).date()


            else:

                inicio = (
                    hoy
                    -
                    pd.DateOffset(
                        years=1
                    )
                ).date()


            st.caption(
                f"Desde "
                f"{inicio:%d/%m/%Y} "
                f"hasta "
                f"{fin:%d/%m/%Y} "
                f"(UTC)"
            )


        st.button(

            "Limpiar filtros",

            on_click=(
                limpiar_filtros_empresa
            ),

            use_container_width=True
        )


        st.button(

            "Actualizar datos",

            on_click=(
                cargar_datos_empresa.clear
            ),

            use_container_width=True
        )


        st.caption(
            f"Última carga: "
            f"{actualizado:%d/%m/%Y %H:%M} "
            f"- Hora Perú"
        )


    # ========================================================
    # VALIDACIÓN DE FECHAS
    # ========================================================

    if (
        inicio is not None
        and
        inicio > fin
    ):

        st.warning(
            "La fecha inicial no puede "
            "ser posterior a la fecha final."
        )

        st.stop()


    # ========================================================
    # FILTRADO
    # ========================================================

    vista, solicitudes = filtrar_datos(

        ofertas,

        postulaciones,

        empresa,

        area,

        region,

        destacada,

        inicio,

        fin,

        tipo
    )


    # ========================================================
    # TÍTULO PRINCIPAL
    # ========================================================

    titulo = (

        {
            "Todas":
                "Panorama general de empresas",

            "Internas":
                "Ofertas internas",

            "Externas":
                "Ofertas externas",

            "No definido":
                "Ofertas de tipo no definido"
        }[
            tipo
        ]

        if empresa == TODAS

        else

        str(
            por_clave.loc[
                empresa,
                "empresa_nombre"
            ]
        )
    )


    st.subheader(
        titulo
    )


    if (
        empresa
        ==
        SIN_EMPRESA
    ):

        st.info(
            "Este grupo reúne ofertas "
            "sin una empresa identificable. "
            "No representa una única organización."
        )


    elif (
        empresa
        !=
        TODAS
    ):

        st.caption(
            f"Origen de la empresa: "
            f"{por_clave.loc[empresa, 'empresa_origen']}"
        )


    # ========================================================
    # KPIs
    # ========================================================

    kpis = calcular_kpis_empresa(

        vista,

        solicitudes,

        columna_id_postulacion=(
            "_id"
        )
    )


    columnas = st.columns(
        4
    )


    columnas[0].metric(

        "Total de ofertas",

        formato_numero(
            kpis[
                "total_ofertas"
            ]
        )
    )


    columnas[1].metric(

        "Vacantes disponibles",

        formato_numero(
            kpis[
                "vacantes_reales"
            ]
        )
    )


    columnas[2].metric(

        "Ofertas abiertas",

        formato_numero(
            kpis[
                "ofertas_abiertas"
            ]
        )
    )


    columnas[3].metric(

        "Postulaciones registradas",

        formato_numero(
            kpis[
                "total_postulaciones"
            ]
        )
    )


    if vista.empty:

        st.info(
            "No hay ofertas para esta selección. "
            "Puedes limpiar los filtros."
        )


    # ========================================================
    # FILA 1
    # ========================================================

    c1, c2 = st.columns(
        2,
        gap="large"
    )


    with c1:

        with st.container(
            border=True
        ):

            st.subheader(
                "Ofertas por modalidad de trabajo"
            )

            grafico_modalidades(
                vista
            )


    with c2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Ofertas por área profesional"
            )

            grafico_categorias(

                vista,

                "area_visual",

                VERDE_BARRA,

                "areas"
            )


    # ========================================================
    # FILA 2
    # ========================================================

    c1, c2 = st.columns(
        2,
        gap="large"
    )


    with c1:

        with st.container(
            border=True
        ):

            st.subheader(
                "Evolución del total "
                "de ofertas publicadas"
            )

            grafico_mensual(

                vista,

                AZUL_LINEA,

                "ofertas_mes"
            )


    with c2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Evolución del total "
                "de postulaciones"
            )

            grafico_mensual(

                solicitudes,

                AZUL_LINEA,

                "postulaciones_mes"
            )


    # ========================================================
    # FILA 3
    # ========================================================

    detalle_ranking = detalle_ofertas(
        vista,
        solicitudes
    )


    c1, c2 = st.columns(
        2,
        gap="large"
    )


    with c1:

        with st.container(
            border=True
        ):

            st.subheader(
                "Estado de las ofertas"
            )

            grafico_categorias(

                vista,

                "estado_visual",

                MORADO_BARRA,

                "estados_ofertas"
            )


    with c2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Ofertas con más postulaciones"
            )


            ranking = (

                detalle_ranking.loc[
                    detalle_ranking[
                        "Postulaciones"
                    ].gt(0)
                ]

                .sort_values(
                    [
                        "Postulaciones",
                        "ID de oferta"
                    ],
                    ascending=[
                        False,
                        True
                    ]
                )

                .head(5)

                .copy()
            )


            if ranking.empty:

                st.info(
                    "No hay postulaciones "
                    "para esta selección."
                )


            else:

                from html import escape
                from textwrap import wrap


                ranking = (
                    ranking
                    .sort_values(
                        "Postulaciones",
                        ascending=True
                    )
                    .copy()
                )


                etiquetas = [

                    "<br>".join(

                        escape(
                            linea
                        )

                        for linea in wrap(

                            str(
                                puesto
                            ),

                            width=30,

                            break_long_words=False,

                            break_on_hyphens=False
                        )
                    )

                    for puesto in ranking[
                        "Puesto"
                    ]
                ]


                fig = go.Figure(

                    go.Bar(

                        x=ranking[
                            "Postulaciones"
                        ],

                        y=ranking[
                            "ID de oferta"
                        ].astype(str),

                        orientation="h",

                        marker_color="#f8c64b",

                        text=ranking[
                            "Postulaciones"
                        ],

                        textposition="outside",

                        cliponaxis=False,

                        customdata=[

                            [
                                escape(
                                    str(
                                        puesto
                                    )
                                ),

                                str(
                                    identificador
                                )
                            ]

                            for (
                                puesto,
                                identificador
                            )
                            in zip(

                                ranking[
                                    "Puesto"
                                ],

                                ranking[
                                    "ID de oferta"
                                ]
                            )
                        ],

                        hovertemplate=(
                            "%{customdata[0]}<br>"
                            "Postulaciones: "
                            "%{x}"
                            "<extra></extra>"
                        )
                    )
                )


                estilo_figura(
                    fig,
                    altura=430
                )


                fig.update_yaxes(

                    type="category",

                    tickmode="array",

                    tickvals=(
                        ranking[
                            "ID de oferta"
                        ]
                        .astype(str)
                        .tolist()
                    ),

                    ticktext=(
                        etiquetas
                    ),

                    categoryorder="array",

                    categoryarray=(
                        ranking[
                            "ID de oferta"
                        ]
                        .astype(str)
                        .tolist()
                    ),

                    showgrid=False,

                    automargin=True
                )


                fig.update_xaxes(

                    range=[
                        0,
                        max(
                            1,
                            ranking[
                                "Postulaciones"
                            ]
                            .max()
                        )
                        *
                        1.25
                    ],

                    gridcolor="#EEF1F4",

                    tickformat=",d"
                )


                st.plotly_chart(

                    fig,

                    use_container_width=True,

                    theme=None,

                    key=(
                        "ranking_ofertas"
                    ),

                    config={
                        "displayModeBar":
                            False
                    }
                )


    # ========================================================
    # TIPO DE PUESTO + HERRAMIENTAS
    # ========================================================

    c1, c2 = st.columns(
        2,
        gap="large"
    )


    with c1:

        with st.container(
            border=True
        ):

            st.subheader(
                "Ofertas por tipo de puesto"
            )


            st.caption(
                "Distribución de las ofertas "
                "según el nivel o tipo de puesto."
            )


            if (
                "jobType"
                in
                vista.columns
                and
                not vista.empty
            ):

                jobtype_df = (
                    vista[
                        [
                            "jobType"
                        ]
                    ]
                    .copy()
                )


                jobtype_df[
                    "jobType"
                ] = (

                    jobtype_df[
                        "jobType"
                    ]

                    .fillna(
                        "Sin especificar"
                    )

                    .astype(str)

                    .str.strip()
                )


                jobtype_df.loc[

                    jobtype_df[
                        "jobType"
                    ]
                    ==
                    "",

                    "jobType"

                ] = "Sin especificar"


                jobtype_grafico = (

                    jobtype_df[
                        "jobType"
                    ]

                    .value_counts()

                    .reset_index()
                )


                jobtype_grafico.columns = [
                    "Tipo de puesto",
                    "Cantidad"
                ]


                jobtype_grafico = (

                    jobtype_grafico

                    .sort_values(
                        "Cantidad",
                        ascending=True
                    )
                )


                barras(

                    jobtype_grafico,

                    "Tipo de puesto",

                    "Cantidad",

                    NARANJA,

                    "tipo_puesto"
                )


            else:

                st.info(
                    "No existe información de tipo "
                    "de puesto para esta selección."
                )


    with c2:

        with st.container(
            border=True
        ):

            st.subheader(
                "Herramientas y programas "
                "más solicitados"
            )


            (
                ranking_requisitos,
                ofertas_con_requisitos
            ) = top_terminos_requisitos(

                vista,

                limite=10
            )


            if (
                ranking_requisitos.empty
            ):

                st.info(
                    "No hay herramientas "
                    "identificadas para esta selección."
                )


            else:

                barras(

                    ranking_requisitos,

                    "Término",

                    "Ofertas",

                    "#e35693",

                    "ranking_requisitos"
                )


                st.caption(

                    f"{formato_numero(ofertas_con_requisitos)} "
                    "ofertas incluyen al menos una herramienta "
                    "o programa identificado. "
                    "Se usa skills cuando está disponible "
                    "y requirements como respaldo histórico."
                )


    # ========================================================
    # MAPA
    # ========================================================

    if (
        region
        ==
        REGION_TODAS
    ):

        with st.container(
            border=True
        ):

            st.subheader(
                "Distribución geográfica "
                "de ofertas y vacantes"
            )


            st.caption(
                "Visualiza la cantidad de ofertas "
                "publicadas y las vacantes registradas "
                "por departamento del Perú."
            )


            grafico_mapa_ofertas(
                vista
            )


    # ========================================================
    # DETALLE DE OFERTAS
    # ========================================================

    st.subheader(
        "Detalle de ofertas"
    )


    ordenadas = (
        vista
        .sort_values(
            "createdAt",
            ascending=False,
            na_position="last"
        )
    )


    detalle = detalle_ofertas(
        ordenadas,
        solicitudes
    )


    if (
        "department"
        in
        ordenadas.columns
    ):

        areas_registradas = (
            ordenadas
            .set_index(
                "_id"
            )[
                "department"
            ]
        )


        detalle[
            "Área"
        ] = (

            detalle[
                "ID de oferta"
            ]

            .map(
                areas_registradas
            )

            .astype(
                "string"
            )

            .str.strip()

            .replace({
                "":
                    pd.NA,

                "<NA>":
                    pd.NA,

                "nan":
                    pd.NA,

                "None":
                    pd.NA
            })

            .fillna(
                "Sin especificar"
            )
        )


        detalle = (
            detalle.rename(
                columns={
                    "Área":
                        "Área registrada"
                }
            )
        )


    detalle[
        "Ubicación"
    ] = (

        detalle[
            "Ubicación"
        ]

        .astype(
            "string"
        )

        .str.strip()

        .replace({
            "":
                pd.NA,

            "<NA>":
                pd.NA,

            "nan":
                pd.NA,

            "None":
                pd.NA
        })

        .fillna(
            "Sin especificar"
        )
    )


    mostrar_tabla(
        detalle,
        "ofertas"
    )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()
