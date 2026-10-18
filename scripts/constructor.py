import os
import unicodedata
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient


# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "data_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


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
# OBTENER VARIABLES DE CONFIGURACIÓN
# ============================================================

def obtener_configuracion(nombre):

    valor = os.getenv(nombre)

    if valor:
        return valor

    try:
        valor = st.secrets.get(nombre)
    except Exception:
        valor = None

    return valor


# ============================================================
# NORMALIZACIÓN DE TEXTO PARA CLASIFICACIÓN
# ============================================================

def normalizar_texto_area(valor):

    if pd.isna(valor):
        return ""

    texto = str(valor).strip().casefold()

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    return " ".join(
        texto.split()
    )


# ============================================================
# CLASIFICACIÓN HISTÓRICA
#
# Las ofertas antiguas que NO tienen category se redistribuyen
# utilizando department y, como apoyo, title.
#
# El resultado siempre pertenece a la taxonomía oficial.
# ============================================================

def clasificar_area_profesional(department, title=None):

    departamento = normalizar_texto_area(
        department
    )

    titulo = normalizar_texto_area(
        title
    )

    texto = f"{departamento} {titulo}".strip()


    # ========================================================
    # 1. ADMINISTRACIÓN, CONTABILIDAD Y FINANZAS
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "administracion",
            "administrativo",
            "administrativa",
            "contabilidad",
            "contable",
            "finanzas",
            "financiero",
            "financiera",
            "tesoreria",
            "auditoria",
            "cobranzas",
            "cobranza",
            "facturacion",
            "presupuesto",
            "creditos",
            "credito",
            "costos"
        ]
    ):
        return "Administración, Contabilidad y Finanzas"


    # ========================================================
    # 2. ADUANAS Y COMERCIO EXTERIOR
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "aduana",
            "aduanas",
            "comercio exterior",
            "comercio internacional",
            "importacion",
            "importaciones",
            "exportacion",
            "exportaciones",
            "freight forwarder"
        ]
    ):
        return "Aduanas y Comercio Exterior"


    # ========================================================
    # 3. AGRICULTURA, GANADERÍA Y AGROINDUSTRIA
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "agricultura",
            "agricola",
            "ganaderia",
            "agroindustria",
            "agroindustrial",
            "agropecuario",
            "agropecuaria",
            "agronegocio",
            "agronomia"
        ]
    ):
        return "Agricultura, Ganadería y Agroindustria"


    # ========================================================
    # 4. ARQUITECTURA, DISEÑO DE INTERIORES Y DECORACIÓN
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "arquitectura",
            "arquitecto",
            "arquitecta",
            "diseño de interiores",
            "diseno de interiores",
            "interiorismo",
            "decoracion"
        ]
    ):
        return "Arquitectura, Diseño de Interiores y Decoración"


    # ========================================================
    # 5. COMERCIAL, VENTAS Y DESARROLLO DE NEGOCIOS
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "comercial",
            "ventas",
            "venta",
            "desarrollo de negocios",
            "business development",
            "ejecutivo comercial",
            "asesor comercial",
            "atencion al cliente",
            "servicio al cliente",
            "customer service",
            "retail"
        ]
    ):
        return "Comercial, Ventas y Desarrollo de Negocios"


    # ========================================================
    # 6. CONSTRUCCIÓN E INGENIERÍA CIVIL
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "construccion",
            "ingenieria civil",
            "ingeniero civil",
            "ingeniera civil",
            "obras civiles",
            "obra civil",
            "estructuras",
            "edificaciones",
            "ssoma",
            "seguridad industrial"
        ]
    ):
        return "Construcción e Ingeniería Civil"


    # ========================================================
    # 7. DISEÑO Y ARTES GRÁFICAS
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "diseño grafico",
            "diseno grafico",
            "artes graficas",
            "diseño audiovisual",
            "diseno audiovisual",
            "multimedia",
            "diseñador grafico",
            "disenador grafico"
        ]
    ):
        return "Diseño y Artes Gráficas"


    # ========================================================
    # 8. GASTRONOMÍA, HOTELERÍA Y TURISMO
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "gastronomia",
            "hoteleria",
            "turismo",
            "hotel",
            "restaurante",
            "cocina",
            "hospitalidad"
        ]
    ):
        return "Gastronomía, Hotelería y Turismo"


    # ========================================================
    # 9. LEGAL Y CUMPLIMIENTO
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "legal",
            "juridico",
            "juridica",
            "derecho",
            "abogado",
            "abogada",
            "cumplimiento",
            "compliance"
        ]
    ):
        return "Legal y Cumplimiento"


    # ========================================================
    # 10. LOGÍSTICA, ABASTECIMIENTO Y TRANSPORTE
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "logistica",
            "abastecimiento",
            "supply chain",
            "cadena de suministro",
            "transporte",
            "almacen",
            "almacenes",
            "compras",
            "distribucion",
            "inventario",
            "inventarios"
        ]
    ):
        return "Logística, Abastecimiento y Transporte"


    # ========================================================
    # 11. MANTENIMIENTO Y REPARACIONES TÉCNICAS
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "mantenimiento",
            "reparacion",
            "reparaciones",
            "servicio tecnico",
            "soporte tecnico",
            "mecanica",
            "mecanico",
            "mecanica industrial",
            "electromecanica"
        ]
    ):
        return "Mantenimiento y Reparaciones Técnicas"

    # ========================================================
    # 12. TECNOLOGÍA, SISTEMAS Y TELECOMUNICACIONES
    #
    # Se evalúa antes de "Otras Ingenierías" para evitar que
    # Ingeniería de Sistemas termine en una categoría genérica.
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "tecnologia",
            "sistemas",
            "informatica",
            "software",
            "telecomunicaciones",
            "tecnologia de informacion",
            "tecnologias de informacion",
            "infraestructura ti",
            "soporte ti",
            "desarrollo de software",
            "programacion",
            "programador",
            "programadora",
            "data",
            "datos",
            "analytics",
            "analisis de datos",
            "business intelligence",
            "ciberseguridad",
            "seguridad informatica",
            "redes",
            "cloud",
            "devops"
        ]
    ):
        return "Tecnología, Sistemas y Telecomunicaciones"


    # ========================================================
    # 13. MARKETING, PUBLICIDAD Y COMUNICACIÓN
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "marketing",
            "mercadotecnia",
            "publicidad",
            "comunicacion",
            "comunicaciones",
            "relaciones publicas",
            "contenido",
            "branding",
            "community manager",
            "social media"
        ]
    ):
        return "Marketing, Publicidad y Comunicación"


    # ========================================================
    # 14. MINERÍA, PETRÓLEO, ENERGÍA Y GAS
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "mineria",
            "minero",
            "minera",
            "petroleo",
            "energia",
            "energetico",
            "energetica",
            "gas",
            "minas",
            "hidrocarburos"
        ]
    ):
        return "Minería, Petróleo, Energía y Gas"


    # ========================================================
    # 15. PRODUCCIÓN, MANUFACTURA Y OPERACIONES
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "produccion",
            "manufactura",
            "operaciones",
            "operacion",
            "planta",
            "procesos productivos",
            "manufacturing"
        ]
    ):
        return "Producción, Manufactura y Operaciones"


    # ========================================================
    # 16. RECURSOS HUMANOS Y CAPACITACIÓN
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "recursos humanos",
            "rrhh",
            "talento humano",
            "gestion humana",
            "capital humano",
            "seleccion",
            "reclutamiento",
            "capacitacion",
            "cultura",
            "bienestar",
            "people",
            "psicologia"
        ]
    ):
        return "Recursos Humanos y Capacitación"


    # ========================================================
    # 17. SALUD, MEDICINA Y FARMACIA
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "salud",
            "medicina",
            "medico",
            "medica",
            "farmacia",
            "farmaceutico",
            "farmaceutica",
            "enfermeria",
            "odontologia",
            "nutricion",
            "clinica"
        ]
    ):
        return "Salud, Medicina y Farmacia"


   
    # ========================================================
    # 18. OTRAS INGENIERÍAS
    #
    # Aquí se concentran especialidades de ingeniería que no
    # pertenecen a Civil, Minería, Tecnología o Mantenimiento.
    # ========================================================

    if any(
        termino in texto
        for termino in [
            "ingenieria",
            "ingeniero",
            "ingeniera",
            "ingenierias",
            "industrial",
            "ingenieria industrial",
            "electricidad",
            "electrotecnia",
            "electronica",
            "mecatronica",
            "calidad",
            "procesos",
            "sostenibilidad",
            "maestranza"
        ]
    ):
        return "Otras Ingenierías"


    # ========================================================
    # RESPALDO FINAL
    #
    # La plataforma actual no posee una categoría "Otros".
    # Los registros históricos que no puedan determinarse con
    # seguridad se concentran temporalmente en Otras Ingenierías
    # para conservar las 18 categorías oficiales.
    # ========================================================

    return "Otras Ingenierías"


# ============================================================
# CONSTRUCTOR DE DATOS
# ============================================================

def constructor():

    # ========================================================
    # 1. CONEXIÓN Y CARGA DESDE MONGODB
    # ========================================================

    mongo_uri = obtener_configuracion(
        "MONGO_URI"
    )

    db_name = obtener_configuracion(
        "DB_NAME"
    )


    if not mongo_uri:

        raise ValueError(
            "No se encontró MONGO_URI. "
            "Configúralo en el archivo .env localmente "
            "o en Streamlit Secrets."
        )


    if not db_name:

        raise ValueError(
            "No se encontró DB_NAME. "
            "Configúralo en el archivo .env localmente "
            "o en Streamlit Secrets."
        )


    client = MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=10000
    )


    client.admin.command(
        "ping"
    )


    db = client[
        db_name
    ]


    # ========================================================
    # COLUMNAS DE COMPANIES
    # ========================================================

    companies_columns = [
        "_id",
        "businessName",
        "industry",
        "verificationStatus",
        "country",
        "plan",
        "isActive",
        "createdAt"
    ]


    # ========================================================
    # COLUMNAS DE JOBS
    # ========================================================

    jobs_columns = [
        "_id",
        "companyId",
        "title",
        "department",
        "modality",
        "requirements",
        "publishUntil",
        "status",
        "createdAt",
        "country",
        "geographicDepartment",
        "jobType",
        "verificationStatus",
        "isExternalOffer",
        "externalCompanyName",

        # Campos nuevos
        "vacancies",
        "workExperience",
        "isFeatured",
        "skills",
        "category",
        "categoryId",
        "departmentId",
        "provinceId",
        "locations"
    ]


    # ========================================================
    # COLUMNAS DE APPLICATIONS
    # ========================================================

    applications_columns = [
        "_id",
        "job",
        "createdAt",
        "applicationStatus"
    ]


    # ========================================================
    # CARGA DE COLLECTIONS
    # ========================================================

    companies = pd.DataFrame(
        db[
            "companies"
        ].find(
            {},
            {
                column: 1
                for column
                in companies_columns
            }
        )
    )


    jobs = pd.DataFrame(
        db[
            "jobs"
        ].find(
            {},
            {
                column: 1
                for column
                in jobs_columns
            }
        )
    )


    applications = pd.DataFrame(
        db[
            "applications"
        ].find(
            {},
            {
                column: 1
                for column
                in applications_columns
            }
        )
    )


    # ========================================================
    # 2. LIMPIEZA DE COMPANIES
    # ========================================================

    companies_clean = (
        companies.copy()
    )


    columnas_texto_companies = [
        "businessName",
        "industry",
        "verificationStatus",
        "country"
    ]


    for col in columnas_texto_companies:

        if (
            col
            not in
            companies_clean.columns
        ):

            companies_clean[
                col
            ] = pd.NA


        companies_clean[
            col
        ] = (
            companies_clean[
                col
            ]
            .astype(
                "string"
            )
            .str.strip()
        )


    companies_clean[
        "country"
    ] = (
        companies_clean[
            "country"
        ]
        .replace({
            "Peru":
                "Perú"
        })
    )


    if (
        "plan"
        not in
        companies_clean.columns
    ):

        companies_clean[
            "plan"
        ] = None


    companies_clean[
        "planType"
    ] = (
        companies_clean[
            "plan"
        ]
        .apply(
            lambda x:
                x.get(
                    "type"
                )
                if isinstance(
                    x,
                    dict
                )
                else None
        )
    )


    companies_clean[
        "planType"
    ] = (
        companies_clean[
            "planType"
        ]
        .replace({
            "None":
                "NONE"
        })
        .fillna(
            "NONE"
        )
    )


    # ========================================================
    # 3. LIMPIEZA DE JOBS
    # ========================================================

    jobs_clean = (
        jobs.copy()
    )


    columnas_texto_jobs = [
        "title",
        "department",
        "modality",
        "status",
        "country",
        "geographicDepartment",
        "jobType",
        "verificationStatus",
        "externalCompanyName",
        "category"
    ]


    for col in columnas_texto_jobs:

        if (
            col
            not in
            jobs_clean.columns
        ):

            jobs_clean[
                col
            ] = pd.NA


        jobs_clean[
            col
        ] = (
            jobs_clean[
                col
            ]
            .astype(
                "string"
            )
            .str.strip()
        )


    jobs_clean[
        "modality"
    ] = (
        jobs_clean[
            "modality"
        ]
        .replace({
            "hibrido":
                "híbrido"
        })
    )


    jobs_clean[
        "country"
    ] = (
        jobs_clean[
            "country"
        ]
        .replace({
            "Peru":
                "Perú"
        })
    )


    jobs_clean[
        "geographicDepartment"
    ] = (
        jobs_clean[
            "geographicDepartment"
        ]
        .astype(
            "string"
        )
        .str.strip()
        .replace({
            "5":
                pd.NA,

            "":
                pd.NA
        })
    )


    # ========================================================
    # DEPARTMENTS HISTÓRICOS INVÁLIDOS
    # ========================================================

    valores_invalidos = [
        "test",
        "prueba",
        "Test de departamento",
        "Test de Funcionalidades",
        "fghjklñ",
        "Lima"
    ]


    jobs_clean[
        "department"
    ] = (
        jobs_clean[
            "department"
        ]
        .replace(
            valores_invalidos,
            pd.NA
        )
    )


    # ========================================================
    # CORRECCIONES DE DEPARTMENT
    # ========================================================

    correcciones_department = {

        "Comercia":
            "Comercial",

        "Contabilidad y Finanzasc":
            "Contabilidad y Finanzas",

        "Auditoria":
            "Auditoría",

        "Psicologia":
            "Psicología",

        "Tecnologia":
            "Tecnología",

        "Tecnologia / Sistemas":
            "Tecnología / Sistemas",

        "Tecnologia / TI":
            "Tecnología / TI",

        "Tecnologia /Soporte Técnico":
            "Tecnología / Soporte Técnico",

        "Tecnologia / TI , Soporte Técnico":
            "Tecnología / TI, Soporte Técnico",

        "Comunicaciónes":
            "Comunicaciones",

        "Comunicacion":
            "Comunicación",

        "Diseño Grafico":
            "Diseño Gráfico",

        "Diseño gráfico":
            "Diseño Gráfico",

        "Mineria":
            "Minería",

        "Atención al cliente":
            "Atención al Cliente",

        "Trabajo social":
            "Trabajo Social",

        "Administración y Finanzas.":
            "Administración y Finanzas",

        "Administración y Oficina.":
            "Administración y Oficina",

        "Logística y Cadena de Suministro.":
            "Logística y Cadena de Suministro",

        "Tecnología e Innovación.":
            "Tecnología e Innovación",

        "Seguridad Industrial / SSOMA.":
            "Seguridad Industrial / SSOMA",

        "Ingeniería Industrial y Operaciones.":
            "Ingeniería Industrial y Operaciones",

        "Electricidad Industrial, Electrotecnia o Electricidad.":
            "Electricidad Industrial, Electrotecnia o Electricidad",

        "Energía y Electricidad.":
            "Energía y Electricidad",

        "Mantenimiento Eléctrico Industrial":
            "Mantenimiento Eléctrico Industrial"
    }


    jobs_clean[
        "department"
    ] = (
        jobs_clean[
            "department"
        ]
        .replace(
            correcciones_department
        )
    )


    # ========================================================
    # RECLASIFICACIÓN HISTÓRICA
    #
    # Aquí está uno de los cambios principales:
    # professionalArea ya no usa la taxonomía antigua.
    #
    # Ahora distribuye los registros históricos usando las
    # mismas 18 categorías oficiales actuales.
    # ========================================================

    jobs_clean[
        "professionalArea"
    ] = jobs_clean.apply(

        lambda fila:
            clasificar_area_profesional(
                fila.get(
                    "department"
                ),
                fila.get(
                    "title"
                )
            ),

        axis=1
    )


    # ========================================================
    # 4. CONVERSIÓN DE FECHAS
    # ========================================================

    jobs_clean[
        "createdAt"
    ] = pd.to_datetime(
        jobs_clean[
            "createdAt"
        ],
        errors="coerce"
    )


    jobs_clean[
        "publishUntil"
    ] = pd.to_datetime(
        jobs_clean[
            "publishUntil"
        ],
        errors="coerce"
    )


    # ========================================================
    # 5. CORRECCIÓN DE FECHA DE UNA OFERTA ESPECÍFICA
    # ========================================================

    filas_antes = len(
        jobs_clean
    )


    condicion_registro = (
        jobs_clean[
            "_id"
        ]
        .astype(str)
        .eq(
            "6a5ecc649e10ebf257a0baf8"
        )
    )


    print(
        "\nRegistros seleccionados:",
        int(
            condicion_registro.sum()
        )
    )


    print(
        "\nRegistro antes de la corrección:"
    )


    print(
        jobs_clean.loc[
            condicion_registro,
            [
                "_id",
                "title",
                "createdAt",
                "publishUntil"
            ]
        ].to_string(
            index=False
        )
    )


    jobs_clean.loc[
        condicion_registro,
        "publishUntil"
    ] = (
        jobs_clean.loc[
            condicion_registro,
            "createdAt"
        ]
        .dt.normalize()
        +
        pd.Timedelta(
            days=30
        )
    )


    print(
        "\nRegistro después de la corrección:"
    )


    print(
        jobs_clean.loc[
            condicion_registro,
            [
                "_id",
                "title",
                "createdAt",
                "publishUntil"
            ]
        ].to_string(
            index=False
        )
    )


    fechas_inconsistentes = (
        jobs_clean[
            "publishUntil"
        ].notna()
        &
        jobs_clean[
            "createdAt"
        ].notna()
        &
        (
            jobs_clean[
                "publishUntil"
            ]
            <
            jobs_clean[
                "createdAt"
            ]
        )
    )


    print(
        "\nFechas inconsistentes restantes:",
        int(
            fechas_inconsistentes.sum()
        )
    )


    print(
        "Filas antes:",
        filas_antes
    )


    print(
        "Filas después:",
        len(
            jobs_clean
        )
    )


    assert (
        len(
            jobs_clean
        )
        ==
        filas_antes
    ), (
        "La cantidad de ofertas cambió "
        "durante la corrección."
    )


    print(
        "No se eliminó ninguna fila "
        "en esta corrección."
    )
        # ========================================================
    # 6. LIMPIEZA DE APPLICATIONS
    # ========================================================

    applications_clean = (
        applications.copy()
    )


    if (
        "applicationStatus"
        not in
        applications_clean.columns
    ):
        applications_clean[
            "applicationStatus"
        ] = "SIN_ESTADO"


    applications_clean[
        "applicationStatus"
    ] = (
        applications_clean[
            "applicationStatus"
        ]
        .fillna(
            "SIN_ESTADO"
        )
    )


    # ========================================================
    # 7. ESTANDARIZACIÓN DE EMPRESAS
    # ========================================================

    estandarizacion_empresas = {

        "Importante empresa del sector":
            "Importante Empresa en el sector",

        "Importante Empresa en el sector":
            "Importante Empresa en el sector",

        "Importante del Sector":
            "Importante Empresa en el sector",

        "Importante":
            "Importante Empresa en el sector",

        "Empresa importante en el sector":
            "Importante Empresa en el sector",

        "Empresa Confidencial":
            "Importante Empresa en el sector",

        "Confidencial":
            "Importante Empresa en el sector",

        "Gloria":
            "Grupo Gloria",

        "Gloria S.A":
            "Grupo Gloria",

        "Gloria S.A.":
            "Grupo Gloria",

        "KOMATSU - MITSUI MAQUINARIAS":
            "Komatsu Mitsui",

        "KOMATSU MITSUI":
            "Komatsu Mitsui",

        "CAJA TRUJILLO":
            "Caja Trujillo",

        "REPSOL":
            "Repsol",

        "CAMPOSOL":
            "Camposol",

        "CAMPOSOL S.A.":
            "Camposol",

        "EUROFIRMS":
            "Eurofirms",

        "Eurofirms Perú":
            "Eurofirms",

        "UNIVERSIDAD TECNOLOGICA DEL PERU":
            "Universidad Tecnológica del Perú",

        "UNIVERSIDAD TECNOLOGICA DEL PERU(UTP)":
            "Universidad Tecnológica del Perú",

        "CAJA CUSCO":
            "Caja Cusco",

        "Cartavio Rum Company":
            "CARTAVIO RUM COMPANY S.A.C.",

        "Adecco Perú":
            "Adecco Perú S.A.",

        "Adecco Perú S.A.SAC":
            "Adecco Perú S.A.",

        "ADECCO BCP":
            "Adecco Perú S.A.",

        "Practicante Profesional de Contabilidad Adecco Perú S.A.":
            "Adecco Perú S.A.",

        "Tisur":
            "Tisur S.A.",

        "Cetemin":
            "CETEMIN",

        "Manpower":
            "ManpowerGroup",

        "ManpowerGroup Perú":
            "ManpowerGroup",

        "MANPOWER PERU S.A.C.":
            "ManpowerGroup",

        "Manpower Perú":
            "ManpowerGroup",

        "MANPOWER RPO BCP":
            "ManpowerGroup",

        "ManpowerGroup RPO":
            "ManpowerGroup",

        "Practicante de tesorería Manpower":
            "ManpowerGroup",

        "Dirigido a hombres y mujeres Danper Trujillo SAC":
            "Danper Trujillo SAC",

        "Grupo Centenario Lima":
            "Grupo Centenario",

        "Grupo Aenza":
            "AENZA",

        "PROSERING SRLTDA":
            "PROSERING",

        "PROSERING Arequipa":
            "PROSERING",

        "Natura Lima Metropolitan Area":
            "Natura",

        "Expertia Travel Lima":
            "Expertia Travel",

        "OVERALL STRATEGY S.A.C":
            "Overall Strategy",

        "Topitop":
            "Topi Top",

        "BACKUS":
            "Backus",

        "Transportes Cruz Del Sur S.A.C":
            "Transportes Cruz Del Sur S.A.C.",

        "Pacifico Eps":
            "Pacífico EPS",

        "Pacífico EPS":
            "Pacífico EPS",

        "RANSA COMERCIAL S.A.C":
            "Ransa Comercial S.A.C.",

        "Ransa Comercial S.A.":
            "Ransa Comercial S.A.C.",

        "Yura S.A":
            "Yura S.A.",

        "Mind Group Arequipa":
            "Mind Group",

        "Nexus Salud Ocupacional Arequipa, Arequipa, Perú":
            "Nexus Salud Ocupacional",

        "Club Internacional Arequipa Arequipa":
            "Club Internacional Arequipa",

        "Indra Group":
            "Indra",

        "INDRA PERU":
            "Indra",

        "FINANCIERA CONFIANZA":
            "Financiera Confianza",

        "SHOUGANG HIERRO PERU S.A.A":
            "SHOUGANG HIERRO PERU S.A.A.",

        "Compañía Minera Sol de los Andes":
            "Compañía Minera Sol de los Andes S.A.C.",

        "DIAR INGENIEROS S.A":
            "Diar Ingenieros S.A.",

        "Diar Ingenieros S. A.":
            "Diar Ingenieros S.A.",

        "TIENDAS TAMBO":
            "Tiendas Tambo",

        "8A INGENIERIA SUMINISTROS Y SOLUCIONES":
            "Ingeniería Suministros y Soluciones"
    }


    if (
        "externalCompanyName"
        not in
        jobs_clean.columns
    ):
        jobs_clean[
            "externalCompanyName"
        ] = pd.NA


    jobs_clean[
        "externalCompanyName"
    ] = (
        jobs_clean[
            "externalCompanyName"
        ]
        .replace(
            estandarizacion_empresas
        )
    )


    # ========================================================
    # 8. NORMALIZACIÓN DE IDS
    # ========================================================

    if (
        "job"
        not in
        applications_clean.columns
    ):
        applications_clean[
            "job"
        ] = pd.NA


    if (
        "_id"
        not in
        jobs_clean.columns
    ):
        jobs_clean[
            "_id"
        ] = pd.NA


    if (
        "companyId"
        not in
        jobs_clean.columns
    ):
        jobs_clean[
            "companyId"
        ] = pd.NA


    if (
        "_id"
        not in
        companies_clean.columns
    ):
        companies_clean[
            "_id"
        ] = pd.NA


    applications_clean[
        "job"
    ] = (
        applications_clean[
            "job"
        ]
        .astype(str)
    )


    jobs_clean[
        "_id"
    ] = (
        jobs_clean[
            "_id"
        ]
        .astype(str)
    )


    jobs_clean[
        "companyId"
    ] = (
        jobs_clean[
            "companyId"
        ]
        .astype(str)
    )


    companies_clean[
        "_id"
    ] = (
        companies_clean[
            "_id"
        ]
        .astype(str)
    )


    # ========================================================
    # 9. CRUCE APPLICATIONS → JOBS
    # ========================================================

    applications_jobs = (
        applications_clean
        .merge(
            jobs_clean,
            left_on="job",
            right_on="_id",
            how="left",
            suffixes=(
                "_application",
                "_job"
            )
        )
    )


    # ========================================================
    # 10. CRUCE APPLICATIONS + JOBS → COMPANIES
    # ========================================================

    applications_final = (
        applications_jobs
        .merge(
            companies_clean,
            left_on="companyId",
            right_on="_id",
            how="left",
            suffixes=(
                "",
                "_company"
            )
        )
    )


    # ========================================================
    # 11. VALIDACIÓN DE DATASETS
    # ========================================================

    print(
        "========================================"
    )

    print(
        "RESUMEN DE DATASETS"
    )

    print(
        "========================================"
    )


    print(
        "\n========== COMPANIES =========="
    )

    print(
        "Filas:",
        companies_clean.shape[0]
    )

    print(
        "Columnas:",
        companies_clean.shape[1]
    )


    print(
        "\n========== JOBS =========="
    )

    print(
        "Filas:",
        jobs_clean.shape[0]
    )

    print(
        "Columnas:",
        jobs_clean.shape[1]
    )


    print(
        "\n========== APPLICATIONS =========="
    )

    print(
        "Filas:",
        applications_clean.shape[0]
    )

    print(
        "Columnas:",
        applications_clean.shape[1]
    )


    # ========================================================
    # 12. VALIDACIÓN DE CRUCES
    # ========================================================

    print(
        "\n========================================"
    )

    print(
        "VALIDACIÓN DE CRUCES"
    )

    print(
        "========================================"
    )


    print(
        "Postulaciones originales:",
        len(
            applications_clean
        )
    )


    print(
        "Postulaciones después del cruce:",
        len(
            applications_final
        )
    )


    if (
        "_id_application"
        in
        applications_final.columns
    ):

        print(
            "Postulaciones duplicadas:",
            applications_final[
                "_id_application"
            ]
            .duplicated()
            .sum()
        )


    if (
        "_id_job"
        in
        applications_final.columns
    ):

        print(
            "Postulaciones con oferta:",
            applications_final[
                "_id_job"
            ]
            .notna()
            .sum()
        )


    if (
        "businessName"
        in
        applications_final.columns
    ):

        print(
            "Postulaciones con empresa:",
            applications_final[
                "businessName"
            ]
            .notna()
            .sum()
        )


    # ========================================================
    # 13. VALIDACIÓN DE ÁREAS PROFESIONALES
    # ========================================================

    print(
        "\n========================================"
    )

    print(
        "ÁREAS PROFESIONALES HISTÓRICAS RECLASIFICADAS"
    )

    print(
        "========================================"
    )


    print(
        jobs_clean[
            "professionalArea"
        ]
        .value_counts()
    )


    # ========================================================
    # 14. VALIDACIÓN DE TAXONOMÍA OFICIAL
    # ========================================================

    areas_no_oficiales = sorted(
        set(
            jobs_clean[
                "professionalArea"
            ]
            .dropna()
            .unique()
        )
        -
        set(
            AREAS_OFICIALES
        )
    )


    print(
        "\nÁreas fuera de la taxonomía oficial:",
        areas_no_oficiales
    )


    # ========================================================
    # 15. VALIDACIÓN DE NUEVOS CAMPOS
    # ========================================================

    print(
        "\n========================================"
    )

    print(
        "NUEVOS CAMPOS"
    )

    print(
        "========================================"
    )


    for campo in [
        "category",
        "skills",
        "vacancies",
        "isFeatured"
    ]:

        if (
            campo
            in
            jobs_clean.columns
        ):

            print(
                f"{campo}: "
                f"{jobs_clean[campo].notna().sum()} "
                "registros con dato"
            )

        else:

            print(
                f"{campo}: "
                "columna no disponible"
            )


    # ========================================================
    # 16. VALIDACIÓN CATEGORY VS HISTÓRICO
    # ========================================================

    print(
        "\n========================================"
    )

    print(
        "CATEGORY VS PROFESSIONAL AREA"
    )

    print(
        "========================================"
    )


    print(
        "Ofertas con category:",
        jobs_clean[
            "category"
        ]
        .notna()
        .sum()
    )


    print(
        "Ofertas sin category:",
        jobs_clean[
            "category"
        ]
        .isna()
        .sum()
    )


    # ========================================================
    # 17. RESULTADO FINAL
    # ========================================================

    print(
        "\n========================================"
    )

    print(
        "RESULTADO FINAL"
    )

    print(
        "========================================"
    )


    print(
        "La carga, limpieza y estandarización "
        "de los datos ha sido completada."
    )


    print(
        "Las collections applications, jobs "
        "y companies fueron relacionadas "
        "mediante sus identificadores."
    )


    print(
        "Los nombres de empresas externas "
        "fueron agrupados bajo nombres "
        "estandarizados."
    )


    print(
        "Las ofertas históricas fueron "
        "reclasificadas usando las 18 "
        "áreas profesionales oficiales."
    )


    print(
        "Los campos category y skills quedan "
        "disponibles para que el dashboard "
        "utilice la nueva estructura."
    )


    print(
        "Los cruces fueron validados "
        "correctamente."
    )


    # ========================================================
    # 18. GUARDAR DATASETS EN CACHE
    # ========================================================

    companies_clean.to_csv(
        CACHE_DIR
        /
        "companies_clean.csv",
        index=False
    )


    jobs_clean.to_csv(
        CACHE_DIR
        /
        "jobs_clean.csv",
        index=False
    )


    applications_clean.to_csv(
        CACHE_DIR
        /
        "applications_clean.csv",
        index=False
    )


    applications_jobs.to_csv(
        CACHE_DIR
        /
        "applications_jobs.csv",
        index=False
    )


    applications_final.to_csv(
        CACHE_DIR
        /
        "applications_final.csv",
        index=False
    )


    print(
        "\n========================================"
    )

    print(
        "CACHE"
    )

    print(
        "========================================"
    )


    print(
        f"Datasets guardados en: "
        f"{CACHE_DIR}"
    )


    print(
        "\nArchivos generados:"
    )


    print(
        "✓ companies_clean.csv"
    )

    print(
        "✓ jobs_clean.csv"
    )

    print(
        "✓ applications_clean.csv"
    )

    print(
        "✓ applications_jobs.csv"
    )

    print(
        "✓ applications_final.csv"
    )


    # ========================================================
    # 19. RETORNO DE TABLAS
    # ========================================================

    return (
        companies_clean,
        jobs_clean,
        applications_clean,
        applications_jobs,
        applications_final
    )


# ============================================================
# EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":

    (
        companies_clean,
        jobs_clean,
        applications_clean,
        applications_jobs,
        applications_final
    ) = constructor()
