# Proyecto 1 — Analítica de contratación pública (ACTD)

Producto de analítica sobre la contratación pública del **Ministerio de Hacienda y
Crédito Público**, a partir de los datos de **SECOP II - Contratos Electrónicos**.

- **Equipo:** Juan José Galvis · Sofía Arango Azcárate · Juan Sebastián Quiñones
- **Usuario final:** Ente de control / veeduría ciudadana
- **Universidad de los Andes** — Analítica Computacional para la Toma de Decisiones

## Preguntas de negocio

1. **(Sofía — Análisis de negocio/datos)** ¿Cuánta plata contrató el Ministerio cada
   año y en qué tipo de contratos se concentra?
2. **(Juan Sebastián — Análisis de negocio/datos)** ¿Difiere la ejecución presupuestal
   —brecha entre valor contratado y valor pagado— según las características del
   contratista (PyME, consorcio) y el género del representante legal?
3. **(Juan José — Análisis de negocio/datos)** ¿A través de qué modalidades de
   contratación asigna sus recursos el Ministerio, y cómo se relaciona la modalidad con
   el valor y la duración de los contratos?

## Estructura del repositorio

| Carpeta | Contenido | Rol responsable |
|---|---|---|
| `tarea1_negocio/` | Definición de las preguntas de negocio | Análisis de negocio |
| `tarea2_ingenieria_datos/` | Extracción (S3/Glue/Athena), limpieza y alistamiento | Ingeniería de datos |
| `tarea3_analisis/` | Análisis exploratorio (un notebook por analista) | Análisis de datos |
| `tarea4_tablero/` | Desarrollo del tablero en Dash | Tablero de datos |
| `despliegue/` | Última versión del tablero, lista para lanzar en AWS EC2 | Despliegue y mantenimiento |

## Cómo lanzar el tablero

```bash
cd despliegue
pip install -r requirements.txt
python app.py
```

Luego abrir en el navegador la dirección que indique la terminal
(`http://127.0.0.1:8050/` en local, o `http://IP_PUBLICA:8050` en la EC2).

## Fuente de datos

Datos Abiertos Colombia — SECOP II Contratos Electrónicos, subconjunto del Ministerio
de Hacienda y Crédito Público (4.695 registros), extraído con AWS Glue + Athena.
