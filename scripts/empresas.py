"""Identidades de empresas: no elimina ofertas ni escribe en MongoDB."""
import re
import unicodedata
import pandas as pd

EQUIVALENCIAS = {
    "ADECO PERÚ": "Adecco Perú S.A.",
         "Adecco Perú SA": "Adecco Perú S.A.",


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

def limpiar_texto(serie):
    return serie.astype("string").str.strip().replace(
        {"": pd.NA, "None": pd.NA, "nan": pd.NA, "<NA>": pd.NA}
    )


def normalizar_empresa(nombre):
    """Clave comparable. Conserva la forma jurídica; no usa similitud difusa."""
    if pd.isna(nombre):
        return ""
    nombre = unicodedata.normalize("NFKD", str(nombre).strip())
    nombre = "".join(c for c in nombre if not unicodedata.combining(c)).upper()
    nombre = re.sub(r"[.,;:_\-]", " ", nombre)
    nombre = " ".join(nombre.split())
    # Más largos primero: S A A no debe convertirse antes en SA A.
    sufijos = {
        " SOCIEDAD COMERCIAL DE RESPONSABILIDAD LIMITADA": " SRL",
        " SOCIEDAD ANONIMA CERRADA": " SAC",
        " SOCIEDAD ANONIMA ABIERTA": " SAA",
        " SOCIEDAD ANONIMA": " SA",
        " S A C": " SAC",
        " S A A": " SAA",
        " S R L": " SRL",
        " S A": " SA",
    }
    for origen, destino in sorted(sufijos.items(), key=lambda par: -len(par[0])):
        if nombre.endswith(origen):
            return nombre[:-len(origen)].strip() + destino
    return nombre


def preparar_equivalencias():
    mapa = {}
    for variante, destino in EQUIVALENCIAS.items():
        clave = normalizar_empresa(variante)
        if clave in mapa and normalizar_empresa(mapa[clave]) != normalizar_empresa(destino):
            raise ValueError("Hay equivalencias de empresas contradictorias.")
        mapa[clave] = destino
    for destino in EQUIVALENCIAS.values():
        mapa.setdefault(normalizar_empresa(destino), destino)
    return mapa


MAPA_EQUIVALENCIAS = preparar_equivalencias()
NOMBRES_GENERICOS = {
    normalizar_empresa(x) for x in [
        "confidencial", "empresa confidencial", "importante",
        "importante del sector", "importante empresa del sector",
        "importante empresa en el sector", "empresa importante en el sector",
        "empresa no especificada", "empresas no especificadas",
        "empresa no identificada", "sin especificar", "no especificada",
        "no especificado", "sin información"
    ]
}


def nombre_externo_canonico(nombre):
    clave = normalizar_empresa(nombre)
    if not clave:
        return pd.NA
    return MAPA_EQUIVALENCIAS.get(clave, clave)


def construir_directorio_empresas(companies, jobs):
    """
    Devuelve directorio y ofertas. Normaliza solo las identidades externas.
    Las internas conservan su nombre e ID y no se fusionan con externas.
    Los nombres genéricos permanecen sin clave; app.py muestra su grupo.
    """
    empresas, ofertas = companies.copy(), jobs.copy()
    filas_iniciales = len(ofertas)
    for col in ["_id", "businessName"]:
        if col not in empresas:
            empresas[col] = pd.NA
        empresas[col] = limpiar_texto(empresas[col])
    for col in ["_id", "companyId", "externalCompanyName"]:
        if col not in ofertas:
            ofertas[col] = pd.NA
        ofertas[col] = limpiar_texto(ofertas[col])
    if "createdAt" not in ofertas:
        ofertas["createdAt"] = pd.NaT
    if empresas["_id"].dropna().duplicated().any():
        raise ValueError("Existen IDs repetidos en companies; no se eliminaron filas.")

    internas = empresas.loc[empresas["_id"].notna(), ["_id", "businessName"]].copy()
    internas["empresa_clave"] = "interna:" + internas["_id"]
    internas["empresa_nombre"] = internas["businessName"].fillna(
        "Empresa sin nombre · " + internas["_id"]
    )
    internas["empresa_origen"] = "Interna"
    mapa_internas = internas.set_index("_id")["empresa_clave"]

    if "isExternalOffer" in ofertas:
        marca_externa = ofertas["isExternalOffer"].astype("string").str.strip().str.lower().isin(
            ["true", "1", "1.0"]
        )
    else:
        marca_externa = pd.Series(False, index=ofertas.index)
    usar_nombre_externo = marca_externa | ~ofertas["companyId"].isin(internas["_id"])
    ofertas["empresa_clave"] = ofertas["companyId"].map(mapa_internas).astype("string")
    ofertas.loc[usar_nombre_externo, "empresa_clave"] = pd.NA

    # Conserva el externalCompanyName recibido del constructor para trazabilidad.
    # La nueva columna solo se informa en ofertas clasificadas como externas.
    ofertas["externalCompanyName_normalizado"] = pd.Series(
        pd.NA, index=ofertas.index, dtype="string"
    )
    ofertas.loc[usar_nombre_externo, "externalCompanyName_normalizado"] = (
        ofertas.loc[usar_nombre_externo, "externalCompanyName"]
        .map(nombre_externo_canonico).astype("string")
    )
    claves = ofertas["externalCompanyName_normalizado"].map(normalizar_empresa).astype("string")
    identificable = usar_nombre_externo & claves.ne("") & ~claves.isin(NOMBRES_GENERICOS)
    ofertas.loc[identificable, "empresa_clave"] = "externa:" + claves.loc[identificable]

    externas = ofertas.loc[
        identificable, ["empresa_clave", "externalCompanyName_normalizado"]
    ].rename(columns={"externalCompanyName_normalizado": "empresa_nombre"})
    externas = externas.groupby("empresa_clave", as_index=False)["empresa_nombre"].first()
    externas["empresa_origen"] = "Externa"
    columnas = ["empresa_clave", "empresa_nombre", "empresa_origen"]
    directorio = pd.concat([internas[columnas], externas[columnas]], ignore_index=True)
    ofertas["createdAt"] = pd.to_datetime(
        ofertas["createdAt"], errors="coerce", utc=True, format="mixed"
    )
    resumen = ofertas.groupby("empresa_clave").agg(
        total_ofertas=("_id", "nunique"), ultima_publicacion=("createdAt", "max")
    ).reset_index()
    directorio = directorio.merge(resumen, on="empresa_clave", how="left", validate="one_to_one")
    directorio["total_ofertas"] = directorio["total_ofertas"].fillna(0).astype(int)
    directorio = directorio.sort_values(
        ["total_ofertas", "empresa_nombre"], ascending=[False, True]
    ).reset_index(drop=True)
    mapa = directorio.set_index("empresa_clave")
    ofertas["empresa_nombre"] = ofertas["empresa_clave"].map(mapa["empresa_nombre"]).fillna(
        "Empresa no identificada"
    )
    ofertas["empresa_origen"] = ofertas["empresa_clave"].map(mapa["empresa_origen"]).fillna(
        "Sin identificar"
    )
    if len(ofertas) != filas_iniciales:
        raise ValueError("Cambió la cantidad de ofertas al construir el directorio.")
    return directorio, ofertas

