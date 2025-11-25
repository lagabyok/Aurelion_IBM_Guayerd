import pandas as pd
import os

# ---------- CONFIG ----------
# Ruta de entrada (tu archivo actual)
INPUT_PATH = r"data_final\productos_categorias_normalizadas_clean.csv"

# Ruta de salida (nuevo archivo con categorías)
OUTPUT_PATH = r"data_final\productos_categorias_normalizadas_con_categorias.csv"
# -----------------------------


def infer_categoria(nombre: str) -> str:
    """
    Asigna una categoría a partir del nombre del producto (string).
    Las reglas son simples, basadas en palabras clave en minúsculas.
    Podés ajustar/afinar todo esto después.
    """
    n = str(nombre).lower()

    # 1) BEBIDAS ALCOHÓLICAS
    if any(x in n for x in ["vino", "cerveza", "fernet", "ron", "gin", "whisky"]):
        return "bebidas_alcoholicas"

    # 2) GASEOSAS / BEBIDAS SIN ALCOHOL
    if any(x in n for x in ["coca cola", "fanta", "sprite", "gaseosa", "cola"]):
        return "bebidas_sin_alcohol"
    if any(x in n for x in ["agua mineral", "agua sin gas", "agua con gas"]):
        return "bebidas_sin_alcohol"
    if "jugo" in n or "nectar" in n:
        return "bebidas_sin_alcohol"
    if "te verde" in n or "té verde" in n or "te negro" in n or "té negro" in n:
        return "infusiones"
    if "café" in n or "cafe " in n:
        return "infusiones"
    if "leche" in n:
        return "lacteos"

    # 3) CONGELADOS
    if any(x in n for x in ["helado", "empanadas congeladas", "hamburguesas congeladas", "verduras congeladas"]):
        return "congelados"

    # 4) DULCES / SNACKS
    if any(x in n for x in ["alfajor", "galletitas", "bizcocho", "chocolate", "turrón", "turron"]):
        return "snacks_dulces"
    if any(x in n for x in ["caramelos", "gomitas", "bombones", "barrita de cereal", "barrita"]):
        return "snacks_dulces"
    if "dulce de leche" in n or "mermelada" in n or "miel" in n:
        return "untables_dulces"

    # 5) ALMACÉN SECO / SALADO
    if any(x in n for x in ["arroz", "harina", "fideos", "pasta", "cous cous", "cuscus"]):
        return "almacen_seco"
    if any(x in n for x in ["lentejas", "garbanzos", "porotos", "legumbre"]):
        return "almacen_seco"
    if any(x in n for x in ["azúcar", "azucar", "sal"]):
        return "basicos_despensa"
    if any(x in n for x in ["aceite", "vinagre", "salsa", "mayonesa", "ketchup", "mostaza"]):
        return "condimentos_aceites"
    if any(x in n for x in ["avena", "granola", "cereal"]):
        return "desayuno_cereales"
    if "pan " in n or "tostadas" in n:
        return "panificados"

    # 6) LÁCTEOS / QUESOS / YOGURES
    if "queso" in n:
        return "lacteos_quesos"
    if "yogur" in n or "yogurt" in n:
        return "lacteos_yogures"
    if "manteca" in n:
        return "lacteos_grasas"

    # 7) LIMPIEZA
    if any(x in n for x in ["lavandina", "detergente", "desinfectante", "jabón en polvo", "jabon en polvo"]):
        return "limpieza"
    if any(x in n for x in ["trapo de piso", "esponja", "rejilla"]):
        return "limpieza_utensilios"

    # 8) HIGIENE PERSONAL
    if any(x in n for x in ["shampoo", "acondicionador", "crema de enjuague"]):
        return "higiene_cabello"
    if any(x in n for x in ["crema dental", "pasta dental", "hilo dental", "cepillo de dientes"]):
        return "higiene_bucal"
    if any(x in n for x in ["jabón de tocador", "jabon de tocador", "jabón barra", "jabon barra"]):
        return "higiene_corporal"

    # 9) PAPEL / HOGAR
    if "papel higiénico" in n or "papel higienico" in n:
        return "hogar_papel"
    if "servilleta" in n:
        return "hogar_papel"
    if "fosforos" in n or "fósforos" in n or "encendedor" in n:
        return "hogar_varios"

    # 10) DEFAULT
    return "otros"


def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {INPUT_PATH}")

    print(f"Leyendo: {INPUT_PATH}")
    df = pd.read_csv(INPUT_PATH)

    if "nombre_producto" not in df.columns:
        raise ValueError("El CSV debe tener una columna 'nombre_producto'")

    print("Generando columna 'categoria'...")
    df["categoria"] = df["nombre_producto"].apply(infer_categoria)

    print("Ejemplo de asignaciones:")
    print(df[["nombre_producto", "categoria"]].drop_duplicates().head(20))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\nArchivo con categorías guardado en:\n{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
