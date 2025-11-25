# bundle_dashboard.py


import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px


OUT_DIR = "data_final/bundles_output"


st.set_page_config(page_title="Bundles Dashboard", layout="wide")
st.title("Bundles Alta Conversión - Tienda Aurelion")


# ============================
# Buscar archivos FULL reales
# ============================
files = sorted(
    glob.glob(os.path.join(OUT_DIR, "bundles_rules_full_*.csv")),
    reverse=True
)


if not files:
    st.warning("No se encontraron bundles FULL generados. Ejecutá bb.py primero.")
    st.stop()


latest = files[0]
st.markdown(f"**Archivo cargado:** `{os.path.basename(latest)}`")


df = pd.read_csv(latest)


# Crear columna "rule"
def limpiar_set(x):
    return str(x).replace("{", "").replace("}", "").replace("'", "")


df["rule"] = df.apply(
    lambda r: f"{limpiar_set(r['antecedents'])} → {limpiar_set(r['consequents'])}",
    axis=1
)


# ======================================
# ELIMINAR REGLAS INVERTIDAS DUPLICADAS
# ======================================


def clean_item(x):
    return str(x).replace("{","").replace("}","").replace("'","").strip()


def normalizar_regla(a, b):
    items = sorted([a, b])
    return f"{items[0]}__{items[1]}"


# crear clave única del par
df["pair_key"] = df.apply(
    lambda r: normalizar_regla(
        clean_item(r["antecedents"]),
        clean_item(r["consequents"])
    ),
    axis=1
)


# quedarnos SOLO con la regla con mayor margen (la más relevante del par)
df = df.sort_values("margen_estimado", ascending=False)
df = df.drop_duplicates(subset="pair_key", keep="first")
df = df.drop(columns=["pair_key"])


# Fix sliders
min_supp = float(df["support"].min())
max_supp = float(df["support"].max())
if min_supp == max_supp:
    max_supp = min_supp + 0.001


min_lift_v = float(df["lift"].min())
max_lift_v = float(df["lift"].max())
if min_lift_v == max_lift_v:
    max_lift_v = min_lift_v + 0.01


# ============================
# Filtros
# ============================
st.sidebar.header("Filtros")


min_lift = st.sidebar.slider("Lift mínimo", min_lift_v, max_lift_v, min_lift_v)
max_support = st.sidebar.slider(
    "Support máximo",
    min_supp,
    max_supp,
    float(df["support"].quantile(0.90))
)
top_n = st.sidebar.slider("Top N bundles", 5, 50, 10)


# Filtrar
df_f = df[(df["lift"] >= min_lift) & (df["support"] <= max_support)].copy()
df_f = df_f.sort_values("margen_estimado", ascending=False).head(top_n)


# ============================
# Vista tipo TARJETAS
# ============================


st.subheader("Bundles recomendados (vista tarjetas)")


for idx, row in df_f.iterrows():
    with st.container():
        st.markdown(
            f"""
            <div style="
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 12px;
                background-color: #111111;
                border: 1px solid #333;
            ">
                <h4 style="margin:0; color:#E74B3C;">
                    {row['rule'].replace("frozenset(", "").replace(")", "")}
                </h4>
                <p style="margin:4px 0; color:#BBBBBB;">
                    <b>Lift:</b> {row['lift']:.2f} ·
                    <b>Confianza:</b> {row['confidence']:.2f} ·
                    <b>Support:</b> {row['support']:.4f}
                </p>
                <p style="margin:4px 0; color:#06D6A0;">
                    <b>Margen estimado:</b> ${row['margen_estimado']:.0f}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================
# Scatter plot
# ============================


st.subheader("Distribución de bundles")
fig = px.scatter(
    df,
    x="support",
    y="lift",
    size="margen_estimado",
    color="confidence",
    hover_data=["rule"],
    title="Lift vs Support (tamaño ~ margen estimado)",
)
st.plotly_chart(fig, use_container_width=True)




# ============================
# Notas
# ============================
st.markdown("### Análisis rápido")
st.markdown("""
- **Lift alto + support bajo → oportunidades ocultas**  
- **Margen alto → máxima utilidad por promoción**  
- **Ideal para campañas de cross-selling automático**  
""")


st.markdown("---")
st.markdown("© 2025 Tienda Aurelion | Dashboard automático")
