# Simplex Paso a Paso — Plan del proyecto

Calculadora web del **método simplex extendido** (Dos Fases) para **Maximizar y Minimizar**. Las calculadoras que hay en internet solo dan el resultado, o muestran las tablas sin decir de dónde sale cada número. Esta muestra **cada operación interna**, una por una, como un depurador que avanza instrucción por instrucción.

- **Referencia de entrada de datos:** <https://www.plandemejora.com/calculadora-metodo-simplex-online/>
- **Stack:** React + TypeScript (front) · Python + FastAPI (back) · PostgreSQL + SQLAlchemy (BD)
- **Versión del plan:** 1.5 — 2026-09-12 (incluye la reunión grabada con el profesor, las capturas de la página de referencia y las decisiones sobre las preguntas pendientes)

---

## Contenido

1. [Lo que pidió el profesor](#1-lo-que-pidió-el-profesor)
2. [Decisiones](#2-decisiones)
3. [Simplex normal, simplex extendido y Dos Fases](#3-simplex-normal-simplex-extendido-y-dos-fases)
4. [Formato de la tabla y reglas](#4-formato-de-la-tabla-y-reglas)
5. [Alcance](#5-alcance)
6. [Tecnologías](#6-tecnologías)
7. [Arquitectura](#7-arquitectura)
8. [Algoritmo del motor](#8-algoritmo-del-motor)
9. [El paso a paso](#9-el-paso-a-paso)
10. [Ejemplo del profesor resuelto](#10-ejemplo-del-profesor-resuelto)
11. [API](#11-api)
12. [Base de datos](#12-base-de-datos)
13. [Exportar e importar](#13-exportar-e-importar)
14. [Interfaz (IU / UX)](#14-interfaz-iu--ux)
15. [Estructura de carpetas](#15-estructura-de-carpetas)
16. [Pruebas](#16-pruebas)
17. [Despliegue en el hosting de la facultad](#17-despliegue-en-el-hosting-de-la-facultad)
18. [Sprints](#18-sprints)
19. [Decisiones sobre las preguntas pendientes](#19-decisiones-sobre-las-preguntas-pendientes)
20. [Posibles módulos futuros](#20-posibles-módulos-futuros)
21. [Fuentes](#21-fuentes)

---

## 1. Lo que pidió el profesor

Resumen de la reunión grabada. Entre corchetes, el minuto aproximado del audio.

### Lo que falta en las calculadoras actuales (el objetivo del proyecto)

La calculadora de referencia muestra las tablas y dice qué variable entra y cuál sale, pero **no muestra las operaciones internas** [03:36–05:05, 13:36–13:59]. Hay que mostrar:

1. **La fila Z inicial:** en maximización, la primera operación es `0 − Z`, que equivale a **multiplicar la fila por −1** [04:20–04:42].
2. **Por qué entra esa variable:** se toma el **menor negativo**, “el que está más alejado del cero”. Ej.: entre −15 y −28, entra −28 [04:42–04:55].
3. **La prueba de razón:** dividir cada `b` (lado derecho: B1, B2, B3…) entre el valor de la columna que entra; **los ceros no se consideran porque da infinito**; se toma el **menor** resultado [05:19–06:50].
4. **El valor Cb de la variable que entra:** si entra x2, en esa fila aparece su coeficiente de la función objetivo (ej. 15). La referencia no lo muestra [09:52–10:18].
5. **Gauss-Jordan paso por paso** [11:56–16:47]:
   - Si el pivote no es 1, **se multiplica la fila por el inverso del pivote** (ej. por 1/8). Es lo **primero** que se llena en la nueva tabla.
   - Los demás valores de la columna se hacen 0 con: **(opuesto del valor) × fila pivote + fila original**. Ej.: `R1' = −20·R3' + R1`.
   - También la fila Z (ej. el 28 se hace 0).
6. **Cuándo termina** [17:06–17:52, 22:04]: en **maximización** cuando la fila Z es toda **cero o positiva**; en **minimización** cuando es toda **cero o negativa**.
7. **El paso de Fase 1 a Fase 2** y qué valores se toman [18:02–19:31].
8. **Cómo leer el resultado** [22:14–23:00]: cada variable toma el valor del lado derecho de la fila donde tiene el 1 de la matriz identidad; **las artificiales no se consideran** en la respuesta.

### Cómo quiere verlo

- **Como un depurador:** “como un puntero que va pasando de una instrucción a otra… un *step* de cada operación” [08:43–09:09, 15:21–15:31, 24:24–24:37]. Cada operación se muestra y se pasa a la siguiente.
- **La tabla fija y las operaciones al lado o en cascada hacia abajo** [14:50–15:14, 05:12].
- **Iteraciones plegables:** si estás en la iteración 5, las anteriores se minimizan porque ocupan espacio (como el proyecto de transporte de compañeros anteriores) [36:18–37:16].
- **Exportar a JSON y a PDF, e importar el JSON** [37:37–42:00]. Así los estudiantes practican y llevan el desarrollo impreso si están en desacuerdo con una calificación.

### Datos del problema

- Se ingresa primero **cantidad de variables y de restricciones**, luego *Generar modelo*, luego **Maximizar o Minimizar** [00:29–00:48, 45:30–45:44].
- Coeficientes de la función objetivo (ej. 10 y 15) y restricciones con **≤, ≥ o =**, “los tres únicos tipos” [01:01–01:40].
- **Un coeficiente puede quedar en blanco** cuando la variable no está en esa restricción: vale 0 [01:46–02:18].
- **Tamaño:** en clase 2–3 variables; “máximo tal vez cinco… y cinco ya es bastante”. Lo importante es que **no se cuelgue** [00:00–00:23, 44:41–44:55].

### Sobre el algoritmo

- **Nombres:** holgura **S** (o H); en ≥ “la misma S pero se llama de exceso” más una artificial **A**; en = solo **A** [29:17–30:03, 40:58–41:24].
- **Filas movidas:** la referencia cambia de posición la fila de la variable que entra; es válido, pero confunde [10:36–11:30].
- **Empates:** el algoritmo elige siempre por **posición en la matriz** (de arriba hacia abajo); a mano el estudiante puede elegir cualquiera [33:57–34:32].
- **Simplex normal vs. extendido:** ver [sección 3](#3-simplex-normal-simplex-extendido-y-dos-fases) [40:22–41:00].

### Otros puntos

- Quiere proponer subirlo al **hosting de la facultad**, cargando por partes front, back y base de datos [42:30–44:01].
- Menciona posibles proyectos futuros: **ruta más corta / redes de nodos**, y **transporte** (ya hecho por otros estudiantes) [30:47–33:21].
- El **método gráfico no hace falta**: ya hay páginas que lo hacen [42:04–42:16].

---

## 2. Decisiones

| Tema | Decisión | Origen |
|---|---|---|
| Simplex extendido | Modelo en forma extendida + **Dos Fases** | Profesor + equipo |
| Gran M | No se implementa (el profesor acepta Dos Fases **o** Gran M) | Equipo |
| Cuentas de usuario | **No** | Equipo |
| Formato de la tabla | Filas **Cj, Cb, Zj, Zj − Cj**. Equivale a “multiplicar Z por −1” que explica el profesor | Profesor |
| Fase 1 | Se muestra como **Max W = −ΣA**, así la fila tiene negativos y entra el **menor negativo**, igual que en la referencia (−15, −28). Equivale a Min W = ΣA | Profesor + referencia + documentación |
| Minimizar con solo ≤ | **No se ejecuta Fase 1** (no hay artificiales); se explica por qué y se resuelve con simplex directo | Documentación |
| Minimización (Fase 2) | Directa: entra el **mayor positivo**; termina cuando todo es **cero o negativo** | Profesor |
| Operaciones de fila | Notación Gauss-Jordan del profesor: `R3' = (1/8)·R3`, `R1' = −20·R3' + R1` | Profesor |
| Fila Z | Se actualiza **también con una operación de fila** (`Z' = 28·R3' + Z`); el cálculo `Zj − Cj` se muestra como comprobación | Profesor |
| Orden de filas | La variable que entra **ocupa la fila de la que sale**; las filas no se reordenan | Profesor (evitar confusión) |
| Empates | Entra la **primera columna** de izquierda a derecha; sale la **primera fila** de arriba hacia abajo; se avisa del empate y de las alternativas. El estudiante no elige (v1). Si se detecta un ciclo, se cambia a la regla de Bland | Profesor + documentación |
| Nombres de variables | `S1, S2…` para holgura y exceso (el exceso con signo −), `A1, A2…` para artificiales, numeradas en orden de aparición | Profesor + referencia |
| Coeficiente en blanco | Vale 0 | Profesor |
| Números | Cálculo **siempre con fracciones exactas**; se muestran fracciones (`25/2`) y un botón *Ver decimales* cambia solo la vista | Documentación + profesor |
| Tamaño | Hasta 20 variables y 50 restricciones como la referencia; interfaz pensada para **2–5 variables** | Profesor + referencia |
| Max y Min | Todo el sistema (motor, paso a paso, PDF, pruebas) debe funcionar **igual de completo para Maximizar y Minimizar** | Equipo |
| Pantalla de entrada | Misma distribución que la página de referencia (sección 14) | Profesor + capturas |
| Exportar / importar | **JSON** (exportar e importar) y **PDF** (exportar) | Profesor |
| Contenido del PDF | **Todo el desarrollo del ejemplo**: cada tabla y cada operación, igual que en pantalla (sección 13) | Equipo |
| Hosting | **Servidor de la facultad**, desplegado con **Docker Compose** (alternativa sin Docker documentada) | Profesor + equipo |
| Base de datos | **No obligatoria.** PostgreSQL se activa con `DATABASE_URL`; sin ella todo funciona menos los enlaces compartidos | Equipo |

---

## 3. Simplex normal, simplex extendido y Dos Fases

### Cómo lo explica el profesor [40:22–41:00]

| Caso | Nombre en clase | Método |
|---|---|---|
| Maximizar, solo ≤ | **Simplex normal** | Solo holguras; 3 o 4 tablas |
| Maximizar, alguna ≥ o = | **Simplex extendido** | Dos Fases |
| Minimizar | **Simplex extendido** (“de ley es dos fases”) | Dos Fases |

### Qué hace el algoritmo

Técnicamente, la **Fase 1 solo existe si hay variables artificiales**, es decir, restricciones ≥ o =. El profesor también lo dice: “la fase 2 se implica cuando hay restricciones de igualdad o de mayor o igual” [18:08–18:26].

En clase los problemas de minimizar casi siempre tienen restricciones ≥, por eso se dice que minimizar es “de ley” Dos Fases.

**Cómo lo resolvemos** (según la documentación del método, ver [sección 19](#19-decisiones-sobre-las-preguntas-pendientes)):

| Caso | Etiqueta en pantalla | Qué se ejecuta |
|---|---|---|
| Max o Min con alguna ≥ o = | **Simplex extendido — Dos Fases** | Fase 1 + Fase 2 |
| Max con solo ≤ | **Simplex normal** | Simplex directo |
| Min con solo ≤ | **Simplex normal (minimización sin variables artificiales)** | Simplex directo, con el aviso: *“Todas las restricciones son ≤ y los lados derechos son ≥ 0. Las holguras ya forman la base inicial, así que no se necesitan variables artificiales ni Fase 1.”* |
- Si un lado derecho es negativo, se multiplica la fila por −1 y cambia el signo (≤ ↔ ≥). Esa restricción puede pasar a necesitar Dos Fases.

> **Nota:** en el audio el profesor dice “el método de dos fases es el método de la Big M”. Son **dos métodos distintos** para lo mismo (manejar artificiales). Gran M usa una penalización M en la función objetivo en una sola fase. Nosotros implementamos **Dos Fases**.

### Forma extendida

| Restricción | Se transforma en | Variables |
|---|---|---|
| `a·x ≤ b` | `a·x + S = b` | Holgura S |
| `a·x ≥ b` | `a·x − S + A = b` | Exceso S y artificial A |
| `a·x = b` | `a·x + A = b` | Artificial A |

### Fase 1

- **Objetivo:** `Max W = −A1 − A2 − …` (equivale a minimizar la suma de artificiales). Cj = −1 en las artificiales y 0 en las demás.
- **Fila W inicial**, en dos operaciones visibles:
  1. `0 − W`: se escriben los coeficientes multiplicados por −1.
  2. Para que las artificiales básicas tengan 0 en la fila W, se suman las filas de sus restricciones multiplicadas por −1.
- Se itera con la regla de **maximizar**.
- **Al terminar:**
  - `W < 0` (quedan artificiales con valor) → **infactible**.
  - `W = 0` → factible, se pasa a la Fase 2.
  - Si una artificial sigue en la base con valor 0: si en su fila hay un valor distinto de 0 en una columna no artificial, se hace un pivote para sacarla; si no, la restricción es **redundante** y se elimina.

### Fase 2

1. Se eliminan las columnas artificiales.
2. Se ponen los **Cj originales** (ej. 10 y 15) y se actualiza Cb.
3. Se rehace la fila Z: `0 − Z`, y se hacen 0 las columnas de las variables básicas con operaciones de fila.
4. Se itera con la regla del objetivo (Max o Min).

---

## 4. Formato de la tabla y reglas

|  |  | **Cj →** | 10 | 15 | 0 | 0 | −1 | −1 |
|---|---|---|---|---|---|---|---|---|
| **Cb** | **Base** | **LD (b)** | **x1** | **x2** | **S1** | **S2** | **A1** | **A2** |
| … | … | … | … | … | … | … | … | … |
|  | **Zj − Cj** | Z | … | … | … | … | … | … |

- **Cj:** coeficiente de cada variable en la función objetivo de la fase actual.
- **Cb:** Cj de la variable básica de esa fila.
- **Zj − Cj** (la “fila Z” del profesor) se obtiene con operaciones de fila; se comprueba con `Σ(Cb × columna) − Cj`.

| | Maximizar (y Fase 1) | Minimizar |
|---|---|---|
| **¿Terminó?** | Toda la fila `Zj − Cj` es **≥ 0** | Toda la fila `Zj − Cj` es **≤ 0** |
| **Entra** | El **menor negativo** (más alejado de 0) | El **mayor positivo** |
| **Sale** | Menor `b ÷ valor de la columna`, solo con valores **> 0** | Igual |
| **No acotado** | La columna que entra no tiene valores > 0 | Igual |
| **Óptimos múltiples** | En la tabla final, una variable **no básica** tiene 0 en la fila Z | Igual |
| **Empates** | Primera columna (izquierda) / primera fila (arriba) | Igual |

---

## 5. Alcance

**Entrada (igual que la referencia)**

- **Paso 1:** cantidad de variables y de restricciones; *Generar modelo* y *Limpiar*.
- **Paso 2:** *Maximizar* o *Minimizar*.
- **Paso 3:** coeficientes de `X1 + X2 + … + Xn` y de cada restricción, con signo `≤ ≥ =` y lado derecho. Acepta blanco (= 0), negativos, decimales y fracciones (`3/4`).
- *Resolver*.

**Lo que agregamos**

- Forma extendida explicada restricción por restricción.
- Si es simplex normal o extendido, y por qué.
- **Modo paso a paso** que avanza **operación por operación** (sección 9).
- Fase 1 y Fase 2 completas, con el cálculo de la fila Z, la prueba de razón, el pivote y cada operación Gauss-Jordan.
- Lectura del resultado desde la matriz identidad.
- Casos especiales explicados: infactible, no acotado, óptimos múltiples, empates, restricción redundante.
- **Exportar JSON**, **importar JSON**, **exportar PDF**.
- Ejemplos precargados, enlace para compartir e historial en el navegador.

**Fuera de alcance (v1):** cuentas de usuario, Gran M, método gráfico, análisis de sensibilidad, dual, ruta más corta, transporte.

---

## 6. Tecnologías

### Frontend (IU / UX)

| Uso | Tecnología | Por qué |
|---|---|---|
| Lenguaje | **TypeScript** | Tipos compartidos con la API. |
| Framework | **React 19 + Vite** | El más usado; genera archivos estáticos fáciles de subir al hosting. |
| Estilos y componentes | **Tailwind CSS + shadcn/ui** | Acordeones (iteraciones plegables), tabs, diálogos accesibles. |
| Formularios | **React Hook Form + Zod** | Cuadrícula dinámica n × m con validación en vivo. |
| Llamadas a la API | **TanStack Query** | Carga, errores y caché. |
| Estado | **Zustand** | Pasos 1–3 y posición del “puntero” del paso a paso. |
| Rutas | **React Router** | `/calculadora`, `/solucion/:slug`, `/historial`, `/ejemplos`. |
| Fórmulas | **KaTeX** | Fracciones y operaciones como en el cuaderno. |
| Animación del paso a paso | **Motion** (Framer Motion) | Resaltar la celda/fila que cambia en cada operación. |
| Tipos de la API | **openapi-typescript** | Tipos generados desde FastAPI. |
| Pruebas | **Vitest + Testing Library + Playwright** | Componentes y flujo completo. |

### Backend (lógica)

| Uso | Tecnología | Por qué |
|---|---|---|
| Lenguaje | **Python 3.11+** (imagen Docker `python:3.12-slim`) | `fractions.Fraction`: resultados exactos como a mano. FastAPI, SQLAlchemy y ReportLab funcionan con 3.11, que es la versión instalada en el equipo. |
| Framework | **FastAPI + Uvicorn** | API REST con documentación Swagger en `/docs`. |
| Validación | **Pydantic v2** | Límites, blancos = 0, `"3/4"` → fracción; valida el JSON importado. |
| Motor simplex | **Propio, Python puro** | Tiene que registrar cada operación; ninguna librería lo hace. |
| PDF | **ReportLab** | Genera el PDF del desarrollo en el servidor; es Python puro, sin dependencias del sistema. |
| Pruebas | **pytest + SciPy** | `linprog` solo en tests, para confirmar el óptimo. |
| Calidad | **Ruff + mypy** | Formato, lint y tipos. |

### Base de datos

| Uso | Tecnología | Por qué |
|---|---|---|
| Motor | **PostgreSQL 16+** | Relacional, gratuito, `JSONB` para las tablas. |
| ORM | **SQLAlchemy 2.0** | ORM estándar de Python. |
| Migraciones | **Alembic** | Versiona el esquema. |
| Driver | **psycopg 3** | Conexión Python ↔ PostgreSQL. |

> La BD **no es obligatoria**. Resolver, paso a paso, exportar/importar JSON, PDF, historial local y ejemplos (archivos JSON en `backend/app/ejemplos/`) funcionan sin ella. Si se define `DATABASE_URL`, se activan los enlaces compartidos (ver secciones 17 y 19).

### Infraestructura

| Uso | Tecnología |
|---|---|
| Entorno local | **Docker Compose** (web + api + db) |
| Repositorio y CI | **GitHub + GitHub Actions** |
| Producción | **Hosting de la facultad** (ver sección 17) |

### Entorno de desarrollo (verificado en el equipo, 2026-09-12)

| Herramienta | Versión instalada | Para qué | Estado |
|---|---|---|---|
| Docker | 29.1.3 (motor Linux) | Levantar web + api + db | ✅ |
| Docker Compose | v5.0.1 | `docker compose up` | ✅ |
| Python | 3.11.9 | Backend y pruebas fuera de Docker | ✅ (el plan pide 3.11+) |
| Node.js | 24.13.0 | Frontend con Vite | ✅ |
| npm | 11.6.2 | Paquetes del frontend | ✅ |
| Git | 2.52.0 | Control de versiones | ✅ |

Cada integrante puede trabajar de dos formas:
- **Todo en Docker:** `docker compose up`. No hace falta instalar nada más.
- **Local:** el backend con Python 3.11+ en un entorno virtual (`python -m venv .venv`) y el frontend con `npm run dev`, para recargas más rápidas. PostgreSQL puede ir en Docker o no usarse (es opcional).

> **Alternativa si el equipo solo sabe JavaScript:** NestJS + TypeScript, Prisma, fraction.js, pdfmake. Misma arquitectura.

---

## 7. Arquitectura

```
┌──────────────────────┐   REST / JSON   ┌───────────────────────────────────────┐   SQLAlchemy   ┌──────────────┐
│  NAVEGADOR           │ ◄─────────────► │  API  (FastAPI)                       │ ◄────────────► │  PostgreSQL  │
│  React + TypeScript  │                 │                                       │                │              │
│                      │                 │  api/           rutas + Pydantic      │                │  problemas   │
│  · Asistente 3 pasos │                 │  services/      orquesta              │                │  restriccion │
│  · Paso a paso       │                 │  simplex/       MOTOR PURO ──┐        │                │  soluciones  │
│  · Exportar/Importar │                 │  explicador     pasos→texto ─┘        │                │              │
│  · Historial (local) │                 │  exportacion/   JSON y PDF            │                │              │
│  · Ejemplos          │                 │  repositories/  acceso a datos        │                │              │
└──────────────────────┘                 └───────────────────────────────────────┘                └──────────────┘
```

**Reglas de diseño**

1. **El motor es código puro:** recibe el problema y devuelve la lista completa de **operaciones atómicas**, sin HTTP ni BD.
2. **Cada operación atómica es un paso** del “puntero” (sección 9). El front solo avanza por esa lista; **no calcula nada**.
3. **Cada paso guarda cómo queda la tabla después de aplicarlo**, así el front puede saltar a cualquier paso sin recalcular.
4. El **explicador** convierte cada paso en texto en español y LaTeX.

---

## 8. Algoritmo del motor

1. **Validar y convertir:** blancos → 0; `"3/4"`, `"-2"`, `"0.5"` → `Fraction`. Error con el campo exacto si algo no es válido.
2. **Normalizar:** si `b < 0`, multiplicar la fila por −1 e invertir el signo.
3. **Clasificar:** simplex normal o extendido (sección 3).
4. **Forma extendida:** agregar S y A y nombrarlas en orden.
5. **Fase 1** (si hay A):
   1. Tabla inicial con `Max W = −ΣA`.
   2. Fila W: `0 − W` (× −1) y operaciones para dejar en 0 las columnas de las A básicas.
   3. Iterar (paso 7).
   4. Evaluar W: infactible, factible, o artificial básica en 0 (sacarla o eliminar la fila).
   5. Eliminar columnas A.
6. **Fase 2:**
   1. Poner los Cj originales y actualizar Cb.
   2. Fila Z: `0 − Z` y operaciones para dejar en 0 las columnas básicas.
   3. Iterar (paso 7).
7. **Iteración:**
   1. ¿Terminó? (regla de Max o Min).
   2. Variable que entra (menor negativo / mayor positivo; empate → primera columna).
   3. Prueba de razón fila por fila (`b ÷ valor`; se excluyen 0 y negativos). Si ninguna fila participa → **no acotado**.
   4. Variable que sale (menor razón; empate → primera fila) y pivote.
   5. `Rp' = (1/pivote) · Rp`: la fila pivote queda con 1 en el pivote; Cb toma el Cj de la variable que entra.
   6. Para cada otra fila con valor `v ≠ 0` en la columna pivote: `Ri' = (−v) · Rp' + Ri`. Las filas con `v = 0` no cambian (se dice).
   7. Fila Z: `Z' = (−v) · Rp' + Z`.
   8. Comprobación: `Zj − Cj = Σ(Cb × columna) − Cj`.
   9. Si una base se repite (ciclo por degeneración), desde ese punto se usa la **regla de Bland** (menor índice) y se explica. Límite de seguridad: 500 iteraciones.
8. **Resultado:** cada variable básica toma el `b` de su fila (el 1 de la matriz identidad); las no básicas valen 0; **las artificiales no se reportan**. Z final y estado: `optimo`, `multiples_optimos`, `no_acotado` o `infactible`.

---

## 9. El paso a paso

### Modo depurador

La solución es una lista ordenada de pasos. La interfaz tiene un **puntero** y controles:

| Control | Acción |
|---|---|
| ⏮ Inicio | Primer paso (modelo original) |
| ◀ Anterior | Paso anterior |
| ▶ Siguiente | Siguiente operación |
| ⏭ Siguiente iteración | Salta al inicio de la próxima iteración |
| ⏵ Reproducir | Avanza solo cada N segundos (velocidad ajustable) |
| Ver todo | Muestra la solución completa sin pasos |

Teclado: `→` siguiente, `←` anterior.

Diseño en pantalla:

- **Tabla fija** arriba o a la izquierda; la celda, fila o columna que cambia se resalta en ese paso.
- **Panel de operación** al lado o debajo, con la fórmula y el cálculo.
- **Registro en cascada** hacia abajo con las operaciones ya hechas de esa iteración.
- **Iteraciones anteriores plegadas**; solo la iteración actual está abierta.

### Lista de pasos (tipos)

| Tipo | Qué se muestra |
|---|---|
| `modelo_original` | Función objetivo y restricciones como las escribió el usuario. |
| `clasificacion` | “Simplex normal / extendido” y por qué. |
| `forma_extendida` | Una por restricción: “R2 es ≥: se resta S2 y se suma A1”. |
| `tabla_inicial` | Tabla con Cj, Cb, Base, b. |
| `fila_z_inicial` | `0 − Z`: coeficientes multiplicados por −1. |
| `anular_basica_en_z` | Operación de fila para dejar 0 en la fila Z bajo una variable básica. |
| `prueba_optimalidad` | Recorre la fila Z y concluye si continúa o termina. |
| `variable_entra` | “Entra x2: −28 es el menor negativo (el más alejado de 0)”, con aviso si hubo empate. |
| `prueba_razon` | Una línea por fila: `500 ÷ 20 = 25`, `400 ÷ 0 → no se considera (infinito)`, `100 ÷ 8 = 25/2 ← menor`. |
| `variable_sale` | “Sale A2; pivote = 8”. |
| `fila_pivote` | `R3' = (1/8)·R3`, valor por valor; Cb pasa a ser el Cj de la variable que entra. |
| `operacion_fila` | `R2' = −20·R3' + R2`, valor por valor, antes y después. |
| `fila_sin_cambio` | “R1 no cambia: su valor en la columna x2 es 0”. |
| `operacion_fila_z` | `Z' = 28·R3' + Z`, valor por valor. |
| `comprobacion_zj` | `Zj − Cj` calculado con Cb (opcional, plegado). |
| `solucion_actual` | Valores básicos y Z (o W) al final de la iteración. |
| `fin_fase_1` | Valor de W, conclusión y columnas que se eliminan. |
| `inicio_fase_2` | Cj originales, nuevo Cb y nueva fila Z. |
| `lectura_resultado` | Lectura desde la matriz identidad; artificiales excluidas. |
| `caso_especial` | Infactible, no acotado, óptimos múltiples, redundancia. |

---

## 10. Ejemplo del profesor resuelto

Datos dictados en el audio [01:01–02:58]:

```
Max Z = 10x1 + 15x2
s.a.  x1            ≤ 400
      15x1 + 20x2   ≥ 500
             8x2    = 100        x1, x2 ≥ 0
```

**Forma extendida:** `x1 + S1 = 400` · `15x1 + 20x2 − S2 + A1 = 500` · `8x2 + A2 = 100`

**Fase 1:** `Max W = −A1 − A2`

### Tabla inicial de Fase 1 (después de preparar la fila W)

|  |  | **Cj →** | 0 | 0 | 0 | 0 | −1 | −1 |
|---|---|---|---|---|---|---|---|---|
| **Cb** | **Base** | **b** | **x1** | **x2** | **S1** | **S2** | **A1** | **A2** |
| 0 | S1 | 400 | 1 | 0 | 1 | 0 | 0 | 0 |
| −1 | A1 | 500 | 15 | 20 | 0 | −1 | 1 | 0 |
| −1 | A2 | 100 | 0 | **8** | 0 | 0 | 0 | 1 |
|  | **W** | −600 | −15 | **−28** | 0 | 1 | 0 | 0 |

Cómo se llegó a la fila W:
- `0 − W` → `[0, 0, 0, 0, 1, 1 | 0]`.
- `W' = −1·R2 + W` → `[−15, −20, 0, 1, 0, 1 | −500]`.
- `W'' = −1·R3 + W'` → `[−15, −28, 0, 1, 0, 0 | −600]`.

### Iteración 1 (lo que el profesor describe)

1. **Optimalidad:** hay negativos (−15, −28) → continúa.
2. **Entra x2:** −28 es el menor negativo.
3. **Razón:** R1: 400 ÷ 0 → no se considera · R2: 500 ÷ 20 = 25 · R3: 100 ÷ 8 = **25/2** → **sale A2**, pivote = 8.
4. **Fila pivote:** `R3' = (1/8)·R3` → `[0, 1, 0, 0, 0, 1/8 | 25/2]`.
5. **R2:** `R2' = −20·R3' + R2` → `[15, 0, 0, −1, 1, −5/2 | 250]`.
6. **R1:** no cambia (valor 0 en la columna x2).
7. **Fila W:** `W' = 28·R3' + W` → `[−15, 0, 0, 1, 0, 7/2 | −250]`.

### Iteración 2

- Entra **x1** (−15).
- Razón: R1: 400 ÷ 1 = 400 · R2: 250 ÷ 15 = **50/3** · R3: 0 → no se considera. Sale **A1**, pivote 15.
- `R2'' = (1/15)·R2'` → `[1, 0, 0, −1/15, 1/15, −1/6 | 50/3]`.
- `R1' = −1·R2'' + R1` → `[0, 0, 1, 1/15, −1/15, 1/6 | 1150/3]`.
- `W'' = 15·R2'' + W'` → `[0, 0, 0, 0, 1, 1 | 0]`.
- **W = 0 → factible.** Fin de la Fase 1; se eliminan A1 y A2.

### Fase 2

- **Maximizar:** entra S2; x1 = **400**, x2 = **25/2**, S2 = 5750, **Z = 8375/2 (4187.5)**.
- **Si fuera minimizar** (mismos datos): la Fase 2 termina de inmediato con x1 = **50/3**, x2 = **25/2**, **Z = 2125/6**.

> **Nota:** en el audio el profesor dice que el resultado era x1 = “100 tercios” y x2 = “25 medios”. x2 coincide. x1 = 100/3 solo sale si la restricción 2 fuera `15x1 ≥ 500` (sin x2) y se minimiza. Como la transcripción no es exacta, el sistema queda preparado para **ambos objetivos** y las pruebas cubren las tres variantes (casos 1, 2 y 2b de la sección 16). Además, en el Sprint 0 se mete el ejemplo en la calculadora de referencia y se guardan sus tablas como prueba oficial.

---

## 11. API

Base: `/api/v1`.

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/resolver` | Resuelve y devuelve la lista de pasos. No guarda. |
| `POST` | `/importar` | Recibe un archivo `.json` exportado, lo valida y **lo vuelve a resolver**. |
| `POST` | `/exportar/pdf` | Recibe el problema y devuelve el PDF del desarrollo completo. |
| `POST` | `/problemas` | Guarda problema y solución; devuelve `slug` (enlace). |
| `GET` | `/problemas/{slug}` | Reabre un problema guardado. |
| `GET` | `/ejemplos` | Problemas precargados (incluye el del profesor). |
| `GET` | `/health` | Estado del servicio. |

Exportar a JSON no necesita endpoint: el front descarga la respuesta de `/resolver` (sección 13). Sin cuentas, el historial es una lista de `slug` en el `localStorage` del navegador.

### Petición

```python
# backend/app/schemas/problema.py
class Restriccion(BaseModel):
    coeficientes: list[Fraccion | None]    # None o "" = 0
    signo: Literal["<=", ">=", "="]
    lado_derecho: Fraccion

class Problema(BaseModel):
    objetivo: Literal["max", "min"]
    coef_objetivo: list[Fraccion | None] = Field(min_length=1, max_length=20)
    restricciones: list[Restriccion] = Field(min_length=1, max_length=50)
```

### Respuesta (resumida)

```json
{
  "version_formato": 1,
  "problema": { "objetivo": "max", "coef_objetivo": ["10", "15"], "restricciones": ["..."] },
  "clasificacion": { "tipo": "extendido", "motivo": "Hay restricciones ≥ y =" },
  "estado": "optimo",
  "pasos": [
    {
      "indice": 12,
      "fase": 1,
      "iteracion": 1,
      "tipo": "prueba_razon",
      "texto": "Se divide cada b entre el valor de la columna x2. Los ceros no se consideran porque da infinito.",
      "detalle": [
        { "fila": "S1", "calculo": "400 ÷ 0", "resultado": null, "motivo": "división entre 0" },
        { "fila": "A1", "calculo": "500 ÷ 20", "resultado": "25" },
        { "fila": "A2", "calculo": "100 ÷ 8", "resultado": "25/2", "menor": true }
      ],
      "resaltar": { "columna": "x2", "filas": ["A1", "A2"] },
      "tabla": { "columnas": ["x1","x2","S1","S2","A1","A2"], "cj": ["0","0","0","0","-1","-1"],
                 "base": ["S1","A1","A2"], "cb": ["0","-1","-1"], "b": ["400","500","100"],
                 "matriz": [["1","0","1","0","0","0"], ["15","20","0","-1","1","0"], ["0","8","0","0","0","1"]],
                 "fila_z": ["-15","-28","0","1","0","0"], "valor_z": "-600" }
    },
    {
      "indice": 14,
      "fase": 1,
      "iteracion": 1,
      "tipo": "operacion_fila",
      "latex": "R_2' = -20\\,R_3' + R_2",
      "antes":   ["15","20","0","-1","1","0","500"],
      "suma":    ["0","-20","0","0","0","-5/2","-250"],
      "despues": ["15","0","0","-1","1","-5/2","250"],
      "resaltar": { "filas": ["A1"] },
      "tabla": { "...": "estado después del paso" }
    }
  ],
  "solucion": { "variables": { "x1": "400", "x2": "25/2" }, "holguras": { "S1": "0", "S2": "5750" }, "z": "8375/2" }
}
```

- Los números viajan como texto de fracción.
- Errores de validación: HTTP 422 con la ruta del campo (`restricciones[2].coeficientes[0]`).

---

## 12. Base de datos

**Opcional**: solo para enlaces compartidos. Se activa con la variable de entorno `DATABASE_URL`. No hay usuarios. Los ejemplos se leen de archivos JSON, no de la BD.

```
problemas 1 ── N restricciones
          1 ── N soluciones
```

**problemas**

| Columna | Tipo |
|---|---|
| id | uuid PK |
| titulo | text |
| objetivo | enum (`max`, `min`) |
| num_variables | smallint (1–20) |
| coef_objetivo | jsonb |
| slug_publico | text, único |
| creado_en | timestamptz |

**restricciones**

| Columna | Tipo |
|---|---|
| id | uuid PK |
| problema_id | uuid FK → problemas, on delete cascade |
| orden | smallint (1–50) |
| coeficientes | jsonb |
| signo | enum (`<=`, `>=`, `=`) |
| lado_derecho | text (fracción) |

**soluciones**

| Columna | Tipo |
|---|---|
| id | uuid PK |
| problema_id | uuid FK → problemas, on delete cascade |
| estado | enum (`optimo`, `multiples_optimos`, `no_acotado`, `infactible`) |
| clasificacion | enum (`normal`, `extendido`) |
| valor_optimo | text, nullable |
| num_pasos | integer |
| resultado | jsonb (respuesta completa de `/resolver`) |
| version_motor | text |
| creado_en | timestamptz |

---

## 13. Exportar e importar

El profesor lo pidió para que los estudiantes practiquen y lleven el desarrollo si reclaman una nota [37:37–42:00].

| Acción | Formato | Cómo |
|---|---|---|
| **Exportar JSON** | `nombre.simplex.json` | El front descarga el problema + la solución + `version_formato`. El usuario elige el nombre (ej. “ejemplo 1”). |
| **Importar JSON** | `.simplex.json` | Se envía a `POST /importar`. El back valida el formato y **vuelve a resolver** desde los datos del problema (no confía en las tablas del archivo). El resultado se abre en el paso 1 del modo paso a paso. |
| **Exportar PDF** | `.pdf` | `POST /exportar/pdf` con ReportLab. Contiene **todo el desarrollo** (ver abajo). |

### Contenido del PDF: todo el ejemplo

El PDF tiene **los mismos pasos que el modo “Ver todo” de la pantalla**, en orden, sin omitir ninguno:

1. **Encabezado:** título del problema, fecha de generación y número de página en cada hoja.
2. **Modelo original:** objetivo (Max o Min), función objetivo, restricciones y no negatividad.
3. **Clasificación:** simplex normal o extendido, y por qué.
4. **Forma extendida:** una línea por restricción indicando qué variable se agregó y por qué.
5. **Fase 1** (si aplica), por cada iteración:
   - Tabla al inicio de la iteración, con Cj, Cb, Base, b y fila W.
   - Preparación de la fila W (`0 − W` y las operaciones para anular las artificiales), solo en la primera iteración.
   - Prueba de optimalidad.
   - Variable que entra y por qué.
   - Prueba de razón con **todas** las divisiones, incluidas las que no se consideran.
   - Variable que sale y pivote.
   - Fila pivote (`(1/pivote)·R`), valor por valor.
   - **Cada** operación de fila y de la fila W, con antes, suma y después.
   - Filas que no cambian y por qué.
   - Tabla resultante y solución actual.
6. **Fin de Fase 1:** valor de W, conclusión y columnas eliminadas.
7. **Fase 2:** nuevos Cj y Cb, preparación de la fila Z e iteraciones con el mismo detalle que la Fase 1.
8. **Lectura del resultado** desde la matriz identidad (artificiales excluidas).
9. **Resultado final:** valores de las variables, holguras/excesos y Z; o el caso especial (infactible, no acotado, óptimos múltiples) con su explicación.

**Formato**

- Pivote, columna que entra y fila que sale marcados con **negrita y recuadro**, además de color, para que se distingan al imprimir en blanco y negro.
- Fracciones exactas (y decimales si el usuario activó esa opción).
- Página horizontal automáticamente cuando la tabla tiene más de 8 columnas.
- Una tabla nunca se corta entre dos páginas; si no cabe, pasa entera a la siguiente.
- Prueba automática: el PDF generado debe contener el mismo número de pasos que la respuesta de `/resolver`.

### Notas

- Importar también sirve para **editar**: carga los datos en el asistente para cambiar un coeficiente y resolver de nuevo.
- Si el archivo es de una versión anterior del formato, se convierte; si está dañado, se dice qué campo falla.
- Pregunten a los compañeros del proyecto de **transporte** qué librerías usaron para exportar e importar; el profesor lo sugirió [39:03–39:38].

---

## 14. Interfaz (IU / UX)

### Pantalla de entrada (según la página de referencia)

Se copia la **distribución** de la calculadora de referencia, que los estudiantes ya conocen. No se copian su marca ni sus estilos.

**Paso 1 — Tamaño del modelo**

```
Cantidad de Variables:      [   ]  Máx. 20
Cantidad de Restricciones:  [   ]  Máx. 50
                    [ Generar Modelo ]  [ Limpiar ]
```

**Paso 2 — Objetivo** (recuadro gris)

```
Objetivo:
[ Maximizar          ▾ ]      ← lista: Maximizar (por defecto) / Minimizar
```

**Paso 3 — Función objetivo y restricciones** (se genera con n variables y m restricciones)

```
Función Objetivo:
[    ] X₁ +  [    ] X₂ +  [    ] X₃ +  [    ] X₄ +  [    ] X₅

Restricciones

Restricción 1:
[    ] X₁ +  [    ] X₂ +  [    ] X₃ +  [    ] X₄ +  [    ] X₅   [ ≤ ▾ ]   [    ]
                                                                  ≤ ≥ =    lado derecho
Restricción 2:
[    ] X₁ +  [    ] X₂ +  [    ] X₃ +  [    ] X₄ +  [    ] X₅   [ ≤ ▾ ]   [    ]
…

X₁, X₂, X₃, X₄, X₅ ≥ 0

                    [ Resolver ]  [ Limpiar ]
```

Detalles tomados de la referencia:

| Elemento | Comportamiento |
|---|---|
| Etiquetas | `X₁ +`, `X₂ +` … con subíndice; la última variable no lleva `+`. |
| Signo | Lista desplegable con `≤` (por defecto), `≥` y `=`. |
| Lado derecho | Campo después del signo. En la referencia pasa a la línea siguiente; nosotros lo dejamos en la misma fila si cabe. |
| No negatividad | Línea fija al final: `X₁, X₂, …, Xₙ ≥ 0`. |
| Botones | *Resolver* (principal) y *Limpiar* (secundario) debajo de las restricciones. |

Mejoras nuestras sobre la referencia:

| Mejora | Detalle |
|---|---|
| Campo vacío = 0 | El campo muestra `0` en gris como texto de ayuda; si queda en blanco vale 0. |
| Grupo campo + etiqueta | `[campo] X₃ +` se mantiene junto al saltar de línea, para que nunca quede un `+` suelto. |
| Validación por celda | Si un valor no es número ni fracción, la celda se marca y dice: *“Escribe un número, un decimal (0.5) o una fracción (3/4)”*. |
| Teclado | Tab recorre la fila de izquierda a derecha y pasa a la siguiente restricción. |
| Signo `≥` o `=` | Pequeño aviso junto a la lista: *“Esta restricción usará variable artificial (Dos Fases)”*. |
| Limpiar | *Limpiar* del paso 1 reinicia todo; *Limpiar* de abajo borra solo los coeficientes y conserva el tamaño. Ambos piden confirmación si hay datos. |
| Cambiar tamaño | Si se vuelve a *Generar Modelo* con otro tamaño, se conservan los valores que sigan existiendo. |
| Extras | *Cargar ejemplo* e *Importar JSON* junto al paso 1. |
| Móvil | Cada restricción se muestra en bloque: las variables en cuadrícula de 2 columnas y el signo y el lado derecho en una fila aparte. |

### Pantallas

- **Calculadora:** los 3 pasos anteriores con indicador de progreso; *Cargar ejemplo* e *Importar JSON*.
- **Solución:**
  - Resumen: tipo (normal/extendido), estado, Z y valores.
  - **Modo paso a paso** (por defecto) o **Ver todo**.
  - Iteraciones en acordeón: solo la actual abierta.
  - *Exportar JSON*, *Exportar PDF*, *Compartir enlace*, *Editar datos*.
- **Historial:** problemas resueltos en este navegador.
- **Ejemplos:** el del profesor, simplex normal, minimizar, infactible, no acotado, óptimos múltiples.

### Componentes clave

| Componente | Función |
|---|---|
| `CampoFraccion` | Acepta blanco (= 0), `3/4`, `-2`, `0.5`. |
| `EditorModelo` | Cuadrícula n × m con selector `≤ ≥ =`. |
| `TablaSimplex` | Cj, Cb, Base, b y fila Z; resalta la celda, fila o columna del paso actual; columnas Base y b fijas. |
| `PanelOperacion` | Texto + fórmula KaTeX + valores antes / suma / después. |
| `ControlesPaso` | Inicio, anterior, siguiente, siguiente iteración, reproducir, velocidad. |
| `RegistroIteracion` | Cascada de operaciones ya hechas en la iteración. |
| `AcordeonIteraciones` | Pliega automáticamente las iteraciones anteriores. |
| `ResumenSolucion` | Estado, Z y valores; artificiales excluidas. |

### Criterios de UX

- Pensado para **2–5 variables**: tabla y panel caben sin desplazar en una laptop. Con más variables la tabla se desplaza horizontalmente.
- Tab/Enter en la cuadrícula como en una hoja de cálculo.
- Flechas del teclado para avanzar pasos.
- Móvil: tabla arriba con desplazamiento, panel de operación debajo.
- Vista de impresión además del PDF.
- Contraste AA y foco visible.

---

## 15. Estructura de carpetas

```
SimplexCalculadora/
├── PLAN.md
├── README.md
├── docs/
│   └── despliegue.md          # guía para el servidor de la facultad (con y sin Docker)
├── docker-compose.yml
├── docker-compose.prod.yml
├── .github/workflows/ci.yml
├── frontend/
│   ├── package.json
│   └── src/
│       ├── main.tsx
│       ├── pages/                 # Calculadora, Solucion, Historial, Ejemplos
│       ├── features/
│       │   ├── modelo/            # asistente 1–3, importar JSON, esquemas Zod
│       │   └── solucion/          # TablaSimplex, PanelOperacion, ControlesPaso, Acordeon
│       ├── stores/                # Zustand: modelo y puntero del paso a paso
│       ├── components/ui/         # shadcn/ui
│       └── lib/api/               # cliente + tipos generados
└── backend/
    ├── pyproject.toml
    ├── alembic/
    ├── app/
    │   ├── main.py
    │   ├── core/config.py
    │   ├── api/v1/                # resolver, importar, exportar, problemas, ejemplos
    │   ├── schemas/               # Pydantic (problema, pasos, archivo exportado)
    │   ├── services/
    │   ├── simplex/               # MOTOR PURO
    │   │   ├── fracciones.py
    │   │   ├── clasificacion.py   # normal / extendido
    │   │   ├── forma_extendida.py
    │   │   ├── tabla.py           # estado de la tabla (inmutable)
    │   │   ├── operaciones.py     # fila pivote, Ri' = (−v)·Rp' + Ri
    │   │   ├── reglas.py          # optimalidad, entra, razón, empates
    │   │   ├── dos_fases.py
    │   │   ├── pasos.py           # tipos de paso
    │   │   └── explicador.py      # paso → texto y LaTeX
    │   ├── exportacion/           # json.py, pdf.py (ReportLab)
    │   ├── ejemplos/              # problemas precargados en .simplex.json
    │   ├── db/
    │   └── repositories/
    └── tests/
        ├── simplex/
        ├── exportacion/
        └── api/
```

---

## 16. Pruebas

| # | Caso | Verifica | Esperado |
|---|---|---|---|
| 1 | **Ejemplo del profesor**, Max | Fase 1 con ≥ y =, fila W = −15, −28 | x1 = 400, x2 = 25/2, Z = 8375/2 |
| 2 | Ejemplo del profesor, Min | Minimización tras Fase 1 | x1 = 50/3, x2 = 25/2, Z = 2125/6 |
| 2b | Variante Min con `15x1 ≥ 500` (sin x2) | Coeficiente en blanco + Dos Fases | x1 = 100/3, x2 = 25/2, Z = 3125/6 |
| 3 | Max 3x1 + 5x2; x1 ≤ 4; 2x2 ≤ 12; 3x1 + 2x2 ≤ 18 | Simplex normal | x1 = 2, x2 = 6, Z = 36 |
| 4 | Min 4x1 + x2; 3x1 + x2 = 3; 4x1 + 3x2 ≥ 6; x1 + 2x2 ≤ 4 | Dos Fases, Min | x1 = 2/5, x2 = 9/5, Z = 17/5 |
| 5 | Min −3x1 − 5x2 con restricciones del caso 3 | Min con solo ≤ (sin Fase 1) | Z = −36 |
| 6 | Max x1 + x2; x1 + x2 ≤ 2; x1 + x2 ≥ 4 | Infactible | `infactible` |
| 7 | Max x1 + x2; x1 − x2 ≤ 1 | No acotado | `no_acotado` |
| 8 | Max 2x1 + 4x2; x1 + 2x2 ≤ 5; x1 + x2 ≤ 4 | Óptimos múltiples | `multiples_optimos`, Z = 10 |
| 9 | Coeficientes en blanco | Blanco = 0 | Igual que con ceros |
| 10 | `−x1 − x2 ≤ −2` | b negativo | Se convierte a ≥ y usa Fase 1 |
| 11 | Restricción = repetida | Artificial básica en 0 | Fila redundante eliminada |
| 12 | Empate en entrada y en salida | Regla por posición | Primera columna / primera fila, con aviso |
| 13 | Exportar → importar | Archivo | Mismos pasos y resultado |
| 13b | Exportar PDF (casos 1 y 2) | PDF completo | Mismo número de pasos que `/resolver`, en Max y en Min |
| 14 | 5 variables × 5 restricciones | Caso grande de clase | Coincide con SciPy; < 1 s |
| 15 | 20 variables × 50 restricciones | No se cuelga | Coincide con SciPy; < 3 s |

Los casos 1–8 comparan con `scipy.optimize.linprog`. Los casos 1 y 3 comparan además cada tabla con la calculadora de referencia.

---

## 17. Despliegue en el hosting de la facultad

El profesor quiere proponer subirlo al servidor de la facultad, pidiendo usuario y clave y cargando **por partes**: front, back y base de datos [42:30–44:01].

| Parte | Qué se sube | Requisito en el servidor |
|---|---|---|
| Frontend | Carpeta `dist/` (HTML, JS, CSS estáticos) | Cualquier servidor web (Apache / Nginx) |
| Backend | App FastAPI | **Python 3.11+** con Uvicorn/Gunicorn, o **Docker** |
| Base de datos | Migraciones Alembic | **PostgreSQL** |

**Decisión:** se despliega con **Docker Compose** (`docker-compose.prod.yml`: Nginx con el front estático + API + PostgreSQL opcional). La guía `docs/despliegue.md` se escribe en el Sprint 0 y cubre también la opción sin Docker.

- **Opción principal:** el servidor acepta **Docker** → se sube con `docker compose -f docker-compose.prod.yml up -d`.
- **Si no hay Docker pero sí Python:** Gunicorn + Uvicorn como servicio y Nginx como proxy.
- **Si no hay PostgreSQL:** no se define `DATABASE_URL`; todo funciona salvo los enlaces compartidos. SQLAlchemy también permite usar MySQL/MariaDB.
- **Riesgo:** si el hosting solo acepta PHP (hosting compartido), el backend en Python no correría. Cuando se pida el usuario y la clave hay que confirmar la lista de requisitos de la [sección 19](#19-decisiones-sobre-las-preguntas-pendientes).
- Mientras tanto, para demos: Vercel (front), Render (API) y Neon (BD).

---

## 18. Sprints

Cada sprint dura 1–2 semanas según el calendario del curso.

| Sprint | Backend | Frontend | Listo cuando |
|---|---|---|---|
| **0 · Base** | Repo, Docker, CI, esquemas Pydantic, tipos de paso, contrato OpenAPI, `docs/despliegue.md`. Meter el ejemplo del profesor en la referencia y guardar sus tablas. | Wireframes del modo paso a paso; proyecto Vite + Tailwind + shadcn | `docker compose up` levanta todo; `/docs` muestra el contrato |
| **1 · Simplex normal** | Fracciones, forma extendida, operaciones de fila, reglas Max/Min, explicador | Asistente 3 pasos; `TablaSimplex`; `PanelOperacion` | Caso 3 se ve operación por operación |
| **2 · Dos Fases** | Fase 1 (W = −ΣA), transición, Fase 2, casos especiales, empates | `ControlesPaso`, acordeón, reproducción automática | Casos 1–12 pasan; el ejemplo del profesor coincide con la referencia |
| **3 · Exportar e importar** | JSON, `/importar`, PDF con ReportLab; BD y enlaces | Botones exportar/importar, historial local, ejemplos | Caso 13 pasa; PDF revisado por el profesor |
| **4 · Entrega** | Pruebas de rendimiento; despliegue en hosting de la facultad | Accesibilidad, móvil, Playwright | Funciona en el servidor de la facultad; manual y demo |

### Flujo de trabajo con Git

**Regla del equipo:** cada cambio, por mínimo que sea, va en **su propio commit**. Un commit hace una sola cosa y el proyecto debe seguir funcionando después de cada uno.

**Ramas**

| Rama | Uso |
|---|---|
| `main` | Versión estable. Solo recibe merges de `develop` al terminar un sprint. |
| `develop` | Integración de lo terminado. |
| `feature/sprint-N-tema` | Trabajo diario. Se crea desde `develop` y vuelve a `develop` con Pull Request. |

**Formato del mensaje** ([Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/), en español, en imperativo y sin punto final)

```
tipo(ámbito): descripción corta
```

| Tipo | Cuándo |
|---|---|
| `feat` | Funcionalidad nueva |
| `fix` | Corrección de un error |
| `test` | Pruebas nuevas o corregidas |
| `docs` | Solo documentación |
| `build` | Dependencias, Docker, configuración de compilación |
| `ci` | GitHub Actions |
| `chore` | Mantenimiento que no cambia la funcionalidad |
| `refactor` | Cambio interno sin cambiar el comportamiento |
| `perf` | Mejora de rendimiento |
| `style` | Formato (espacios, comas) sin cambiar código |

Ámbitos: `backend`, `frontend`, `simplex`, `explicador`, `exportacion`, `api`, `db`. Sin ámbito cuando afecta a todo el repo.

### Plan de commits

#### Sprint 0 · Base

**A. Repositorio** (rama `main`)

| # | Commit |
|---|---|
| 1 | `chore: inicializar repositorio con .gitignore` |
| 2 | `chore: agregar .gitattributes y .editorconfig` |
| 3 | `docs: agregar flujo de Git y plan de commits al plan` (el plan ya estaba en el repositorio) |
| 4 | `docs: agregar guía de contribución con convención de commits` |
| 5 | `docs: agregar README inicial` |

A partir de aquí: se crea `develop` y desde ella `feature/sprint-0-base`.

**B. Backend base**

| # | Commit |
|---|---|
| 6 | `build(backend): crear pyproject.toml con dependencias base` |
| 7 | `feat(backend): crear aplicación FastAPI con endpoint /health` |
| 8 | `feat(backend): agregar configuración por variables de entorno` |
| 9 | `feat(backend): habilitar CORS para el frontend` |
| 10 | `test(backend): probar endpoint /health` |
| 11 | `chore(backend): configurar Ruff y mypy` |

**C. Contrato de la API**

| # | Commit |
|---|---|
| 12 | `feat(backend): agregar tipo Fraccion para coeficientes` |
| 13 | `test(backend): probar conversión de Fraccion` |
| 14 | `feat(backend): agregar esquema Problema con límites 20 × 50` |
| 15 | `test(backend): probar validaciones del esquema Problema` |
| 16 | `feat(backend): agregar esquema de tabla simplex` |
| 17 | `feat(backend): agregar tipos de paso del modo paso a paso` |
| 18 | `feat(backend): agregar esquema de respuesta de /resolver` |
| 19 | `feat(backend): agregar esquema del archivo .simplex.json` |
| 20 | `feat(backend): agregar endpoint POST /resolver pendiente de motor` |
| 21 | `feat(backend): agregar endpoints de importar y exportar PDF pendientes` |
| 22 | `feat(backend): agregar endpoints de problemas pendientes` |
| 23 | `feat(backend): agregar ejemplos precargados en JSON` |
| 24 | `feat(backend): agregar endpoint GET /ejemplos` |
| 25 | `test(backend): probar endpoint de ejemplos` |
| 26 | `test(backend): probar que el contrato OpenAPI tenga todas las rutas` |
| 27 | `feat(backend): agregar script para exportar el contrato OpenAPI` |
| 28 | `docs(backend): agregar contrato openapi.json generado` |

**D. Base de datos opcional**

| # | Commit |
|---|---|
| 29 | `build(backend): agregar dependencias opcionales de base de datos` |
| 30 | `feat(backend): agregar sesión de BD opcional según DATABASE_URL` |
| 31 | `feat(backend): agregar modelos de problemas, restricciones y soluciones` |
| 32 | `build(backend): inicializar Alembic` |
| 33 | `feat(backend): agregar migración inicial` |

**E. Frontend base**

| # | Commit |
|---|---|
| 34 | `build(frontend): crear proyecto Vite con React y TypeScript` |
| 35 | `chore(frontend): limpiar plantilla inicial de Vite` |
| 36 | `build(frontend): configurar Tailwind CSS` |
| 37 | `build(frontend): configurar alias @ para imports` |
| 38 | `build(frontend): inicializar shadcn/ui` |
| 39 | `build(frontend): agregar React Router` |
| 40 | `feat(frontend): agregar layout con navegación` |
| 41 | `feat(frontend): agregar páginas Calculadora, Solución, Historial y Ejemplos` |
| 42 | `build(frontend): agregar TanStack Query, Zustand, React Hook Form y Zod` |
| 43 | `build(frontend): generar tipos desde el contrato OpenAPI` |
| 44 | `feat(frontend): agregar cliente de API` |
| 45 | `feat(frontend): mostrar estado de la API en el pie de página` |
| 46 | `test(frontend): configurar Vitest y Testing Library` |
| 47 | `test(frontend): probar navegación del layout` |

**F. Docker**

| # | Commit |
|---|---|
| 48 | `build(backend): agregar Dockerfile del backend` |
| 49 | `build(frontend): agregar Dockerfile de desarrollo del frontend` |
| 50 | `build: agregar docker-compose.yml con web, api y db` |
| 51 | `build: agregar .env.example` |
| 52 | `build(frontend): agregar Dockerfile de producción con Nginx` |
| 53 | `build: agregar docker-compose.prod.yml` |

**G. Integración continua**

| # | Commit |
|---|---|
| 54 | `ci: agregar flujo de backend con Ruff, mypy y pytest` |
| 55 | `ci: agregar flujo de frontend con lint, pruebas y build` |
| 56 | `ci: verificar que el contrato OpenAPI esté actualizado` |

**H. Documentación**

| # | Commit |
|---|---|
| 57 | `docs: agregar wireframes del modo paso a paso` |
| 58 | `docs: agregar guía de despliegue` |
| 59 | `docs: actualizar README con instrucciones de desarrollo` |
| 60 | `docs: marcar Sprint 0 como completado` |

**Tarea manual del equipo:** meter el ejemplo del profesor (Max y Min) en la calculadora de referencia, copiar sus tablas y agregarlas con `test(backend): agregar tablas de referencia del ejemplo del profesor`.

#### Sprint 1 · Simplex normal

Rama `feature/sprint-1-simplex-normal`.

**Motor**

| Commit |
|---|
| `feat(simplex): agregar formateo de fracciones para mostrar` |
| `feat(simplex): agregar modelo inmutable de tabla simplex` |
| `test(simplex): probar creación y copia de la tabla` |
| `feat(simplex): normalizar restricciones con lado derecho negativo` |
| `test(simplex): probar normalización de lado derecho negativo` |
| `feat(simplex): clasificar problema como simplex normal o extendido` |
| `test(simplex): probar clasificación del problema` |
| `feat(simplex): construir forma extendida con holguras` |
| `test(simplex): probar forma extendida con holguras` |
| `feat(simplex): construir tabla inicial con Cj, Cb y base` |
| `feat(simplex): calcular fila Z inicial como 0 − Z` |
| `test(simplex): probar tabla inicial y fila Z` |
| `feat(simplex): agregar prueba de optimalidad para maximizar y minimizar` |
| `test(simplex): probar prueba de optimalidad` |
| `feat(simplex): elegir variable que entra con desempate por posición` |
| `test(simplex): probar elección de variable que entra` |
| `feat(simplex): agregar prueba de razón mínima excluyendo ceros y negativos` |
| `test(simplex): probar prueba de razón mínima` |
| `feat(simplex): detectar problema no acotado` |
| `feat(simplex): agregar operación de fila pivote (1/pivote)·R` |
| `feat(simplex): agregar operación de fila (−v)·Rp' + Ri` |
| `feat(simplex): actualizar fila Z con operación de fila` |
| `test(simplex): probar operaciones de Gauss-Jordan` |
| `feat(simplex): agregar comprobación Zj − Cj con Cb` |
| `feat(simplex): registrar pasos de cada iteración` |
| `feat(simplex): iterar hasta el óptimo en simplex normal` |
| `feat(simplex): leer resultado desde la matriz identidad` |
| `feat(simplex): detectar óptimos múltiples` |
| `test(simplex): comparar casos 3, 5, 7 y 8 con SciPy` |
| `feat(explicador): agregar textos de los pasos del simplex normal` |
| `test(explicador): probar textos de los pasos` |
| `feat(api): conectar POST /resolver con el motor` |
| `test(api): resolver caso 3 de punta a punta` |

**Frontend**

| Commit |
|---|
| `feat(frontend): agregar componente CampoFraccion` |
| `test(frontend): probar CampoFraccion` |
| `feat(frontend): agregar paso 1 con tamaño del modelo` |
| `feat(frontend): agregar paso 2 con objetivo` |
| `feat(frontend): agregar paso 3 con función objetivo` |
| `feat(frontend): agregar restricciones con signo y lado derecho` |
| `feat(frontend): agregar línea de no negatividad y botones Resolver y Limpiar` |
| `feat(frontend): validar el modelo con Zod` |
| `feat(frontend): guardar el modelo en Zustand` |
| `feat(frontend): enviar el modelo a /resolver` |
| `feat(frontend): agregar componente TablaSimplex` |
| `feat(frontend): resaltar columna, fila y pivote` |
| `feat(frontend): agregar PanelOperacion con KaTeX` |
| `feat(frontend): mostrar todos los pasos en la vista Solución` |
| `test(frontend): resolver caso 3 desde la interfaz con Playwright` |

#### Sprint 2 · Dos Fases

Rama `feature/sprint-2-dos-fases`.

**Motor**

| Commit |
|---|
| `feat(simplex): agregar excesos y artificiales en la forma extendida` |
| `test(simplex): probar forma extendida con ≥ y =` |
| `feat(simplex): construir Fase 1 con Max W = −ΣA` |
| `feat(simplex): preparar fila W anulando artificiales básicas` |
| `test(simplex): probar tabla inicial de Fase 1 del ejemplo del profesor` |
| `feat(simplex): detectar infactibilidad al final de la Fase 1` |
| `feat(simplex): sacar artificiales básicas con valor cero` |
| `feat(simplex): eliminar restricciones redundantes` |
| `feat(simplex): eliminar columnas artificiales al pasar a Fase 2` |
| `feat(simplex): preparar fila Z de Fase 2 con Cj originales` |
| `feat(simplex): avisar minimización sin variables artificiales` |
| `feat(simplex): avisar empates y alternativas` |
| `feat(simplex): avisar solución degenerada` |
| `feat(simplex): detectar ciclos y cambiar a regla de Bland` |
| `test(simplex): comparar ejemplo del profesor Max con la referencia` |
| `test(simplex): probar ejemplo del profesor Min y variante 2b` |
| `test(simplex): probar casos 4, 6, 9, 10, 11 y 12` |
| `test(simplex): medir rendimiento con 5 × 5 y 20 × 50` |
| `feat(explicador): agregar textos de Fase 1, transición y casos especiales` |

**Frontend**

| Commit |
|---|
| `feat(frontend): guardar el puntero del paso a paso en Zustand` |
| `feat(frontend): agregar controles inicio, anterior y siguiente` |
| `feat(frontend): saltar a la siguiente iteración` |
| `feat(frontend): agregar reproducción automática con velocidad` |
| `feat(frontend): agregar atajos de teclado ← y →` |
| `feat(frontend): agregar registro en cascada de la iteración` |
| `feat(frontend): plegar iteraciones anteriores en acordeón` |
| `feat(frontend): agregar pestañas Fase 1 y Fase 2` |
| `feat(frontend): agregar resumen de la solución` |
| `feat(frontend): animar celdas que cambian con Motion` |
| `feat(frontend): agregar botón Ver decimales` |
| `feat(frontend): avisar variable artificial al elegir ≥ o =` |
| `test(frontend): recorrer el ejemplo del profesor paso a paso con Playwright` |

#### Sprint 3 · Exportar e importar

Rama `feature/sprint-3-exportar-importar`.

| Commit |
|---|
| `feat(exportacion): serializar la solución a .simplex.json` |
| `feat(api): agregar POST /importar que valida y vuelve a resolver` |
| `test(api): probar importación válida e inválida` |
| `feat(exportacion): generar encabezado y modelo del PDF` |
| `feat(exportacion): dibujar tablas con pivote marcado en el PDF` |
| `feat(exportacion): escribir las operaciones de cada paso en el PDF` |
| `feat(exportacion): usar página horizontal para tablas anchas` |
| `feat(api): conectar POST /exportar/pdf` |
| `test(exportacion): verificar que el PDF tenga todos los pasos` |
| `feat(db): agregar repositorio de problemas` |
| `feat(api): conectar POST /problemas y GET /problemas/{slug}` |
| `test(api): probar guardar y abrir problema por enlace` |
| `feat(frontend): agregar botón Exportar JSON` |
| `feat(frontend): agregar Importar JSON` |
| `feat(frontend): agregar botón Exportar PDF` |
| `feat(frontend): guardar historial en el navegador` |
| `feat(frontend): agregar página Ejemplos` |
| `feat(frontend): agregar Compartir enlace cuando hay BD` |
| `feat(frontend): agregar vista de impresión` |
| `test(frontend): exportar e importar con Playwright` |

#### Sprint 4 · Entrega

Rama `feature/sprint-4-entrega`.

| Commit |
|---|
| `feat(frontend): adaptar formulario a móvil` |
| `feat(frontend): adaptar paso a paso a móvil` |
| `fix(frontend): mejorar etiquetas, foco y contraste` |
| `test(frontend): probar flujo completo en móvil con Playwright` |
| `perf(simplex): reducir tamaño de respuesta para 20 × 50` |
| `docs: agregar manual de usuario` |
| `docs: agregar guion de demo` |
| `build: ajustar docker-compose.prod.yml al servidor de la facultad` |
| `docs: registrar datos del despliegue en la facultad` |
| `chore(release): publicar versión 1.0.0` |

Los Sprints 1–4 pueden ganar commits al empezar cada uno; la regla es la misma: un cambio, un commit.

---

## 19. Decisiones sobre las preguntas pendientes

Se resolvieron siguiendo el plan, la teoría del método simplex, la documentación consultada (sección 21) y lo que dijo el profesor. Cada decisión indica qué cambiaría si el profesor pide otra cosa.

| # | Tema | Decisión |
|---|---|---|
| 1 | Hosting | Docker Compose; alternativa sin Docker; BD opcional |
| 2 | Minimizar con solo ≤ | Sin Fase 1; simplex directo con explicación |
| 3 | Fracciones o decimales | Cálculo exacto con fracciones; decimales solo como vista |
| 4 | Empates | Regla fija por posición con aviso; Bland si hay ciclo |
| 5 | Forma de la Fase 1 | Max W = −ΣA |
| 6 | Base de datos | No obligatoria; se activa con `DATABASE_URL` |

### 1. Hosting de la facultad

- **Decisión:** desplegar con **Docker Compose**: Nginx sirve el front estático y hace de proxy a la API; PostgreSQL es opcional. Se documenta también la instalación sin Docker (Python 3.11+ + Gunicorn/Uvicorn + Nginx).
- **Por qué:** el profesor explicó que se sube “por partes” (front, back, BD). Con contenedores cada parte va separada, pero se instala con un solo comando y funciona igual en la laptop del equipo y en el servidor.
- **Riesgo que queda:** no sabemos qué ofrece el servidor. Al pedir el usuario y la clave, confirmar:
  - [ ] ¿Docker disponible? Si no: ¿Python 3.11+ y permiso para dejar un proceso corriendo?
  - [ ] ¿PostgreSQL o MySQL? (opcional)
  - [ ] ¿Dominio o subruta asignada? (ej. `facultad.edu/simplex`)
  - [ ] ¿HTTPS?
  - [ ] ¿Acceso por SSH o solo panel web / FTP?

  Si solo acepta PHP, el backend en Python no correría allí. Conviene confirmarlo lo antes posible, aunque no bloquea los Sprints 0–3.

### 2. Minimizar con solo restricciones ≤

- **Decisión:** **no se ejecuta la Fase 1.** Se resuelve con simplex directo y se explica por qué.
- **Por qué (documentación):** la Fase 1 sirve para encontrar una solución básica factible inicial cuando el problema tiene **variables artificiales**, que solo aparecen con restricciones ≥ o =. Con solo ≤ y lados derechos ≥ 0, las holguras ya forman esa base; la Fase 1 terminaría con W = 0 sin hacer ninguna iteración. Esto coincide con lo que dijo el profesor: “la fase 2 se implica cuando hay restricciones de igualdad o de mayor o igual” [18:08].
- **Cómo se ve:**
  - Etiqueta: *Simplex normal (minimización sin variables artificiales)*.
  - Aviso: *“Todas las restricciones son ≤ y los lados derechos son ≥ 0. Las holguras ya forman la base inicial, así que no se necesitan variables artificiales ni Fase 1.”*
  - Si además todos los coeficientes de la función objetivo son ≥ 0, la tabla inicial ya es óptima y se explica: *“Todos los valores de la fila Z son ≤ 0: la solución óptima es producir 0 de cada variable, con Z = 0.”*
- **Si el profesor quiere ver la Fase 1 igual:** se muestra una Fase 1 vacía con W = 0 antes de la Fase 2. Es un cambio pequeño en `dos_fases.py`.

### 3. Fracciones o decimales

- **Decisión:** el motor **siempre calcula con fracciones exactas**. Las tablas y el PDF muestran **fracciones** por defecto; el botón *Ver decimales* (4 decimales) solo cambia la vista.
- **Por qué:**
  - Gauss-Jordan a mano se hace con fracciones; el profesor habla de “un octavo”, “25 medios”, “100 tercios”.
  - Con decimales se acumulan redondeos (1/3 → 0.3333) que pueden cambiar qué variable entra o sale y hacer que el resultado no coincida con el cuaderno.
- **Entrada:** se aceptan decimales y se convierten de forma exacta (`0.5` → `1/2`, `0.1` → `1/10`).
- **PDF:** usa la vista elegida al momento de exportar.

### 4. Empates

- **Decisión:** regla **fija por posición**; el estudiante **no elige** en la v1.
  - **Entra:** entre las empatadas, la primera columna de izquierda a derecha.
  - **Sale:** entre las empatadas en la razón mínima, la primera fila de arriba hacia abajo.
  - Aviso con las alternativas: *“x1 y x3 empatan con −5. Se elige x1 por estar primero. A mano puedes elegir cualquiera: el valor óptimo de Z es el mismo, aunque las tablas intermedias pueden cambiar.”*
- **Por qué:**
  - La documentación del método indica que los empates se pueden romper de forma arbitraria.
  - El profesor explicó que el algoritmo elige siempre por posición en la matriz [33:57].
  - Una regla fija hace que el mismo problema dé **siempre el mismo JSON y el mismo PDF**, lo que permite probar y comparar con la calculadora de referencia.
- **Degeneración:** un empate en la razón mínima deja una variable básica en 0 (solución degenerada); se avisa. En casos raros la degeneración provoca **ciclos** (se repite una base). Si el motor detecta una base repetida, desde ahí aplica la **regla de Bland** (menor índice), que garantiza que el método termina, y lo explica.
- **Futuro:** opción *“Elegir en empates”* para practicar caminos distintos (aprox. medio sprint).

### 5. Forma de la Fase 1

- **Decisión:** **Max W = −ΣA**. La fila W tiene negativos; entra el menor negativo; termina cuando todo es ≥ 0.
- **Por qué:**
  - Es **equivalente** a Min W = ΣA, que es como aparece en libros como el de Taha: la solución es la misma y W solo cambia de signo.
  - Coincide con la calculadora de referencia que mostró el profesor (fila con −15 y −28).
  - La Fase 1 usa **la misma regla que la maximización** que explicó el profesor, sea el problema Max o Min: una sola regla que aprender.
- **Cómo se ve:** al iniciar la Fase 1 se explica: *“Minimizar la suma de artificiales es lo mismo que maximizar su negativo. Usamos Max W = −ΣA para aplicar la misma regla que en maximización.”*
- **Al terminar:** W = 0 → factible; W < 0 → infactible.
- **Si el profesor prefiere Min W = ΣA:** es un parámetro del motor; cambian los signos de la fila W y la regla de entrada de la Fase 1.

### 6. Base de datos

- **Decisión:** **no es obligatoria.** Se mantiene PostgreSQL + SQLAlchemy + Alembic como en el plan, pero **opcional**:
  - Sin `DATABASE_URL`: funcionan resolver, paso a paso, exportar/importar JSON, PDF, historial local y ejemplos. El botón *Compartir enlace* se oculta.
  - Con `DATABASE_URL`: además se guardan problemas y se comparten por enlace.
- **Por qué:** el método no necesita guardar nada; lo que pidió el profesor es exportar e importar JSON. Hacer la BD opcional reduce el riesgo de despliegue si el servidor no la ofrece.
- **Ejemplos:** se leen de archivos `.simplex.json` en `backend/app/ejemplos/`, así siempre están disponibles.

### Respuestas anteriores

- Simplex extendido = forma extendida + Dos Fases.
- Gran M: no, solo Dos Fases.
- Cuentas de usuario: no.
- Ejemplo del profesor: el sistema debe estar preparado para **Max y Min**; se prueban ambas variantes.
- PDF: **todo el desarrollo del ejemplo**, cada tabla y cada operación.
- Pantalla de entrada: igual distribución que la página de referencia.
- Formato de la fila Z: la del profesor (× −1 / Zj − Cj; Max termina con todo ≥ 0, Min con todo ≤ 0).
- Operaciones Gauss-Jordan: `(1/pivote)·Rp` y `(−v)·Rp' + Ri`.
- Método gráfico: no hace falta.
- Exportar/importar JSON y PDF: sí.

---

## 20. Posibles módulos futuros

El profesor los mencionó como interés, **no como parte de este proyecto** [30:47–35:00, 44:13–44:30]:

- **Ruta más corta en redes de nodos:** ingresar nodos y arcos, analizar cada nodo mostrando los arcos que llegan y dejar que el estudiante elija el de menor tiempo (algoritmo de Dijkstra).
- **Ruta crítica** en redes de actividades.
- **Transporte** (esquina noroeste, costo mínimo): ya lo hicieron compañeros anteriores.

La arquitectura (motor puro que produce pasos + visor paso a paso genérico) permite agregar estos métodos después como módulos nuevos.

---

## 21. Fuentes

- Reunión grabada con el profesor (transcripción `transcript_timestamps.txt`).
- Calculadora de referencia: <https://www.plandemejora.com/calculadora-metodo-simplex-online/>
- Método simplex paso a paso (convención Zj − Cj, reglas Max/Min): <https://www.plandemejora.com/metodo-simplex-paso-a-paso-ejemplos-maximizar-minimizar/>
- Teoría del método de las 2 fases: <https://juancruzindustrial.com/teoria-metodo-de-las-2-fases/>
- El método de las dos fases paso a paso: <https://reisdigital.es/investigaciones/metodo-de-las-2-fases-paso-a-paso-investigacion-de-operaciones/>
- Taha, H. A. *Investigación de Operaciones* — capítulo del método simplex.
