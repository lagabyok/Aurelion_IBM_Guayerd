import pandas as pd

# ruta del archivo original
ruta = "data_final/productos_categorias_normalizadas.csv"

# cargar
df = pd.read_csv(ruta, dtype=str)  # cargar como str para inspección inicial

# mostrar columnas y primeras filas (inspección)
print("Columnas originales:", df.columns.tolist())
print(df[['nombre_cliente','nombre_cliente_cliente','email','email_cliente']].head(6))

# --- 1) Comparar si las columnas duplicadas son idénticas fila a fila ---
if 'nombre_cliente' in df.columns and 'nombre_cliente_cliente' in df.columns:
    same_name = (df['nombre_cliente'].fillna('').str.strip() == df['nombre_cliente_cliente'].fillna('').str.strip()).all()
    print("¿nombre_cliente == nombre_cliente_cliente en todas las filas?", same_name)

if 'email' in df.columns and 'email_cliente' in df.columns:
    same_email = (df['email'].fillna('').str.strip().str.lower() == df['email_cliente'].fillna('').str.strip().str.lower()).all()
    print("¿email == email_cliente en todas las filas?", same_email)

# --- 2) Si no son idénticas, conservar la columna más completa (no nula) fila a fila ---
# Creamos columna canon: nombre_cliente_final, email_final usando prioridad
def choose_preferred(col_a, col_b, df):
    a = df[col_a].fillna('').astype(str).str.strip()
    b = df[col_b].fillna('').astype(str).str.strip()
    preferred = a.where(a != '', b)  # usa a si no vacío, sino b
    preferred = preferred.replace('', pd.NA)
    return preferred

if 'nombre_cliente_cliente' in df.columns:
    df['nombre_cliente_final'] = choose_preferred('nombre_cliente', 'nombre_cliente_cliente', df)
else:
    df['nombre_cliente_final'] = df['nombre_cliente'].fillna(pd.NA)

if 'email_cliente' in df.columns:
    df['email_final'] = choose_preferred('email', 'email_cliente', df)
else:
    df['email_final'] = df['email'].fillna(pd.NA)

# --- 3) Normalizar formato de texto ---
df['nombre_cliente_final'] = df['nombre_cliente_final'].astype(str).str.strip().replace('nan', pd.NA)
df['nombre_cliente_final'] = df['nombre_cliente_final'].where(df['nombre_cliente_final'].isna(), df['nombre_cliente_final'].str.title())

df['email_final'] = df['email_final'].astype(str).str.strip().replace('nan', pd.NA)
df['email_final'] = df['email_final'].where(df['email_final'].isna(), df['email_final'].str.lower())

# --- 4) Convertir tipos ---
# parsear fechas
for f in ['fecha', 'fecha_alta']:
    if f in df.columns:
        df[f] = pd.to_datetime(df[f], errors='coerce')

# numeric
for n in ['cantidad','precio_unitario','importe']:
    if n in df.columns:
        df[n] = pd.to_numeric(df[n], errors='coerce')

# --- 5) Seleccionar columnas finales (reemplazando duplicadas) ---
# Decide qué columnas finales quieres conservar:
columnas_finales = [
    'id_venta','id_producto','nombre_producto','cantidad','precio_unitario','importe',
    'fecha','id_cliente','nombre_cliente_final','email_final','medio_pago','categoria',
    'ciudad','fecha_alta','mes'
]

# Mantener solo las que existan realmente
columnas_finales = [c for c in columnas_finales if c in df.columns]
df_clean = df[columnas_finales].copy()

# Renombrar nombre_cliente_final -> nombre_cliente y email_final -> email (si lo deseas)
df_clean = df_clean.rename(columns={'nombre_cliente_final':'nombre_cliente','email_final':'email'})

# --- 6) Guardar CSV limpio ---
ruta_salida = "data_final/productos_categorias_normalizadas_clean.csv"
df_clean.to_csv(ruta_salida, index=False)
print("CSV limpio guardado en:", ruta_salida)

# --- 7) Resumen de limpieza ---
print("Dimensiones antes:", df.shape)
print("Dimensiones después:", df_clean.shape)
print("Columnas finales:", df_clean.columns.tolist())
