import polars as pl
import pandas as pd

def sustituir_nulos(df: pl.DataFrame, variable: str, text: str) -> pl.DataFrame:
    """
    Sustituye los valores nulos de una columna específica en un DataFrame de Polars.

    Args:
        df (pl.DataFrame): DataFrame en el que se realizará la sustitución.
        variable (str): Nombre de la columna donde se reemplazarán valores nulos.
        text (str): Texto con el que se sustituirán los valores nulos.

    Returns:
        pl.DataFrame: DataFrame modificado con valores nulos sustituidos.
    """
    return df.with_columns(
        pl.col(variable).fill_null(text)
    )

def sustituir_nulos_pd(df: pd.DataFrame, variable: str, text: str) -> pd.DataFrame:
    """
    Sustituye los valores nulos de una columna específica en un DataFrame de pandas.

    Args:
        df (pd.DataFrame): DataFrame en el que se realizará la sustitución.
        variable (str): Nombre de la columna donde se reemplazarán valores nulos.
        text (str): Texto con el que se sustituirán los valores nulos.

    Returns:
        pd.DataFrame: DataFrame modificado con valores nulos sustituidos.
    """
    # Crear una copia para evitar modificar el DataFrame original
    df_copy = df.copy()
    
    if variable in df_copy.columns:
        df_copy[variable] = df_copy[variable].fillna(text)
    else:
        print(f"Advertencia: La columna '{variable}' no existe en el DataFrame.")
    
    return df_copy