# =============================================================
# BLOQUE 3 - CONSULTAS INTERACTIVAS Y ANALÍTICAS
# Proyecto: Tienda Aurelion
# Dataset: data_final/ventas_completas.csv
# =============================================================

import pandas as pd
import webbrowser

# --- 1. CARGA DEL DATASET MAESTRO ---
df = pd.read_csv("data_final/productos_categorias_normalizadas.csv")
df['fecha'] = pd.to_datetime(df['fecha'])
df['mes'] = df['fecha'].dt.month_name()

print("\n✅ Dataset maestro cargado correctamente")
print(f"Dimensiones: {df.shape}")
print("Columnas:", df.columns.tolist())

# =============================================================
# FUNCIONES DE CONSULTA
# =============================================================

def ventas_por_categoria():
    resultado = df.groupby("categoria")["importe"].sum().sort_values(ascending=False)
    print("\n🏷️ Ventas por categoría:")
    print(resultado)
    return resultado.reset_index()

def ventas_por_medio_pago():
    resultado = df.groupby("medio_pago")["importe"].sum().sort_values(ascending=False)
    print("\n💳 Ventas por medio de pago:")
    print(resultado)
    return resultado.reset_index()

def top_ciudades():
    resultado = df.groupby("ciudad")["importe"].sum().sort_values(ascending=False).head(5)
    print("\n🏙️ Top 5 ciudades con más ventas:")
    print(resultado)
    return resultado.reset_index()

def top_clientes():
    resultado = df.groupby('nombre_cliente_venta')['importe'].sum().sort_values(ascending=False).head(5)
    print("\n🏅 Top 5 clientes con mayor gasto total:")
    print(resultado)
    return resultado.reset_index()

def ventas_mensuales():
    resultado = df.groupby('mes')['importe'].sum().sort_values(ascending=False)
    print("\n📅 Ventas totales por mes:")
    print(resultado)
    return resultado.reset_index()

def ticket_promedio():
    promedio = df.groupby('id_venta')['importe'].sum().mean()
    print(f"\n💸 Ticket promedio por venta: ${promedio:,.2f}")
    return pd.DataFrame({'Ticket Promedio': [promedio]})

def rentabilidad_categoria():
    df['costo_estimado'] = df['importe'] * 0.7
    df['ganancia_estimada'] = df['importe'] - df['costo_estimado']
    resultado = df.groupby('categoria')['ganancia_estimada'].sum()
    print("\n📈 Rentabilidad estimada por categoría:")
    print(resultado)
    return resultado.reset_index()

# =============================================================
# FUNCIONES DE EXPORTACIÓN
# =============================================================

def exportar(df_result, nombre_base):
    print("\n📂 Opciones de exportación:")
    print("1 - CSV")
    print("2 - Excel")
    print("0 - Cancelar")
    opcion = input("Seleccione formato de exportación: ")
    if opcion == "1":
        archivo = f"{nombre_base}.csv"
        df_result.to_csv(archivo, index=False)
        print(f"✅ Exportado a CSV: {archivo}")
    elif opcion == "2":
        archivo = f"{nombre_base}.xlsx"
        df_result.to_excel(archivo, index=False)
        print(f"✅ Exportado a Excel: {archivo}")
    else:
        print("❌ Exportación cancelada")

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
        print("8 - Abrir dashboard interactivo HTML")
        print("0 - Salir")
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            res = ventas_por_categoria()
            exportar(res, "ventas_por_categoria")
        elif opcion == "2":
            res = ventas_por_medio_pago()
            exportar(res, "ventas_por_medio_pago")
        elif opcion == "3":
            res = top_ciudades()
            exportar(res, "top_ciudades")
        elif opcion == "4":
            res = top_clientes()
            exportar(res, "top_clientes")
        elif opcion == "5":
            res = ventas_mensuales()
            exportar(res, "ventas_mensuales")
        elif opcion == "6":
            res = ticket_promedio()
            exportar(res, "ticket_promedio")
        elif opcion == "7":
            res = rentabilidad_categoria()
            exportar(res, "rentabilidad_categoria")
        elif opcion == "8":
            print("🌐 Abriendo dashboard interactivo en navegador...")
            webbrowser.open("http://127.0.0.1:5500/dashboard_tienda_aurelion.html")
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
