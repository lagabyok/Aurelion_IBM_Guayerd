# =============================================================
# BLOQUE 2 - UNIÓN DE DATASETS Y CREACIÓN DEL DATAFRAME MAESTRO
# Proyecto: Tienda Aurelion
# Archivos limpios: ventas_limpio.csv, detalle_ventas_limpio.csv,
# productos_limpio.csv, clientes_limpio.csv
# =============================================================

import pandas as pd
import os

# --- 1. CARGA DE ARCHIVOS LIMPIOS ---
ventas = pd.read_csv("data_limpia/ventas_limpio.csv")
detalle = pd.read_csv("data_limpia/detalle_ventas_limpio.csv")
productos = pd.read_csv("data_limpia/productos_limpio.csv")
clientes = pd.read_csv("data_limpia/clientes_limpio.csv")

print("Archivos cargados correctamente ✅\n")

# --- 2. UNIÓN ENTRE TABLAS ---

# 🔗 Paso 1: unir ventas + detalle_ventas por id_venta
ventas_detalle = pd.merge(detalle, ventas, on="id_venta", how="left")

# 🔗 Paso 2: unir con productos por id_producto
ventas_productos = pd.merge(ventas_detalle, productos, on="id_producto", how="left")

# 🔗 Paso 3: unir con clientes por id_cliente
ventas_completas = pd.merge(ventas_productos, clientes, on="id_cliente", how="left", suffixes=('_venta', '_cliente'))

# --- 3. VALIDACIÓN DE CLAVES Y DUPLICADOS ---
print("Filas totales luego de la unión:", len(ventas_completas))
duplicados = ventas_completas.duplicated().sum()
print(f"Duplicados encontrados: {duplicados}")
if duplicados > 0:
    ventas_completas.drop_duplicates(inplace=True)
    print("Duplicados eliminados.")

# --- 4. CREACIÓN DE COLUMNAS DERIVADAS ---
# Calcular importe total por venta (si no existiera)
if 'importe' not in ventas_completas.columns:
    ventas_completas['importe'] = ventas_completas['cantidad'] * ventas_completas['precio_unitario']

# Crear una columna de mes (para análisis temporal)
ventas_completas["mes"] = pd.to_datetime(ventas_completas["fecha"]).dt.month

# --- 5. ANÁLISIS INICIAL ---
print("\n=== ANÁLISIS INICIAL ===")

# Total de ventas
total_ventas = ventas_completas["importe"].sum()
print(f"💰 Importe total vendido: ${total_ventas:,.0f}")

# Ventas por categoría
ventas_por_categoria = ventas_completas.groupby("categoria")["importe"].sum().sort_values(ascending=False)
print("\n🏷️ Ventas por categoría:\n", ventas_por_categoria)

# Ventas por medio de pago
ventas_por_medio = ventas_completas.groupby("medio_pago")["importe"].sum().sort_values(ascending=False)
print("\n💳 Ventas por medio de pago:\n", ventas_por_medio)

# Ciudades con más ventas
ventas_por_ciudad = ventas_completas.groupby("ciudad")["importe"].sum().sort_values(ascending=False).head(5)
print("\n🏙️ Top 5 ciudades con más ventas:\n", ventas_por_ciudad)

# --- 6. GUARDAR EL DATASET FINAL ---
os.makedirs("data_final", exist_ok=True)
ventas_completas.to_csv("data_final/ventas_completas.csv", index=False)

print("\n✅ Dataset maestro guardado en 'data_final/ventas_completas.csv'")
print(f"Dimensiones finales: {ventas_completas.shape}")
