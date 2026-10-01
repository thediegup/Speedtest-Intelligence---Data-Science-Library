# -*- coding: utf-8 -*-
"""
Libreria: analisis_telco.py
Modulo de utilidades para analisis de mercado, filtrado y generacion de graficos.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import numpy as np
import textwrap
import plotly.graph_objects as go

# =====================================================================
# PALETA DE COLORES OFICIAL POR PROVEEDOR
# =====================================================================

COLORES_PROVEEDORES = {
    'Inter': '#0056B5',
    'Thundernet': '#089C5E',
    'Boom Solutions': '#FFCC80',
    'Servitel': '#11B327',
    'Conetcom': '#11B327',
    'CONETCOM': '#11B327',
    'IDatanet Vzla 2021, C.a': '#015CC7',
    'Fibex Telecom': '#00184E',
    'CANTV': '#0D7191',
    'NetUno': '#E5AA29',
    'Digitel': '#E0003F',
    'Vnet': '#2E0073',
    'Intercom Servicios C.a': '#86B34D',
    'Simplefibra': '#E65100',
    'Galanet': '#B8E258',
    'Movistar': '#009EF7',
    'Gandalf': '#FD111A',
    'Airtek Solutions': '#0066FF',
    'MDS Telecom': '#52087B',
    'Norte': '#5D2500',
    'KM NET': '#99D9EA',
    'IFX': '#C5271E',
    'CIDATA': '#25A7E0',
    '360NET': '#6CB42A',
    'MINET': '#FF8C00',
    'Gigapop': '#1CE81C',
    'HHNetwork': '#00B6EC',
    'Besser Solutions': '#00187C',
    'SpaceX Starlink': '#000000',
    'Datavoip': '#570279',
    'Datanet Vzla 2021, C.a': '#0A0BB5',
    'Gold Data': '#A2A165',
    'IFX Networks': '#C5271E',
    'GALAIT': '#00A0C6',
    'FullData': '#0391FF',
    'Cidata': '#E6007F',
    'CIDATA VE': '#E6007F',
    'Galup': '#FFC7B1',
    'Matrix TV': '#E4222A',
    'Navegante Network, C.a.': '#FCD04B',
    'Gbit Tecnology': '#FE4B08',
    'INTERNEXA': '#E2AE32',
    'SuperCable': '#E2AE32',
    'Lumen': '#16A2DB',
    'Telcorp Latam': '#F4741A',
    'SavannaNetworks': '#DDA5EA',
    'Savanna Networks': '#DDA5EA',
    'Samm Tecnologia E Telecomunicacoes S.A': '#992D77',
    'Corporacion_Matrix_TV_CA': '#E4222A',
    'Abraham Network, C.A': '#0170F6',
    'Wlink Telecom': '#EF6423',
    'SilverData': '#FF512F',
    'Radnet Telecom, C.a': '#257DE1',
    'IP Net': '#F9B439',
    'Skylink': '#DE1E26',
    'Datalink': '#0088CE',
    'Power Link Corp': '#CCCCCC',
    'Soluciones Dcn Network C.a': '#CCCCCC',
    'G-Network': '#F7127C',
    'STARCONECTADOS': '#252D5E',
    'Tecnoven': '#FFAEC9',
    'Sucrenet' : '#B6A500',
    'TotalCom' : '#3C8929',
    'Oit Servicio De Datos, C.a.': '#07969E',
    'Cosan Telecom': '#FFD700',
    'Multicanal' : '#FF0012',
    'Telecom 3 C.a': '#FBE300',
    'Nervicom': '#F26722',
    'Wisp Tecnoger' : '#10AAA8',
    'Interking' : '#FFDE17',
    'CIX' : '#E0802C',
    'Otros': '#9E9E9E'
}

colores_proveedores = COLORES_PROVEEDORES

# =====================================================================
# 0. CONSULTA DE INFORMACION DE LA MUESTRA
# =====================================================================

def consultar_regionesexactas(df, mostrar_conteo=True):
    """
    Retorna la lista de regiones (attr_place_region) exactamente como estan
    escritas en el dataset original.
    """
    col_region = 'attr_place_region'
    
    if col_region not in df.columns:
        print(f"[Advertencia] No se encontro la columna '{col_region}'.")
        return []

    # Obtener valores unicos exactamente como vienen en el dataset (sin alterar texto)
    regiones_exactas = df[col_region].dropna().unique().tolist()

    if mostrar_conteo:
        resumen = (
            df.groupby(col_region, observed=False)
            .agg(
                Registros=('id_device', 'count'),
                Dispositivos_Unicos=('id_device', 'nunique')
            )
            .sort_values(by='Dispositivos_Unicos', ascending=False)
            .reset_index()
        )
        print("=" * 65)
        print("REGIONES EXACTAS EN EL DATASET")
        print("=" * 65)
        print(resumen.to_string(index=False))
        print("=" * 65)
        print(f"Total regiones: {len(regiones_exactas)}")
        print(f"Lista exacta: {regiones_exactas}\n")

    return regiones_exactas

def consultar_subregionesexactas_por_region(df, region, mostrar_conteo=True):
    """
    Retorna la lista de subregiones (attr_place_subregion) de una region dada
    exactamente como estan escritas en el dataset original.
    """
    col_region = 'attr_place_region'
    col_subregion = 'attr_place_subregion'

    if col_region not in df.columns or col_subregion not in df.columns:
        print("[Advertencia] No se encontraron las columnas de region o subregion.")
        return []

    # Filtro flexible para encontrar la region sin que afecten mayusculas
    condicion_region = df[col_region].astype(str).str.contains(region, case=False, na=False)
    df_region = df[condicion_region].copy()

    if len(df_region) == 0:
        print(f"[Advertencia] No se encontraron datos para: '{region}'.")
        return []

    # Obtener los valores literales exactos de la columna de subregion
    subregiones_exactas = df_region[col_subregion].dropna().unique().tolist()

    if mostrar_conteo:
        resumen = (
            df_region.groupby(col_subregion, observed=False)
            .agg(
                Registros=('id_device', 'count'),
                Dispositivos_Unicos=('id_device', 'nunique')
            )
            .sort_values(by='Dispositivos_Unicos', ascending=False)
            .reset_index()
        )
        print("=" * 65)
        print(f"SUBREGIONES EXACTAS PARA: {region}")
        print("=" * 65)
        print(resumen.to_string(index=False))
        print("=" * 65)
        print(f"Total subregiones: {len(subregiones_exactas)}")
        print(f"Lista exacta: {subregiones_exactas}\n")

    return subregiones_exactas

def consultar_subregiones_por_region(df, region, mostrar_conteo=True):
    """
    Consulta y lista todas las subregiones (attr_place_subregion) únicas presentes 
    en una región dada (attr_place_region).
    
    Parámetros:
    - df (pd.DataFrame): DataFrame con la data de mercado.
    - region (str): Nombre o texto de la región (ej: 'Lara', 'Capital District', 'Portuguesa').
    - mostrar_conteo (bool): Si es True, imprime una tabla con la cantidad de registros y dispositivos por subregión.
    
    Retorna:
    - list: Lista ordenada de nombres de subregiones (para copiar y pegar directo en tus filtros).
    """
    # 1. Filtro flexible de región (insensible a mayúsculas/minúsculas)
    condicion_region = df['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
    df_region = df[condicion_region].copy()

    if len(df_region) == 0:
        print(f"[Advertencia] No se encontraron datos para la región: '{region}'.")
        print("Regiones disponibles en la muestra:")
        print(df['attr_place_region'].dropna().unique()[:10])
        return []

    # 2. Obtener la lista única de subregiones limpias
    subregiones_unicas = (
        df_region['attr_place_subregion']
        .dropna()
        .astype(str)
        .unique()
    )
    subregiones_ordenadas = sorted(subregiones_unicas.tolist())

    # 3. Mostrar resumen en pantalla
    if mostrar_conteo:
        resumen = (
            df_region.groupby('attr_place_subregion', observed=False)
            .agg(
                Registros=('id_device', 'count'),
                Dispositivos_Unicos=('id_device', 'nunique')
            )
            .sort_values(by='Dispositivos_Unicos', ascending=False)
            .reset_index()
        )
        print("=" * 65)
        print(f"📍 SUBREGIONES ENCONTRADAS EN: {region.upper()}")
        print("=" * 65)
        print(resumen.to_string(index=False))
        print("=" * 65)
        print(f"Lista para copiar: {subregiones_ordenadas}\n")

    return subregiones_ordenadas

def consultar_regiones(df, mostrar_conteo=True):
    """
    Consulta y lista todas las regiones (attr_place_region) unicas presentes 
    en el dataset, mostrando la cantidad de registros y dispositivos unicos.
    
    Parametros:
    - df (pd.DataFrame): DataFrame con la data de mercado.
    - mostrar_conteo (bool): Si es True, imprime la tabla detallada.
    
    Retorna:
    - list: Lista ordenada con los nombres de todas las regiones.
    """
    col_region = 'attr_place_region'
    
    if col_region not in df.columns:
        print(f"[Advertencia] No se encontro la columna '{col_region}' en el DataFrame.")
        return []

    # 1. Obtener lista ordenada de regiones unicas limpias
    regiones_unicas = (
        df[col_region]
        .dropna()
        .astype(str)
        .unique()
    )
    regiones_ordenadas = sorted(regiones_unicas.tolist())

    # 2. Resumen ordenado por cantidad de dispositivos
    if mostrar_conteo:
        resumen = (
            df.groupby(col_region, observed=False)
            .agg(
                Registros=('id_device', 'count'),
                Dispositivos_Unicos=('id_device', 'nunique')
            )
            .sort_values(by='Dispositivos_Unicos', ascending=False)
            .reset_index()
        )
        print("=" * 65)
        print("REGIONES DISPONIBLES EN EL DATASET")
        print("=" * 65)
        print(resumen.to_string(index=False))
        print("=" * 65)
        print(f"Total regiones encontradas: {len(regiones_ordenadas)}")
        print(f"Lista para copiar: {regiones_ordenadas}\n")

    return regiones_ordenadas

# =====================================================================
# 0. FILTRO PARA OOKLA
# =====================================================================

def filtrar_por_codigo_postal(df, codigos_postales):
    """
    Filtra el DataFrame según uno o varios códigos postales (attr_place_postal_code),
    garantizando que el dato de la columna sea tratado estrictamente como entero.
    
    Parámetros:
    - df (pd.DataFrame): DataFrame de entrada (ej. dfMes1, dfMesA).
    - codigos_postales (list, int, str): Lista de códigos postales o un único código.
    
    Retorna:
    - pd.DataFrame: DataFrame filtrado.
    """
    df_filtrado = df.copy()
    
    # 1. Convertir la columna a numérico y forzar el tipo entero (Int64), ignorando errores/nulos
    df_filtrado['attr_place_postal_code'] = pd.to_numeric(
        df_filtrado['attr_place_postal_code'], 
        errors='coerce'
    ).astype('Int64')
    
    # 2. Asegurar que los códigos de entrada sean siempre una lista para poder usar .isin()
    if not isinstance(codigos_postales, list):
        codigos_postales = [codigos_postales]
        
    # Limpiamos la lista de entrada para asegurarnos de que sean enteros puros y coincidan
    codigos_postales = [int(cp) for cp in codigos_postales if pd.notna(cp)]
    
    # 3. Filtrar evaluando que el código postal esté en la lista indicada[cite: 3]
    df_final = df_filtrado[df_filtrado['attr_place_postal_code'].isin(codigos_postales)].copy()
    
    # Aviso por si la consulta queda vacía
    if df_final.empty:
        print(f"[Aviso] No se encontraron datos para los códigos postales: {codigos_postales}")
        
    return df_final

def filtrar_por_subregion(df, subregiones):
    """
    Filtra el DataFrame según una o varias subregiones (attr_place_subregion).
    
    Parámetros:
    - df (pd.DataFrame): DataFrame de entrada (ej. dfMes1, dfMesA).
    - subregiones (list, str): Lista de subregiones o una única subregión.
    
    Retorna:
    - pd.DataFrame: DataFrame filtrado.
    """
    df_filtrado = df.copy()
    
    # 1. Asegurar que la entrada sea siempre una lista para poder usar .isin()
    if not isinstance(subregiones, list):
        subregiones = [subregiones]
        
    # 2. Filtrar evaluando que la subregión esté en la lista indicada
    df_final = df_filtrado[df_filtrado['attr_place_subregion'].isin(subregiones)].copy()
    
    # Aviso por si la consulta queda vacía
    if df_final.empty:
        print(f"[Aviso] No se encontraron datos para las subregiones: {subregiones}")
        
    return df_final

def filtrar_por_lugar(df, lugar):
    """
    Filtra el DataFrame según una o varias subregiones (attr_place_subregion).
    
    Parámetros:
    - df (pd.DataFrame): DataFrame de entrada (ej. dfMes1, dfMesA).
    - subregiones (list, str): Lista de subregiones o una única subregión.
    
    Retorna:
    - pd.DataFrame: DataFrame filtrado.
    """
    df_filtrado = df.copy()
    
    # 1. Asegurar que la entrada sea siempre una lista para poder usar .isin()
    if not isinstance(lugar, list):
        lugar = [lugar]
        
    # 2. Filtrar evaluando que la subregión esté en la lista indicada
    df_final = df_filtrado[df_filtrado['attr_place_name'].isin(lugar)].copy()
    
    # Aviso por si la consulta queda vacía
    if df_final.empty:
        print(f"[Aviso] No se encontraron datos para los lugares: {lugar}")
        
    return df_final

# =====================================================================
# 1. FUNCIONES DE FILTRADO
# =====================================================================

def filtrar_clientes(df, compania, estado='Activo', mostrar_resumen=True):
    df_filtrado = df.copy()

    # 1. Limpiar BOM (\ufeff), espacios y caracteres invisibles de todas las columnas
    df_filtrado.columns = (
        df_filtrado.columns
        .astype(str)
        .str.replace('\ufeff', '', regex=False)
        .str.strip()
    )

    # 2. Localizar columna de Compañía de forma 100% infalible
    col_compania = None
    posibles_nombres = [
        'Compañía', 'Compañia', 'Compania', 
        'compañía', 'compañia', 'compania',
        'Contrato/Compañía', 'Contrato/Compañia'
    ]
    
    # Intento 1: Coincidencia en lista conocida
    for nombre in posibles_nombres:
        if nombre in df_filtrado.columns:
            col_compania = nombre
            break

    # Intento 2: Búsqueda flexible (detecta incluso si vino corrupto como 'CompaÃ±Ã­a')
    if col_compania is None:
        for col in df_filtrado.columns:
            col_baja = col.lower()
            if 'compa' in col_baja or 'comp' in col_baja:
                col_compania = col
                break

    # Intento 3: Si tiene la estructura típica de Odoo, Compañía es la 2da columna (índice 1)
    if col_compania is None and len(df_filtrado.columns) > 1:
        if 'Creado' in df_filtrado.columns[0]:
            col_compania = df_filtrado.columns[1]

    # 3. Aplicar filtro de Compañía
    if compania is not None:
        if col_compania:
            comp_busqueda = compania.strip().lower()
            serie_comp = df_filtrado[col_compania].astype(str).str.strip().str.lower()
            condicion_comp = serie_comp == comp_busqueda
            df_filtrado = df_filtrado[condicion_comp]
        else:
            print(f"[Advertencia] No se encontro columna de Compania. Columnas detectadas: {list(df_filtrado.columns)}")

    # 4. Localizar columna de Estado
    col_estado = None
    for nombre in ['Contrato/Estado', 'Estado', 'estado', 'contrato/estado']:
        if nombre in df_filtrado.columns:
            col_estado = nombre
            break

    # 5. Aplicar filtro de Estado
    if estado is not None:
        if col_estado:
            condicion_est = df_filtrado[col_estado].astype(str).str.strip().str.lower() == estado.strip().lower()
            df_filtrado = df_filtrado[condicion_est]
        else:
            print(f"[Advertencia] No se encontro la columna de Estado.")

    # 6. Mostrar resumen
    if mostrar_resumen:
        print("=" * 60)
        print("RESUMEN DE FILTRADO")
        print("=" * 60)
        print(f" Registros de entrada:  {len(df):,}")
        print(f" Columna Compania usada: '{col_compania}' -> Filtro: {compania if compania else 'Todos'}")
        print(f" Columna Estado usada:   '{col_estado}' -> Filtro: {estado if estado else 'Todos'}")
        print(f" Registros resultantes: {len(df_filtrado):,}")
        print("=" * 60)

    return df_filtrado

def filtrar_clientes_ventas(df, compania, mostrar_resumen=True):
    df_filtrado = df.copy()

    # 1. Limpiar BOM (\ufeff), espacios y caracteres invisibles de todas las columnas
    df_filtrado.columns = (
        df_filtrado.columns
        .astype(str)
        .str.replace('\ufeff', '', regex=False)
        .str.strip()
    )

    # 2. Localizar columna de Compañía de forma 100% infalible
    col_compania = None
    posibles_nombres = [
        'Compañía', 'Compañia', 'Compania', 
        'compañía', 'compañia', 'compania',
        'Contrato/Compañía', 'Contrato/Compañia'
    ]
    
    # Intento 1: Coincidencia en lista conocida
    for nombre in posibles_nombres:
        if nombre in df_filtrado.columns:
            col_compania = nombre
            break

    # Intento 2: Búsqueda flexible (detecta incluso si vino corrupto como 'CompaÃ±Ã­a')
    if col_compania is None:
        for col in df_filtrado.columns:
            col_baja = col.lower()
            if 'compa' in col_baja or 'comp' in col_baja:
                col_compania = col
                break

    # Intento 3: Si tiene la estructura típica de Odoo, Compañía es la 2da columna (índice 1)
    if col_compania is None and len(df_filtrado.columns) > 1:
        if 'Creado' in df_filtrado.columns[0]:
            col_compania = df_filtrado.columns[1]

    # 3. Aplicar filtro de Compañía
    if compania is not None:
        if col_compania:
            comp_busqueda = compania.strip().lower()
            serie_comp = df_filtrado[col_compania].astype(str).str.strip().str.lower()
            condicion_comp = serie_comp == comp_busqueda
            df_filtrado = df_filtrado[condicion_comp]
        else:
            print(f"[Advertencia] No se encontro columna de Compania. Columnas detectadas: {list(df_filtrado.columns)}")

    # 6. Mostrar resumen
    if mostrar_resumen:
        print("=" * 60)
        print("RESUMEN DE FILTRADO")
        print("=" * 60)
        print(f" Registros de entrada:  {len(df):,}")
        print(f" Columna Compania usada: '{col_compania}' -> Filtro: {compania if compania else 'Todos'}")
#        print(f" Columna Estado usada:   '{col_estado}' -> Filtro: {estado if estado else 'Todos'}")
        print(f" Registros resultantes: {len(df_filtrado):,}")
        print("=" * 60)

    return df_filtrado

def filtrar_clientes_porsede(df, compania, estado='Activo', mostrar_resumen=True):
    df_filtrado = df.copy()

    col_compania = None
    for posible_nombre in ['Compania', 'Compañía', 'Compañia', 'compania', 'compañia']:
        if posible_nombre in df_filtrado.columns:
            col_compania = posible_nombre
            break

    if compania is not None:
        if col_compania:
            condicion_comp = df_filtrado[col_compania].astype(str).str.strip().str.lower() == compania.strip().lower()
            df_filtrado = df_filtrado[condicion_comp]
        else:
            print("[Advertencia] No se encontro columna de Compania.")

    if mostrar_resumen:
        print("=" * 60)
        print("RESUMEN DE FILTRADO")
        print("=" * 60)
        print(f" Registros de entrada:  {len(df):,}")
        print(f" Filtro Compania:       {compania if compania else 'Todos'}")
        print(f" Registros resultantes: {len(df_filtrado):,}")
        print("=" * 60)

    return df_filtrado
    

def consultar_lugares_por_region(df, region=None, mostrar_conteo=True):
    """
    Consulta y lista todas las localidades/lugares (attr_place_name) unicos presentes,
    con la opcion de filtrar por una region especifica (attr_place_region).
    
    Parametros:
    - df (pd.DataFrame): DataFrame con la data cruda.
    - region (str, opcional): Nombre de la region a filtrar (ej: 'Guarico', 'Lara'). Si es None, muestra todo el dataset.
    - mostrar_conteo (bool): Si es True, imprime la tabla detallada de registros y dispositivos unicos.
    
    Retorna:
    - list: Lista exacta de nombres de localidades (attr_place_name).
    """
    col_lugar = 'attr_place_name'
    col_region = 'attr_place_region'

    if col_lugar not in df.columns:
        print(f"[Advertencia] No se encontro la columna '{col_lugar}' en el DataFrame.")
        return []

    df_filtrado = df.copy()

    # 1. Filtro opcional por region
    if region is not None:
        if col_region in df_filtrado.columns:
            condicion_region = df_filtrado[col_region].astype(str).str.contains(region, case=False, na=False)
            df_filtrado = df_filtrado[condicion_region]
        else:
            print(f"[Advertencia] No se encontro la columna '{col_region}'.")

    if len(df_filtrado) == 0:
        print(f"[Advertencia] No se encontraron registros para la region '{region}'.")
        return []

    # 2. Obtener lista exacta de lugares unicos
    lugares_exactos = df_filtrado[col_lugar].dropna().unique().tolist()

    # 3. Mostrar resumen en pantalla
    if mostrar_conteo:
        resumen = (
            df_filtrado.groupby(col_lugar, observed=False)
            .agg(
                Registros=('id_device', 'count'),
                Dispositivos_Unicos=('id_device', 'nunique')
            )
            .sort_values(by='Dispositivos_Unicos', ascending=False)
            .reset_index()
        )
        titulo = f"LUGARES (attr_place_name) ENCONTRADOS" + (f" EN: {region.upper()}" if region else "")
        print("=" * 65)
        print(titulo)
        print("=" * 65)
        print(resumen.to_string(index=False))
        print("=" * 65)
        print(f"Total lugares: {len(lugares_exactos)}")
        print(f"Lista exacta para copiar: {lugares_exactos}\n")

    return lugares_exactos


# =====================================================================
# 4. FILTRADO POR SEGMENTO B2B / B2C (PLANTILLA DE CONTRATO)
# =====================================================================

PATRON_EXCLUSION_B2B = (
    r'DEDICAD|'
    r'TELEFONICA|'
    r'CORPORATIVO|'
    r'BES EMPRESARIAL|'
    r'TRANSPORTE|'
    r'EXONERAD|'
    r'CATV|'
    r'REPLICA|'
    r'SIMPLE\s*TV|'
    r'CONATEL'
)


def _obtener_columna_plantilla(df):
    """
    Busca de manera robusta la columna de plantilla de contrato.
    """
    posibles_nombres = [
        'Plantilla de contrato', 
        'Contrato/Plantilla de contrato', 
        'plantilla de contrato',
        'plantilla_contrato'
    ]
    for col in posibles_nombres:
        if col in df.columns:
            return col
    return None

def filtrar_clientesB2C(df, patron_exclusion=PATRON_EXCLUSION_B2B, mostrar_resumen=True):
    """
    Filtra los clientes residenciales (B2C) excluyendo los contratos empresariales,
    dedicados, exonerados, corporativos, etc.
    """
    col_plantilla = _obtener_columna_plantilla(df)
    
    if not col_plantilla:
        print("[Advertencia] No se encontro la columna 'Plantilla de contrato' o 'Contrato/Plantilla de contrato'.")
        return df.copy()

    # Aplica NOT (~) sobre el patron de exclusion
    condicion_residencial = ~df[col_plantilla].astype(str).str.contains(
        patron_exclusion, case=False, na=False
    )
    df_residencial = df[condicion_residencial].copy()

    if mostrar_resumen:
        print("=" * 60)
        print("RESUMEN FILTRADO B2C (RESIDENCIAL)")
        print("=" * 60)
        print(f"• Registros totales de entrada: {len(df):,}")
        print(f"• Registros B2C resultantes:    {len(df_residencial):,}")
        print(f"• Registros B2B/Excluidos:      {len(df) - len(df_residencial):,}")
        print("=" * 60)

    return df_residencial


def filtrar_clientesB2B(df, patron_inclusion=PATRON_EXCLUSION_B2B, mostrar_resumen=True):
    """
    Filtra los clientes corporativos/empresariales (B2B) conservando únicamente
    los contratos que coinciden con el patron (Dedicados, Corporativos, etc.).
    """
    col_plantilla = _obtener_columna_plantilla(df)
    
    if not col_plantilla:
        print("[Advertencia] No se encontro la columna 'Plantilla de contrato' o 'Contrato/Plantilla de contrato'.")
        return df.copy()

    # Conserva unicamente los que coinciden con el patron corporativo
    condicion_corporativo = df[col_plantilla].astype(str).str.contains(
        patron_inclusion, case=False, na=False
    )
    df_corporativo = df[condicion_corporativo].copy()

    if mostrar_resumen:
        print("=" * 60)
        print("RESUMEN FILTRADO B2B (EMPRESARIAL / CORPORATIVO)")
        print("=" * 60)
        print(f"• Registros totales de entrada: {len(df):,}")
        print(f"• Registros B2B resultantes:    {len(df_corporativo):,}")
        print(f"• Registros B2C descartados:    {len(df) - len(df_corporativo):,}")
        print("=" * 60)

    return df_corporativo


# =====================================================================
# 2. CALCULO DE MARKET SHARE
# =====================================================================

def calcular_marketshare_region(df, region):
    df_postal = df[df['attr_place_region'] == region].copy()
    
    proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
    df_postal = df_postal[~df_postal['attr_provider_name_common'].isin(proveedores_excluir)]
    
    reemplazos = {
        'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
        'Netuno': 'NetUno',
        'Cable Norte': 'Norte'
    }
    df_postal['attr_provider_name_common'] = df_postal['attr_provider_name_common'].replace(reemplazos)
    
    marketshare = df_postal.groupby('attr_provider_name_common')['id_device'].nunique().reset_index()
    marketshare = marketshare.sort_values(by='id_device', ascending=False)
    
    total_dispositivos_real = marketshare['id_device'].sum()
    if total_dispositivos_real == 0:
        return pd.DataFrame()
        
    top_10 = marketshare.head(10).copy()
    dispositivos_top_10 = top_10['id_device'].sum()
    dispositivos_otros = total_dispositivos_real - dispositivos_top_10
    
    df_otros = pd.DataFrame({'attr_provider_name_common': ['Otros'], 'id_device': [dispositivos_otros]})
    marketshare_final = pd.concat([top_10, df_otros], ignore_index=True)
    marketshare_final['porcentaje'] = (marketshare_final['id_device'] / total_dispositivos_real) * 100
    
    df_pivot = marketshare_final.set_index('attr_provider_name_common')[['porcentaje']].T
    return df_pivot


def calcular_marketshare_codigoPostal(df, municipio):
    df_postal = df[df['attr_place_postal_code'].isin(municipio)].copy()
    
    proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
    df_postal = df_postal[~df_postal['attr_provider_name_common'].isin(proveedores_excluir)]
    
    reemplazos = {
        'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
        'Netuno': 'NetUno',
        'Cable Norte': 'Norte'
    }
    df_postal['attr_provider_name_common'] = df_postal['attr_provider_name_common'].replace(reemplazos)
    
    marketshare = df_postal.groupby('attr_provider_name_common')['id_device'].nunique().reset_index()
    marketshare = marketshare.sort_values(by='id_device', ascending=False)
    
    total_dispositivos_real = marketshare['id_device'].sum()
    if total_dispositivos_real == 0:
        return pd.DataFrame()

    top_10 = marketshare.head(10).copy()
    dispositivos_top_10 = top_10['id_device'].sum()
    dispositivos_otros = total_dispositivos_real - dispositivos_top_10
    
    df_otros = pd.DataFrame({'attr_provider_name_common': ['Otros'], 'id_device': [dispositivos_otros]})
    marketshare_final = pd.concat([top_10, df_otros], ignore_index=True)
    marketshare_final['porcentaje'] = (marketshare_final['id_device'] / total_dispositivos_real) * 100
    
    df_pivot = marketshare_final.set_index('attr_provider_name_common')[['porcentaje']].T
    return df_pivot

def calcular_marketshare_subregiones(df, subregiones, region):
    """
    Calcula el Market Share agrupando una o varias subregiones (attr_place_subregion),
    con la opcion de acotarlo a una region/estado especifico (attr_place_region).
    
    Parametros:
    - df (pd.DataFrame): DataFrame con los datos crudos.
    - subregiones (list o str): Lista de subregiones a evaluar (ej: ['Francisco de Miranda', 'Roscio']) 
                                o una sola subregion como texto.
    - region (str, opcional): Region o estado al que deben pertenecer esas subregiones (ej: 'Guarico', 'Lara').
                                
    Retorna:
    - pd.DataFrame: DataFrame pivotado con los porcentajes de Market Share.
    """
    df_sub = df.copy()

    # 1. Filtro opcional por Region (si se especifica, casa primero con el estado)
    if region is not None:
        condicion_region = df_sub['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
        df_sub = df_sub[condicion_region]

    # 2. Asegurar que subregiones sea siempre una lista
    if isinstance(subregiones, str):
        subregiones = [subregiones]
        
    # 3. Filtrar evaluando que la subregion este presente en la lista proporcionada
    df_sub = df_sub[df_sub['attr_place_subregion'].isin(subregiones)].copy()
    
    # 4. Exclusion de proveedores celulares/inalambricos
    proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
    df_sub = df_sub[~df_sub['attr_provider_name_common'].isin(proveedores_excluir)]
    
    # 5. Reemplazo unificado de nombres comerciales
    reemplazos = {
        'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
        'Netuno': 'NetUno',
        'Cable Norte': 'Norte'
    }
    df_sub['attr_provider_name_common'] = df_sub['attr_provider_name_common'].replace(reemplazos)
    
    # 6. Agrupar y contar dispositivos unicos por proveedor
    marketshare = df_sub.groupby('attr_provider_name_common')['id_device'].nunique().reset_index()
    marketshare = marketshare.sort_values(by='id_device', ascending=False)
    
    # 7. Obtener la poblacion total real de dispositivos
    total_dispositivos_real = marketshare['id_device'].sum()
    if total_dispositivos_real == 0:
        ubicacion = f"subregiones: {subregiones}" + (f" en la region '{region}'" if region else "")
        print(f"[Aviso] No se encontraron datos para {ubicacion}")
        return pd.DataFrame()
        
    # 8. Separar estrictamente el Top 10 y acumular el resto en 'Otros'
    top_10 = marketshare.head(10).copy()
    dispositivos_top_10 = top_10['id_device'].sum()
    dispositivos_otros = total_dispositivos_real - dispositivos_top_10
    
    df_otros = pd.DataFrame({'attr_provider_name_common': ['Otros'], 'id_device': [dispositivos_otros]})
    marketshare_final = pd.concat([top_10, df_otros], ignore_index=True)
    
    # 9. Calcular porcentajes
    marketshare_final['porcentaje'] = (marketshare_final['id_device'] / total_dispositivos_real) * 100
    
    # 10. Pivotar y retornar
    df_pivot = marketshare_final.set_index('attr_provider_name_common')[['porcentaje']].T
    return df_pivot

def calcular_marketshare_subregionesV2(df, subregiones, region):
    """
    Calcula el Market Share agrupando una o varias subregiones (attr_place_subregion),
    con la opción de acotarlo a una región/estado específico (attr_place_region)
    e identifica los 5 primeros proveedores principales.
    """
    df_sub = df.copy()

    # 1. Filtro opcional por Región
    if region is not None:
        condicion_region = df_sub['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
        df_sub = df_sub[condicion_region]

    # 2. Asegurar que subregiones sea siempre una lista
    if isinstance(subregiones, str):
        subregiones = [subregiones]
        
    # 3. Filtrar evaluando que la subregión esté presente
    df_sub = df_sub[df_sub['attr_place_subregion'].isin(subregiones)].copy()
    
    # 4. Exclusión de proveedores celulares/inalámbricos
    proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
    df_sub = df_sub[~df_sub['attr_provider_name_common'].isin(proveedores_excluir)]
    
    # 5. Reemplazo unificado de nombres comerciales
    reemplazos = {
        'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
        'Netuno': 'NetUno',
        'Cable Norte': 'Norte'
    }
    df_sub['attr_provider_name_common'] = df_sub['attr_provider_name_common'].replace(reemplazos)
    
    # 6. Agrupar y contar dispositivos únicos por proveedor
    marketshare = df_sub.groupby('attr_provider_name_common')['id_device'].nunique().reset_index()
    marketshare = marketshare.sort_values(by='id_device', ascending=False)
    
    # 7. Obtener la población total real de dispositivos
    total_dispositivos_real = marketshare['id_device'].sum()
    if total_dispositivos_real == 0:
        ubicacion = f"subregiones: {subregiones}" + (f" en la región '{region}'" if region else "")
        print(f"[Aviso] No se encontraron datos para {ubicacion}")
        return pd.DataFrame(), ""
        
    # EXTRA: Obtener el texto con los nombres de los 5 primeros proveedores
    top_5_nombres = marketshare.head(5)['attr_provider_name_common'].tolist()
    texto_top_5 = ", ".join(top_5_nombres)
    
    # 8. Separar estrictamente el Top 10 y acumular el resto en 'Otros'
    top_10 = marketshare.head(10).copy()
    dispositivos_top_10 = top_10['id_device'].sum()
    dispositivos_otros = total_dispositivos_real - dispositivos_top_10
    
    df_otros = pd.DataFrame({'attr_provider_name_common': ['Otros'], 'id_device': [dispositivos_otros]})
    marketshare_final = pd.concat([top_10, df_otros], ignore_index=True)
    
    # 9. Calcular porcentajes
    marketshare_final['porcentaje'] = (marketshare_final['id_device'] / total_dispositivos_real) * 100
    
    # 10. Pivotar y retornar tanto la tabla como el texto informativo de los 5 principales
    df_pivot = marketshare_final.set_index('attr_provider_name_common')[['porcentaje']].T
    
    return df_pivot, texto_top_5

def calcular_marketshare_lugares(df, lugares, region=None):
    """
    Calcula el Market Share agrupando una o varias localidades especificas (attr_place_name),
    con la opcion de acotarlo a una region/estado (attr_place_region).
    
    Parametros:
    - df (pd.DataFrame): DataFrame con los datos crudos.
    - lugares (list o str): Lista de localidades a evaluar (ej: ['Calabozo']) 
                            o una sola localidad como texto.
    - region (str, opcional): Region a la que deben pertenecer (ej: 'Guarico').
                                
    Retorna:
    - pd.DataFrame: DataFrame pivotado con los porcentajes de Market Share.
    """
    df_loc = df.copy()

    # 1. Filtro opcional por Region (acota al estado)
    if region is not None:
        condicion_region = df_loc['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
        df_loc = df_loc[condicion_region]

    # 2. Asegurar que lugares sea siempre una lista
    if isinstance(lugares, str):
        lugares = [lugares]
        
    # 3. Filtrar evaluando que el lugar este en la lista indicada
    df_loc = df_loc[df_loc['attr_place_name'].isin(lugares)].copy()
    
    # 4. Exclusion de operadores moviles
    proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
    df_loc = df_loc[~df_loc['attr_provider_name_common'].isin(proveedores_excluir)]
    
    # 5. Reemplazo unificado de nombres comerciales
    reemplazos = {
        'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
        'Netuno': 'NetUno',
        'Cable Norte': 'Norte'
    }
    df_loc['attr_provider_name_common'] = df_loc['attr_provider_name_common'].replace(reemplazos)
    
    # 6. Agrupar y contar dispositivos unicos por proveedor
    marketshare = df_loc.groupby('attr_provider_name_common')['id_device'].nunique().reset_index()
    marketshare = marketshare.sort_values(by='id_device', ascending=False)
    
    # 7. Obtener total real de dispositivos
    total_dispositivos_real = marketshare['id_device'].sum()
    if total_dispositivos_real == 0:
        ubicacion = f"lugares: {lugares}" + (f" en la region '{region}'" if region else "")
        print(f"[Aviso] No se encontraron datos para {ubicacion}")
        return pd.DataFrame()
        
    # 8. Separar Top 10 y agrupar el resto en 'Otros'
    top_10 = marketshare.head(10).copy()
    dispositivos_top_10 = top_10['id_device'].sum()
    dispositivos_otros = total_dispositivos_real - dispositivos_top_10
    
    df_otros = pd.DataFrame({'attr_provider_name_common': ['Otros'], 'id_device': [dispositivos_otros]})
    marketshare_final = pd.concat([top_10, df_otros], ignore_index=True)
    
    # 9. Calcular porcentajes
    marketshare_final['porcentaje'] = (marketshare_final['id_device'] / total_dispositivos_real) * 100
    
    # 10. Pivotar y retornar
    df_pivot = marketshare_final.set_index('attr_provider_name_common')[['porcentaje']].T
    return df_pivot

# =====================================================================
# 3. GRAFICOS Y VISUALIZACION
# =====================================================================

def generar_grafico_evolucion_marketshare(lista_dfs, lista_titulos, 
                                          diccionario_colores=None, 
                                          ruta_exportacion=None, 
                                          figsize=None,
                                          ncol_leyenda=6,
                                          umbral_etiqueta=2.0):
    """
    Genera una fila de graficos de barras apiladas para comparar la evolucion 
    temporal del Market Share entre meses, con leyenda global unificada y ordenada.
    """
    if len(lista_dfs) != len(lista_titulos):
        raise ValueError("La cantidad de DataFrames debe ser igual a la cantidad de titulos.")

    if diccionario_colores is None:
        diccionario_colores = COLORES_PROVEEDORES

    n_graficos = len(lista_dfs)
    
    if figsize is None:
        figsize = (max(14, n_graficos * 2.7), 12)

    fig, axes = plt.subplots(1, n_graficos, figsize=figsize)
    if n_graficos == 1:
        axes = [axes]

    todos_los_handles = {}

    for i, (df_plot, ax, titulo) in enumerate(zip(lista_dfs, axes, lista_titulos)):
        lista_colores = [diccionario_colores.get(prov, '#CCCCCC') for prov in df_plot.columns]
        df_plot.plot(kind='bar', stacked=True, ax=ax, color=lista_colores)

        handles, labels = ax.get_legend_handles_labels()
        for handle, label in zip(handles, labels):
            if label not in todos_los_handles:
                todos_los_handles[label] = handle

        for p in ax.patches:
            height = p.get_height()
            if height > umbral_etiqueta:
                ax.text(
                    p.get_x() + p.get_width() / 2, 
                    p.get_y() + height / 2, 
                    f'{height:.1f}%', 
                    ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=18
                )

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xticks([])

        ax.set_title(titulo, fontsize=25, pad=20)
        ax.set_ylabel('Porcentaje (%)' if i == 0 else '')

        if ax.get_legend() is not None:
            ax.get_legend().remove()

    labels_ordenados = sorted(todos_los_handles.keys())
    handles_ordenados = [todos_los_handles[lbl] for lbl in labels_ordenados]

    fig.legend(
        handles_ordenados, 
        labels_ordenados, 
        title_fontsize=25,
        loc='upper center', 
        bbox_to_anchor=(0.5, 0.20),
        ncol=ncol_leyenda,
        fontsize=18,
        frameon=False
    )

    plt.subplots_adjust(bottom=0.25)

    if ruta_exportacion:
        plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
        print(f"Grafico guardado exitosamente en: {ruta_exportacion}")

    plt.show()
    plt.close()

import matplotlib.pyplot as plt
import textwrap

import matplotlib.pyplot as plt

def generar_grafico_evolucion_marketsharev2(lista_dfs, lista_titulos, 
                                          diccionario_colores=None, 
                                          ruta_exportacion=None, 
                                          figsize=None,
                                          ncol_leyenda=6,
                                          umbral_etiqueta=2.0):
    """
    Genera una fila de gráficos de barras apiladas, ubicando el Top 5 
    de proveedores en un cuadro de texto a la derecha de cada columna.
    """
    if len(lista_dfs) != len(lista_titulos):
        raise ValueError("La cantidad de DataFrames debe ser igual a la cantidad de títulos.")

    if diccionario_colores is None:
        diccionario_colores = COLORES_PROVEEDORES

    n_graficos = len(lista_dfs)
    
    # Aumentamos ligeramente el ancho base para dar espacio al texto lateral
    if figsize is None:
        figsize = (max(16, n_graficos * 3.5), 12)

    fig, axes = plt.subplots(1, n_graficos, figsize=figsize)
    if n_graficos == 1:
        axes = [axes]

    todos_los_handles = {}

    for i, (df_plot, ax, titulo) in enumerate(zip(lista_dfs, axes, lista_titulos)):
        lista_colores = [diccionario_colores.get(prov, '#CCCCCC') for prov in df_plot.columns]
        
        # Generar la barra (por defecto se ubica en x=0 con un ancho de 0.5)
        df_plot.plot(kind='bar', stacked=True, ax=ax, color=lista_colores, width=0.5)

        # 1. EXTRAER EL TOP 5 Y FORMATEARLO COMO LISTA VERTICAL
        cols_proveedores = [col for col in df_plot.columns if col != 'Otros']
        lista_top = [f"• {prov}" for prov in cols_proveedores[:5]]
        texto_lateral = "** Top 5 **\n\n" + "\n".join(lista_top)

        # Recopilar leyendas
        handles, labels = ax.get_legend_handles_labels()
        for handle, label in zip(handles, labels):
            if label not in todos_los_handles:
                todos_los_handles[label] = handle

        # Dibujar porcentajes dentro de las barras
        for p in ax.patches:
            height = p.get_height()
            if height > umbral_etiqueta:
                ax.text(
                    p.get_x() + p.get_width() / 2, 
                    p.get_y() + height / 2, 
                    f'{height:.1f}%', 
                    ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=16
                )

        # Limpieza visual del gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xticks([])

        ax.set_title(titulo, fontsize=22, pad=20)
        
        # 2. AMPLIAR EL EJE X PARA HACER ESPACIO AL TEXTO
        # La barra va de x=-0.25 a x=0.25. Damos espacio hasta x=1.3 para que quepa el cuadro.
        ax.set_xlim(-0.3, 1.3)
        
        # 3. COLOCAR EL CUADRO DE TEXTO AL LADO DE LA COLUMNA
        # x=0.35 ubica el texto justo a la derecha de la barra.
        # y=50 ubica el texto en la mitad vertical exacta (ya que el total es 100%).
        ax.text(
            0.32, 50, 
            texto_lateral, 
            ha='left', va='center', 
            fontsize=13, 
            color='#333333',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8F9FA', edgecolor='#DDDDDD', alpha=0.9)
        )

        if ax.get_legend() is not None:
            ax.get_legend().remove()

    labels_ordenados = sorted(todos_los_handles.keys())
    handles_ordenados = [todos_los_handles[lbl] for lbl in labels_ordenados]

    fig.legend(
        handles_ordenados, 
        labels_ordenados, 
        title_fontsize=22,
        loc='upper center', 
        bbox_to_anchor=(0.5, 0.15),
        ncol=ncol_leyenda,
        fontsize=16,
        frameon=False
    )

    # Ajustar espacios generales
    plt.subplots_adjust(bottom=0.20, wspace=0.1)

    if ruta_exportacion:
        plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
        print(f"Gráfico guardado exitosamente en: {ruta_exportacion}")

    plt.show()
    plt.close()

import matplotlib.pyplot as plt

def generar_grafico_evolucion_marketsharev3(lista_dfs, lista_titulos, 
                                          diccionario_colores=None, 
                                          ruta_exportacion=None, 
                                          figsize=None,
                                          ncol_leyenda=6,
                                          umbral_etiqueta=2.0):
    """
    Genera una fila de gráficos de barras apiladas, ubicando el Top 5 
    de proveedores en un cuadro de texto lateral, numerado e invertido 
    para coincidir con el apilado visual de la columna.
    """
    if len(lista_dfs) != len(lista_titulos):
        raise ValueError("La cantidad de DataFrames debe ser igual a la cantidad de títulos.")

    if diccionario_colores is None:
        diccionario_colores = COLORES_PROVEEDORES

    n_graficos = len(lista_dfs)
    
    if figsize is None:
        figsize = (max(16, n_graficos * 3.5), 12)

    fig, axes = plt.subplots(1, n_graficos, figsize=figsize)
    if n_graficos == 1:
        axes = [axes]

    todos_los_handles = {}

    for i, (df_plot, ax, titulo) in enumerate(zip(lista_dfs, axes, lista_titulos)):
        lista_colores = [diccionario_colores.get(prov, '#CCCCCC') for prov in df_plot.columns]
        
        # Generar la barra
        df_plot.plot(kind='bar', stacked=True, ax=ax, color=lista_colores, width=0.5)

        # 1. EXTRAER, NUMERAR E INVERTIR EL TOP 5
        cols_proveedores = [col for col in df_plot.columns if col != 'Otros']
        top_5 = cols_proveedores[:5]
        
        # Crear la lista con formato "1. Proveedor"
        lista_top = [f"{idx + 1}. {prov}" for idx, prov in enumerate(top_5)]
        
        # Invertir el orden de la lista para que el #1 quede en la parte inferior del texto,
        # coincidiendo con el primer bloque en la base de la columna.
        lista_top.reverse()
        
        texto_lateral = "** Top 5 **\n\n" + "\n".join(lista_top)

        # Recopilar leyendas
        handles, labels = ax.get_legend_handles_labels()
        for handle, label in zip(handles, labels):
            if label not in todos_los_handles:
                todos_los_handles[label] = handle

        # Dibujar porcentajes dentro de las barras
        for p in ax.patches:
            height = p.get_height()
            if height > umbral_etiqueta:
                ax.text(
                    p.get_x() + p.get_width() / 2, 
                    p.get_y() + height / 2, 
                    f'{height:.1f}%', 
                    ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=16
                )

        # Limpieza visual del gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xticks([])

        ax.set_title(titulo, fontsize=22, pad=20)
        
        # 2. AMPLIAR EL EJE X Y COLOCAR EL CUADRO DE TEXTO
        ax.set_xlim(-0.3, 1.3)
        
        ax.text(
            0.32, 50, 
            texto_lateral, 
            ha='left', va='center', 
            fontsize=13, 
            color='#333333',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8F9FA', edgecolor='#DDDDDD', alpha=0.9)
        )

        if ax.get_legend() is not None:
            ax.get_legend().remove()

    labels_ordenados = sorted(todos_los_handles.keys())
    handles_ordenados = [todos_los_handles[lbl] for lbl in labels_ordenados]

    fig.legend(
        handles_ordenados, 
        labels_ordenados, 
        title_fontsize=22,
        loc='upper center', 
        bbox_to_anchor=(0.5, 0.15),
        ncol=ncol_leyenda,
        fontsize=16,
        frameon=False
    )

    plt.subplots_adjust(bottom=0.20, wspace=0.1)

    if ruta_exportacion:
        plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
        print(f"Gráfico guardado exitosamente en: {ruta_exportacion}")

    plt.show()
    plt.close()


def generar_grafico_barras(df_pivot, titulo, diccionario_colores=None):
    """
    Genera un unico grafico de barras apiladas a partir de un DataFrame pivotado.
    """
    if diccionario_colores is None:
        diccionario_colores = COLORES_PROVEEDORES

    lista_colores = [diccionario_colores.get(prov, '#CCCCCC') for prov in df_pivot.columns] 
    ax1 = df_pivot.plot(kind='bar', stacked=True, figsize=(6, 12), color=lista_colores)

    for p in ax1.patches:
        width, height = p.get_width(), p.get_height()
        if height > 1.5:
            x, y = p.get_xy() 
            ax1.text(x + width / 2, 
                     y + height / 2, 
                     f'{height:.1f}%', 
                     ha='center', 
                     va='center', 
                     color='white', 
                     fontweight='bold')

    plt.title(titulo, pad=20)
    plt.ylabel('Porcentaje Total (%)')
    plt.xticks([])
    plt.legend(title='Proveedores', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def generar_torta_zona_cliente(df, ruta_exportacion="torta_zona_cliente.png"):
    datos = df['Zona Cliente'].value_counts().dropna()
    plt.figure(figsize=(8, 8))
    plt.pie(datos.values, labels=datos.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Distribucion por Zona Cliente', fontweight='bold')
    plt.savefig(ruta_exportacion, bbox_inches='tight')
    plt.close()
    return ruta_exportacion


def generar_torta_plantilla_contrato(df, ruta_exportacion="torta_plantilla_contrato.png"):
    datos = df['Plantilla de contrato'].value_counts().dropna()
    plt.figure(figsize=(8, 8))
    plt.pie(datos.values, labels=datos.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
    plt.title('Distribucion por Plantilla de Contrato', fontweight='bold')
    plt.savefig(ruta_exportacion, bbox_inches='tight')
    plt.close()
    return ruta_exportacion


def generar_tortaventas_zona_cliente(df, ruta_exportacion="torta_zona_cliente.png"):
    datos = df['Contrato/Zona Cliente'].value_counts().dropna()
    plt.figure(figsize=(8, 8))
    plt.pie(datos.values, labels=datos.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Distribucion por Zona Cliente', fontweight='bold')
    plt.savefig(ruta_exportacion, bbox_inches='tight')
    plt.close()
    return ruta_exportacion


def generar_tortaventas_plantilla_contrato(df, ruta_exportacion="torta_plantilla_contrato.png"):
    datos = df['Contrato/Plantilla de contrato'].value_counts().dropna()
    plt.figure(figsize=(8, 8))
    plt.pie(datos.values, labels=datos.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
    plt.title('Distribucion por Plantilla de Contrato', fontweight='bold')
    plt.savefig(ruta_exportacion, bbox_inches='tight')
    plt.close()
    return ruta_exportacion


def generar_tortaventas_listadeprecios(df, ruta_exportacion="torta_plantilla_listaprecios.png"):
    datos = df['Contrato/Lista de precios'].value_counts().dropna()
    plt.figure(figsize=(8, 8))
    plt.pie(datos.values, labels=datos.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Set3.colors)
    plt.title('Distribucion por Lista de Precios', fontweight='bold')
    plt.savefig(ruta_exportacion, bbox_inches='tight')
    plt.close()
    return ruta_exportacion


def generar_grafico_parque(datos_dict, ruta_exportacion="parque_clientes.png"):
    meses = datos_dict["meses"]
    parque_info = datos_dict["parque"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    color_barra = parque_info.get("color", "#2b5c8f")
    bars = ax.bar(meses, parque_info["valores"], color=color_barra, width=0.55)
    
    ax.set_title(parque_info.get("titulo", "Evolucion de Parque B2C de Clientes"), fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel(parque_info.get("unidad", "Total Clientes"), fontsize=11)
    
    max_parque = max(parque_info["valores"]) if parque_info["valores"] else 1
    for bar in bars:
        yval = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0, 
            yval + (max_parque * 0.015), 
            f'{int(yval):,}', 
            ha='center', va='bottom', 
            fontsize=11, fontweight='bold'
        )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
    plt.close()
    return ruta_exportacion


def purgar_graficos_diarios(rutas_archivos):
    for ruta in rutas_archivos:
        if os.path.exists(ruta):
            os.remove(ruta)
            print(f"Archivo eliminado: {ruta}")
        else:
            print(f"Archivo no encontrado: {ruta}")

def generar_grafico_distribucion_velocidades(
    df, 
    region, 
    cantidad_proveedores=6,
    cortes=None, 
    etiquetas=None,
    diccionario_colores=None,
    titulo=None,
    ruta_exportacion=None,
    figsize=(14, 7)
):
    """
    Genera la distribución de usuarios por rango de velocidad y proveedor.

    Parámetros de entrada principales:
    - df (pd.DataFrame): DataFrame con la data del mes (ej: dfMesC).
    - region (str): Región a filtrar (ej: 'Lara', 'Capital District', r'La Guaira|Vargas').
    - cantidad_proveedores (int): Cantidad de proveedores top a mostrar (por defecto 6).
    """
    try:
        # 1. Filtro flexible por region (acepta nombre exacto o regex)
        condicion_region = df['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
        df_region = df[condicion_region].copy()

        if len(df_region) == 0:
            print(f"[Advertencia] No se encontraron registros para la region '{region}'.")
            print("Muestra de regiones disponibles en el DataFrame:")
            print(df['attr_place_region'].dropna().unique()[:10])
            return pd.DataFrame()

        # 2. Exclusión de operadores móviles
        proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
        df_region = df_region[~df_region['attr_provider_name_common'].isin(proveedores_excluir)]

        # 3. Estandarización de nombres
        reemplazos = {
            'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
            'Netuno': 'NetUno',
            'Cable Norte': 'Norte'
        }
        df_region['attr_provider_name_common'] = df_region['attr_provider_name_common'].replace(reemplazos)

        # 4. Filtrar la cantidad de proveedores indicada
        top_proveedores = (
            df_region['attr_provider_name_common']
            .value_counts()
            .nlargest(cantidad_proveedores)
            .index
            .tolist()
        )
        df_plot = df_region[df_region['attr_provider_name_common'].isin(top_proveedores)].copy()

        # 5. Limpieza de velocidades y cortes
        df_plot['val_download_mbps'] = pd.to_numeric(df_plot['val_download_mbps'], errors='coerce')

        if cortes is None:
            cortes = [0, 400, 750, 850, 10000]
        if etiquetas is None:
            etiquetas = ['1) 0 - 400', '2) 401 - 750', '3) 751 - 850', '4) 851 - 1Gbps']

        df_plot['Rango de Velocidades'] = pd.cut(
            df_plot['val_download_mbps'], 
            bins=cortes, 
            labels=etiquetas, 
            include_lowest=True
        )

        # 6. Agrupación por usuarios únicos
        datos_grafico = (
            df_plot.groupby(['Rango de Velocidades', 'attr_provider_name_common'], observed=False)['id_device']
            .nunique()
            .reset_index()
        )
        datos_grafico.rename(columns={'id_device': 'Usuarios'}, inplace=True)

        # 7. Generación del gráfico
        plt.figure(figsize=figsize)
        sns.set_theme(style="whitegrid")

        if diccionario_colores is None:
            diccionario_colores = COLORES_PROVEEDORES

        paleta = {prov: diccionario_colores.get(prov, '#CCCCCC') for prov in top_proveedores}

        grafico = sns.barplot(
            data=datos_grafico,
            x='Rango de Velocidades',
            y='Usuarios',
            hue='attr_provider_name_common',
            palette=paleta
        )

        # Etiquetas de número encima de cada barra
        for p in grafico.patches:
            height = p.get_height()
            if height > 0:
                grafico.annotate(
                    f'{int(height):,}',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold',
                    xytext=(0, 3),
                    textcoords='offset points'
                )

        # 8. Estética y títulos
        if titulo is None:
            titulo = f'Distribucion de Usuarios por Rango de Velocidad y Proveedor ({region})'

        plt.title(titulo, fontsize=15, fontweight='bold', pad=40)
        plt.xlabel('Rango de Velocidades (Mbps)', fontsize=12)
        plt.ylabel('Usuarios (Dispositivos Unicos)', fontsize=12)
        
        plt.legend(
            title='Proveedor', 
            bbox_to_anchor=(0., 1.02, 1., .102), 
            loc='lower center',
            ncol=min(len(top_proveedores), 6), 
            mode=None, 
            borderaxespad=0.,
            frameon=False
        )

        plt.tight_layout()

        if ruta_exportacion:
            plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
            print(f"Grafico guardado exitosamente en: {ruta_exportacion}")

        plt.show()
        plt.close()

        return datos_grafico

    except Exception as e:
        print(f"[Error al ejecutar distribucion de velocidades]: {e}")
        return pd.DataFrame()


import plotly.graph_objects as go
import numpy as np


def generar_grafico_distribucion_latencias(
    df, 
    region, 
    cantidad_proveedores=6,
    cortes=None,
    etiquetas=None,
    diccionario_colores=None,
    titulo=None,
    umbral_texto=8,
    height=700
):
    """
    Genera un grafico de cintas apiladas (ribbons en Plotly) con la distribucion 
    de usuarios segun rangos de latencia minima (ms) y proveedor.

    Parametros:
    - df (pd.DataFrame): DataFrame con la data del mes (ej: dfMesC).
    - region (str): Region a filtrar (ej: 'Lara', 'Capital District', r'La Guaira|Vargas').
    - cantidad_proveedores (int): Cantidad de proveedores top a mostrar (por defecto 6).
    - cortes (list, opcional): Puntos de corte para latencia en ms (por defecto [-1, 2, 4, 5, 11, 33, 10000]).
    - etiquetas (list, opcional): Nombres de los rangos de latencia.
    - diccionario_colores (dict, opcional): Diccionario {proveedor: color_hex}. Si es None usa COLORES_PROVEEDORES.
    - titulo (str, opcional): Titulo del grafico.
    - umbral_texto (int): Cantidad minima de usuarios para mostrar etiqueta de texto en la cinta (por defecto > 8).
    - height (int): Altura del grafico interactivo en pixeles.

    Retorna:
    - go.Figure: Objeto figura de Plotly (tambien ejecuta fig.show()).
    """
    try:
        # 1. Filtro flexible por region
        condicion_region = df['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
        df_region = df[condicion_region].copy()

        if len(df_region) == 0:
            print(f"[Advertencia] No se encontraron registros para la region '{region}'.")
            print("Muestra de regiones disponibles en el DataFrame:")
            print(df['attr_place_region'].dropna().unique()[:10])
            return None

        # 2. Exclusion de operadores moviles
        proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
        df_region = df_region[~df_region['attr_provider_name_common'].isin(proveedores_excluir)]

        # 3. Estandarizacion de nombres
        reemplazos = {
            'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
            'Netuno': 'NetUno',
            'Cable Norte': 'Norte'
        }
        df_region['attr_provider_name_common'] = df_region['attr_provider_name_common'].replace(reemplazos)

        # 4. Filtrar top N proveedores
        top_proveedores = (
            df_region['attr_provider_name_common']
            .value_counts()
            .nlargest(cantidad_proveedores)
            .index
            .tolist()
        )
        df_grafico = df_region[df_region['attr_provider_name_common'].isin(top_proveedores)].copy()

        # 5. Rangos de latencia
        if cortes is None:
            cortes = [-1, 2, 4, 5, 11, 33, 10000]
        if etiquetas is None:
            etiquetas = ['1) < 2', '2) 2 - <4', '3) 4 - <5', '4) 5 - <11', '5) 11 - <33', '6) 33+']

        df_grafico['val_latency_min_ms'] = pd.to_numeric(df_grafico['val_latency_min_ms'], errors='coerce')

        df_grafico['Rango de Latencias'] = pd.cut(
            df_grafico['val_latency_min_ms'], 
            bins=cortes, 
            labels=etiquetas, 
            right=False
        )

        datos_latencia = (
            df_grafico.groupby(['Rango de Latencias', 'attr_provider_name_common'], observed=False)['id_device']
            .nunique()
            .reset_index()
        )
        
        tabla_pivote = datos_latencia.pivot(
            index='Rango de Latencias',
            columns='attr_provider_name_common',
            values='id_device'
        ).fillna(0)

        # Reordenar las columnas segun el orden descendente de volumen
        proveedores_ordenados = tabla_pivote.sum().sort_values(ascending=False).index

        # 6. Truco de cintas (ribbons) con Plotly
        ancho_barra = 0.25
        indices_originales = np.arange(len(tabla_pivote.index))
        
        x_con_grosor = []
        for i in indices_originales:
            x_con_grosor.extend([i - ancho_barra, i + ancho_barra])
        
        fig = go.Figure()
        acumulado_y_por_categoria = np.zeros(len(indices_originales))
        
        if diccionario_colores is None:
            diccionario_colores = COLORES_PROVEEDORES

        for proveedor in proveedores_ordenados:
            valores_originales = tabla_pivote[proveedor].values
            valores_duplicados = np.repeat(valores_originales, 2)
            
            color_hex = diccionario_colores.get(proveedor, '#1f77b4')
            
            # A. Cinta (Ribbon spline)
            fig.add_trace(go.Scatter(
                x=x_con_grosor,
                y=valores_duplicados,
                name=proveedor,
                mode='lines', 
                line=dict(width=0, color=color_hex),
                stackgroup='one', 
                fillcolor=color_hex,
                line_shape='spline',
                hoverinfo='name+y'
            ))

            # B. Posicion de texto en centro de bloque
            posicion_y_texto = acumulado_y_por_categoria + (valores_originales / 2)
            acumulado_y_por_categoria += valores_originales

            textos_etiqueta = []
            for v in valores_originales:
                if v > umbral_texto:
                    textos_etiqueta.append(f"<b>{proveedor}</b><br>{int(v):,}")
                else:
                    textos_etiqueta.append("")

            # C. Capa de texto sobre las barras
            fig.add_trace(go.Scatter(
                x=indices_originales,
                y=posicion_y_texto,
                mode='text',
                text=textos_etiqueta,
                textposition="middle center",
                textfont=dict(color='white', size=10, family="Arial"),
                showlegend=False,
                hoverinfo='skip'
            ))

        # 7. Ajustes de diseno y leyenda
        if titulo is None:
            titulo = f'Distribucion de Latencia (ms) - Top {cantidad_proveedores} Proveedores ({region})'

        fig.update_layout(
            title_text=titulo,
            title_x=0.5,
            plot_bgcolor='white',
            height=height,
            margin=dict(l=20, r=20, t=60, b=120),
            xaxis=dict(
                showgrid=False,
                linecolor='black',
                tickmode='array',
                tickvals=indices_originales,
                ticktext=etiquetas,
                range=[-0.6, len(indices_originales) - 0.4], 
                fixedrange=True
            ),
            yaxis=dict(
                showgrid=False, 
                visible=False,
                rangemode='tozero'
            ),
            legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.1,
                 xanchor="center",
                 x=0.5,
                 bgcolor='rgba(0,0,0,0)'
            )
        )

        return fig

    except Exception as e:
        print(f"[Error al generar grafico de latencias]: {e}")
        return None


    # =====================================================================
# DISTRIBUCIÓN DE VELOCIDADES Y LATENCIAS (CON SOPORTE DE SUBREGIONES)
# =====================================================================

def generar_grafico_distribucion_velocidades(
    df, 
    subregiones=None,
    region=None, 
    cantidad_proveedores=6,
    cortes=None, 
    etiquetas=None,
    diccionario_colores=None,
    titulo=None,
    ruta_exportacion=None,
    figsize=(14, 7)
):
    """
    Genera un gráfico de barras agrupadas con la distribución de usuarios (dispositivos únicos)
    por rangos de velocidad (Mbps) y por proveedor.
    
    Permite filtrar por una lista de subregiones (attr_place_subregion) o por región (attr_place_region).
    """
    try:
        df_filtrado = df.copy()

        # 1. Filtro por subregiones (prioritario) o por región
        if subregiones is not None:
            if isinstance(subregiones, str):
                subregiones = [subregiones]
            condicion_geo = df_filtrado['attr_place_subregion'].isin(subregiones)
            df_plot_base = df_filtrado[condicion_geo].copy()
            etiqueta_geo = ", ".join(subregiones)
        elif region is not None:
            condicion_geo = df_filtrado['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
            df_plot_base = df_filtrado[condicion_geo].copy()
            etiqueta_geo = region
        else:
            raise ValueError("Debes especificar al menos 'subregiones' o 'region'.")

        if len(df_plot_base) == 0:
            print(f"[Advertencia] No se encontraron registros para la ubicación indicada.")
            return pd.DataFrame()

        # 2. Exclusión de operadores móviles
        proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
        df_plot_base = df_plot_base[~df_plot_base['attr_provider_name_common'].isin(proveedores_excluir)]

        # 3. Estandarización de nombres de proveedores
        reemplazos = {
            'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
            'Netuno': 'NetUno',
            'Cable Norte': 'Norte'
        }
        df_plot_base['attr_provider_name_common'] = df_plot_base['attr_provider_name_common'].replace(reemplazos)

        # 4. Filtrar top N proveedores
        top_proveedores = (
            df_plot_base['attr_provider_name_common']
            .value_counts()
            .nlargest(cantidad_proveedores)
            .index
            .tolist()
        )
        df_plot = df_plot_base[df_plot_base['attr_provider_name_common'].isin(top_proveedores)].copy()

        # 5. Limpieza de velocidades y cortes
        df_plot['val_download_mbps'] = pd.to_numeric(df_plot['val_download_mbps'], errors='coerce')

        if cortes is None:
            cortes = [0, 400, 750, 850, 10000]
        if etiquetas is None:
            etiquetas = ['1) 0 - 400', '2) 401 - 750', '3) 751 - 850', '4) 851 - 1Gbps']

        df_plot['Rango de Velocidades'] = pd.cut(
            df_plot['val_download_mbps'], 
            bins=cortes, 
            labels=etiquetas, 
            include_lowest=True
        )

        # 6. Agrupación por usuarios únicos
        datos_grafico = (
            df_plot.groupby(['Rango de Velocidades', 'attr_provider_name_common'], observed=False)['id_device']
            .nunique()
            .reset_index()
        )
        datos_grafico.rename(columns={'id_device': 'Usuarios'}, inplace=True)

        # 7. Generación del gráfico
        plt.figure(figsize=figsize)
        sns.set_theme(style="whitegrid")

        if diccionario_colores is None:
            diccionario_colores = COLORES_PROVEEDORES

        paleta = {prov: diccionario_colores.get(prov, '#CCCCCC') for prov in top_proveedores}

        grafico = sns.barplot(
            data=datos_grafico,
            x='Rango de Velocidades',
            y='Usuarios',
            hue='attr_provider_name_common',
            palette=paleta
        )

        # Etiquetas de número encima de cada barra
        for p in grafico.patches:
            height = p.get_height()
            if height > 0:
                grafico.annotate(
                    f'{int(height):,}',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold',
                    xytext=(0, 3),
                    textcoords='offset points'
                )

        # 8. Estética y títulos
        if titulo is None:
            titulo = f'Distribucion de Usuarios por Rango de Velocidad y Proveedor ({etiqueta_geo})'

        plt.title(titulo, fontsize=15, fontweight='bold', pad=40)
        plt.xlabel('Rango de Velocidades (Mbps)', fontsize=12)
        plt.ylabel('Usuarios (Dispositivos Unicos)', fontsize=12)
        
        plt.legend(
            title='Proveedor', 
            bbox_to_anchor=(0., 1.02, 1., .102), 
            loc='lower center',
            ncol=min(len(top_proveedores), 6), 
            mode=None, 
            borderaxespad=0.,
            frameon=False
        )

        plt.tight_layout()

        if ruta_exportacion:
            plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
            print(f"Grafico guardado exitosamente en: {ruta_exportacion}")

        plt.show()
        plt.close()

        return datos_grafico

    except Exception as e:
        print(f"[Error al ejecutar distribucion de velocidades]: {e}")
        return pd.DataFrame()


def generar_grafico_distribucion_latencias(
    df, 
    subregiones=None,
    region=None, 
    cantidad_proveedores=6,
    cortes=None,
    etiquetas=None,
    diccionario_colores=None,
    titulo=None,
    umbral_texto=8,
    height=700
):
    """
    Genera un gráfico de cintas apiladas (ribbons en Plotly) con la distribución 
    de usuarios según rangos de latencia mínima (ms) y proveedor.
    
    Permite filtrar por una lista de subregiones (attr_place_subregion) o por región (attr_place_region).
    """
    try:
        import plotly.graph_objects as go
        import numpy as np

        df_filtrado = df.copy()

        # 1. Filtro por subregiones (prioritario) o por región
        if subregiones is not None:
            if isinstance(subregiones, str):
                subregiones = [subregiones]
            condicion_geo = df_filtrado['attr_place_subregion'].isin(subregiones)
            df_grafico_base = df_filtrado[condicion_geo].copy()
            etiqueta_geo = ", ".join(subregiones)
        elif region is not None:
            condicion_geo = df_filtrado['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
            df_grafico_base = df_filtrado[condicion_geo].copy()
            etiqueta_geo = region
        else:
            raise ValueError("Debes especificar al menos 'subregiones' o 'region'.")

        if len(df_grafico_base) == 0:
            print(f"[Advertencia] No se encontraron registros para la ubicación indicada.")
            return None

        # 2. Exclusión de operadores móviles
        proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
        df_grafico_base = df_grafico_base[~df_grafico_base['attr_provider_name_common'].isin(proveedores_excluir)]

        # 3. Estandarización de nombres
        reemplazos = {
            'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
            'Netuno': 'NetUno',
            'Cable Norte': 'Norte'
        }
        df_grafico_base['attr_provider_name_common'] = df_grafico_base['attr_provider_name_common'].replace(reemplazos)

        # 4. Filtrar top N proveedores
        top_proveedores = (
            df_grafico_base['attr_provider_name_common']
            .value_counts()
            .nlargest(cantidad_proveedores)
            .index
            .tolist()
        )
        df_grafico = df_grafico_base[df_grafico_base['attr_provider_name_common'].isin(top_proveedores)].copy()

        # 5. Rangos de latencia
        if cortes is None:
            cortes = [-1, 2, 4, 5, 11, 33, 10000]
        if etiquetas is None:
            etiquetas = ['1) < 2', '2) 2 - <4', '3) 4 - <5', '4) 5 - <11', '5) 11 - <33', '6) 33+']

        df_grafico['val_latency_min_ms'] = pd.to_numeric(df_grafico['val_latency_min_ms'], errors='coerce')

        df_grafico['Rango de Latencias'] = pd.cut(
            df_grafico['val_latency_min_ms'], 
            bins=cortes, 
            labels=etiquetas, 
            right=False
        )

        datos_latencia = (
            df_grafico.groupby(['Rango de Latencias', 'attr_provider_name_common'], observed=False)['id_device']
            .nunique()
            .reset_index()
        )
        
        tabla_pivote = datos_latencia.pivot(
            index='Rango de Latencias',
            columns='attr_provider_name_common',
            values='id_device'
        ).fillna(0)

        proveedores_ordenados = tabla_pivote.sum().sort_values(ascending=False).index

        # 6. Construcción de cintas (ribbons)
        ancho_barra = 0.25
        indices_originales = np.arange(len(tabla_pivote.index))
        
        x_con_grosor = []
        for i in indices_originales:
            x_con_grosor.extend([i - ancho_barra, i + ancho_barra])
        
        fig = go.Figure()
        acumulado_y_por_categoria = np.zeros(len(indices_originales))
        
        if diccionario_colores is None:
            diccionario_colores = COLORES_PROVEEDORES

        for proveedor in proveedores_ordenados:
            valores_originales = tabla_pivote[proveedor].values
            valores_duplicados = np.repeat(valores_originales, 2)
            
            color_hex = diccionario_colores.get(proveedor, '#1f77b4')
            
            # Cinta
            fig.add_trace(go.Scatter(
                x=x_con_grosor,
                y=valores_duplicados,
                name=proveedor,
                mode='lines', 
                line=dict(width=0, color=color_hex),
                stackgroup='one', 
                fillcolor=color_hex,
                line_shape='spline',
                hoverinfo='name+y'
            ))

            # Posición del texto
            posicion_y_texto = acumulado_y_por_categoria + (valores_originales / 2)
            acumulado_y_por_categoria += valores_originales

            textos_etiqueta = []
            for v in valores_originales:
                if v > umbral_texto:
                    textos_etiqueta.append(f"<b>{proveedor}</b><br>{int(v):,}")
                else:
                    textos_etiqueta.append("")

            # Capa de texto sobre las barras
            fig.add_trace(go.Scatter(
                x=indices_originales,
                y=posicion_y_texto,
                mode='text',
                text=textos_etiqueta,
                textposition="middle center",
                textfont=dict(color='white', size=10, family="Arial"),
                showlegend=False,
                hoverinfo='skip'
            ))

        # 7. Títulos y ajustes de layout
        if titulo is None:
            titulo = f'Distribucion de Latencia (ms) - Top {cantidad_proveedores} Proveedores ({etiqueta_geo})'

        fig.update_layout(
            title_text=titulo,
            title_x=0.5,
            plot_bgcolor='white',
            height=height,
            margin=dict(l=20, r=20, t=60, b=120),
            xaxis=dict(
                showgrid=False,
                linecolor='black',
                tickmode='array',
                tickvals=indices_originales,
                ticktext=etiquetas,
                range=[-0.6, len(indices_originales) - 0.4], 
                fixedrange=True
            ),
            yaxis=dict(
                showgrid=False, 
                visible=False,
                rangemode='tozero'
            ),
            legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.1,
                 xanchor="center",
                 x=0.5,
                 bgcolor='rgba(0,0,0,0)'
            )
        )

        return fig

    except Exception as e:
        print(f"[Error al generar grafico de latencias]: {e}")
        return None


# =====================================================================
# DISTRIBUCION DE VELOCIDADES Y LATENCIAS POR CIUDAD (attr_place_name)
# =====================================================================

def generar_grafico_distribucion_velocidades_ciudades(
    df, 
    ciudades, 
    region=None, 
    cantidad_proveedores=6,
    cortes=None, 
    etiquetas=None,
    diccionario_colores=None,
    titulo=None,
    ruta_exportacion=None,
    figsize=(14, 7)
):
    """
    Genera un grafico de barras agrupadas con la distribucion de usuarios (dispositivos unicos)
    por rangos de velocidad (Mbps) y por proveedor para una o varias ciudades (attr_place_name),
    con la opcion de acotarlo a una region (attr_place_region).
    """
    try:
        df_plot_base = df.copy()

        # 1. Filtro opcional por region
        if region is not None:
            condicion_reg = df_plot_base['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
            df_plot_base = df_plot_base[condicion_reg]

        # 2. Filtro obligatorio por ciudades (attr_place_name)
        if isinstance(ciudades, str):
            ciudades = [ciudades]
            
        df_plot_base = df_plot_base[df_plot_base['attr_place_name'].isin(ciudades)]

        etiqueta_geo = ", ".join(ciudades) + (f" ({region})" if region else "")

        if len(df_plot_base) == 0:
            print(f"[Advertencia] No se encontraron registros para las ciudades indicadas: {ciudades}")
            return pd.DataFrame()

        # 3. Exclusion de operadores moviles
        proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
        df_plot_base = df_plot_base[~df_plot_base['attr_provider_name_common'].isin(proveedores_excluir)]

        # 4. Estandarizacion de nombres
        reemplazos = {
            'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
            'Netuno': 'NetUno',
            'Cable Norte': 'Norte'
        }
        df_plot_base['attr_provider_name_common'] = df_plot_base['attr_provider_name_common'].replace(reemplazos)

        # 5. Filtrar top N proveedores
        top_proveedores = (
            df_plot_base['attr_provider_name_common']
            .value_counts()
            .nlargest(cantidad_proveedores)
            .index
            .tolist()
        )
        df_plot = df_plot_base[df_plot_base['attr_provider_name_common'].isin(top_proveedores)].copy()

        # 6. Limpieza de velocidades y cortes
        df_plot['val_download_mbps'] = pd.to_numeric(df_plot['val_download_mbps'], errors='coerce')

        if cortes is None:
            cortes = [0, 400, 750, 850, 10000]
        if etiquetas is None:
            etiquetas = ['1) 0 - 400', '2) 401 - 750', '3) 751 - 850', '4) 851 - 1Gbps']

        df_plot['Rango de Velocidades'] = pd.cut(
            df_plot['val_download_mbps'], 
            bins=cortes, 
            labels=etiquetas, 
            include_lowest=True
        )

        # 7. Agrupacion por usuarios unicos
        datos_grafico = (
            df_plot.groupby(['Rango de Velocidades', 'attr_provider_name_common'], observed=False)['id_device']
            .nunique()
            .reset_index()
        )
        datos_grafico.rename(columns={'id_device': 'Usuarios'}, inplace=True)

        # 8. Generacion del grafico
        plt.figure(figsize=figsize)
        sns.set_theme(style="whitegrid")

        if diccionario_colores is None:
            diccionario_colores = COLORES_PROVEEDORES

        paleta = {prov: diccionario_colores.get(prov, '#CCCCCC') for prov in top_proveedores}

        grafico = sns.barplot(
            data=datos_grafico,
            x='Rango de Velocidades',
            y='Usuarios',
            hue='attr_provider_name_common',
            palette=paleta
        )

        # Etiquetas encima de cada barra
        for p in grafico.patches:
            height = p.get_height()
            if height > 0:
                grafico.annotate(
                    f'{int(height):,}',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold',
                    xytext=(0, 3),
                    textcoords='offset points'
                )

        # 9. Titulos y formato
        if titulo is None:
            titulo = f'Distribucion de Usuarios por Rango de Velocidad y Proveedor ({etiqueta_geo})'

        plt.title(titulo, fontsize=15, fontweight='bold', pad=40)
        plt.xlabel('Rango de Velocidades (Mbps)', fontsize=12)
        plt.ylabel('Usuarios (Dispositivos Unicos)', fontsize=12)
        
        plt.legend(
            title='Proveedor', 
            bbox_to_anchor=(0., 1.02, 1., .102), 
            loc='lower center',
            ncol=min(len(top_proveedores), 6), 
            mode=None, 
            borderaxespad=0.,
            frameon=False
        )

        plt.tight_layout()

        if ruta_exportacion:
            plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
            print(f"Grafico guardado exitosamente en: {ruta_exportacion}")

        plt.show()
        plt.close()

        return datos_grafico

    except Exception as e:
        print(f"[Error al ejecutar distribucion de velocidades por ciudad]: {e}")
        return pd.DataFrame()


def generar_grafico_distribucion_latencias_ciudades(
    df, 
    ciudades, 
    region=None, 
    cantidad_proveedores=6,
    cortes=None,
    etiquetas=None,
    diccionario_colores=None,
    titulo=None,
    umbral_texto=8,
    height=700
):
    """
    Genera un grafico de cintas apiladas (ribbons en Plotly) con la distribucion 
    de usuarios segun rangos de latencia minima (ms) y proveedor para una o varias ciudades (attr_place_name),
    con la opcion de acotarlo a una region (attr_place_region).
    """
    try:
        import plotly.graph_objects as go
        import numpy as np

        df_grafico_base = df.copy()

        # 1. Filtro opcional por region
        if region is not None:
            condicion_reg = df_grafico_base['attr_place_region'].astype(str).str.contains(region, case=False, na=False)
            df_grafico_base = df_grafico_base[condicion_reg]

        # 2. Filtro obligatorio por ciudades (attr_place_name)
        if isinstance(ciudades, str):
            ciudades = [ciudades]
            
        df_grafico_base = df_grafico_base[df_grafico_base['attr_place_name'].isin(ciudades)]

        etiqueta_geo = ", ".join(ciudades) + (f" ({region})" if region else "")

        if len(df_grafico_base) == 0:
            print(f"[Advertencia] No se encontraron registros para las ciudades indicadas: {ciudades}")
            return None

        # 3. Exclusion de operadores moviles
        proveedores_excluir = ['Digitel', 'Movilnet', 'Movistar']
        df_grafico_base = df_grafico_base[~df_grafico_base['attr_provider_name_common'].isin(proveedores_excluir)]

        # 4. Estandarizacion de nombres
        reemplazos = {
            'Galaxy Entertainment de Venezuela C.A.': 'Simplefibra',
            'Netuno': 'NetUno',
            'Cable Norte': 'Norte'
        }
        df_grafico_base['attr_provider_name_common'] = df_grafico_base['attr_provider_name_common'].replace(reemplazos)

        # 5. Filtrar top N proveedores
        top_proveedores = (
            df_grafico_base['attr_provider_name_common']
            .value_counts()
            .nlargest(cantidad_proveedores)
            .index
            .tolist()
        )
        df_grafico = df_grafico_base[df_grafico_base['attr_provider_name_common'].isin(top_proveedores)].copy()

        # 6. Rangos de latencia
        if cortes is None:
            cortes = [-1, 2, 4, 5, 11, 33, 10000]
        if etiquetas is None:
            etiquetas = ['1) < 2', '2) 2 - <4', '3) 4 - <5', '4) 5 - <11', '5) 11 - <33', '6) 33+']

        df_grafico['val_latency_min_ms'] = pd.to_numeric(df_grafico['val_latency_min_ms'], errors='coerce')

        df_grafico['Rango de Latencias'] = pd.cut(
            df_grafico['val_latency_min_ms'], 
            bins=cortes, 
            labels=etiquetas, 
            right=False
        )

        datos_latencia = (
            df_grafico.groupby(['Rango de Latencias', 'attr_provider_name_common'], observed=False)['id_device']
            .nunique()
            .reset_index()
        )
        
        tabla_pivote = datos_latencia.pivot(
            index='Rango de Latencias',
            columns='attr_provider_name_common',
            values='id_device'
        ).fillna(0)

        proveedores_ordenados = tabla_pivote.sum().sort_values(ascending=False).index

        # 7. Construccion de cintas Plotly
        ancho_barra = 0.25
        indices_originales = np.arange(len(tabla_pivote.index))
        
        x_con_grosor = []
        for i in indices_originales:
            x_con_grosor.extend([i - ancho_barra, i + ancho_barra])
        
        fig = go.Figure()
        acumulado_y_por_categoria = np.zeros(len(indices_originales))
        
        if diccionario_colores is None:
            diccionario_colores = COLORES_PROVEEDORES

        for proveedor in proveedores_ordenados:
            valores_originales = tabla_pivote[proveedor].values
            valores_duplicados = np.repeat(valores_originales, 2)
            
            color_hex = diccionario_colores.get(proveedor, '#1f77b4')
            
            fig.add_trace(go.Scatter(
                x=x_con_grosor,
                y=valores_duplicados,
                name=proveedor,
                mode='lines', 
                line=dict(width=0, color=color_hex),
                stackgroup='one', 
                fillcolor=color_hex,
                line_shape='spline',
                hoverinfo='name+y'
            ))

            posicion_y_texto = acumulado_y_por_categoria + (valores_originales / 2)
            acumulado_y_por_categoria += valores_originales

            textos_etiqueta = []
            for v in valores_originales:
                if v > umbral_texto:
                    textos_etiqueta.append(f"<b>{proveedor}</b><br>{int(v):,}")
                else:
                    textos_etiqueta.append("")

            fig.add_trace(go.Scatter(
                x=indices_originales,
                y=posicion_y_texto,
                mode='text',
                text=textos_etiqueta,
                textposition="middle center",
                textfont=dict(color='white', size=10, family="Arial"),
                showlegend=False,
                hoverinfo='skip'
            ))

        # 8. Layout y estetica
        if titulo is None:
            titulo = f'Distribucion de Latencia (ms) - Top {cantidad_proveedores} Proveedores ({etiqueta_geo})'

        fig.update_layout(
            title_text=titulo,
            title_x=0.5,
            plot_bgcolor='white',
            height=height,
            margin=dict(l=20, r=20, t=60, b=120),
            xaxis=dict(
                showgrid=False,
                linecolor='black',
                tickmode='array',
                tickvals=indices_originales,
                ticktext=etiquetas,
                range=[-0.6, len(indices_originales) - 0.4], 
                fixedrange=True
            ),
            yaxis=dict(
                showgrid=False, 
                visible=False,
                rangemode='tozero'
            ),
            legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.1,
                 xanchor="center",
                 x=0.5,
                 bgcolor='rgba(0,0,0,0)'
            )
        )

        return fig

    except Exception as e:
        print(f"[Error al generar grafico de latencias por ciudad]: {e}")
        return None

# =====================================================================
# CONSOLIDADO
# =====================================================================


def generar_grafico_consolidado(
    dfs_fila1, 
    dfs_fila2, 
    titulos_columnas,
    titulo_fila1="Market Share - Periodo 1", 
    titulo_fila2="Market Share - Periodo 2",
    max_proveedores_leyenda=None,
    ncol_leyenda=1,
    diccionario_colores=None,
    ruta_exportacion=None,
    figsize=(38, 18),
    umbral_etiqueta=2.0
):
    """
    Genera un tablero consolidado de 2 filas de graficos de barras apiladas 
    para comparar dos periodos a traves de multiples ciudades/sedes.

    Parametros:
    - dfs_fila1 (list): Lista de DataFrames pivotados para la fila 1 (inferior).
    - dfs_fila2 (list): Lista de DataFrames pivotados para la fila 2 (superior).
    - titulos_columnas (list): Nombres de las sedes/ciudades (ej. ['Caracas', 'Barquisimeto', ...]).
    - titulo_fila1 (str): Titulo del periodo para la fila 1.
    - titulo_fila2 (str): Titulo del periodo para la fila 2.
    - max_proveedores_leyenda (int, opcional): Cantidad maxima de proveedores a mostrar en la leyenda.
    - ncol_leyenda (int): Columnas para la leyenda lateral (por defecto 1).
    - diccionario_colores (dict, opcional): Diccionario de colores por proveedor.
    - ruta_exportacion (str, opcional): Ruta para guardar la imagen (ej: 'consolidado.png').
    - figsize (tuple): Tamano de la figura.
    - umbral_etiqueta (float): Porcentaje minimo para mostrar la etiqueta numerica en la barra.
    """
    n_cols = len(titulos_columnas)
    if len(dfs_fila1) != n_cols or len(dfs_fila2) != n_cols:
        raise ValueError(
            f"La cantidad de titulos ({n_cols}) debe coincidir con la cantidad de DataFrames "
            f"en dfs_fila1 ({len(dfs_fila1)}) y dfs_fila2 ({len(dfs_fila2)})."
        )

    if diccionario_colores is None:
        diccionario_colores = COLORES_PROVEEDORES

    fig, axes = plt.subplots(2, n_cols, figsize=figsize)

    todos_los_handles = {}
    peso_proveedores = {}

    # Construir parejas (df, ax, titulo)
    # Fila superior = index 0 (dfs_fila2)
    # Fila inferior = index 1 (dfs_fila1)
    datasets_fila_superior = [(df, axes[0, i], titulos_columnas[i]) for i, df in enumerate(dfs_fila2)]
    datasets_fila_inferior = [(df, axes[1, i], titulos_columnas[i]) for i, df in enumerate(dfs_fila1)]

    # Procesar todos los graficos
    for df_plot, ax, titulo in (datasets_fila_superior + datasets_fila_inferior):
        lista_colores = [diccionario_colores.get(prov, '#CCCCCC') for prov in df_plot.columns]
        
        df_plot.plot(kind='bar', stacked=True, ax=ax, color=lista_colores, width=0.55)

        # Capturar handles y acumular pesos porcentuales
        h, l = ax.get_legend_handles_labels()
        for handle, label in zip(h, l):
            if label not in todos_los_handles:
                todos_los_handles[label] = handle
            peso_proveedores[label] = peso_proveedores.get(label, 0) + df_plot[label].sum()

        # Etiquetas porcentuales dentro de cada segmento
        for p in ax.patches:
            height = p.get_height()
            if height > umbral_etiqueta:
                ax.text(
                    p.get_x() + p.get_width() / 2, 
                    p.get_y() + height / 2, 
                    f'{height:.1f}%', 
                    ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=16
                )

        # Limpieza estetica
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xticks([]) 
        ax.set_title(titulo, fontsize=20, pad=10)
        
        if ax.get_legend() is not None:
            ax.get_legend().remove()

    # Subtitulos de fila (Periodos)
    fig.text(0.46, 0.95, titulo_fila2, ha='center', fontsize=30, fontweight='bold')
    fig.text(0.46, 0.48, titulo_fila1, ha='center', fontsize=30, fontweight='bold')

    # Filtrar proveedores a mostrar en leyenda segun max_proveedores_leyenda
    if max_proveedores_leyenda is not None:
        # Ordenar por presencia/peso acumulado
        proveedores_ordenados_peso = sorted(
            [k for k in peso_proveedores.keys() if k != 'Otros'], 
            key=lambda k: peso_proveedores[k], 
            reverse=True
        )
        labels_seleccionados = proveedores_ordenados_peso[:max_proveedores_leyenda]
        if 'Otros' in todos_los_handles:
            labels_seleccionados.append('Otros')
    else:
        labels_seleccionados = sorted(todos_los_handles.keys())

    handles_ordenados = [todos_los_handles[l] for l in labels_seleccionados if l in todos_los_handles]
    labels_finales = [l for l in labels_seleccionados if l in todos_los_handles]

    # Configuracion de leyenda lateral
    fig.legend(
        handles_ordenados, 
        labels_finales, 
        loc='center left',
        bbox_to_anchor=(0.89, 0.5),
        fontsize=15,
        ncol=ncol_leyenda,
        frameon=False,
        title="Proveedores",
        title_fontsize=16
    )

    # Margenes
    plt.subplots_adjust(left=0.04, right=0.88, top=0.88, bottom=0.05, hspace=0.4, wspace=0.4)

    if ruta_exportacion:
        plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
        print(f"Grafico consolidado guardado en: {ruta_exportacion}")

    plt.show()
    plt.close()

import matplotlib.pyplot as plt

def generar_grafico_consolidadov2(
    dfs_fila1, 
    dfs_fila2, 
    titulos_columnas,
    titulo_fila1="Market Share - Periodo 1", 
    titulo_fila2="Market Share - Periodo 2",
    max_proveedores_leyenda=None,
    ncol_leyenda=1,
    diccionario_colores=None,
    ruta_exportacion=None,
    figsize=(42, 18), # Ligeramente más ancho para acomodar el texto lateral
    umbral_etiqueta=2.0
):
    """
    Genera un tablero consolidado de 2 filas de gráficos de barras apiladas, 
    incluyendo el cuadro de texto lateral con el Top 5 numerado para cada sede.
    """
    n_cols = len(titulos_columnas)
    if len(dfs_fila1) != n_cols or len(dfs_fila2) != n_cols:
        raise ValueError(
            f"La cantidad de títulos ({n_cols}) debe coincidir con la cantidad de DataFrames "
            f"en dfs_fila1 ({len(dfs_fila1)}) y dfs_fila2 ({len(dfs_fila2)})."
        )

    if diccionario_colores is None:
        diccionario_colores = COLORES_PROVEEDORES

    fig, axes = plt.subplots(2, n_cols, figsize=figsize)

    todos_los_handles = {}
    peso_proveedores = {}

    datasets_fila_superior = [(df, axes[0, i], titulos_columnas[i]) for i, df in enumerate(dfs_fila2)]
    datasets_fila_inferior = [(df, axes[1, i], titulos_columnas[i]) for i, df in enumerate(dfs_fila1)]

    for df_plot, ax, titulo in (datasets_fila_superior + datasets_fila_inferior):
        lista_colores = [diccionario_colores.get(prov, '#CCCCCC') for prov in df_plot.columns]
        
        # Generar la barra (ancho ajustado a 0.5 para dejar espacio)
        df_plot.plot(kind='bar', stacked=True, ax=ax, color=lista_colores, width=0.5)

        # 1. EXTRAER, NUMERAR E INVERTIR EL TOP 5
        cols_proveedores = [col for col in df_plot.columns if col != 'Otros']
        top_5 = cols_proveedores[:5]
        
        lista_top = [f"{idx + 1}. {prov}" for idx, prov in enumerate(top_5)]
        lista_top.reverse() # Invertir para que coincida con el apilado base
        texto_lateral = "** Top 5 **\n\n" + "\n".join(lista_top)

        # Capturar handles y acumular pesos
        h, l = ax.get_legend_handles_labels()
        for handle, label in zip(h, l):
            if label not in todos_los_handles:
                todos_los_handles[label] = handle
            peso_proveedores[label] = peso_proveedores.get(label, 0) + df_plot[label].sum()

        # Etiquetas porcentuales dentro de la barra
        for p in ax.patches:
            height = p.get_height()
            if height > umbral_etiqueta:
                ax.text(
                    p.get_x() + p.get_width() / 2, 
                    p.get_y() + height / 2, 
                    f'{height:.1f}%', 
                    ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=16
                )

        # Limpieza estética
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_xticks([]) 
        ax.set_title(titulo, fontsize=22, pad=15)
        
        # 2. AMPLIAR EJE X Y COLOCAR EL CUADRO DE TEXTO LATERAL
        ax.set_xlim(-0.3, 1.3)
        ax.text(
            0.32, 50, 
            texto_lateral, 
            ha='left', va='center', 
            fontsize=12, 
            color='#333333',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#F8F9FA', edgecolor='#DDDDDD', alpha=0.9)
        )
        
        if ax.get_legend() is not None:
            ax.get_legend().remove()

    # Subtítulos de fila
    fig.text(0.46, 0.95, titulo_fila2, ha='center', fontsize=30, fontweight='bold')
    fig.text(0.46, 0.48, titulo_fila1, ha='center', fontsize=30, fontweight='bold')

    # Filtrado de leyenda global
    if max_proveedores_leyenda is not None:
        proveedores_ordenados_peso = sorted(
            [k for k in peso_proveedores.keys() if k != 'Otros'], 
            key=lambda k: peso_proveedores[k], 
            reverse=True
        )
        labels_seleccionados = proveedores_ordenados_peso[:max_proveedores_leyenda]
        if 'Otros' in todos_los_handles:
            labels_seleccionados.append('Otros')
    else:
        labels_seleccionados = sorted(todos_los_handles.keys())

    handles_ordenados = [todos_los_handles[l] for l in labels_seleccionados if l in todos_los_handles]
    labels_finales = [l for l in labels_seleccionados if l in todos_los_handles]

    # Leyenda lateral global
    fig.legend(
        handles_ordenados, 
        labels_finales, 
        loc='center left',
        bbox_to_anchor=(0.89, 0.5),
        fontsize=15,
        ncol=ncol_leyenda,
        frameon=False,
        title="Proveedores",
        title_fontsize=16
    )

    # 3. AJUSTE DE MÁRGENES (wspace ampliado a 0.7 para que los cuadros no choquen)
    plt.subplots_adjust(left=0.04, right=0.85, top=0.88, bottom=0.05, hspace=0.4, wspace=0.7)

    if ruta_exportacion:
        plt.savefig(ruta_exportacion, bbox_inches='tight', dpi=300)
        print(f"Gráfico consolidado guardado en: {ruta_exportacion}")

    plt.show()
    plt.close()

# =====================================================================
# SANKEY
# =====================================================================

# (Asumo que COLORES_PROVEEDORES está definido por aquí arriba en este mismo archivo)

def generar_sankey_migraciones(df_mes_anterior, df_mes_actual):
    """
    Evalúa la migración de usuarios filtrando el último registro de cada 
    id_device según ts_result y genera un diagrama de Sankey interactivo.
    Toma los colores directamente de la variable global COLORES_PROVEEDORES.
    """
    # 1. Preparar Mes Anterior
    df_ant = df_mes_anterior.copy()
    df_ant['ts_result'] = pd.to_datetime(df_ant['ts_result'])
    df_ant = df_ant.sort_values('ts_result').drop_duplicates(subset=['id_device'], keep='last')
    df_ant = df_ant[['id_device', 'attr_provider_name_common']].rename(
        columns={'attr_provider_name_common': 'proveedor_origen'}
    )
    
    # 2. Preparar Mes Actual
    df_act = df_mes_actual.copy()
    df_act['ts_result'] = pd.to_datetime(df_act['ts_result'])
    df_act = df_act.sort_values('ts_result').drop_duplicates(subset=['id_device'], keep='last')
    df_act = df_act[['id_device', 'attr_provider_name_common']].rename(
        columns={'attr_provider_name_common': 'proveedor_destino'}
    )
    
    # 3. Cruzar los datos (inner join)
    df_migracion = pd.merge(df_ant, df_act, on='id_device', how='inner')
    
    # 4. Cuantificar los volúmenes
    df_flujo = df_migracion.groupby(['proveedor_origen', 'proveedor_destino']).size().reset_index(name='cantidad')
    
    # 5. Formatear nodos
    df_flujo['nodo_origen'] = df_flujo['proveedor_origen'] + " (Mes 1)"
    df_flujo['nodo_destino'] = df_flujo['proveedor_destino'] + " (Mes 2)"
    
    lista_nodos = list(df_flujo['nodo_origen'].unique()) + list(df_flujo['nodo_destino'].unique())
    diccionario_indices = {nombre: i for i, nombre in enumerate(lista_nodos)}
    
    df_flujo['origen_id'] = df_flujo['nodo_origen'].map(diccionario_indices)
    df_flujo['destino_id'] = df_flujo['nodo_destino'].map(diccionario_indices)
    
    # 6. Mapear colores usando la variable global del mismo archivo
    colores_nodos = []
    for nodo in lista_nodos:
        nombre_real = nodo.replace(" (Mes 1)", "").replace(" (Mes 2)", "")
        # Llama a COLORES_PROVEEDORES directamente
        colores_nodos.append(COLORES_PROVEEDORES.get(nombre_real, '#CCCCCC'))
    
    # 7. Construir la visualización
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 20,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = lista_nodos,
            color = colores_nodos
        ),
        link = dict(
            source = df_flujo['origen_id'],
            target = df_flujo['destino_id'],
            value = df_flujo['cantidad'],
            color = "rgba(180, 180, 180, 0.4)" 
        )
    )])
    
    fig.update_layout(
        title_text="Flujo de Migración de Dispositivos por Proveedor", 
        font_size=12,
        height=800
    )
    
    return fig

def obtener_cuadro_migracion_proveedor(df_mes_anterior, df_mes_actual, proveedor_objetivo):
    """
    Evalúa la migración de usuarios filtrando el último registro de cada 
    id_device según ts_result y devuelve únicamente un DataFrame (cuadro)
    con las entradas y salidas del proveedor objetivo.
    """
    # 1. Preparar Mes Anterior
    df_ant = df_mes_anterior.copy()
    df_ant['ts_result'] = pd.to_datetime(df_ant['ts_result'])
    df_ant = df_ant.sort_values('ts_result').drop_duplicates(subset=['id_device'], keep='last')
    df_ant = df_ant[['id_device', 'attr_provider_name_common']].rename(
        columns={'attr_provider_name_common': 'proveedor_origen'}
    )
    
    # 2. Preparar Mes Actual
    df_act = df_mes_actual.copy()
    df_act['ts_result'] = pd.to_datetime(df_act['ts_result'])
    df_act = df_act.sort_values('ts_result').drop_duplicates(subset=['id_device'], keep='last')
    df_act = df_act[['id_device', 'attr_provider_name_common']].rename(
        columns={'attr_provider_name_common': 'proveedor_destino'}
    )
    
    # 3. Cruzar los datos (inner join)
    df_migracion = pd.merge(df_ant, df_act, on='id_device', how='inner')
    
    # 4. Cuantificar los flujos totales
    df_flujo = df_migracion.groupby(['proveedor_origen', 'proveedor_destino']).size().reset_index(name='cantidad')
    
    # 5. FILTRAR: Solo entradas y salidas del proveedor objetivo (excluyendo retención)
    condicion_salida = (df_flujo['proveedor_origen'] == proveedor_objetivo) & (df_flujo['proveedor_destino'] != proveedor_objetivo)
    condicion_entrada = (df_flujo['proveedor_origen'] != proveedor_objetivo) & (df_flujo['proveedor_destino'] == proveedor_objetivo)
    
    # 6. Unir y ordenar el cuadro final
    df_cuadro = df_flujo[condicion_salida | condicion_entrada].copy()
    
    if df_cuadro.empty:
        print(f"No se encontraron migraciones de entrada o salida para {proveedor_objetivo}.")
        return pd.DataFrame()
        
    # Ordenar por cantidad de mayor a menor para una mejor lectura
    df_cuadro = df_cuadro.sort_values(by='cantidad', ascending=False).reset_index(drop=True)
    
    return df_cuadro

# =====================================================================
# CARTOGRAFIA INTERACTIVA CON TOOLBOX POR PROVEEDOR
# =====================================================================

import pandas as pd
import folium

import pandas as pd
import folium

def generar_mapa_por_subregion_toolbox(df, nombre_grupo, lista_municipios, diccionario_colores, max_mostrar=None):
    """
    Filtra el DataFrame para una subregión, limita los proveedores según un Top N, 
    y genera un mapa interactivo con control de capas (toolbox) centrado automáticamente.
    """
    # 1. Filtrar el DataFrame únicamente para los municipios/lugares de esta subregión
    columna_ubicacion = 'attr_place_name'
    columna_proveedor = 'attr_provider_name_common'
    
    df_filtrado = df[df[columna_ubicacion].isin(lista_municipios)].copy()
    
    if df_filtrado.empty:
        print(f"Advertencia: No se encontraron registros para la subregión: {nombre_grupo}")
        return folium.Map(location=[10.0, -66.0], zoom_start=6) # Mapa por defecto si está vacío

    # 2. Limpiar nulos en coordenadas y calcular el Top N de proveedores si se solicita
    df_filtrado = df_filtrado.dropna(subset=['attr_location_latitude', 'attr_location_longitude'])
    
    if max_mostrar is not None:
        # Contar y ordenar para obtener los principales
        top_proveedores = (
            df_filtrado.groupby(columna_proveedor)['id_device']
            .nunique()
            .reset_index()
            .sort_values(by='id_device', ascending=False)
            .head(max_mostrar)[columna_proveedor]
            .tolist()
        )
        # Filtrar el DataFrame solo con esos proveedores top
        df_filtrado = df_filtrado[df_filtrado[columna_proveedor].isin(top_proveedores)]

    # 3. Crear el mapa base inicial (se ajustará automáticamente a los puntos)
    mapa = folium.Map(zoom_start=13)
    
    # 4. Obtener la lista final de proveedores únicos
    proveedores = df_filtrado[columna_proveedor].dropna().unique()
    
    # Lista para almacenar todas las coordenadas y centrar automáticamente el mapa al final
    coordenadas_totales = []
    
    # 5. Crear una capa independiente (FeatureGroup) por cada proveedor para la Toolbox
    for proveedor in proveedores:
        grupo_proveedor = folium.FeatureGroup(name=str(proveedor))
        
        df_prov = df_filtrado[df_filtrado[columna_proveedor] == proveedor]
        color_asignado = diccionario_colores.get(proveedor, 'gray')
        
        # Agregar los puntos individuales de este proveedor
        for _, row in df_prov.iterrows():
            lat = row['attr_location_latitude']
            lon = row['attr_location_longitude']
            coordenadas_totales.append([lat, lon])
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                color=color_asignado,
                weight=1,
                fill=True,
                fill_color=color_asignado,
                fill_opacity=0.8,
                tooltip=f"Proveedor: {proveedor} | Lugar: {row.get(columna_ubicacion, '')}"
            ).add_to(grupo_proveedor)
                
        # Añadir el grupo al mapa
        grupo_proveedor.add_to(mapa)

    # 6. Centrar automáticamente el mapa cubriendo los límites de los puntos encontrados
    if coordenadas_totales:
        mapa.fit_bounds(coordenadas_totales)

    # 7. Agregar el Toolbox de capas interactivo en la esquina
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    print(f"Mapa generado exitosamente para la región: {nombre_grupo}")
    return mapa

def generar_mapa_por_region_toolbox(df, region_seleccionada, diccionario_colores, max_mostrar=None):
    """
    Filtra el DataFrame para una región completa (attr_place_region), limita los proveedores según un Top N, 
    y genera un mapa interactivo con control de capas (toolbox) centrado automáticamente.
    """
    columna_region = 'attr_place_region'
    columna_proveedor = 'attr_provider_name_common'
    columna_ubicacion = 'attr_place_name'  # Solo para mostrar detalles en el tooltip
    
    # 1. Filtrar el DataFrame únicamente para la región especificada
    df_filtrado = df[df[columna_region] == region_seleccionada].copy()
    
    if df_filtrado.empty:
        print(f"Advertencia: No se encontraron registros para la región: {region_seleccionada}")
        return folium.Map(location=[10.0, -66.0], zoom_start=6)

    # 2. Limpiar nulos en coordenadas y calcular el Top N de proveedores si se solicita
    df_filtrado = df_filtrado.dropna(subset=['attr_location_latitude', 'attr_location_longitude'])
    
    if max_mostrar is not None:
        top_proveedores = (
            df_filtrado.groupby(columna_proveedor)['id_device']
            .nunique()
            .reset_index()
            .sort_values(by='id_device', ascending=False)
            .head(max_mostrar)[columna_proveedor]
            .tolist()
        )
        df_filtrado = df_filtrado[df_filtrado[columna_proveedor].isin(top_proveedores)]

    # 3. Crear el mapa base inicial (el zoom y centro se ajustarán automáticamente)
    mapa = folium.Map(zoom_start=13)
    
    # 4. Obtener la lista final de proveedores únicos
    proveedores = df_filtrado[columna_proveedor].dropna().unique()
    coordenadas_totales = []
    
    # 5. Crear una capa independiente (FeatureGroup) por cada proveedor para la Toolbox
    for proveedor in proveedores:
        grupo_proveedor = folium.FeatureGroup(name=str(proveedor))
        
        df_prov = df_filtrado[df_filtrado[columna_proveedor] == proveedor]
        color_asignado = diccionario_colores.get(proveedor, 'gray')
        
        for _, row in df_prov.iterrows():
            lat = row['attr_location_latitude']
            lon = row['attr_location_longitude']
            coordenadas_totales.append([lat, lon])
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                color=color_asignado,
                weight=1,
                fill=True,
                fill_color=color_asignado,
                fill_opacity=0.8,
                tooltip=f"Proveedor: {proveedor} | Lugar: {row.get(columna_ubicacion, '')}"
            ).add_to(grupo_proveedor)
                
        grupo_proveedor.add_to(mapa)

    # 6. Centrar automáticamente el mapa cubriendo los límites de los puntos encontrados
    if coordenadas_totales:
        mapa.fit_bounds(coordenadas_totales)

    # 7. Agregar el Toolbox de capas interactivo en la esquina
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    print(f"Mapa generado exitosamente para la región: {region_seleccionada}")
    return mapa