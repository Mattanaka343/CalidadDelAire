## Dataset Final — Documentación

**Dimensiones:** 35 columnas × N filas (una por minuto de medición continua, excluidos gaps largos)

**Índice:** `datetime` — timestamp regularizado a frecuencia de 1 minuto

### Variables originales (6 columnas)

Concentraciones de contaminantes medidas por el sensor, resampleadas a 1 minuto mediante promedio.

| Columna | Unidad | Descripción |
|---|---|---|
| `PM2_5_ugm3` | µg/m³ | Concentración de partículas finas (diámetro ≤ 2.5 µm) |
| `PM10_ugm3` | µg/m³ | Concentración de partículas gruesas (diámetro ≤ 10 µm) |
| `O3_ppm` | ppm | Concentración de ozono troposférico |
| `NO2_ppm` | ppm | Concentración de dióxido de nitrógeno |
| `SO2_ppm` | ppm | Concentración de dióxido de azufre |
| `CO_ppm` | ppm | Concentración de monóxido de carbono |

### Variable de segmentación (1 columna)

| Columna | Descripción |
|---|---|
| `segment` | Identificador entero del segmento continuo al que pertenece la observación. Se incrementa cada vez que se detectó un gap largo (> 5 min) en la serie original. Observaciones del mismo segmento son temporalmente contiguas. |

### Features temporales cíclicas (4 columnas)

Codificación seno/coseno para preservar la naturaleza cíclica del tiempo. Rango: [-1, 1].

| Columna | Descripción |
|---|---|
| `hour_sin` | Componente seno de la hora del día (ciclo de 24h) |
| `hour_cos` | Componente coseno de la hora del día (ciclo de 24h) |
| `dow_sin` | Componente seno del día de la semana (ciclo de 7 días) |
| `dow_cos` | Componente coseno del día de la semana (ciclo de 7 días) |

### Lag features y estadísticos rodantes (24 columnas)

Para cada contaminante se generaron 4 features que capturan su comportamiento reciente. El sufijo indica el tipo de feature.

| Sufijo | Descripción |
|---|---|
| `_lag1` | Valor del contaminante 1 minuto antes |
| `_lag5` | Valor del contaminante 5 minutos antes |
| `_roll_mean_10` | Promedio móvil de los últimos 10 minutos |
| `_roll_std_10` | Desviación estándar móvil de los últimos 10 minutos (proxy de volatilidad) |

Estas features se generaron para: `PM2_5_ugm3`, `PM10_ugm3`, `O3_ppm`, `NO2_ppm`, `SO2_ppm`, `CO_ppm`.

::: {.callout-note}
## Notas importantes

- Las primeras 10 filas de cada segmento contienen `NaN` en las columnas de lags y rolling — deben eliminarse antes de entrenar.
- El dataset **no está escalado ni transformado logarítmicamente** — esas transformaciones se aplican después del split temporal y no se persisten en este archivo.
- El dataset **no incluye el target** — las ventanas de predicción (sliding window) se construyen dinámicamente durante el entrenamiento.
:::