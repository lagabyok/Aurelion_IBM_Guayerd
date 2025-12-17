# Análisis del Dashboard – Tienda Aurelion

## 1. Introducción

Este notebook presenta el análisis del dashboard de Power BI correspondiente a la **Tienda Aurelion**, para el período comprendido entre **febrero y junio de 2024**. A partir de los datos visualizados, se analizan las ventas, los clientes, los productos y los medios de pago, con el objetivo de obtener insights relevantes y proponer acciones concretas para mejorar el desempeño del negocio.

---

## 2. Objetivos del análisis

### Objetivo general

Analizar el desempeño comercial de la Tienda Aurelion durante el período febrero–junio de 2024, utilizando indicadores de ventas, clientes, productos y medios de pago, con el fin de obtener información útil para la toma de decisiones.

### Objetivos específicos

* Identificar el volumen total de ventas, la cantidad de productos vendidos y el ticket promedio.
* Analizar la evolución temporal de las ventas.
* Comparar el desempeño de las categorías de productos (alimentos y limpieza).
* Determinar los productos más vendidos y los clientes con mayor nivel de compra.
* Evaluar la distribución de ventas por ciudad.
* Analizar la participación y evolución de los distintos medios de pago.

---

## 3. Análisis del dashboard

### 3.1 Indicadores generales

* **Total de ventas:** aproximadamente $2,65 millones, lo que refleja un buen nivel de facturación.
* **Cantidad total vendida:** más de 1.000 unidades.
* **Ticket promedio:** cercano a $22.100, indicando el valor medio de cada compra.

### 3.2 Evolución temporal de las ventas

Las ventas presentan variaciones a lo largo de los meses analizados, con valores más bajos e irregulares al inicio del período y una tendencia a mayores montos hacia los últimos meses. Esto sugiere un crecimiento progresivo de la actividad comercial.

### 3.3 Ventas por categoría

La categoría **alimentos** concentra la mayor parte de las ventas y de las unidades vendidas, mientras que **limpieza** presenta una participación menor.

### 3.4 Productos

El Top 5 de productos más vendidos está compuesto por artículos de consumo masivo, lo que evidencia hábitos de compra recurrentes y una alta rotación de estos productos.

### 3.5 Clientes

* Se registran **67 clientes totales**.
* El Top 10 de clientes concentra una parte significativa del importe total vendido.
* Existe una relación directa entre la frecuencia de compra y el importe total gastado.

### 3.6 Ventas por ciudad

Río Cuarto es la ciudad con mayor facturación, seguida por Córdoba y Alta Gracia, mientras que otras ciudades presentan menor nivel de ventas.

### 3.7 Medios de pago

El efectivo es el medio de pago más utilizado, seguido por QR, transferencias y tarjetas. Esto muestra una combinación de métodos tradicionales y digitales.

---

## 4. Insights principales

* La tienda tiene una base sólida de ventas, con oportunidades de crecimiento.
* Alimentos es la categoría más fuerte y funciona como motor del negocio.
* Limpieza tiene potencial de crecimiento mediante acciones comerciales específicas.
* Un grupo reducido de clientes genera una parte importante de las ventas.
* Existen diferencias claras en el desempeño por ciudad.
* Los medios de pago digitales tienen margen para ser incentivados.

---

## 5. Acciones propuestas

### 5.1 Acción sobre la categoría limpieza

**Objetivo:** aumentar la rotación y participación de la categoría limpieza.

**Oferta propuesta:**

* Promoción **2×1 en productos de limpieza seleccionados** (detergente, lavandina, desinfectante).
* Válida por tiempo limitado.

**Justificación:**

* Productos de uso necesario.
* Oferta simple y directa.
* Incentiva mayor volumen de compra.

---

### 5.2 Acción sobre la categoría alimentos

**Objetivo:** aumentar el ticket promedio y la cantidad de unidades por compra.

**Oferta propuesta:**

* Promoción **2×1 en productos de alta rotación** (pizza congelada, yerba mate, queso rallado).

**Justificación:**

* Aprovecha productos con alta demanda.
* Incrementa el valor del carrito.

---

### 5.3 Acción combinada alimentos + limpieza

**Objetivo:** utilizar la fortaleza de alimentos para impulsar la venta de limpieza.

**Oferta propuesta:**

* Comprando un producto de alimentos seleccionado, el cliente obtiene **30% de descuento en un producto de limpieza**.

**Justificación:**

* El cliente ya compra alimentos.
* Reduce la barrera de compra de limpieza.
* Aumenta el ticket promedio.

---

### 5.4 Acción sobre clientes frecuentes

**Objetivo:** fidelizar a los clientes con mayor nivel de compra.

**Acción propuesta:**

* Beneficios exclusivos o descuentos para clientes del Top 10.
* Incentivos para aumentar la frecuencia de compra.

---

### 5.5 Acción sobre medios de pago

**Objetivo:** incentivar el uso de medios de pago digitales.

**Acción propuesta:**

* Descuentos por pagar con QR o transferencia.

---

## 6. Estrategia complementaria: insights de cross-selling basados en el dashboard + IA

### Enfoque del bonus analítico

Además de las acciones comerciales tradicionales, el análisis conjunto del **dashboard general** y del **dashboard de bundles basado en IA** permite identificar oportunidades adicionales de cross-selling. Esta estrategia funciona como una **mirada complementaria u oculta**, ya que surge de cruzar indicadores descriptivos del negocio con patrones de asociación detectados automáticamente.

---

## 6.1 Aportes del dashboard general al cross-selling

El dashboard tradicional aporta información clave que permite **potenciar y validar** las reglas de asociación generadas por la IA:

* La categoría **alimentos** es la más vendida y con mayor rotación, lo que la convierte en el principal punto de entrada para acciones de cross-selling.
* El **ticket promedio** y la **cantidad de productos vendidos** indican margen para incrementar el tamaño del carrito.
* La concentración de ventas en determinados **clientes frecuentes** sugiere que las acciones de cross-selling pueden tener mayor impacto en este segmento.
* La evolución temporal muestra meses con mayor actividad, ideales para aplicar recomendaciones cruzadas.

Estos datos permiten decidir **dónde y cuándo** aplicar las sugerencias generadas por la IA.

---

## 6.2 Aportes del dashboard de IA al análisis tradicional

El dashboard de bundles agrega una capa predictiva al análisis:

* Identifica productos que se compran juntos aunque no pertenezcan a la misma categoría.
* Utiliza métricas como **lift, confianza y support** para medir la fuerza de cada asociación.
* Incorpora un **margen estimado**, permitiendo priorizar combinaciones rentables.
* Elimina reglas duplicadas para facilitar la toma de decisiones.

Esto permite pasar de promociones generales a **acciones de cross-selling basadas en probabilidad real de compra**.

---

## 6.3 Insights combinados (dashboard + IA)

Al integrar ambos dashboards surgen nuevos insights:

* Productos líderes del dashboard general funcionan como **productos ancla** para activar reglas de asociación.
* Reglas con **lift alto y support bajo** representan oportunidades ocultas que el análisis tradicional no detecta.
* El cross-selling puede orientarse no solo a vender más, sino a **mejorar el margen total**.
* Las asociaciones detectadas refuerzan la estrategia de aumentar el ticket promedio sin depender únicamente de descuentos agresivos.

---

## 6.4 Acciones de cross-selling como bonus estratégico

### Acción 1: Sugerencias inteligentes basadas en productos ancla

**Ejemplo:**

* *Caramelos masticables → Té verde 20 saquitos*

**Implementación:**

* Recomendación en el punto de venta o cartel de “Producto sugerido”.
* Descuento leve (10–15%) en el producto sugerido.

**Valor agregado:**

* Se apoya en la alta rotación de alimentos.
* Aumenta el ticket promedio con bajo costo promocional.

---

### Acción 2: Bundles de alto margen validados por el dashboard

**Ejemplo:**

* *Dulce de leche 400g → Mermelada de frutilla 400g*

**Implementación:**

* Combo con precio especial.
* Comunicación como “Combo desayuno”.

**Valor agregado:**

* Asociación detectada por IA.
* Margen estimado elevado.

---

### Acción 3: Cross-selling en compras planificadas

**Ejemplo:**

* *Hamburguesas congeladas x4 → Helado vainilla 1L*

**Implementación:**

* Oferta “Completá tu compra”.

**Valor agregado:**

* Aprovecha compras de alto compromiso.
* Incrementa el valor del carrito.

---

### Acción 4: Promociones temáticas por patrón de consumo

**Ejemplo:**

* *Verduras congeladas mix → Jugo de manzana 1L*

**Implementación:**

* Bundle sugerido como opción saludable.

**Valor agregado:**

* Segmentación por hábitos de consumo.
* Base para futuras campañas personalizadas.

---

## 7. Conclusión final 

El cruce entre los indicadores del dashboard general y los insights del dashboard de IA permite identificar oportunidades de cross-selling que permanecen ocultas en un análisis tradicional. Esta mirada complementaria aporta una capa prescriptiva al análisis, permitiendo aplicar acciones más precisas, aumentar el ticket promedio y mejorar la rentabilidad del negocio sin modificar la estrategia principal.
