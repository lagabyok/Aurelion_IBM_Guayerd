import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
import matplotlib.pyplot as plt
import seaborn as sns


# ===============================
# Función: crear ticket-producto matrix
# ===============================
def create_basket(df):
    """
    Crea una matriz booleana id_venta x nombre_producto,
    con 1 si el producto aparece en el ticket, 0 si no.
    """
    basket = (
        df.groupby(["id_venta", "nombre_producto"])
          .agg({"cantidad": "sum"})
          .unstack()
          .fillna(0)
    )
    basket.columns = basket.columns.get_level_values(1)
    basket = basket.map(lambda x: 1 if x > 0 else 0)
    return basket.astype(bool)


# ===============================
# Función: estimación de margen del bundle
# ===============================
def estimate_rule_margin(rule_row, df_reference):
    """
    Estima el margen promedio por ticket para el bundle (antecedente + consecuente).
    """
    lhs = list(rule_row["antecedents"])
    rhs = list(rule_row["consequents"])
    products = lhs + rhs

    mask_any = df_reference["nombre_producto"].isin(products)
    df_any = df_reference[mask_any]

    productos_por_ticket = df_any.groupby("id_venta")["nombre_producto"].nunique()
    tickets_validos = productos_por_ticket[productos_por_ticket >= len(products)].index

    if len(tickets_validos) == 0:
        return 0.0

    margen_total = df_reference[df_reference["id_venta"].isin(tickets_validos)]["margen_total"].sum()
    return margen_total / len(tickets_validos)


# ===============================
# Ejecución completa
# ===============================
def run_bundle_pipeline(
        path_csv,
        min_support,
        min_conf,
        min_lift,
        method,
        cost_pct,
        min_occurrences_bundle=2,
        min_support_abs_rules=2):

    print("Cargando dataset...")
    df = pd.read_csv(path_csv)

    # 1. Calcular margen si no existe
    if "margen_total" not in df.columns:
        print("-> Calculando margen automáticamente (costo_estimado = importe * cost_pct)")
        df["costo_estimado"] = df["importe"] * cost_pct
        df["margen_total"] = df["importe"] - df["costo_estimado"]

    # 2. Split Train/Test
    ventas_unicas = df["id_venta"].unique()
    np.random.shuffle(ventas_unicas)

    n_tickets_total = len(ventas_unicas)
    n_train = int(0.75 * n_tickets_total)

    train_ids = ventas_unicas[:n_train]
    test_ids = ventas_unicas[n_train:]

    df_train = df[df["id_venta"].isin(train_ids)]
    df_test = df[df["id_venta"].isin(test_ids)]

    print(f"Tamaño total tickets: {n_tickets_total}")
    print(f"Tamaño train tickets: {len(train_ids)}")
    print(f"Tamaño test tickets: {len(test_ids)}")

    # 3. Basket encoding
    basket_train = create_basket(df_train)
    basket_test = create_basket(df_test)
    basket_full = create_basket(df)

    # 4. Ajuste de min_support
    if min_support is None:
        min_support = min_occurrences_bundle / n_tickets_total
        print(f"-> min_support ajustado automáticamente a {min_support:.4f}")
    else:
        print(f"-> min_support fijo: {min_support:.4f}")

    # 5. Frequent Itemsets
    print("Generando itemsets frecuentes...")
    algo = apriori if method == "apriori" else fpgrowth

    itemsets_train = algo(basket_train, min_support=min_support, use_colnames=True)
    itemsets_test = algo(basket_test, min_support=min_support, use_colnames=True)
    itemsets_full_raw = algo(basket_full, min_support=min_support, use_colnames=True)

    itemsets_full_len2 = itemsets_full_raw[itemsets_full_raw["itemsets"].apply(len) >= 2]
    print(f"Itemsets frecuentes en FULL (len>=2): {len(itemsets_full_len2)}")

    # 6. Reglas Train/Test
    rules_train = association_rules(itemsets_train, metric="confidence", min_threshold=min_conf)
    rules_train = rules_train[rules_train["lift"] >= min_lift].reset_index(drop=True)

    rules_test = association_rules(itemsets_test, metric="confidence", min_threshold=min_conf)
    rules_test = rules_test[rules_test["lift"] >= min_lift].reset_index(drop=True)

    n_train_tickets = len(train_ids)
    n_test_tickets = len(test_ids)

    rules_train = rules_train[rules_train["support"] * n_train_tickets >= min_support_abs_rules].reset_index(drop=True)
    rules_test = rules_test[rules_test["support"] * n_test_tickets >= min_support_abs_rules].reset_index(drop=True)

    print(f"Reglas train después de filtros: {len(rules_train)}")
    print(f"Reglas test después de filtros: {len(rules_test)}")

    # 7. Reglas FULL
    print("-> Calculando reglas FULL y margen estimado por bundle...")
    rules_full = association_rules(itemsets_full_raw, metric="confidence", min_threshold=min_conf)

    rules_full = rules_full[rules_full["lift"] >= min_lift].reset_index(drop=True)
    rules_full = rules_full[rules_full["support"] * n_tickets_total >= min_support_abs_rules].reset_index(drop=True)

    rules_full = rules_full[
        (rules_full["antecedents"].apply(len) + rules_full["consequents"].apply(len)) >= 2
    ].reset_index(drop=True)

    if len(rules_full) > 0:
        rules_full["margen_estimado"] = rules_full.apply(
            lambda r: estimate_rule_margin(r, df), axis=1
        )
    else:
        rules_full["margen_estimado"] = []

    rules_full = rules_full.sort_values(["lift", "margen_estimado"], ascending=[False, False])

    # 8. Estabilidad Train vs Test
    set_train = set(rules_train["antecedents"].astype(str) + "->" + rules_train["consequents"].astype(str))
    set_test = set(rules_test["antecedents"].astype(str) + "->" + rules_test["consequents"].astype(str))

    jaccard = len(set_train & set_test) / max(len(set_train | set_test), 1)

    if len(rules_train) > 0 and len(rules_test) > 0:
        mean_delta_lift = float(abs(rules_train["lift"].mean() - rules_test["lift"].mean()))
    else:
        mean_delta_lift = None

    # 9. Dashboard (gráfico)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = "data_final/bundles_output"
    os.makedirs(output_folder, exist_ok=True)

    if len(rules_full) > 0:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=rules_full,
            x="support",
            y="lift",
            size="margen_estimado",
            sizes=(20, 400),
            alpha=0.6
        )
        plt.title("Lift vs Support (tamaño = margen estimado) - FULL")
        plot_path = f"{output_folder}/bundles_plots_{timestamp}.png"
        plt.savefig(plot_path, dpi=300)
        plt.close()
    else:
        plot_path = None

    # 10. Guardar resultados
    resumen = {
        "timestamp": timestamp,
        "n_tickets_total": int(n_tickets_total),
        "n_bundles_full": int(len(rules_full)),
        "n_bundles_train": int(len(rules_train)),
        "n_bundles_test": int(len(rules_test)),
        "stability_jaccard": float(jaccard),
        "mean_delta_lift": mean_delta_lift,
        "avg_margin_ticket": float(df["margen_total"].mean()),
        "output_folder": output_folder,
        "plots": plot_path,
    }

    print("Pipeline finalizado. Resumen:")
    print(resumen)

    print("\nTop bundles (FULL, ordenados por lift y margen):")
    if len(rules_full) > 0:
        print(
            rules_full[[
                "antecedents",
                "consequents",
                "support",
                "confidence",
                "lift",
                "margen_estimado"
            ]].head(10)
        )
    else:
        print("No se encontraron bundles con los filtros actuales.")

    rules_full.to_csv(f"{output_folder}/bundles_rules_full_{timestamp}.csv", index=False)

    return resumen


# ===============================
# Argumentos CLI
# ===============================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--min_support", type=float, default=None)
    parser.add_argument("--min_conf", type=float, default=0.3)
    parser.add_argument("--min_lift", type=float, default=1.2)
    parser.add_argument("--method", type=str, default="fpgrowth", choices=["fpgrowth", "apriori"])
    parser.add_argument("--cost_pct", type=float, default=0.65)
    parser.add_argument("--min_occurrences_bundle", type=int, default=2)
    parser.add_argument("--min_support_abs_rules", type=int, default=2)

    args = parser.parse_args()

    run_bundle_pipeline(
        path_csv=args.input,
        min_support=args.min_support,
        min_conf=args.min_conf,
        min_lift=args.min_lift,
        method=args.method,
        cost_pct=args.cost_pct,
        min_occurrences_bundle=args.min_occurrences_bundle,
        min_support_abs_rules=args.min_support_abs_rules,
    )
