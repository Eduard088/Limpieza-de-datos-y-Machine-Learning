import polars as pl
from typing import Optional

ESTADOS_MEXICO = {
    1: "Aguascalientes", 2: "Baja California", 3: "Baja California Sur",
    4: "Campeche", 5: "Coahuila", 6: "Colima", 7: "Chiapas", 8: "Chihuahua",
    9: "Ciudad de México", 10: "Durango", 11: "Guanajuato", 12: "Guerrero",
    13: "Hidalgo", 14: "Jalisco", 15: "México", 16: "Michoacán",
    17: "Morelos", 18: "Nayarit", 19: "Nuevo León", 20: "Oaxaca",
    21: "Puebla", 22: "Querétaro", 23: "Quintana Roo", 24: "San Luis Potosí",
    25: "Sinaloa", 26: "Sonora", 27: "Tabasco", 28: "Tamaulipas",
    29: "Tlaxcala", 30: "Veracruz", 31: "Yucatán", 32: "Zacatecas"
}

def construir_expr_mapeo(columna: str) -> pl.Expr:
    """
    Construye una expresión condicional para mapear valores numéricos a nombres de estados.
    """
    expr = None
    for clave, valor in ESTADOS_MEXICO.items():
        condicion = pl.col(columna) == clave
        if expr is None:
            expr = pl.when(condicion).then(pl.lit(valor))
        else:
            expr = expr.when(condicion).then(pl.lit(valor))
    expr = expr.otherwise(None)
    return expr


def reemplazar_estados(df: pl.DataFrame, columna: Optional[str] = None, nombre: Optional[str] = None) -> pl.DataFrame:
    """
    Reemplaza valores del 1 al 32 por nombres de estados mexicanos usando Polars.
    
    :param df: DataFrame original
    :param columna: Columna en la que se desea aplicar el reemplazo
    :param nombre: Nombre de la nueva columna. Si no se proporciona, se usa columna + '_estado'
    :return: DataFrame con la nueva columna agregada
    """
    if columna:
        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")
        nombre_columna_resultado = nombre if nombre else f"{columna}_estado"
        expr = construir_expr_mapeo(columna).alias(nombre_columna_resultado)
        return df.with_columns([expr])
    else:
        nuevas_columnas = []
        for col in df.columns:
            if df[col].dtype in (pl.Int32, pl.Int64):
                valores = df[col].unique().to_list()
                if all(isinstance(v, int) and 1 <= v <= 32 for v in valores):
                    nombre_columna_resultado = f"{col}_estado"
                    expr = construir_expr_mapeo(col).alias(nombre_columna_resultado)
                    nuevas_columnas.append(expr)
        return df.with_columns(nuevas_columnas)