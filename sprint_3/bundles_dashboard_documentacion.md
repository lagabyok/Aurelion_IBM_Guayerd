# 📦 Dashboard de Bundles -- Tienda Aurelion

Análisis automático de reglas de asociación, margen estimado y
oportunidades de cross-selling.

## 🔍 ¿Qué muestra este dashboard?

El dashboard permite visualizar: - Reglas de asociación (antecedente →
consecuente). - Support, confianza y lift. - Margen estimado del
bundle. - Ranking filtrado por métricas. - Gráficos: lift vs support +
top margen. - Ocultar reglas duplicadas (A→B y B→A) para mostrar más
variedad.

## ✨ Transformación de reglas

Formato limpio:

    producto A → producto B

## 🔁 Eliminación de duplicados

Solo se deja la mejor regla entre A→B y B→A.

## 📊 Ejemplo sin duplicados

caramelos masticables → té verde 20 saquitos\
Lift: 8.00 · Confianza: 0.40 · Support: 0.0167\
Margen estimado: \$15203

dulce de leche 400g → mermelada de frutilla 400g\
Lift: 5.71 · Confianza: 0.33 · Support: 0.0167\
Margen estimado: \$13775

hamburguesas congeladas x4 → helado vainilla 1l\
Lift: 8.00 · Confianza: 0.33 · Support: 0.0167\
Margen estimado: \$11959

verduras congeladas mix → jugo de manzana 1l\
Lift: 20.00 · Confianza: 0.67 · Support: 0.0167\
Margen estimado: \$11549

## 🧠 Insights

-   Lift alto + support bajo → oportunidades ocultas\
-   Margen alto → mayor utilidad\
-   Ideal para campañas de cross‑selling

© 2025 Tienda Aurelion -- Dashboard automático
