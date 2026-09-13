# Simplex Paso a Paso — Plan del proyecto

Calculadora web del **método simplex extendido** (forma extendida + método de las Dos Fases) para **Maximizar y Minimizar**. A diferencia de las calculadoras gratuitas que hay en internet, muestra **cómo se llega al resultado**: cada tabla, cada cálculo de Zj, la variable que entra, la razón mínima, el pivote y las operaciones de fila.

- **Referencia de entrada de datos:** <https://www.plandemejora.com/calculadora-metodo-simplex-online/>
- **Stack:** React + TypeScript (front) · Python + FastAPI (back) · PostgreSQL + SQLAlchemy (BD)
- **Versión del plan:** 1.2 — 2026-09-12

---

## Contenido

1. [Decisiones confirmadas](#1-decisiones-confirmadas)
2. [¿Cuándo se usan las Dos Fases?](#2-cuándo-se-usan-las-dos-fases)
3. [Formato de la tabla simplex](#3-formato-de-la-tabla-simplex)
4. [Alcance](#4-alcance)
5. [Tecnologías](#5-tecnologías)
6. [Arquitectura](#6-arquitectura)
7. [Algoritmo del motor](#7-algoritmo-del-motor)
8. [El paso a paso: qué se muestra](#8-el-paso-a-paso-qué-se-muestra)
9. [API](#9-api)
10. [Base de datos](#10-base-de-datos)
11. [Interfaz (IU / UX)](#11-interfaz-iu--ux)
12. [Estructura de carpetas](#12-estructura-de-carpetas)
13. [Pruebas](#13-pruebas)
14. [Sprints](#14-sprints)
15. [Preguntas pendientes para el profesor](#15-preguntas-pendientes-para-el-profesor)
16. [Fuentes](#16-fuentes)

---

## 1. Decisiones confirmadas

| Tema | Decisión |
|---|---|
| “Simplex extendido” | Mostrar el modelo en **forma extendida** (holguras, excesos y artificiales) y resolver con **Dos Fases** cuando haga falta. |
| Método para artificiales | **Solo Dos Fases**. No se implementa Gran M. |
| Formato de la tabla | Filas **Cj**, **Cb**, **Zj** y **Zj − Cj** (el formato usado en la referencia). Ver sección 3. |
| Minimización | Se resuelve **directamente** (sin convertir a Max −Z), cambiando el criterio de entrada y de optimalidad. *(Confirmar, ver sección 15.)* |
| Números | Fracciones exactas (`5/2`), con opción de ver decimales. *(Confirmar, ver sección 15.)* |
| Límites | Máximo **20 variables** y **50 restricciones**. |
| Cuentas de usuario | **No.** Sin registro ni inicio de sesión. El historial se guarda en el navegador y cada problema guardado se abre con su enlace. |

---

## 2. ¿Cuándo se usan las Dos Fases?

> **Importante:** las Dos Fases **no dependen de si se maximiza o minimiza**. Dependen de los **signos de las restricciones**.

Se usan cuando alguna restricción necesita **variable artificial**, es decir, cuando hay restricciones **≥** o **=**. La confusión es común porque los problemas típicos de minimización (dieta, costos mínimos) suelen tener restricciones ≥.

| Objetivo | Restricciones | Método |
|---|---|---|
| Maximizar | Solo ≤ | Simplex directo (base inicial = holguras) |
| Minimizar | Solo ≤ | Simplex directo (base inicial = holguras) |
| Maximizar | Alguna ≥ o = | **Dos Fases** |
| Minimizar | Alguna ≥ o = | **Dos Fases** |

**Caso a tener en cuenta:** si el lado derecho es negativo (ej. `−x1 − x2 ≤ −2`), se multiplica la fila por −1 y queda `x1 + x2 ≥ 2`. Ese problema pasa a necesitar Dos Fases aunque el usuario haya escrito ≤.

### Forma extendida

| Restricción original | Se transforma en | Variables agregadas |
|---|---|---|
| `a·x ≤ b` | `a·x + S = b` | Holgura S (Cj = 0) |
| `a·x ≥ b` | `a·x − E + A = b` | Exceso E (Cj = 0) y artificial A |
| `a·x = b` | `a·x + A = b` | Artificial A |

### Fase 1

- **Función objetivo:** `Min W = A1 + A2 + … + Ak`, con Cj = 1 en las artificiales y Cj = 0 en las demás variables.
- **Base inicial:** holguras (en filas ≤) y artificiales (en filas ≥ y =).
- Se resuelve con la regla de **minimizar**.
- **Al terminar:**
  - `W > 0` → el problema original es **infactible** (fin; se explica al usuario).
  - `W = 0` → el problema es factible; se pasa a la Fase 2.
  - Si una artificial sigue en la base con valor 0: si en su fila hay un coeficiente distinto de 0 en una columna no artificial, se hace un pivote para sacarla; si toda la fila es 0 en columnas no artificiales, la restricción es **redundante** y se elimina.

### Fase 2

1. Se eliminan las columnas de las artificiales.
2. Se ponen los **Cj originales** del problema y se actualiza **Cb** con la base actual.
3. Se recalculan **Zj** y **Zj − Cj**.
4. Se continúa el simplex con la regla del objetivo original (Max o Min).

---

## 3. Formato de la tabla simplex

Formato estándar en los cursos de Investigación de Operaciones y en la calculadora de referencia:

|  |  | **Cj →** |  | 3 | 5 | 0 | 0 | 0 |
|---|---|---|---|---|---|---|---|---|
| **Cb** | **Base** | **LD** |  | **x1** | **x2** | **S1** | **S2** | **S3** |
| 0 | S1 | 4 |  | 1 | 0 | 1 | 0 | 0 |
| 0 | S2 | 12 |  | 0 | 2 | 0 | 1 | 0 |
| 0 | S3 | 18 |  | 3 | 2 | 0 | 0 | 1 |
|  | **Zj** | 0 |  | 0 | 0 | 0 | 0 | 0 |
|  | **Zj − Cj** |  |  | −3 | −5 | 0 | 0 | 0 |

- **Zj** de cada columna = Σ (Cb de la fila × coeficiente de la columna).
- **Z** (valor actual) = Σ (Cb × LD).

### Reglas

| | Maximizar | Minimizar |
|---|---|---|
| **¿Es óptima?** | Todos los `Zj − Cj ≥ 0` | Todos los `Zj − Cj ≤ 0` |
| **Variable que entra** | La de `Zj − Cj` **más negativo** | La de `Zj − Cj` **más positivo** |
| **Variable que sale** | Menor razón `LD ÷ coeficiente`, solo con coeficientes **> 0** | Igual |
| **No acotado** | La columna que entra no tiene coeficientes > 0 | Igual |
| **Óptimos múltiples** | En la tabla óptima, una variable **no básica** tiene `Zj − Cj = 0` | Igual |
| **Empates** | Regla de Bland: menor índice (evita ciclos por degeneración) | Igual |

---

## 4. Alcance

**Entrada (igual que la referencia)**

- **Paso 1:** cantidad de variables (máx. 20) y de restricciones (máx. 50). Botones *Generar modelo* y *Limpiar*.
- **Paso 2:** objetivo *Maximizar* o *Minimizar*.
- **Paso 3:** coeficientes de la función objetivo (`X1 + X2 + … + Xn`) y de cada restricción, con signo `≤`, `≥` o `=` y lado derecho. Acepta negativos, decimales y fracciones (`3/4`).
- Botón *Resolver*.

**Lo que agregamos (lo que la referencia no da gratis)**

- Modelo en forma extendida antes de la primera tabla.
- Aviso de si se usará simplex directo o Dos Fases, y por qué.
- Todas las tablas de la Fase 1 y la Fase 2, con la columna, fila y pivote resaltados.
- Explicación escrita de cada cálculo de cada iteración (sección 8).
- Casos especiales explicados: infactible, no acotado, óptimos múltiples, degeneración, restricción redundante.
- Guardar problemas, historial, enlace para compartir, ejemplos precargados e impresión/PDF.

**Fuera de alcance (v1):** cuentas de usuario, método Gran M, método gráfico, análisis de sensibilidad, dual.

---

## 5. Tecnologías

### Frontend (IU / UX)

| Uso | Tecnología | Por qué |
|---|---|---|
| Lenguaje | **TypeScript** | Tipos compartidos con la API; menos errores con matrices de 20 × 50. |
| Framework | **React 19 + Vite** | El más usado; arranque rápido; mucha documentación. |
| Estilos y componentes | **Tailwind CSS + shadcn/ui** | Componentes accesibles (tabs, acordeones, diálogos). |
| Formularios | **React Hook Form + Zod** | Formularios dinámicos de n × m campos con validación en vivo. |
| Llamadas a la API | **TanStack Query** | Estados de carga, error y caché. |
| Estado del asistente | **Zustand** | Conserva los pasos 1–3 al navegar. |
| Rutas | **React Router** | `/calculadora`, `/solucion/:id`, `/historial`, `/ejemplos`. |
| Fórmulas | **KaTeX** | Fracciones y operaciones como en el cuaderno. |
| Tipos de la API | **openapi-typescript** | Genera tipos desde el OpenAPI de FastAPI. |
| Pruebas | **Vitest + Testing Library + Playwright** | Componentes y flujo completo. |

### Backend (lógica)

| Uso | Tecnología | Por qué |
|---|---|---|
| Lenguaje | **Python 3.12+** | `fractions.Fraction` nativo: resultados exactos como a mano. |
| Framework | **FastAPI + Uvicorn** | API REST; documentación Swagger automática en `/docs`. |
| Validación | **Pydantic v2** | Aplica los límites y convierte `"3/4"`, `"-2"`, `"0.5"` a fracción. |
| Motor simplex | **Propio, Python puro** | Es lo que se evalúa y debe registrar cada paso; no se usan librerías de optimización. |
| Pruebas | **pytest + SciPy** | `scipy.optimize.linprog` solo en tests para confirmar el valor óptimo. |
| Calidad | **Ruff + mypy** | Formato, lint y tipos. |
| Autenticación | **No aplica** | No hay cuentas de usuario. |

### Base de datos

| Uso | Tecnología | Por qué |
|---|---|---|
| Motor | **PostgreSQL 16+** | Relacional, gratuito, `JSONB` para guardar las tablas. |
| ORM | **SQLAlchemy 2.0** | ORM estándar de Python con modelos tipados. |
| Migraciones | **Alembic** | Versiona el esquema. |
| Driver | **psycopg 3** | Conexión Python ↔ PostgreSQL. |

### Infraestructura

| Uso | Tecnología |
|---|---|
| Entorno local | **Docker Compose** (web + api + db con un comando) |
| Repositorio y CI | **GitHub + GitHub Actions** (lint y pruebas en cada pull request) |
| Despliegue | Front en **Vercel**, API en **Render**, BD en **Neon** (revisar planes gratuitos vigentes) |

> **Alternativa si el equipo solo sabe JavaScript:** backend con **NestJS + TypeScript**, ORM **Prisma**, fracciones con **fraction.js**, misma BD PostgreSQL. La arquitectura y la API no cambian.

---

## 6. Arquitectura

```
┌──────────────────────┐   REST / JSON   ┌───────────────────────────────────────┐   SQLAlchemy   ┌──────────────┐
│  NAVEGADOR           │ ◄─────────────► │  API  (FastAPI)                       │ ◄────────────► │  PostgreSQL  │
│  React + TypeScript  │                 │                                       │                │              │
│                      │                 │  api/           rutas + Pydantic      │                │  problemas   │
│  · Asistente 3 pasos │                 │  services/      orquesta              │                │  restriccion │
│  · Vista de solución │                 │  simplex/       MOTOR PURO ──┐        │                │  soluciones  │
│  · Historial (local) │                 │  explicador     eventos→texto┘        │                │              │
│  · Ejemplos          │                 │  repositories/  acceso a datos        │                │              │
└──────────────────────┘                 └───────────────────────────────────────┘                └──────────────┘
```

**Reglas de diseño**

1. **El motor simplex es código puro:** no conoce HTTP ni la BD. Recibe un problema y devuelve la solución con todos los pasos. Se prueba aislado y se explica fácil en la sustentación.
2. **El motor emite eventos** (`tabla_inicial`, `calculo_zj`, `entra`, `razon_minima`, `pivote`, `operacion_fila`, `fin_fase`, …). El **explicador** los convierte en texto en español y fórmulas.
3. **El front no calcula nada**, solo muestra lo que devuelve la API.
4. `POST /resolver` **no necesita la BD**. La BD solo sirve para guardar, compartir e historial.

---

## 7. Algoritmo del motor

1. **Validar y convertir:** cada valor pasa a `Fraction`. Se rechazan límites excedidos, campos vacíos y valores no numéricos, indicando el campo exacto.
2. **Normalizar:** si un LD es negativo, multiplicar la fila por −1 e invertir el signo (≤ ↔ ≥).
3. **Construir la forma extendida:** agregar S, E y A según la sección 2 y nombrarlas en orden (`S1`, `E2`, `A2`, …).
4. **Decidir el método:** si hay alguna A → Dos Fases; si no → simplex directo (ir al paso 6).
5. **Fase 1:** `Min W = ΣA`. Iterar (paso 7) con regla de minimizar.
   - `W > 0` → estado `infactible`, fin.
   - `W = 0` → sacar artificiales básicas en 0 o eliminar filas redundantes; eliminar columnas A.
6. **Fase 2:** poner los Cj originales, actualizar Cb, recalcular Zj y Zj − Cj. Iterar (paso 7) con la regla del objetivo.
7. **Iteración:**
   1. Calcular Zj, Zj − Cj y Z.
   2. Prueba de optimalidad (sección 3). Si es óptima → paso 8.
   3. Elegir la variable que entra (Bland si hay empate).
   4. Prueba de razón mínima. Si no hay coeficientes > 0 → estado `no_acotado`, fin.
   5. Elegir la variable que sale (Bland si hay empate) y el pivote.
   6. Nueva fila pivote = fila ÷ pivote.
   7. Cada otra fila = fila − (su coeficiente en la columna pivote) × nueva fila pivote.
   8. Actualizar base y Cb. Registrar la tabla y todos los eventos.
   9. Límite de seguridad: 500 iteraciones.
8. **Resultado:** valores de variables de decisión, holguras y excesos; Z óptimo; estado `optimo` o `multiples_optimos`.

---

## 8. El paso a paso: qué se muestra

### Antes de iterar

- Modelo original escrito.
- Modelo en forma extendida, con una frase por restricción: *“La restricción 2 es ≥: se resta el exceso E2 y se suma la artificial A2”*.
- Método elegido y por qué: *“Hay restricciones ≥ / =, se usarán Dos Fases”* o *“Todas las restricciones son ≤, se usa simplex directo”*.

### En cada iteración

1. Tabla con Cj, Cb, Base, LD, Zj y Zj − Cj.
2. Cálculo de **Zj** columna por columna: `Zj(x1) = 0·1 + 5·0 + 0·3 = 0`.
3. Cálculo de **Zj − Cj**: `0 − 3 = −3`.
4. **Prueba de optimalidad** con el criterio de Max o Min y la conclusión.
5. **Variable que entra** y el motivo.
6. **Razón mínima** fila por fila, indicando las filas que no participan y por qué.
7. **Pivote**.
8. **Nueva fila pivote**, valor por valor.
9. **Operación de cada fila**, antes y después: `R3' = R3 − 2·R2'`.
10. **Solución básica** resultante y valor de Z (o W en Fase 1).

### Al cambiar de fase

- Valor final de W y conclusión (factible / infactible).
- Qué columnas se eliminan y por qué.
- Nuevos Cj y recálculo de Zj − Cj.

### Ejemplo trabajado (simplex directo)

```
Max Z = 3x1 + 5x2
s.a.   x1        ≤  4
            2x2  ≤ 12
       3x1 + 2x2 ≤ 18        x1, x2 ≥ 0
```

**Iteración 1** (tabla de la sección 3)

1. Todos los Cb son 0 → todos los Zj son 0; Z = 0.
2. Zj − Cj = −3, −5, 0, 0, 0.
3. Maximizar y hay valores negativos → **no es óptima**.
4. **Entra x2** (−5 es el más negativo).
5. Razón mínima: S1 no participa (coeficiente 0); S2: 12 ÷ 2 = **6**; S3: 18 ÷ 2 = 9 → **sale S2**.
6. Pivote = **2**.
7. Nueva fila x2 = S2 ÷ 2 → `LD 6 | 0, 1, 0, 1/2, 0` (Cb = 5).
8. S3 = S3 − 2·(nueva x2) → `LD 18 − 12 = 6 | 3, 0, 0, −1, 1`.
9. S1 no cambia (su coeficiente en x2 ya es 0).
10. Nuevos Zj con Cb = (0, 5, 0): Zj − Cj = −3, 0, 0, 5/2, 0; **Z = 30**.

**Iteración 2**

1. Hay un negativo (−3) → **entra x1**.
2. Razón mínima: S1: 4 ÷ 1 = 4; x2 no participa; S3: 6 ÷ 3 = **2** → **sale S3**. Pivote = 3.
3. Nueva fila x1 = S3 ÷ 3 → `LD 2 | 1, 0, 0, −1/3, 1/3` (Cb = 3).
4. S1 = S1 − 1·(nueva x1) → `LD 2 | 0, 0, 1, 1/3, −1/3`.
5. Nuevos Zj con Cb = (0, 5, 3): Zj − Cj = 0, 0, 0, 3/2, 1; **Z = 36**.
6. Todos ≥ 0 → **óptima**: **x1 = 2, x2 = 6, S1 = 2, Z = 36**.

### Ejemplo de tabla inicial de Fase 1 (Dos Fases)

```
Min Z = 4x1 + x2
s.a.  3x1 +  x2  = 3
      4x1 + 3x2 ≥ 6
       x1 + 2x2 ≤ 4          x1, x2 ≥ 0
```

Forma extendida: `3x1 + x2 + A1 = 3` · `4x1 + 3x2 − E2 + A2 = 6` · `x1 + 2x2 + S3 = 4`

Fase 1: `Min W = A1 + A2`

|  |  | **Cj →** | 0 | 0 | 0 | 1 | 1 | 0 |
|---|---|---|---|---|---|---|---|---|
| **Cb** | **Base** | **LD** | **x1** | **x2** | **E2** | **A1** | **A2** | **S3** |
| 1 | A1 | 3 | 3 | 1 | 0 | 1 | 0 | 0 |
| 1 | A2 | 6 | 4 | 3 | −1 | 0 | 1 | 0 |
| 0 | S3 | 4 | 1 | 2 | 0 | 0 | 0 | 1 |
|  | **Zj** | 9 | 7 | 4 | −1 | 1 | 1 | 0 |
|  | **Zj − Cj** |  | **7** | 4 | −1 | 0 | 0 | 0 |

Minimizar → entra el más positivo: **x1 (7)**. Razones: A1 3 ÷ 3 = **1**; A2 6 ÷ 4 = 3/2; S3 4 ÷ 1 = 4 → **sale A1**.
Resultado final esperado del problema: **x1 = 2/5, x2 = 9/5, Z = 17/5**.

---

## 9. API

Base: `/api/v1`. El contrato se define en el Sprint 0; mientras el motor no está listo, el front trabaja con respuestas de ejemplo.

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/resolver` | Resuelve y devuelve tablas y explicaciones. No guarda. |
| `POST` | `/problemas` | Guarda problema y solución; devuelve `slug` (enlace público). |
| `GET` | `/problemas/{slug}` | Reabre un problema guardado desde su enlace. |
| `GET` | `/ejemplos` | Problemas precargados. |
| `GET` | `/health` | Estado del servicio. |

Sin cuentas de usuario: el **historial** es una lista de `slug` guardada en el `localStorage` del navegador. El front consulta `GET /problemas/{slug}` para cada uno. Borrar del historial solo lo quita de esa lista local.

### Petición

```python
# backend/app/schemas/problema.py
class Restriccion(BaseModel):
    coeficientes: list[Fraccion]           # acepta "3/4", "-2", "0.5"
    signo: Literal["<=", ">=", "="]
    lado_derecho: Fraccion

class Problema(BaseModel):
    objetivo: Literal["max", "min"]
    coef_objetivo: list[Fraccion] = Field(min_length=1, max_length=20)
    restricciones: list[Restriccion] = Field(min_length=1, max_length=50)
```

```json
{
  "objetivo": "max",
  "coef_objetivo": ["3", "5"],
  "restricciones": [
    { "coeficientes": ["1", "0"], "signo": "<=", "lado_derecho": "4" },
    { "coeficientes": ["0", "2"], "signo": "<=", "lado_derecho": "12" },
    { "coeficientes": ["3", "2"], "signo": "<=", "lado_derecho": "18" }
  ]
}
```

### Respuesta (resumida)

```json
{
  "estado": "optimo",
  "metodo": "simplex",
  "modelo_extendido": {
    "texto": "Max Z = 3x1 + 5x2 + 0S1 + 0S2 + 0S3",
    "variables": [
      { "nombre": "S1", "tipo": "holgura", "restriccion": 1 }
    ]
  },
  "fases": [
    {
      "numero": 2,
      "iteraciones": [
        {
          "numero": 1,
          "columnas": ["x1", "x2", "S1", "S2", "S3"],
          "cj": ["3", "5", "0", "0", "0"],
          "base": ["S1", "S2", "S3"],
          "cb": ["0", "0", "0"],
          "ld": ["4", "12", "18"],
          "matriz": [["1","0","1","0","0"], ["0","2","0","1","0"], ["3","2","0","0","1"]],
          "zj": ["0", "0", "0", "0", "0"],
          "zj_menos_cj": ["-3", "-5", "0", "0", "0"],
          "z": "0",
          "entra": "x2",
          "sale": "S2",
          "pivote": { "fila": 1, "columna": 1, "valor": "2" },
          "pasos": [
            { "tipo": "calculo_zj", "columna": "x1", "expresion": "0·1 + 0·0 + 0·3", "valor": "0" },
            { "tipo": "optimalidad", "texto": "Maximizar: hay valores negativos en Zj − Cj (−3, −5). La tabla no es óptima." },
            { "tipo": "entra", "variable": "x2", "texto": "−5 es el valor más negativo." },
            { "tipo": "razon_minima", "filas": [
                { "base": "S1", "participa": false, "motivo": "coeficiente 0" },
                { "base": "S2", "participa": true, "calculo": "12 ÷ 2", "valor": "6", "elegida": true },
                { "base": "S3", "participa": true, "calculo": "18 ÷ 2", "valor": "9", "elegida": false }
            ]},
            { "tipo": "operacion_fila", "fila": "S3", "latex": "R_3' = R_3 - 2R_2'",
              "antes": ["18","3","2","0","0","1"], "despues": ["6","3","0","0","-1","1"] }
          ]
        }
      ]
    }
  ],
  "solucion": {
    "variables": { "x1": "2", "x2": "6" },
    "holguras_excesos": { "S1": "2", "S2": "0", "S3": "0" },
    "z": "36"
  }
}
```

- En Fase 1 `numero` es `1` y el valor se llama `w`. Si no hay artificiales, solo existe la fase `2`.
- Los números viajan como texto de fracción para no perder exactitud.
- Estados posibles: `optimo`, `multiples_optimos`, `no_acotado`, `infactible`.
- Errores de validación: HTTP 422 con la ruta del campo (`restricciones[3].coeficientes[1]`).

---

## 10. Base de datos

Datos de entrada en tablas relacionales; la solución completa (todas las tablas) en `JSONB` porque siempre se lee junta.

```
problemas 1 ── N restricciones
          1 ── N soluciones
```

No hay tabla de usuarios.

**problemas**

| Columna | Tipo |
|---|---|
| id | uuid PK |
| titulo | text |
| objetivo | enum (`max`, `min`) |
| num_variables | smallint (1–20) |
| coef_objetivo | jsonb |
| slug_publico | text, único |
| es_ejemplo | boolean |
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
| metodo | enum (`simplex`, `dos_fases`) |
| valor_optimo | text, nullable |
| num_iteraciones | smallint |
| resultado | jsonb (respuesta completa de `/resolver`) |
| version_motor | text |
| creado_en | timestamptz |

`version_motor` permite volver a resolver problemas guardados si el algoritmo cambia.

---

## 11. Interfaz (IU / UX)

### Pantallas

- **Calculadora:** los 3 pasos en una página con indicador de progreso. Volver al paso 1 no borra lo escrito si el tamaño no cambia. Botón *Cargar ejemplo*.
- **Solución:**
  - Resumen arriba: estado, Z óptimo, valores de las variables, método usado.
  - Modelo original y forma extendida.
  - Pestañas **Fase 1** / **Fase 2** (solo Fase 2 si no hubo artificiales).
  - Cada iteración: tabla + explicación. Modo *paso a paso* (anterior / siguiente) o *ver todo*.
  - Botones *Guardar*, *Compartir*, *Imprimir / PDF*.
- **Historial:** problemas guardados desde este navegador, con fecha, objetivo, estado y botón para reabrir.
- **Ejemplos:** simplex directo, Dos Fases, infactible, no acotado, óptimos múltiples.

### Componentes clave

| Componente | Función |
|---|---|
| `CampoFraccion` | Acepta `3/4`, `-2`, `0.5`; marca y explica lo inválido. |
| `EditorModelo` | Cuadrícula n × m con selector de signo por fila. |
| `TablaSimplex` | Filas Cj / Zj / Zj − Cj, columnas Cb, Base y LD fijas, desplazamiento horizontal, resaltado de columna que entra, fila que sale y pivote. |
| `PasoExplicado` | Texto + fórmula KaTeX + valores antes/después. |
| `NavegadorIteraciones` | Anterior / siguiente / ver todo. |
| `ResumenSolucion` | Estado, Z y valores, con color según el estado. |

### Criterios de UX

- Moverse con Tab/Enter en la cuadrícula, como en una hoja de cálculo.
- Validar antes de enviar; los errores del backend señalan la celda exacta.
- Móvil: la tabla se desplaza horizontalmente, la explicación no.
- Estilos de impresión para exportar a PDF.
- Contraste AA, foco visible y etiqueta en cada campo.

---

## 12. Estructura de carpetas

```
SimplexCalculadora/
├── PLAN.md
├── README.md
├── docker-compose.yml
├── .github/workflows/ci.yml
├── frontend/
│   ├── package.json
│   └── src/
│       ├── main.tsx
│       ├── pages/                 # Calculadora, Solucion, Historial, Ejemplos
│       ├── features/
│       │   ├── modelo/            # asistente pasos 1–3, store Zustand, esquemas Zod
│       │   └── solucion/          # TablaSimplex, PasoExplicado, NavegadorIteraciones
│       ├── components/ui/         # shadcn/ui
│       └── lib/api/               # cliente + tipos generados de OpenAPI
└── backend/
    ├── pyproject.toml
    ├── alembic/
    ├── app/
    │   ├── main.py
    │   ├── core/config.py
    │   ├── api/v1/                # resolver.py, problemas.py, ejemplos.py
    │   ├── schemas/               # Pydantic
    │   ├── services/
    │   ├── simplex/               # MOTOR PURO
    │   │   ├── fracciones.py      # parseo "3/4" → Fraction
    │   │   ├── forma_extendida.py # S, E, A
    │   │   ├── tabla.py           # Zj, Zj−Cj, razón mínima, pivoteo
    │   │   ├── reglas.py          # criterios Max/Min, Bland
    │   │   ├── dos_fases.py       # Fase 1, transición, Fase 2
    │   │   ├── eventos.py
    │   │   └── explicador.py      # eventos → texto y LaTeX
    │   ├── db/                    # models.py (SQLAlchemy), session.py
    │   └── repositories/
    └── tests/
        ├── simplex/
        └── api/
```

---

## 13. Pruebas

Cada caso compara estado y valor óptimo con `scipy.optimize.linprog` y, en los ejemplos a mano, las tablas intermedias.

| # | Caso | Verifica | Resultado esperado |
|---|---|---|---|
| 1 | Max 3x1 + 5x2 (sección 8) | Simplex directo | x1 = 2, x2 = 6, Z = 36 |
| 2 | Min −3x1 − 5x2 con las mismas restricciones | Minimizar sin Dos Fases | x1 = 2, x2 = 6, Z = −36 |
| 3 | Min 4x1 + x2 (sección 8) | Dos Fases con = y ≥ | x1 = 2/5, x2 = 9/5, Z = 17/5 |
| 4 | Max x1 + x2; x1 + x2 ≤ 2; x1 + x2 ≥ 4 | Infactible | `infactible` (W > 0) |
| 5 | Max x1 + x2; x1 − x2 ≤ 1 | No acotado | `no_acotado` |
| 6 | Max 2x1 + 4x2; x1 + 2x2 ≤ 5; x1 + x2 ≤ 4 | Óptimos múltiples | `multiples_optimos`, Z = 10 |
| 7 | −x1 − x2 ≤ −2 | Normalización de LD negativo | Se convierte en ≥ y usa Dos Fases |
| 8 | Restricción = repetida (redundante) | Artificial básica en 0 | Fila eliminada; óptimo correcto |
| 9 | Ejemplo de Beale | Degeneración + Bland | Termina sin ciclar |
| 10 | 20 variables × 50 restricciones aleatorio | Rendimiento | Coincide con SciPy; respuesta < 2 s |

---

## 14. Sprints

Cada sprint dura 1–2 semanas según el calendario del curso. Front y back avanzan en paralelo gracias al contrato de la API.

| Sprint | Backend | Frontend | Listo cuando |
|---|---|---|---|
| **0 · Base** | Repo, Docker Compose, CI, esquemas Pydantic y contrato OpenAPI | Wireframes de las 4 pantallas; proyecto Vite + Tailwind + shadcn | `docker compose up` levanta todo y `/docs` muestra el contrato |
| **1 · Simplex directo** | Fracciones, forma extendida, Zj − Cj, pivoteo, reglas Max/Min, eventos, explicador básico | Asistente de 3 pasos con validación; `CampoFraccion` | Casos 1 y 2 se resuelven de punta a punta |
| **2 · Dos Fases** | Fase 1, transición, Fase 2, casos especiales, Bland | `TablaSimplex` con resaltados, pestañas de fases, `PasoExplicado` | Pasan los 10 casos de prueba |
| **3 · Persistencia** | Modelos SQLAlchemy, migraciones Alembic, endpoints de problemas y ejemplos | Historial, ejemplos, enlace compartido, impresión | Un problema guardado se reabre idéntico desde su enlace |
| **4 · Entrega** | Pruebas de rendimiento (20 × 50), despliegue API y BD | Accesibilidad, móvil, Playwright, despliegue | URL pública funcionando, manual y guion de demo |

---

## 15. Preguntas pendientes para el profesor

Hay que confirmarlas antes del Sprint 1. Mientras tanto se trabaja con la **opción por defecto**.

| # | Pregunta | Opción por defecto del plan | Qué cambia si responde otra cosa |
|---|---|---|---|
| 1 | Para **minimizar**, ¿se resuelve directamente o se convierte a **Max (−Z)**? | Directo, como la calculadora de referencia: entra el Zj − Cj más positivo | Si es Max (−Z), las tablas muestran los Cj con signo cambiado y al final Z = −(valor óptimo). |
| 2 | ¿Los valores de las tablas se muestran en **fracciones, decimales o ambos**? | Fracciones exactas, con un botón para ver decimales | Si solo decimales, hay que definir cuántos decimales. |
| 3 | ¿Aprueba el formato **Cj / Cb / Zj / Zj − Cj**? | Sí, es el formato de la referencia | Si usa la fila Z con signo cambiado o Cj − Zj, cambia el signo que indica la variable que entra. |
| 4 | Si hay **empate** en la variable que entra o sale, ¿qué regla se usa? | Regla de Bland: la de menor índice (evita ciclos) | Si prefiere “la primera que aparece”, es un cambio pequeño en `reglas.py`. |
| 5 | ¿Exige **base de datos**, o basta con resolver? | Sí, para guardar problemas, enlaces y ejemplos | Si no la exige, se puede quitar PostgreSQL y el Sprint 3 se dedica a pulir. |
| 6 | Cuando hay **óptimos múltiples**, ¿se debe mostrar otra solución óptima? | Solo se avisa que existen | Si quiere verla, se hace un pivote extra con la variable no básica de Zj − Cj = 0. |
| 7 | ¿Se requiere algo fuera del alcance? (método gráfico para 2 variables, análisis de sensibilidad, dual) | No | Cada uno sería un sprint adicional. |

### Ya respondidas

- **Simplex extendido:** forma extendida + Dos Fases.
- **Gran M:** no, solo Dos Fases.
- **Cuentas de usuario:** no.

---

## 16. Fuentes

- Calculadora de referencia: <https://www.plandemejora.com/calculadora-metodo-simplex-online/>
- Método simplex paso a paso (convención Zj − Cj, reglas Max/Min): <https://www.plandemejora.com/metodo-simplex-paso-a-paso-ejemplos-maximizar-minimizar/>
- Teoría del método de las 2 fases: <https://juancruzindustrial.com/teoria-metodo-de-las-2-fases/>
- El método de las dos fases paso a paso: <https://reisdigital.es/investigaciones/metodo-de-las-2-fases-paso-a-paso-investigacion-de-operaciones/>
- Taha, H. A. *Investigación de Operaciones* — capítulo del método simplex (ejemplo de Dos Fases de la sección 8).
