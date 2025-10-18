# =============================================================
# EXPORTACIÓN DE DASHBOARD INTERACTIVO
# =============================================================

import pandas as pd
import plotly.express as px

# --- Cargar dataset maestro ---
df = pd.read_csv("data_final/ventas_completas.csv")
df['fecha'] = pd.to_datetime(df['fecha'])
df['mes'] = df['fecha'].dt.month_name()

# --- Gráficos ---
# 1️⃣ Ventas por categoría
ventas_categoria = df.groupby('categoria')['importe'].sum().reset_index()
fig_categoria = px.bar(ventas_categoria, x='categoria', y='importe', 
                       title="Ventas por Categoría",
                       color='categoria',
                       color_discrete_sequence=['#F24141','#F27979'])
fig_categoria.write_html("graf_categoria.html", include_plotlyjs='cdn', full_html=False)

# 2️⃣ Ventas por medio de pago
ventas_pago = df.groupby('medio_pago')['importe'].sum().reset_index()
fig_pago = px.bar(ventas_pago, x='medio_pago', y='importe',
                  title="Ventas por Medio de Pago",
                  color='medio_pago',
                  color_discrete_sequence=['#E74B3C','#F24141','#F27979','#CBC8CB'])
fig_pago.write_html("graf_pago.html", include_plotlyjs=False, full_html=False)

# 3️⃣ Top 5 ciudades
ventas_ciudad = df.groupby('ciudad')['importe'].sum().sort_values(ascending=False).head(5).reset_index()
fig_ciudades = px.bar(ventas_ciudad, x='ciudad', y='importe',
                      title="Top 5 Ciudades con Más Ventas",
                      color='ciudad',
                      color_discrete_sequence=['#F24141','#F27979','#E74B3C','#CBC8CB','#FFE3E3'])
fig_ciudades.write_html("graf_ciudades.html", include_plotlyjs=False, full_html=False)

# 4️⃣ Top 5 clientes
ventas_cliente = df.groupby('nombre_cliente_venta')['importe'].sum().sort_values(ascending=False).head(5).reset_index()
fig_clientes = px.bar(ventas_cliente, x='nombre_cliente_venta', y='importe',
                      title="Top 5 Clientes con Mayor Gasto",
                      color='nombre_cliente_venta',
                      color_discrete_sequence=['#F24141','#F27979','#E74B3C','#CBC8CB','#FFE3E3'])
fig_clientes.write_html("graf_clientes.html", include_plotlyjs=False, full_html=False)

# --- HTML principal ---
html_dashboard = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Tienda Aurelion - Dashboard Interactivo</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
body {{ font-family: Arial, sans-serif; background-color: #FFE3E3; color: #333; margin: 0; padding: 0; }}
h1 {{ background-color: #F24141; color: white; padding: 20px; text-align: center; margin: 0; }}
button {{ margin: 10px; padding: 10px 20px; background-color: #F27979; border: none; color: white; cursor: pointer; border-radius: 5px; }}
button:hover {{ background-color: #E74B3C; }}
.chart-container {{ display: none; margin: 20px; border: 2px solid #F24141; padding: 10px; border-radius: 8px; background-color: white; }}
</style>
</head>
<body>
<h1>🛒 Tienda Aurelion - Dashboard Interactivo</h1>

<div style="text-align:center;">
<button onclick="toggleChart('cat')">Ventas por Categoría</button>
<button onclick="toggleChart('pago')">Ventas por Medio de Pago</button>
<button onclick="toggleChart('ciudad')">Top 5 Ciudades</button>
<button onclick="toggleChart('cliente')">Top 5 Clientes</button>
</div>

<div id="cat" class="chart-container">{open('graf_categoria.html').read()}</div>
<div id="pago" class="chart-container">{open('graf_pago.html').read()}</div>
<div id="ciudad" class="chart-container">{open('graf_ciudades.html').read()}</div>
<div id="cliente" class="chart-container">{open('graf_clientes.html').read()}</div>

<script>
function toggleChart(chartId) {{
    let allCharts = document.getElementsByClassName('chart-container');
    for (let c of allCharts) {{ c.style.display = 'none'; }}
    let chart = document.getElementById(chartId);
    chart.style.display = 'block';
}}
</script>
</body>
</html>
"""

# Guardar archivo HTML principal
with open("dashboard_tienda_aurelion.html", "w", encoding="utf-8") as f:
    f.write(html_dashboard)

print("✅ Dashboard HTML generado correctamente: dashboard_tienda_aurelion.html")
