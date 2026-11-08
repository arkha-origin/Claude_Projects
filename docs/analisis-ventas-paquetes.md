# Análisis de ventas por paquete — Cosplay Inc

**Corte:** 8 de noviembre de 2026, base de producción.

**Cómo se obtuvo:** solo lectura, mediante una transacción `READ ONLY` con consultas `SELECT` agregadas. No se modificaron datos, no hubo migraciones ni despliegues. El documento no contiene datos personales.

**Cómo se lee:**
- Montos en COP, enteros.
- «Pagado» significa que la orden inicial del pedido está en estado `pagada`.
- **SOFA26-0046 queda fuera de todos los totales** y se reporta aparte (sección 9).
- El porcentaje de clientes se calcula sobre los 107 clientes de SOFA 2026 que pagaron.

## 1. Pedidos por evento

| Evento | Pedidos | Pagados | No pagados | Cancelados | Clientes que pagaron |
|---|---:|---:|---:|---:|---:|
| SOFA 2026 | 168 | 115 | 39 | 21 | 107 |
| Ibagué Ciudad Rock | 13 | 0 | 13 | 0 | 0 |

Ibagué no tiene ventas pagadas registradas: sus 13 registros son leads que pidieron sus fotos. Todo lo que sigue es de SOFA 2026.

## 2. Ingreso y métrica principal (SOFA 2026)

| Concepto | Valor |
|---|---:|
| Ingreso por compras iniciales | 11.852.000 |
| Ingreso por compras en la galería (postventa) | 797.000 |
| **Ingreso total** | **12.649.000** |
| Clientes con pago | 107 |
| **Ingreso promedio por cliente** | **118.215** |

## 3. Por producto y paquete (SOFA 2026)

El «precio de línea» es lo que pagó esa línea del pedido, ya con descuento.

| Producto | Fotos o videos | Pagados | No pagados | Precio de línea promedio | Mínimo–máximo | Ingreso de la línea | % de clientes |
|---|---:|---:|---:|---:|---|---:|---:|
| Fotoestudio | 1 | 40 | 8 | 35.158 | −40.000 – 47.333 ⚠️ | 1.406.331 | 36,4 % |
| Fotoestudio | 2 | 3 | 5 | 65.897 | 65.000 – 67.692 | 197.692 | 2,8 % |
| Fotoestudio | 3 | 27 | 3 | 106.627 | 94.470 – 110.000 | 2.878.940 | 22,4 % |
| Fotoestudio | 4 | 1 | 0 | 136.000 | — | 136.000 | 0,9 % |
| Fotoestudio | 5 | 8 | 1 | 175.000 | 160.000 – 180.000 | 1.400.000 | 7,5 % |
| Fotoestudio | 6 | 0 | 1 | — | — | — | 0 % |
| Foto Pasarela | 1 | 7 | 0 | 35.000 | — | 245.000 | 6,5 % |
| Foto Pasarela | 2 | 1 | 0 | 70.000 | — | 70.000 | 0,9 % |
| Foto Pasarela | 5 | 1 | 0 | 155.000 | — | 155.000 | 0,9 % |
| Foto FX | 1 | 9 | 1 | 60.000 | — | 540.000 | 7,5 % |
| Foto FX | 2 | 2 | 0 | 120.000 | — | 240.000 | 1,9 % |
| Foto Inmersiva | 1 | 3 | 0 | 120.000 | — | 360.000 | 2,8 % |
| Dúo (foto) | 1 | 3 | 3 | 37.778 | 33.333 – 40.000 | 113.333 | 2,8 % |
| Dúo (foto) | 3 | 1 | 1 | 110.000 | — | 110.000 | 0,9 % |
| Dúo (foto) | 5 | 1 | 0 | 160.000 | — | 160.000 | 0,9 % |
| Video Pasarela | 1 | 14 | 0 | 72.143 | 70.000 – 100.000 | 1.010.000 | 13,1 % |
| Aura (cámara lenta) | 1 | 14 | 1 | 35.573 | 32.667 – 42.511 | 498.023 | 13,1 % |
| Órbita (360°) | 1 | 3 | 0 | 69.346 | 68.019 – 72.000 | 208.038 | 2,8 % |
| Video IA Inmersivo | 1 | 3 | 0 | 140.000 | — | 420.000 | 2,8 % |
| Entrega Rápida | 3 | 1 | 0 | 120.000 | — | 120.000 | 0,9 % |
| Entrega Rápida | 1 | 0 | 0 | — | — | — | 0 % |

**Combos (paquetes armados):** Esencia, 3 pagados; Protagonista, 2 pagados; ninguno sin pagar.

**Notas sobre esta tabla:**
- Las líneas suman 10.268.357, menos que los 11.852.000 de las órdenes iniciales. La diferencia (1.583.643) son conceptos que no están en las líneas de producto: recargo de grupo, acabados y ajustes de combo.
- ⚠️ Una línea de Fotoestudio ×1 tiene un precio de −40.000: su descuento supera al precio. Es un dato anómalo de un pedido y conviene revisarlo.

## 4. Compras después de ver las miniaturas (SOFA 2026)

| Concepto | Valor |
|---|---:|
| Clientes que compraron algo más en su galería (postventa pagada) | **7** |
| Gasto total | 797.000 |
| Gasto promedio | 113.857 |
| Mínimo / máximo | 40.000 / 300.000 |
| Órdenes postventa pagadas | 11 |
| Fotos o videos extra comprados | 18 (692.000), ninguno de ellos video |
| Mejoras de acabado compradas | 0 |

Hay 105.000 del ingreso postventa que no se explican por piezas ni por mejoras de acabado. Probablemente son productos agregados al pedido después de la sesión, que no están desglosados en esta consulta.

## 5. Vieron sus miniaturas y no compraron nada más (SOFA 2026)

Criterio: galería abierta por el cliente y ninguna orden postventa pagada.

| Concepto | Pedidos |
|---|---:|
| Galerías abiertas por el cliente | 112 |
| **Sin ninguna compra postventa pagada** | **101** (90 %) |
| De esas, sin ningún pago (ni el inicial) | 27 |

## 6. Rangos alcanzados (membresías), pedidos pagados de SOFA 2026

| Rango | Código en la base | Pedidos | Gasto promedio |
|---|---|---:|---:|
| (sin rango) | — | 9 | 117.444 |
| PASS | `invitado` | 90 | 84.744 |
| ELITE | `protagonista` | 12 | 177.083 |
| MASTER | `icono` | 3 | 326.667 |
| LEGENDARIO | `inmortal` | 1 | 520.000 |

Los rangos se alcanzan por gasto; no se venden como producto.

## 7. Por modalidad y por fecha (SOFA 2026)

| Modalidad | Pagados | No pagados | Ingreso inicial |
|---|---:|---:|---:|
| Preventa | 21 | 12 | 3.862.000 |
| Durante el evento | 94 | 27 | 7.990.000 |

| Día de la sesión | Pagados | No pagados | Ingreso inicial |
|---|---:|---:|---:|
| 2026-10-08 | 7 | 0 | 970.000 |
| 2026-10-09 | 18 | 2 | 2.072.000 |
| 2026-10-10 | 24 | 6 | 2.515.000 |
| 2026-10-11 | 41 | 7 | 4.185.000 |
| 2026-10-12 | 25 | 6 | 2.110.000 |
| Después del evento (18 oct – 4 nov, 12 días) | 0 | 18 | 0 |

| Mes del pago (hora Bogotá) | Órdenes iniciales | Ingreso inicial | Órdenes postventa | Ingreso postventa |
|---|---:|---:|---:|---:|
| 2026-09 | 3 | 435.000 | 0 | 0 |
| 2026-10 | 111 | 11.137.000 | 11 | 797.000 |
| 2026-11 | 1 | 280.000 | 0 | 0 |

## 8. Datos que no existen en la base

- **Cosplay Crew:** no hay ningún grupo registrado (ni crew de foto ni de video). Los dúos se vendieron como el producto «Dúo», no como grupo.
- **Venta de membresías:** no existe. Los rangos PASS, ELITE, MASTER y LEGENDARIO se alcanzan por gasto (sección 6).
- **«Vio sus miniaturas»** se mide por la primera vez que abrió su galería. No hay un registro de qué miniaturas miró ni por cuánto tiempo.

## 9. Aparte: SOFA26-0046 (fuera de los totales)

| Orden | Estado | Total |
|---|---|---:|
| Inicial | Pagada | 50.000 |
| Postventa | Pagada (confirmada a mano por el equipo, sin comprobante; la clienta dice que no pagó) | 80.000 |
