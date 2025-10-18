# =============================================================
# BLOQUE 1 - EXPLORACIÓN, LIMPIEZA Y NORMALIZACIÓN
# Proyecto: Tienda Aurelion
# Archivos: ventas.csv, detalle_ventas.csv, productos.csv, clientes.csv
# =============================================================

import pandas as pd

ventas = pd.read_csv("data_original/ventas.csv")
detalle_ventas = pd.read_csv("data_original/detalle_ventas.csv")
productos = pd.read_csv("data_original/productos.csv")
clientes = pd.read_csv("data_original/clientes.csv")


# --- 2. EXPLORACIÓN INICIAL ---
print("=== DIMENSIONES ===")
print(f"Ventas: {ventas.shape}")
print(f"Detalle Ventas: {detalle_ventas.shape}")
print(f"Productos: {productos.shape}")
print(f"Clientes: {clientes.shape}\n")

print("=== VISTA RÁPIDA (HEAD) ===")
print("\nVentas:\n", ventas.head())
print("\nDetalle Ventas:\n", detalle_ventas.head())
print("\nProductos:\n", productos.head())
print("\nClientes:\n", clientes.head())

print("\n=== INFORMACIÓN DE TIPOS DE DATOS ===")
print("\nVentas:")
print(ventas.info())
print("\nDetalle Ventas:")
print(detalle_ventas.info())
print("\nProductos:")
print(productos.info())
print("\nClientes:")
print(clientes.info())

# --- 3. LIMPIEZA DE DUPLICADOS ---
print("\n=== ELIMINACIÓN DE DUPLICADOS ===")
ventas.drop_duplicates(inplace=True)
detalle_ventas.drop_duplicates(inplace=True)
productos.drop_duplicates(inplace=True)
clientes.drop_duplicates(inplace=True)

# --- 4. LIMPIEZA DE VALORES FALTANTES ---
print("\n=== VALORES FALTANTES ANTES ===")
print("Ventas:\n", ventas.isnull().sum())
print("Detalle Ventas:\n", detalle_ventas.isnull().sum())
print("Productos:\n", productos.isnull().sum())
print("Clientes:\n", clientes.isnull().sum())

# Reglas simples: si hay nulos en textos -> "Desconocido", en números -> 0
ventas.fillna({"medio_pago": "Desconocido"}, inplace=True)
detalle_ventas.fillna({"cantidad": 0, "importe": 0}, inplace=True)
productos.fillna({"categoria": "Desconocido", "precio_unitario": 0}, inplace=True)
clientes.fillna({"ciudad": "Desconocido", "email": "sin_email@aurelion.com"}, inplace=True)

# --- 5. NORMALIZACIÓN DE FORMATOS ---
print("\n=== NORMALIZANDO FORMATOS ===")

# Fechas al formato datetime
ventas["fecha"] = pd.to_datetime(ventas["fecha"], errors="coerce")

# Strings en minúsculas y sin espacios extra
ventas["medio_pago"] = ventas["medio_pago"].str.strip().str.lower()
productos["categoria"] = productos["categoria"].str.strip().str.title()
clientes["ciudad"] = clientes["ciudad"].str.strip().str.title()

# Nombres de clientes normalizados
clientes["nombre_cliente"] = clientes["nombre_cliente"].str.title()
ventas["nombre_cliente"] = ventas["nombre_cliente"].str.title()

# --- 6. VERIFICACIÓN FINAL ---
print("\n=== INFORMACIÓN FINAL DE LOS DATASETS ===")
for nombre, df in {"ventas": ventas, "detalle_ventas": detalle_ventas, "productos": productos, "clientes": clientes}.items():
    print(f"\nArchivo: {nombre}")
    print(df.info())
    print(df.head(3))
    print("-" * 50)

# --- 7. GUARDADO DE ARCHIVOS LIMPIOS ---
ventas.to_csv("data_limpia/ventas_limpio.csv", index=False)
detalle_ventas.to_csv("data_limpia/detalle_ventas_limpio.csv", index=False)
productos.to_csv("data_limpia/productos_limpio.csv", index=False)
clientes.to_csv("data_limpia/clientes_limpio.csv", index=False)

print("\n✅ Archivos limpios guardados correctamente en carpeta 'data_limpia/'")
