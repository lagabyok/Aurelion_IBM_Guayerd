import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de Matplotlib para mejor visualización
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# ----------------------------------------------------
# 1. CREACIÓN DEL DATAFRAME (Tu código inicial)
# ----------------------------------------------------
print("--- 1. Creación y Visualización Inicial del DataFrame ---")
data = {
    'mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May'],
    'ventas': [45000, 52000, 38000, 61000, 48000],
    'visitantes': [15000, 18200, 12500, 20500, 16800],
    'conversion': [3.2, 2.9, 3.8, 3.1, 2.7], # Porcentaje de conversión
    'gasto_pub': [8500, 9800, 7200, 11200, 9500],
    'productos': [450, 520, 380, 610, 480] # Productos vendidos
}
df = pd.DataFrame(data)

# Mostrar el DataFrame (Para verificar que se creó correctamente)
print(df)
print("\n" + "="*50 + "\n")

# ----------------------------------------------------
# 2. CÁLCULO DE MÉTRICAS CLAVE (Según el plan de trabajo)
# ----------------------------------------------------
# 2.1. Calcular la eficiencia publicitaria (Ventas / Gasto Publicitario)
df['eficiencia_pub'] = df['ventas'] / df['gasto_pub']

# 2.2. Calcular el ticket promedio (Ventas / Productos Vendidos)
df['ticket_promedio'] = df['ventas'] / df['productos']

print("--- 2. DataFrame con Métricas Calculadas (Eficiencia y Ticket) ---")
print(df.round(2))
print("\n" + "="*50 + "\n")

# ----------------------------------------------------
# 3. ANÁLISIS DESCRIPTIVO Y CONCLUSIONES (Según el plan de trabajo)
# ----------------------------------------------------

# 3.1. Identificar el mes con mayor eficiencia (ventas/gasto publicidad)
mes_mayor_eficiencia = df.loc[df['eficiencia_pub'].idxmax()]
print("--- 3. Análisis de Desempeño ---")
print(f"a) Mes con MAYOR Eficiencia Publicitaria (Ventas/Gasto): {mes_mayor_eficiencia['mes']}")
print(f"   Valor de Eficiencia: {mes_mayor_eficiencia['eficiencia_pub']:.2f} (Por cada $ gastado, se generaron {mes_mayor_eficiencia['eficiencia_pub']:.2f} $ en ventas)")

# 3.2. Determinar el mes con mejor tasa de conversión
mes_mejor_conversion = df.loc[df['conversion'].idxmax()]
print(f"b) Mes con MEJOR Tasa de Conversión: {mes_mejor_conversion['mes']} ({mes_mejor_conversion['conversion']:.1f}%)")

# ----------------------------------------------------
# 4. VISUALIZACIONES (Según el plan de trabajo)
# ----------------------------------------------------

# Preparar la figura para 3 gráficos en una fila
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
plt.suptitle('Visualizaciones de Rendimiento E-commerce (Análisis Python)', fontsize=16, y=1.02)

# --- 4.1. Líneas: Evolución de ventas mensuales ---
# Utilizando Seaborn para mejor estética
sns.lineplot(data=df, x='mes', y='ventas', marker='o', ax=axes[0], color='dodgerblue')
axes[0].set_title('Evolución de Ventas Mensuales', fontsize=12)
axes[0].set_ylabel('Ventas ($)')
axes[0].grid(axis='y', linestyle='--')
for i, row in df.iterrows():
    axes[0].text(row['mes'], row['ventas'] + 1500, f'{row["ventas"]:,}', ha='center', fontsize=8)


# --- 4.2. Barras: Comparación de eficiencia publicitaria (ventas/gasto) ---
sns.barplot(data=df, x='mes', y='eficiencia_pub', ax=axes[1], palette='viridis')
axes[1].set_title('Eficiencia Publicitaria por Mes', fontsize=12)
axes[1].set_ylabel('Ratio (Ventas / Gasto Publicitario)')
axes[1].tick_params(axis='x', rotation=0)
for container in axes[1].containers:
    axes[1].bar_label(container, fmt='%.2f', fontsize=8)


# --- 4.3. Dispersión: Relación visitantes vs ventas ---
sns.scatterplot(data=df, x='visitantes', y='ventas', ax=axes[2], hue='mes', s=150, palette='Set1', legend=False)
axes[2].set_title('Relación Visitantes vs. Ventas', fontsize=12)
axes[2].set_xlabel('Visitantes')
axes[2].set_ylabel('Ventas ($)')
# Añadir la etiqueta de los meses
for i, row in df.iterrows():
    axes[2].text(row['visitantes'] + 50, row['ventas'], row['mes'], fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.show()

# --- 4.4. Heatmap: Correlaciones ---
plt.figure(figsize=(8, 7))
# Calculamos la matriz de correlación solo para las variables numéricas clave
correlation_matrix = df[['ventas', 'visitantes', 'gasto_pub', 'conversion', 'productos', 'eficiencia_pub', 'ticket_promedio']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, cbar=True)
plt.title('Mapa de Calor de Correlaciones entre Métricas de E-commerce', fontsize=14)
plt.show()

# ----------------------------------------------------
# 5. ANÁLISIS DE CORRELACIÓN (Nivel Licenciatura)
# ----------------------------------------------------
print("\n" + "="*50 + "\n")
print("--- 5. Interpretación de Correlaciones (Análisis Técnico) ---")
print("El objetivo es entender qué variables se mueven juntas.")
print("La matriz de correlación se ha calculado con .corr() y se muestra en el Heatmap.")
print(f"a) Correlación Ventas vs. Visitantes: {correlation_matrix.loc['ventas', 'visitantes']:.2f}")
print("   Interpretación: Existe una alta correlación positiva. El aumento de visitantes está fuertemente asociado al aumento de ventas.")
print(f"b) Correlación Ventas vs. Gasto Publicitario: {correlation_matrix.loc['ventas', 'gasto_pub']:.2f}")
print("   Interpretación: También muy alta. Indica que la inversión en publicidad es efectiva para impulsar las ventas.")
print(f"c) Correlación Ventas vs. Conversión: {correlation_matrix.loc['ventas', 'conversion']:.2f}")
print("   Interpretación: Es la correlación más baja. Esto es clave: la conversión es más alta en marzo (3.8%), pero las ventas totales son bajas, indicando que el problema de ventas en marzo fue la baja afluencia (visitantes) y no la calidad del sitio (conversión).")
