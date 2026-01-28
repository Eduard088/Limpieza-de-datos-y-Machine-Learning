import polars as pl
import os


def aplicar_catalogos_polars(df: pl.DataFrame, ruta_catalogos: str, verbose: bool = True) -> pl.DataFrame:
    """
    Sustituye los valores de las columnas del DataFrame por sus descripciones,
    usando los catálogos cuyo nombre coincide con el de la columna.
    """
    df = df.clone()
    columnas = set(df.columns)

    for archivo in os.listdir(ruta_catalogos):
        nombre_variable, ext = os.path.splitext(archivo)
        if ext.lower() != ".csv":
            continue
        if nombre_variable in columnas:
            path_catalogo = os.path.join(ruta_catalogos, archivo)
            cat_df = pl.read_csv(path_catalogo)
            # Detectar columna clave
            clave_col = None
            if "CVE" in cat_df.columns:
                clave_col = "CVE"
            elif "CAP" in cat_df.columns:
                clave_col = "CAP"
            if clave_col and "DESCRIP" in cat_df.columns:
                # Renombrar columna clave para coincidir con el DataFrame
                cat_df = cat_df.rename({clave_col: nombre_variable})
                # Hacer join para mapear descripciones
                df = df.join(cat_df.select([nombre_variable, "DESCRIP"]), on=nombre_variable, how="left")
                # Reemplazar la columna original por la descripción
                df = df.with_columns(
                    pl.col("DESCRIP").fill_null(pl.col(nombre_variable)).alias(nombre_variable)
                ).drop("DESCRIP")
                if verbose:
                    print(f"[OK] Catálogo aplicado: {archivo}")
            else:
                if verbose:
                    print(f"[!] Catálogo '{archivo}' no tiene columnas válidas ('CVE'/'CAP' y 'DESCRIP').")
        else:
            if verbose:
                print(f"[!] Catálogo '{archivo}' ignorado (no hay columna '{nombre_variable}' en el DataFrame).")
    return df