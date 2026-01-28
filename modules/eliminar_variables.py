import polars as pl
import pandas as pd
from typing import Union, List, Tuple

variables = (
    'mun_regis', 'tloc_regis', 'loc_regis', 'mun_resid', 'tloc_resid', 'loc_resid', 'ent_ocurr',
    'mun_ocurr', 'loc_ocurr', 'ent_nac', 'ent_ocules', 'mun_ocules', 'loc_ocules', 'dis_re_oax'
    )

variables_ml = (
    'gramos', 'razon_m', 'maternas', 'gr_lismex', 'cod_adicio', 'grupo',
    'complicaro', 'embarazo', 'rel_emba',
    'cond_cert', 'anio_cert', 'ent_regis', 'ent_resid', 'anio_ocur'
)
variables_ml_pca = (
    'gramos', 'razon_m', 'maternas', 'gr_lismex', 'cod_adicio', 'grupo', 'causa_def', 'ent_regis',
    'ent_resid', 'estado_defuncion_residencia', 'tloc_ocurr', 'nacesp_cve', 'nacionalid', 'sem_gest',
    'encefalica', 'embarazo', 'rel_emba', 'horas', 'minutos', 'capitulo', 'complicaro', 'edad', 'afromex',
    'lengua', 'conindig', 'cve_lengua', 'dia_ocurr', 'dia_regis', 'usonecrops', 'donador'
)

def eliminar_variables(df: pl.DataFrame, variables: Union[List[str], Tuple[str, ...]]) -> pl.DataFrame:
    """
    Elimina columnas específicas de un DataFrame de Polars.

    Parámetros:
    - df: pl.DataFrame - el DataFrame original.
    - variables: lista o tupla de strings con los nombres de columnas a eliminar.

    Retorna:
    - pl.DataFrame - el DataFrame resultante sin las columnas especificadas.
    """
    return df.drop(variables)



def eliminar_variables_pd(df: pd.DataFrame, variables: Union[List[str], Tuple[str, ...]]) -> pd.DataFrame:
    """
    Elimina columnas específicas de un DataFrame de pandas.

    Args:
        df (pd.DataFrame): DataFrame original.
        variables (Union[List[str], Tuple[str, ...]]): Lista o tupla de nombres de columnas a eliminar.

    Returns:
        pd.DataFrame: DataFrame resultante sin las columnas especificadas.
    """
    # Solución 1: Convertir tupla a lista si es necesario
    if isinstance(variables, tuple):
        variables = list(variables)
    
    # Verificar qué columnas existen antes de eliminar
    columnas_existentes = [col for col in variables if col in df.columns]
    columnas_no_existentes = [col for col in variables if col not in df.columns]
    
    if columnas_no_existentes:
        print(f"Advertencia: Las siguientes columnas no existen en el DataFrame: {columnas_no_existentes}")
    
    # Eliminar solo las columnas que existen
    if columnas_existentes:
        return df.drop(columns=columnas_existentes)
    else:
        print("No se encontraron columnas válidas para eliminar.")
        return df.copy()