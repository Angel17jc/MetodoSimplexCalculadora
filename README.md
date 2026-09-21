# Simplex Paso a Paso

Calculadora web del **método simplex** (simplex normal y **Dos Fases**) para **Maximizar y Minimizar**, que muestra **cada operación interna** una por una: la fila Z, la variable que entra, la prueba de razón, el pivote y cada operación de Gauss-Jordan.

> Proyecto de la asignatura Investigación de Operaciones.

## Estado

| Sprint | Estado |
|---|---|
| 0 · Base | ✅ Completado |
| 1 · Simplex normal | 🔄 En progreso |
| 2 · Dos Fases | Pendiente |
| 3 · Exportar e importar | Pendiente |
| 4 · Entrega | Pendiente |

El detalle de qué está hecho, quién lo hizo y cuál es el siguiente paso está en **[docs/avance.md](docs/avance.md)**.

## Tecnologías

| Parte | Tecnologías |
|---|---|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, shadcn/ui, React Router, TanStack Query, Zustand, React Hook Form, Zod |
| Backend | Python, FastAPI, Pydantic; motor simplex propio con fracciones exactas |
| Base de datos (opcional) | PostgreSQL, SQLAlchemy, Alembic |
| Pruebas y calidad | pytest, Ruff, mypy · Vitest, Testing Library, oxlint |
| Infraestructura | Docker Compose, Nginx, GitHub Actions |

## Inicio rápido con Docker

Requisitos: Docker con Docker Compose.

```bash
cp .env.example .env        # opcional: cambia puertos o credenciales
docker compose up --build
```

| Servicio | Dirección |
|---|---|
| Aplicación | <http://localhost:5173> |
| API (Swagger) | <http://localhost:8000/docs> |

Los cambios en `frontend/src` y `backend/app` se recargan solos. Para detener: `docker compose down`.

## Desarrollo sin Docker

Requisitos: Python 3.11+ y Node.js 24.

### Backend

```bash
cd backend
python -m venv .venv
# Windows:        .venv\Scripts\activate
# Linux / macOS:  source .venv/bin/activate
pip install -e ".[dev,db]"
uvicorn app.main:app --reload
```

La base de datos es opcional: sin `DATABASE_URL` la API funciona igual.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite reenvía `/api` a `http://localhost:8000`.

## Comandos frecuentes

| Qué | Dónde | Comando |
|---|---|---|
| Pruebas | `backend/` | `pytest` |
| Lint y formato | `backend/` | `ruff check .` · `ruff format .` |
| Tipos | `backend/` | `mypy app tests` |
| Regenerar `openapi.json` | `backend/` | `python -m app.scripts.exportar_openapi` |
| Crear migración | `backend/` | `alembic revision --autogenerate -m "descripción"` |
| Aplicar migraciones | `backend/` | `alembic upgrade head` |
| Pruebas | `frontend/` | `npm run test` |
| Lint | `frontend/` | `npm run lint` |
| Build | `frontend/` | `npm run build` |
| Regenerar tipos de la API | `frontend/` | `npm run generar:tipos` |

Si cambias la API: regenera `openapi.json` y después los tipos del frontend. La integración continua falla si quedan desactualizados.

## Estructura

```
├── backend/            API FastAPI, motor simplex, migraciones y pruebas
│   ├── app/
│   │   ├── api/v1/     rutas
│   │   ├── schemas/    contrato (Pydantic)
│   │   ├── ejemplos/   problemas precargados (.simplex.json)
│   │   └── db/         modelos y sesión (opcional)
│   └── openapi.json    contrato generado
├── frontend/           React + Vite
│   └── src/
│       ├── pages/
│       ├── components/
│       └── lib/api/    cliente y tipos generados
├── docs/               wireframes y guía de despliegue
├── docker-compose.yml        desarrollo
└── docker-compose.prod.yml   producción
```

## Documentación

- [PLAN.md](PLAN.md): alcance, algoritmo, arquitectura, sprints y plan de commits.
- [CONTRIBUTING.md](CONTRIBUTING.md): ramas, convención de commits y revisiones.
- [docs/wireframes.md](docs/wireframes.md): bocetos de las pantallas.
- [docs/despliegue.md](docs/despliegue.md): instalación en el servidor de la facultad.
