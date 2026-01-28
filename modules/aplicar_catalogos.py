import pandas as pd
import polars as pl
import os
import glob

def aplicar_catalogos(df, ruta_catalogos, verbose=True):

    df = df.copy()
    
    for columna in df.columns:
        path_catalogo = os.path.join(ruta_catalogos, f"{columna}.csv")
        
        if os.path.isfile(path_catalogo):
            catalogo = pd.read_csv(path_catalogo)
            
            if 'CVE' in catalogo.columns and 'DESCRIP' in catalogo.columns:
                clave = 'CVE'
            elif 'CAP' in catalogo.columns and 'DESCRIP' in catalogo.columns:
                clave = 'CAP'
            else:
                if verbose:
                    print(f"[!] Catálogo '{columna}.csv' no tiene columnas reconocidas ('CVE' o 'CAP' con 'DESCRIP').")
                continue
            
            mapa = dict(zip(catalogo[clave], catalogo['DESCRIP']))
            df[columna] = df[columna].map(mapa)
        else:
            if verbose:
                print(f"[!] Catálogo '{columna}.csv' no encontrado en {ruta_catalogos}.")
    
    return df