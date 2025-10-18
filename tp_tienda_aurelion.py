# =============================================================
# BLOQUE 3 - CONSULTAS INTERACTIVAS Y ANALÍTICAS
# Proyecto: Tienda Aurelion
# Dataset: data_final/ventas_completas.csv
# =============================================================

import pandas as pd

# --- 1. CARGA DEL DATASET MAESTRO ---
df = pd.read_csv("data_final/ventas_completas.csv")

# Convertimos fecha a datetime
df['fecha'] = pd.to_datetime(df['fecha'])

print("\n✅ Dataset maestro cargado correctamente")
print(f"Dimensiones: {df.shape}")
print("Columnas:", df.columns.tolist())

# =============================================================
# FUNCIONES DE CONSULTA
# =============================================================

# --- 2. Ventas totales por categoría ---
def ventas_por_categoria():
    resultado = df.groupby("categoria")["importe"].sum().sort_values(ascending=False)
    print("\n🏷️ Ventas por categoría:")
    print(resultado)

# --- 3. Ventas por medio de pago ---
def ventas_por_medio_pago():
    resultado = df.groupby("medio_pago")["importe"].sum().sort_values(ascending=False)
    print("\n💳 Ventas por medio de pago:")
    print(resultado)

# --- 4. Top 5 ciudades con más ventas ---
def top_ciudades():
    resultado = df.groupby("ciudad")["importe"].sum().sort_values(ascending=False).head(5)
    print("\n🏙️ Top 5 ciudades con más ventas:")
    print(resultado)

# --- 5. Top 5 clientes con mayor gasto ---
def top_clientes():
    # Usamos la columna correcta
    resultado = df.groupby('nombre_cliente_venta')['importe'].sum().sort_values(ascending=False).head(5)
    print("\n🏅 Top 5 clientes con mayor gasto total:")
    print(resultado)


# --- 6. Ventas mensuales ---
def ventas_mensuales():
    df['mes'] = df['fecha'].dt.month_name()
    resultado = df.groupby('mes')['importe'].sum().sort_values(ascending=False)
    print("\n📅 Ventas totales por mes:")
    print(resultado)

# --- 7. Ticket promedio por venta ---
def ticket_promedio():
    promedio = df.groupby('id_venta')['importe'].sum().mean()
    print(f"\n💸 Ticket promedio por venta: ${promedio:,.2f}")

# --- 8. Rentabilidad estimada por categoría (bonus) ---
def rentabilidad_categoria():
    df['costo_estimado'] = df['importe'] * 0.7
    df['ganancia_estimada'] = df['importe'] - df['costo_estimado']
    resultado = df.groupby('categoria')['ganancia_estimada'].sum()
    print("\n📈 Rentabilidad estimada por categoría:")
    print(resultado)

# =============================================================
# MENÚ INTERACTIVO
# =============================================================

def menu():
    while True:
        print("\n==============================")
        print("🛒 TIENDA AURELION - CONSULTAS")
        print("==============================")
        print("1 - Ventas por categoría")
        print("2 - Ventas por medio de pago")
        print("3 - Top 5 ciudades")
        print("4 - Top 5 clientes")
        print("5 - Ventas mensuales")
        print("6 - Ticket promedio por venta")
        print("7 - Rentabilidad por categoría (bonus)")
        print("0 - Salir")
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            ventas_por_categoria()
        elif opcion == "2":
            ventas_por_medio_pago()
        elif opcion == "3":
            top_ciudades()
        elif opcion == "4":
            top_clientes()
        elif opcion == "5":
            ventas_mensuales()
        elif opcion == "6":
            ticket_promedio()
        elif opcion == "7":
            rentabilidad_categoria()
        elif opcion == "0":
            print("👋 Saliendo del programa. ¡Gracias!")
            break
        else:
            print("❌ Opción inválida, intente de nuevo.")

# =============================================================
# EJECUTAR MENÚ
# =============================================================
if __name__ == "__main__":
    menu()
