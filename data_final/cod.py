import pandas as pd

# --- 1. CARGA DEL DATASET MAESTRO ---
df = pd.read_csv("data_final/ventas_completas.csv")
df['fecha'] = pd.to_datetime(df['fecha'])

# =============================================================
# FUNCIONES DE CONSULTA
# =============================================================

# --- 2. Ventas totales por categoría ---
def ventas_por_categoria():
    resultado = df.groupby("categoria")["importe"].sum().sort_values(ascending=False)
    print("\nVentas por categoría:")
    print(resultado)

# --- 3. Ventas por medio de pago ---
def ventas_por_medio_pago():
    resultado = df.groupby("medio_pago")["importe"].sum().sort_values(ascending=False)
    print("\nVentas por medio de pago:")
    print(resultado)

# --- 4. Top 5 ciudades con más ventas ---
def top_ciudades():
    resultado = df.groupby("ciudad")["importe"].sum().sort_values(ascending=False).head(5)
    print("\nTop 5 ciudades con más ventas:")
    print(resultado)

# =============================================================
# MENÚ INTERACTIVO
# =============================================================

def menu():
    while True:
        print("\n==============================")
        print("TIENDA AURELION - CONSULTAS")
        print("==============================")
        print("1 - Ventas por categoría")
        print("2 - Ventas por medio de pago")
        print("3 - Top 5 ciudades")
        print("0 - Salir")
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            ventas_por_categoria()
        elif opcion == "2":
            ventas_por_medio_pago()
        elif opcion == "3":
            top_ciudades()
        elif opcion == "0":
            print("Saliendo del programa. Gracias.")
            break
        else:
            print("Opción inválida, intente de nuevo.")

# =============================================================
# EJECUTAR MENÚ
# =============================================================
if __name__ == "__main__":
    menu()
