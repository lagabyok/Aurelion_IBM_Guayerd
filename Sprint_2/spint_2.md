# 🧾 **Sprint 2 - Tienda Aurelion**  
### _De Datos Brutos a Insights Estratégicos_

---

## 🔧 1️⃣ Preparación y Limpieza de Datos

Antes de cualquier análisis, se aplicó un riguroso proceso de **Data Wrangling** para garantizar la integridad y consistencia del dataset maestro, unificando **cuatro archivos de origen**.

### 🧹 1.1 Estrategia de Limpieza Aplicada

| **Problema** | **Tarea de Limpieza** | **Descripción** |
|---------------|------------------------|------------------|
| **Integración** | Unión de Datos | Unificación de las cuatro tablas de origen en un único dataset maestro. |
| **Duplicados** | Eliminación | Se eliminaron todos los registros duplicados, asegurando la unicidad de las transacciones. |
| **Datos Faltantes (Nulos)** | Imputación Estratégica | Para campos categóricos (`medio_pago`, `categoría`, `ciudad`) se imputó el valor *“Desconocido”*. Para variables numéricas clave (`cantidad`, `importe`, `precio_unitario`) se imputó con `0` para evitar sesgos. |
| **Consistencia** | Normalización de texto | Todas las columnas de texto se estandarizaron a formato uniforme (minúsculas o mayúsculas de título). |
| **Fechas** | Conversión de formato | Se convirtieron las columnas de fecha al formato universal `datetime` para facilitar el análisis temporal. |
| **Inconsistencia** | Corrección de categorías | Se aplicó una función personalizada `corregir_categoria()` basada en palabras clave para reasignar correctamente productos mal categorizados. |

> ✅ **Resultado:** Dataset limpio, consistente y preparado para el **Análisis Exploratorio de Datos (EDA)**.

---

## 📊 2️⃣ Análisis Exploratorio de Datos (EDA) y Perfil de Transacción  

El dataset resultante contiene **343 registros de transacciones**.  
El análisis estadístico inicial revela una **alta volatilidad en los ingresos**.

| **Métrica** | **Valor** |
|--------------|-----------|
| Promedio | 7,730.08 |
| Desviación Estándar (DS) | 5,265.54 |
| Asimetría (Skewness) | +0.87 |
| Outliers detectados | 7 |

### 🔍 Interpretación
Una desviación estándar notablemente alta respecto al promedio indica una gran dispersión.  
Esto sugiere un perfil de cliente y producto heterogéneo, justificando un **análisis de correlación profunda** para identificar los verdaderos impulsores de las ventas.

---

## 🔗 3️⃣ Correlación de Variables Numéricas  

### 📈 3.1 Interpretación de la Matriz de Correlación

La matriz de calor muestra el grado y la dirección de las relaciones lineales entre variables numéricas clave.

| **Relación** | **Coeficiente** | **Interpretación** |
|---------------|------------------|--------------------|
| `importe` vs `precio_unitario` | +0.68 | Fuerte correlación positiva: el importe crece con el precio unitario. |
| `importe` vs `cantidad` | +0.60 | Correlación moderada positiva: la cantidad impulsa el importe total. |
| `cantidad` vs `precio_unitario` | −0.07 | Relación marginal: no existe correlación lineal significativa. |

![Matriz de Correlación](https://github.com/user-attachments/assets/18ff516c-1001-4d01-9836-9211ef926acd)

> 📌 **Conclusión Clave:**  
> Las estrategias de **aumento de precios** y **venta cruzada** no se afectan negativamente entre sí, ya que la correlación entre `cantidad` y `precio_unitario` es prácticamente nula.

---

### 🔄 3.2 Gráfico de Pares (Pair Plot)

El gráfico de pares refuerza visualmente los hallazgos de la matriz:

- `importe` vs `precio_unitario`: tendencia lineal positiva clara (**coef. 0.68**).  
- `importe` vs `cantidad`: pendiente positiva que confirma correlación moderada (**0.60**).  
- **Distribuciones:** las curvas KDE muestran patrones no normales, con mayor concentración en valores bajos de `cantidad` y `precio_unitario`.

![Pair Plot](https://github.com/user-attachments/assets/07ed0faf-1e63-47c0-9281-500b1578c17e)

---

## ⏱️ 4️⃣ Análisis de Tendencia Temporal  

El gráfico **“Correlación: Importe Promedio de Venta Única vs Día del Mes”** explora la estacionalidad diaria.

| **Métrica** | **Valor** |
|--------------|-----------|
| Pendiente de la tendencia (roja) | −103.04 |
| Promedio General (azul) | 22,432 |

![Tendencia Temporal](https://github.com/user-attachments/assets/dc39c617-729e-4d14-8a87-41f6d6f5ece2)

### 🧭 Interpretación
- Se observa una **tendencia descendente suave** en el importe promedio a lo largo del mes.  
- La alta dispersión sugiere **ausencia de estacionalidad diaria clara**, por lo que no se justifica una estrategia de precios o promociones basada en el día del mes.  
- El impacto de la tendencia lineal es **marginal**.

---

## 🎯 5️⃣ Conclusiones Finales  

A continuación se presentan los **dos insights estratégicos principales** derivados del análisis:

---

### 💡 Insight 1: Diseño de Campañas de Venta Cruzada

> “La independencia entre el Precio y la Cantidad comprada ofrece una ventana estratégica para maximizar el TPV (Ticket Promedio de Venta) sin riesgo de fricción de precios.”

**Detalle técnico:**  
La correlación marginal de `−0.07` entre `precio_unitario` y `cantidad` confirma que el precio de un artículo **no disuade al cliente de agregar más unidades o productos**.

**Acción propuesta:**
- Implementar un **sistema de recomendación de productos complementarios (Cross-Selling)**.  
- Ejemplo: si compra **salsa**, ofrecer **fideos**; si compra **mermelada**, ofrecer **pan**.  
- 🎯 **Objetivo:** incrementar el valor de cada transacción elevando la correlación `importe` vs `cantidad` (>0.60).

---

### 💡 Insight 2: Priorización de la Calidad del Dato

> “La alta dispersión y los 7 valores atípicos en importe son una señal de alerta sobre la granularidad de id_cliente.”

**Detalle técnico:**
- Skewness positiva: **0.87**  
- Ventas excepcionalmente grandes  
- Correlación `id_cliente` vs `importe` = **0.03**, valor inusual  

**Acción propuesta:**
- Investigar los **7 outliers** para determinar si son:
  - Clientes recurrentes B2B / mayoristas  
  - Compras únicas anómalas  
- Crear una nueva variable:  
  ```python
  Valor_Historico_Cliente = total_ingresos_por_cliente


🧠 Síntesis Global

“Un set limpio, un análisis exploratorio riguroso y correlaciones bien interpretadas permiten traducir datos transaccionales en decisiones estratégicas tangibles.”

**SITIO WEB**
https://tienda-aurelion-dashboard.streamlit.app/

<img width="1257" height="428" alt="image" src="https://github.com/user-attachments/assets/de650614-fb01-4d82-a393-4d288d32083d" />

**COLAB GRUPO 11**
https://colab.research.google.com/drive/18lzGHLG5WPeBBs2rFUJI781bvTU_Rl66?usp=sharing

