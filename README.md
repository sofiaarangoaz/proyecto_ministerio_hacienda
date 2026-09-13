# Proyecto 1: Ministerio de Hacienda (ACTD)

Producto de analítica sobre la contratación pública del **Ministerio de Hacienda y
Crédito Público**, a partir de los datos de **SECOP II - Contratos Electrónicos**.

- **Equipo:** Juan José Galvis · Sofía Arango Azcárate · Juan Sebastián Quiñones
- **Universidad de los Andes**: Analítica Computacional para la Toma de Decisiones

## Preguntas de negocio

1. **(Sofía)** ¿Cuánta plata contrató el Ministerio cada
   año y en qué tipo de contratos se concentra?
2. **(Juan Sebastián)** ¿Difiere el porcentaje de ejecución 
   presupuestal (pagado / contratado) al momento del corte según si el contratista es 
   PyME, consorcio, o el género de su representante legal?
3. **(Juan José)** ¿A través de qué modalidades de
   contratación asigna sus recursos el Ministerio, y cómo se relaciona la modalidad con
   el valor y la duración de los contratos?

## Estructura del repositorio

| Carpeta | Contenido | Rol responsable |
|---|---|---|
| `tarea1_negocio/` | Definición de las preguntas de negocio | Análisis de negocio |
| `tarea2_ingenieria_datos/` | Extracción (S3/Glue/Athena), limpieza y alistamiento | Ingeniería de datos |
| `tarea3_analisis/` | Análisis exploratorio (un notebook por analista) | Análisis de datos |
| `tarea4_tablero/` | Desarrollo del tablero en Dash | Tablero de datos (Sofía, Juan José) |
| `despliegue/` | Última versión del tablero, lista para lanzar en AWS EC2 | Despliegue y mantenimiento (Juan Sebastián) |

## Fuente de datos

Datos Abiertos Colombia: SECOP II Contratos Electrónicos, subconjunto del Ministerio
de Hacienda y Crédito Público.
