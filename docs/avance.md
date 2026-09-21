# Registro de avance

Estado real del proyecto, para que todo el equipo sepa qué está hecho, qué falta y quién sigue. El orden de los commits de cada sprint está en [PLAN.md](../PLAN.md#plan-de-commits).

**Última actualización:** 2026-09-21

## Resumen

| Sprint | Estado | Rama |
|---|---|---|
| 0 · Base | ✅ Completado (2026-09-13) | `main` |
| 1 · Simplex normal | 🔄 En progreso: motor 9 de 33 pasos, frontend 0 de 15 | `develop` |
| 2 · Dos Fases | ⬜ Pendiente | — |
| 3 · Exportar e importar | ⬜ Pendiente | — |
| 4 · Entrega | ⬜ Pendiente | — |

**Pruebas:** backend 77 ✅ · frontend 6 ✅

**Siguiente paso:** `feat(simplex): construir tabla inicial con Cj, Cb y base`

---

## Sprint 0 · Base — ✅ Completado

- **Responsable:** Angel17jc
- **Fechas:** 2026-09-12 → 2026-09-13
- **Commits:** 62 (5 de repositorio + 56 del sprint + 1 corrección de CI), en `main`

Qué quedó listo:

- Backend FastAPI con todo el contrato de la API. Funcionan `/health` y `/ejemplos` (7 ejemplos, incluido el del profesor en Max y Min). `/resolver`, `/importar`, `/exportar/pdf` y `/problemas` responden 501 hasta su sprint.
- Base de datos opcional (PostgreSQL + SQLAlchemy + Alembic) con la migración inicial.
- Frontend React + Vite + Tailwind + shadcn/ui con las 4 páginas vacías, cliente de la API con tipos generados e indicador de conexión.
- `docker compose up` levanta todo; `docker-compose.prod.yml` sirve el frontend con Nginx.
- GitHub Actions: Backend, Frontend y Contrato de la API, en verde.
- Documentación: README, CONTRIBUTING, wireframes y guía de despliegue.

Diferencias con el plan: ver *Notas de la ejecución del Sprint 0* en [PLAN.md](../PLAN.md#plan-de-commits).

---

## Sprint 1 · Simplex normal — 🔄 En progreso

### Motor (`backend/app/simplex/`)

| # | Commit del plan | Estado | Responsable | Commit |
|---|---|---|---|---|
| 1 | `feat(simplex): agregar formateo de fracciones para mostrar` | ✅ | Yeiker-Lopez | `1fffca7` |
| — | `test(simplex): probar formateo de fracciones` *(extra)* | ✅ | Yeiker-Lopez | `b0eec67` |
| 2 | `feat(simplex): agregar modelo inmutable de tabla simplex` | ✅ | Yeiker-Lopez | `754430c` |
| 3 | `test(simplex): probar creación y copia de la tabla` | ✅ | Yeiker-Lopez | `c3e1cb8` |
| 4 | `feat(simplex): normalizar restricciones con lado derecho negativo` | ✅ | Yeiker-Lopez | `f26aac0` |
| 5 | `test(simplex): probar normalización de lado derecho negativo` | ✅ | Yeiker-Lopez | `9e3a9c7` |
| 6 | `feat(simplex): clasificar problema como simplex normal o extendido` | ✅ | Yeiker-Lopez | `6adf10c` |
| 7 | `test(simplex): probar clasificación del problema` | ✅ | Yeiker-Lopez | `97b3dc4` |
| 8 | `feat(simplex): construir forma extendida con holguras` | ✅ | Yeiker-Lopez | `ae6c25a` |
| 9 | `test(simplex): probar forma extendida con holguras` | ✅ | Yeiker-Lopez | `d9e1b63` |
| 10 | `feat(simplex): construir tabla inicial con Cj, Cb y base` | ⏳ Siguiente | — | — |
| 11 | `feat(simplex): calcular fila Z inicial como 0 − Z` | ⬜ | — | — |
| 12 | `test(simplex): probar tabla inicial y fila Z` | ⬜ | — | — |
| 13 | `feat(simplex): agregar prueba de optimalidad para maximizar y minimizar` | ⬜ | — | — |
| 14 | `test(simplex): probar prueba de optimalidad` | ⬜ | — | — |
| 15 | `feat(simplex): elegir variable que entra con desempate por posición` | ⬜ | — | — |
| 16 | `test(simplex): probar elección de variable que entra` | ⬜ | — | — |
| 17 | `feat(simplex): agregar prueba de razón mínima excluyendo ceros y negativos` | ⬜ | — | — |
| 18 | `test(simplex): probar prueba de razón mínima` | ⬜ | — | — |
| 19 | `feat(simplex): detectar problema no acotado` | ⬜ | — | — |
| 20 | `feat(simplex): agregar operación de fila pivote (1/pivote)·R` | ⬜ | — | — |
| 21 | `feat(simplex): agregar operación de fila (−v)·Rp' + Ri` | ⬜ | — | — |
| 22 | `feat(simplex): actualizar fila Z con operación de fila` | ⬜ | — | — |
| 23 | `test(simplex): probar operaciones de Gauss-Jordan` | ⬜ | — | — |
| 24 | `feat(simplex): agregar comprobación Zj − Cj con Cb` | ⬜ | — | — |
| 25 | `feat(simplex): registrar pasos de cada iteración` | ⬜ | — | — |
| 26 | `feat(simplex): iterar hasta el óptimo en simplex normal` | ⬜ | — | — |
| 27 | `feat(simplex): leer resultado desde la matriz identidad` | ⬜ | — | — |
| 28 | `feat(simplex): detectar óptimos múltiples` | ⬜ | — | — |
| 29 | `test(simplex): comparar casos 3, 5, 7 y 8 con SciPy` | ⬜ | — | — |
| 30 | `feat(explicador): agregar textos de los pasos del simplex normal` | ⬜ | — | — |
| 31 | `test(explicador): probar textos de los pasos` | ⬜ | — | — |
| 32 | `feat(api): conectar POST /resolver con el motor` | ⬜ | — | — |
| 33 | `test(api): resolver caso 3 de punta a punta` | ⬜ | — | — |

Qué hay en el código hasta ahora:

| Archivo | Qué hace |
|---|---|
| `fracciones.py` | Muestra fracciones como texto (`25/2`, `−3`), LaTeX y decimales (solo para ver) |
| `tabla.py` | Tabla simplex inmutable: Cj, Cb, base, b, matriz y fila Z; cada cambio devuelve una tabla nueva |
| `normalizacion.py` | Multiplica por −1 las restricciones con lado derecho negativo (≤ ↔ ≥) *(archivo nuevo, no estaba en el plan)* |
| `clasificacion.py` | Decide simplex normal o extendido (Dos Fases) y explica por qué |
| `forma_extendida.py` | Agrega las holguras S1, S2…; por ahora solo acepta restricciones ≤ (≥ y = llegan en el Sprint 2) |

### Frontend (`frontend/src/`)

Sin empezar: 0 de 15 commits. El primero es `feat(frontend): agregar componente CampoFraccion`.

### Pendiente del equipo

- [ ] Meter el ejemplo del profesor (Max y Min) en la calculadora de referencia y guardar sus tablas para las pruebas.
- [ ] Pedir a la facultad los datos del servidor (lista en [despliegue.md](despliegue.md#0-antes-de-empezar-datos-que-hay-que-pedir-a-la-facultad)).

---

## Historial

| Fecha | Quién | Qué |
|---|---|---|
| 2026-09-21 | Angel17jc | Revisó e integró el avance del motor de Yeiker-Lopez; creó este registro |
| 2026-09-15 | Yeiker-Lopez | Motor del Sprint 1: fracciones, tabla, normalización, clasificación y forma extendida (10 commits en `develop`) |
| 2026-09-13 | Angel17jc | Sprint 0 completado y subido a `main`; CI en verde |
| 2026-09-12 | Angel17jc | Plan del proyecto y plan de commits |

---

## Cómo actualizar este registro

Cada vez que subas commits a `develop` o `main`:

1. Marca con ✅ los pasos del plan que terminaste y pon tu usuario y el hash corto del commit (`git log --oneline`).
2. Actualiza el **Resumen**: estado del sprint, número de pruebas y **Siguiente paso**.
3. Agrega una línea al **Historial**.
4. Cambia la fecha de **Última actualización**.
5. Súbelo en su propio commit: `docs: actualizar registro de avance`.
