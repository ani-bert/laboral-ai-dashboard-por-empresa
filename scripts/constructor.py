import os
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
# OBTENER VARIABLES DE CONFIGURACIÓN
# ============================================================

def obtener_configuracion(nombre):

    # Primero intenta obtener la variable desde .env
    valor = os.getenv(nombre)

    if valor:
        return valor

    # Si no existe en .env, intenta obtenerla desde Streamlit Secrets
    try:
        valor = st.secrets.get(nombre)
    except Exception:
        valor = None

    return valor


# ============================================================
# CLASIFICACIÓN DE ÁREA PROFESIONAL
# ============================================================

def clasificar_area_profesional(department):

    # --------------------------------------------------------
    # SIN ESPECIFICAR
    # --------------------------------------------------------

    if pd.isna(department):
        return "Otros"

    departamento = str(department).strip().lower()

    if departamento == "":
        return "Otros"

    # --------------------------------------------------------
    # 1. ADMINISTRACIÓN, CONTABILIDAD Y FINANZAS
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "administración",
        "administracion",
        "contabilidad",
        "finanzas",
        "financiera",
        "tesorería",
        "tesoreria",
        "auditoría",
        "auditoria"
    ]):
        return "Administración, Contabilidad y Finanzas"

    # --------------------------------------------------------
    # 2. ADUANAS Y COMERCIO EXTERIOR
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "aduana",
        "comercio exterior",
        "comercio internacional"
    ]):
        return "Aduanas y Comercio Exterior"

    # --------------------------------------------------------
    # 3. AGRICULTURA, GANADERÍA Y AGROINDUSTRIA
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "agricultura",
        "agrícola",
        "agricola",
        "ganadería",
        "ganaderia",
        "agroindustria",
        "agroindustrial",
        "agropecuario",
        "agropecuaria",
        "agronegocio"
    ]):
        return "Agricultura, Ganadería y Agroindustria"

    # --------------------------------------------------------
    # 4. ARQUITECTURA, DISEÑO DE INTERIORES Y DECORACIÓN
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "arquitectura",
        "diseño de interiores",
        "decoración",
        "decoracion"
    ]):
        return "Arquitectura, Diseño de Interiores y Decoración"

    # --------------------------------------------------------
    # 5. COMERCIAL, VENTAS Y DESARROLLO DE NEGOCIOS
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "comercial",
        "ventas",
        "venta",
        "negocios",
        "desarrollo de negocios",
        "business development"
    ]):
        return "Comercial, Ventas y Desarrollo de Negocios"

    # --------------------------------------------------------
    # 6. CONSTRUCCIÓN E INGENIERÍA CIVIL
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "construcción",
        "construccion",
        "ingeniería civil",
        "ingenieria civil",
        "civil"
    ]):
        return "Construcción e Ingeniería Civil"

    # --------------------------------------------------------
    # 7. DISEÑO Y ARTES GRÁFICAS
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "diseño gráfico",
        "diseño grafico",
        "artes gráficas",
        "artes graficas"
    ]):
        return "Diseño y Artes Gráficas"

    # --------------------------------------------------------
    # 8. GASTRONOMÍA, HOTELERÍA Y TURISMO
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "gastronomía",
        "gastronomia",
        "hotelería",
        "hoteleria",
        "turismo",
        "restaurante",
        "cocina"
    ]):
        return "Gastronomía, Hotelería y Turismo"

    # --------------------------------------------------------
    # 9. LEGAL Y CUMPLIMIENTO
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "legal",
        "jurídico",
        "juridico",
        "derecho",
        "cumplimiento",
        "compliance"
    ]):
        return "Legal y Cumplimiento"

    # --------------------------------------------------------
    # 10. LOGÍSTICA, ABASTECIMIENTO Y TRANSPORTE
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "logística",
        "logistica",
        "abastecimiento",
        "supply chain",
        "cadena de suministro",
        "transporte",
        "almacén",
        "almacen",
        "compras"
    ]):
        return "Logística, Abastecimiento y Transporte"

    # --------------------------------------------------------
    # 11. MANTENIMIENTO Y REPARACIONES TÉCNICAS
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "mantenimiento",
        "reparaciones",
        "reparación",
        "reparacion",
        "servicio técnico",
        "servicio tecnico"
    ]):
        return "Mantenimiento y Reparaciones Técnicas"

    # --------------------------------------------------------
    # 12. MARKETING, PUBLICIDAD Y COMUNICACIÓN
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "marketing",
        "mercadotecnia",
        "publicidad",
        "comunicación",
        "comunicacion",
        "relaciones públicas",
        "relaciones publicas"
    ]):
        return "Marketing, Publicidad y Comunicación"

    # --------------------------------------------------------
    # 13. MINERÍA, PETRÓLEO, ENERGÍA Y GAS
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "minería",
        "mineria",
        "petróleo",
        "petroleo",
        "energía",
        "energia",
        "gas",
        "minas"
    ]):
        return "Minería, Petróleo, Energía y Gas"

    # --------------------------------------------------------
    # 14. PRODUCCIÓN, MANUFACTURA Y OPERACIONES
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "producción",
        "produccion",
        "manufactura",
        "operaciones",
        "ingeniería industrial",
        "ingenieria industrial"
    ]):
        return "Producción, Manufactura y Operaciones"

    # --------------------------------------------------------
    # 15. RECURSOS HUMANOS Y CAPACITACIÓN
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "recursos humanos",
        "rrhh",
        "talento humano",
        "capacitación",
        "capacitacion"
    ]):
        return "Recursos Humanos y Capacitación"

    # --------------------------------------------------------
    # 16. SALUD, MEDICINA Y FARMACIA
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "salud",
        "medicina",
        "farmacia",
        "enfermería",
        "enfermeria",
        "odontología",
        "odontologia"
    ]):
        return "Salud, Medicina y Farmacia"

    # --------------------------------------------------------
    # 17. TECNOLOGÍA, SISTEMAS Y TELECOMUNICACIONES
    # --------------------------------------------------------

    if any(palabra in departamento for palabra in [
        "tecnología",
        "tecnologia",
        "sistemas",
        "informática",
        "informatica",
        "software",
        "telecomunicaciones",
        "tecnología / ti",
        "tecnologia / ti",
        "tecnología / sistemas",
        "tecnologia / sistemas"
    ]):
        return "Tecnología, Sistemas y Telecomunicaciones"

    # --------------------------------------------------------
    # 18. OTROS
    # --------------------------------------------------------

    return "Otros"


# ============================================================
# CONSTRUCTOR DE DATOS
# ============================================================

def constructor():

    # ========================================================
    # 1. CONEXIÓN Y CARGA DESDE MONGODB
    # ========================================================

    mongo_uri = obtener_configuracion("MONGO_URI")
    db_name = obtener_configuracion("DB_NAME")


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

    # Verificar conexión
    client.admin.command("ping")

    db = client[db_name]

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
        "publishUntil",
        "status",
        "createdAt",
        "country",
        "geographicDepartment",
        "jobType",
        "verificationStatus",
        "isExternalOffer",
        "externalCompanyName"
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
        db["companies"].find(
            {},
            {column: 1 for column in companies_columns}
        )
    )

    jobs = pd.DataFrame(
        db["jobs"].find(
            {},
            {column: 1 for column in jobs_columns}
        )
    )

    applications = pd.DataFrame(
        db["applications"].find(
            {},
            {column: 1 for column in applications_columns}
        )
    )

    # ========================================================
    # 2. LIMPIEZA DE COMPANIES
    # ========================================================

    companies_clean = companies.copy()

    columnas_texto_companies = [
        "businessName",
        "industry",
        "verificationStatus",
        "country"
    ]

    for col in columnas_texto_companies:

        if col not in companies_clean.columns:
            companies_clean[col] = pd.NA

        companies_clean[col] = (
            companies_clean[col]
            .astype("string")
            .str.strip()
        )

    if "country" in companies_clean.columns:

        companies_clean["country"] = (
            companies_clean["country"]
            .replace({
                "Peru": "Perú"
            })
        )

    if "plan" not in companies_clean.columns:
        companies_clean["plan"] = None

    companies_clean["planType"] = companies_clean["plan"].apply(
        lambda x: (
            x.get("type")
            if isinstance(x, dict)
            else None
        )
    )

    companies_clean["planType"] = (
        companies_clean["planType"]
        .replace({
            "None": "NONE"
        })
        .fillna("NONE")
    )

    # ========================================================
    # 3. LIMPIEZA DE JOBS
    # ========================================================

    jobs_clean = jobs.copy()

    columnas_texto_jobs = [
        "title",
        "department",
        "modality",
        "status",
        "country",
        "geographicDepartment",
        "jobType",
        "verificationStatus",
        "externalCompanyName"
    ]

    for col in columnas_texto_jobs:

        if col not in jobs_clean.columns:
            jobs_clean[col] = pd.NA

        jobs_clean[col] = (
            jobs_clean[col]
            .astype("string")
            .str.strip()
        )

    jobs_clean["modality"] = (
        jobs_clean["modality"]
        .replace({
            "hibrido": "híbrido"
        })
    )

    jobs_clean["country"] = (
        jobs_clean["country"]
        .replace({
            "Peru": "Perú"
        })
    )

    jobs_clean["country"] = (
        jobs_clean["country"]
        .replace(
            r"^\s*\*\s*$",
            pd.NA,
            regex=True
        )
    )

    jobs_clean["geographicDepartment"] = (
        jobs_clean["geographicDepartment"]
        .astype("string")
        .str.strip()
        .replace({
            "5": pd.NA,
            "": pd.NA
        })
    )

    # ========================================================
    # VALORES INVÁLIDOS DE DEPARTMENT
    # ========================================================

    valores_invalidos = [
        "test",
        "prueba",
        "Test de departamento",
        "Test de Funcionalidades",
        "fghjklñ",
        "Lima"
    ]

    jobs_clean["department"] = (
        jobs_clean["department"]
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

    jobs_clean["department"] = (
        jobs_clean["department"]
        .replace(correcciones_department)
    )

    # ========================================================
    # CLASIFICACIÓN DE ÁREA PROFESIONAL
    # ========================================================

    jobs_clean["professionalArea"] = (
        jobs_clean["department"]
        .apply(clasificar_area_profesional)
    )

    # ========================================================
    # 4. CONVERSIÓN DE FECHAS
    # ========================================================

    jobs_clean["createdAt"] = pd.to_datetime(
        jobs_clean["createdAt"],
        errors="coerce"
    )

    jobs_clean["publishUntil"] = pd.to_datetime(
        jobs_clean["publishUntil"],
        errors="coerce"
    )

     # ========================================================
    # 5. CORRECCIÓN DE FECHA DE UNA OFERTA ESPECÍFICA
    # ========================================================

    filas_antes = len(jobs_clean)

    # Identificar únicamente la oferta corregida en Google Colab
    condicion_registro = (
        jobs_clean["_id"]
        .astype(str)
        .eq("6a5ecc649e10ebf257a0baf8")
    )

    print(
        "\nRegistros seleccionados:",
        int(condicion_registro.sum())
    )

    print("\nRegistro antes de la corrección:")

    print(
        jobs_clean.loc[
            condicion_registro,
            ["_id", "title", "createdAt", "publishUntil"]
        ].to_string(index=False)
    )

    # Misma regla de Colab:
    # fecha de creación a medianoche + 30 días
    jobs_clean.loc[
        condicion_registro,
        "publishUntil"
    ] = (
        jobs_clean.loc[
            condicion_registro,
            "createdAt"
        ].dt.normalize()
        + pd.Timedelta(days=30)
    )

    print("\nRegistro después de la corrección:")

    print(
        jobs_clean.loc[
            condicion_registro,
            ["_id", "title", "createdAt", "publishUntil"]
        ].to_string(index=False)
    )

    # Revisar las fechas sin eliminar ninguna fila
    fechas_inconsistentes = (
        jobs_clean["publishUntil"].notna()
        & jobs_clean["createdAt"].notna()
        & (
            jobs_clean["publishUntil"]
            < jobs_clean["createdAt"]
        )
    )

    print(
        "\nFechas inconsistentes restantes:",
        int(fechas_inconsistentes.sum())
    )

    print("Filas antes:", filas_antes)
    print("Filas después:", len(jobs_clean))

    assert len(jobs_clean) == filas_antes, (
        "La cantidad de ofertas cambió durante la corrección."
    )

    print("No se eliminó ninguna fila en esta corrección.")
    
    # ========================================================
    # 6. LIMPIEZA DE APPLICATIONS
    # ========================================================

    applications_clean = applications.copy()

    if "applicationStatus" not in applications_clean.columns:
        applications_clean["applicationStatus"] = "SIN_ESTADO"

    applications_clean["applicationStatus"] = (
        applications_clean["applicationStatus"]
        .fillna("SIN_ESTADO")
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

    if "externalCompanyName" not in jobs_clean.columns:
        jobs_clean["externalCompanyName"] = pd.NA

    jobs_clean["externalCompanyName"] = (
        jobs_clean["externalCompanyName"]
        .replace(estandarizacion_empresas)
    )

    # ========================================================
    # 8. NORMALIZACIÓN DE IDS
    # ========================================================

    if "job" not in applications_clean.columns:
        applications_clean["job"] = pd.NA

    if "_id" not in jobs_clean.columns:
        jobs_clean["_id"] = pd.NA

    if "companyId" not in jobs_clean.columns:
        jobs_clean["companyId"] = pd.NA

    if "_id" not in companies_clean.columns:
        companies_clean["_id"] = pd.NA

    applications_clean["job"] = (
        applications_clean["job"]
        .astype(str)
    )

    jobs_clean["_id"] = (
        jobs_clean["_id"]
        .astype(str)
    )

    jobs_clean["companyId"] = (
        jobs_clean["companyId"]
        .astype(str)
    )

    companies_clean["_id"] = (
        companies_clean["_id"]
        .astype(str)
    )

    # ========================================================
    # 9. CRUCE APPLICATIONS → JOBS
    # ========================================================

    applications_jobs = applications_clean.merge(
        jobs_clean,
        left_on="job",
        right_on="_id",
        how="left",
        suffixes=(
            "_application",
            "_job"
        )
    )

    # ========================================================
    # 10. CRUCE APPLICATIONS + JOBS → COMPANIES
    # ========================================================

    applications_final = applications_jobs.merge(
        companies_clean,
        left_on="companyId",
        right_on="_id",
        how="left",
        suffixes=(
            "",
            "_company"
        )
    )

    # ========================================================
    # 11. VALIDACIÓN DE DATASETS
    # ========================================================

    print("========================================")
    print("RESUMEN DE DATASETS")
    print("========================================")

    print("\n========== COMPANIES ==========")
    print("Filas:", companies_clean.shape[0])
    print("Columnas:", companies_clean.shape[1])

    print("\n========== JOBS ==========")
    print("Filas:", jobs_clean.shape[0])
    print("Columnas:", jobs_clean.shape[1])

    print("\n========== APPLICATIONS ==========")
    print("Filas:", applications_clean.shape[0])
    print("Columnas:", applications_clean.shape[1])

    # ========================================================
    # 12. VALIDACIÓN DE CRUCES
    # ========================================================

    print("\n========================================")
    print("VALIDACIÓN DE CRUCES")
    print("========================================")

    print(
        "Postulaciones originales:",
        len(applications_clean)
    )

    print(
        "Postulaciones después del cruce:",
        len(applications_final)
    )

    if "_id_application" in applications_final.columns:

        print(
            "Postulaciones duplicadas:",
            applications_final[
                "_id_application"
            ].duplicated().sum()
        )

    if "_id_job" in applications_final.columns:

        print(
            "Postulaciones con oferta:",
            applications_final[
                "_id_job"
            ].notna().sum()
        )

    if "businessName" in applications_final.columns:

        print(
            "Postulaciones con empresa:",
            applications_final[
                "businessName"
            ].notna().sum()
        )

    # ========================================================
    # 13. VALIDACIÓN DE ÁREAS PROFESIONALES
    # ========================================================

    print("\n========================================")
    print("ÁREAS PROFESIONALES")
    print("========================================")

    print(
        jobs_clean["professionalArea"]
        .value_counts()
    )

    # ========================================================
    # 14. RESULTADO FINAL
    # ========================================================

    print("\n========================================")
    print("RESULTADO FINAL")
    print("========================================")

    print(
        "La carga, limpieza y estandarización "
        "de los datos ha sido completada."
    )

    print(
        "Las collections applications, jobs y companies "
        "fueron relacionadas mediante sus identificadores."
    )

    print(
        "Los nombres de empresas externas fueron "
        "agrupados bajo nombres estandarizados."
    )

    print(
        "Las ofertas fueron clasificadas por área profesional."
    )

    print(
        "Los cruces fueron validados correctamente."
    )

    # ========================================================
    # 15. GUARDAR DATASETS EN CACHE
    # ========================================================

    companies_clean.to_csv(
        CACHE_DIR / "companies_clean.csv",
        index=False
    )

    jobs_clean.to_csv(
        CACHE_DIR / "jobs_clean.csv",
        index=False
    )

    applications_clean.to_csv(
        CACHE_DIR / "applications_clean.csv",
        index=False
    )

    applications_jobs.to_csv(
        CACHE_DIR / "applications_jobs.csv",
        index=False
    )

    applications_final.to_csv(
        CACHE_DIR / "applications_final.csv",
        index=False
    )

    print("\n========================================")
    print("CACHE")
    print("========================================")

    print(
        f"Datasets guardados en: {CACHE_DIR}"
    )

    print("\nArchivos generados:")

    print("✓ companies_clean.csv")
    print("✓ jobs_clean.csv")
    print("✓ applications_clean.csv")
    print("✓ applications_jobs.csv")
    print("✓ applications_final.csv")

    # ========================================================
    # 16. RETORNO DE TABLAS
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