# Wireframes

Bocetos de baja fidelidad de las pantallas principales. Sirven para acordar la distribución antes de programar; los colores y la tipografía se deciden en el Sprint 1.

Referencias: [PLAN.md §9 El paso a paso](../PLAN.md#9-el-paso-a-paso) y [§14 Interfaz](../PLAN.md#14-interfaz-iu--ux).

---

## 1. Calculadora (escritorio)

Misma distribución que la calculadora de referencia.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Σ Simplex Paso a Paso        Calculadora   Ejemplos   Historial             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ① Tamaño ─────── ② Objetivo ─────── ③ Modelo                                │
│                                                                              │
│  ┌─ Paso 1 ───────────────────────────────────────────────────────────────┐  │
│  │ Cantidad de Variables:      [ 2  ]  Máx. 20                            │  │
│  │ Cantidad de Restricciones:  [ 3  ]  Máx. 50                            │  │
│  │                         [ Generar Modelo ]  [ Limpiar ]                │  │
│  │                         Cargar ejemplo ▾    Importar JSON              │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─ Paso 2 ───────────────────────────────────────────────────────────────┐  │
│  │ Objetivo:  [ Maximizar          ▾ ]                                    │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌─ Paso 3 ───────────────────────────────────────────────────────────────┐  │
│  │ Función Objetivo:                                                      │  │
│  │ [ 10 ] X₁ +  [ 15 ] X₂                                                 │  │
│  │                                                                        │  │
│  │ Restricciones                                                          │  │
│  │ Restricción 1:  [ 1  ] X₁ +  [    ] X₂   [ ≤ ▾ ]  [ 400 ]              │  │
│  │ Restricción 2:  [ 15 ] X₁ +  [ 20 ] X₂   [ ≥ ▾ ]  [ 500 ]              │  │
│  │                 ⓘ Esta restricción usará variable artificial (Dos Fases)│  │
│  │ Restricción 3:  [    ] X₁ +  [ 8  ] X₂   [ = ▾ ]  [ 100 ]              │  │
│  │                 ⓘ Esta restricción usará variable artificial (Dos Fases)│  │
│  │                                                                        │  │
│  │ X₁, X₂ ≥ 0                                                             │  │
│  │                         [ Resolver ]  [ Limpiar ]                      │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  API conectada ●                                                             │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Celda con error**

```
│ Restricción 2:  [ 1,5,2 ] X₁ + …
│                  ▲
│                  Escribe un número, un decimal (0.5) o una fracción (3/4)
```

---

## 2. Solución: modo paso a paso (escritorio)

La tabla queda fija a la izquierda; la operación actual y el registro de la iteración, a la derecha.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Σ Simplex Paso a Paso        Calculadora   Ejemplos   Historial             │
├──────────────────────────────────────────────────────────────────────────────┤
│  Ejemplo del profesor (maximizar)                                            │
│  Simplex extendido · Dos Fases       Estado: Óptimo      Z = 8375/2          │
│  x₁ = 400   x₂ = 25/2                                                        │
│  [ Paso a paso | Ver todo ]   [ Ver decimales ]   Exportar JSON  Exportar PDF│
├──────────────────────────────────────────────────────────────────────────────┤
│  [ Fase 1 ]  Fase 2                                                          │
│                                                                              │
│  ▸ Preparación de la tabla (5 pasos)                                         │
│  ▾ Iteración 1                                                               │
│  ┌──────────────────────────────────────────┐ ┌───────────────────────────┐  │
│  │        Cj →   0    0    0    0   −1   −1 │ │ Paso 12 de 58             │  │
│  │ Cb Base   b   x₁  [x₂]  S₁   S₂  A₁   A₂ │ │ PRUEBA DE RAZÓN           │  │
│  │ 0  S₁   400    1  [ 0]   1    0   0    0 │ │                           │  │
│  │ −1 A₁   500   15  [20]   0   −1   1    0 │ │ Se divide cada b entre el │  │
│  │ −1 A₂   100    0  [▓8▓]  0    0   0    1 │ │ valor de la columna x₂.   │  │
│  │ ──────────────────────────────────────── │ │                           │  │
│  │    W   −600  −15 [−28]   0    1   0    0 │ │ S₁: 400 ÷ 0 → no se       │  │
│  └──────────────────────────────────────────┘ │     considera (infinito)  │  │
│    [ ] columna que entra   ▓ pivote            │ A₁: 500 ÷ 20 = 25         │  │
│                                               │ A₂: 100 ÷ 8 = 25/2 ← menor│  │
│                                               └───────────────────────────┘  │
│                                               ┌─ Registro de la iteración ─┐  │
│                                               │ ✓ Prueba de optimalidad    │  │
│                                               │ ✓ Entra x₂ (−28)           │  │
│                                               │ ● Prueba de razón          │  │
│                                               └───────────────────────────┘  │
│  ▸ Iteración 2                                                               │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│   ⏮ Inicio   ◀ Anterior   ▶ Siguiente   ⏭ Sig. iteración   ⏵ Reproducir  1x  │
│   Atajos: ← →                                                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Paso de operación de fila** (panel derecho)

```
┌───────────────────────────────────────┐
│ Paso 14 de 58 · OPERACIÓN DE FILA     │
│                                       │
│   R₂' = −20 · R₃' + R₂                │
│                                       │
│   antes   [ 15  20   0  −1   1    0  │ 500 ] │
│   suma    [  0 −20   0   0   0  −5/2 │ −250 ] │
│   después [ 15   0   0  −1   1  −5/2 │ 250 ] │
└───────────────────────────────────────┘
```

---

## 3. Solución: modo paso a paso (móvil)

```
┌──────────────────────────────┐
│ ☰  Simplex Paso a Paso       │
├──────────────────────────────┤
│ Óptimo · Z = 8375/2          │
│ x₁ = 400  x₂ = 25/2          │
│ [Fase 1] Fase 2              │
├──────────────────────────────┤
│ ◀ desplazar tabla ▶          │
│ ┌──────────────────────────┐ │
│ │Base  b   x₁ [x₂] S₁  …   │ │
│ │S₁   400   1 [ 0]  1  …   │ │
│ │A₁   500  15 [20]  0  …   │ │
│ │A₂   100   0 [▓8▓] 0  …   │ │
│ │W   −600 −15 [−28] 0  …   │ │
│ └──────────────────────────┘ │
│ PRUEBA DE RAZÓN              │
│ S₁: 400 ÷ 0 → no se considera│
│ A₁: 500 ÷ 20 = 25            │
│ A₂: 100 ÷ 8 = 25/2 ← menor   │
├──────────────────────────────┤
│  ◀        12 / 58        ▶   │
└──────────────────────────────┘
```

---

## 4. Ejemplos

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Ejemplos                                                                    │
│                                                                              │
│  Ejemplo del profesor (maximizar)                         [ Abrir ]          │
│  Dos Fases con restricciones ≤, ≥ y =. Resultado: x1 = 400, x2 = 25/2 …      │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Ejemplo del profesor (minimizar)                         [ Abrir ]          │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Simplex normal                                           [ Abrir ]          │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Dos Fases al minimizar · Problema infactible · No acotado · Óptimos múltiples│
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Historial

Problemas resueltos en este navegador (no hay cuentas de usuario).

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Historial                                               [ Importar JSON ]   │
│                                                                              │
│  Fecha            Título                         Objetivo  Estado            │
│  13/09/2026 10:21 Ejemplo del profesor           Max       ● Óptimo   Abrir  │
│  12/09/2026 18:05 Tarea 3 - ejercicio 2          Min       ● Infactible Abrir│
│                                                                              │
│  Los problemas se guardan solo en este navegador.   [ Borrar historial ]     │
└──────────────────────────────────────────────────────────────────────────────┘
```
