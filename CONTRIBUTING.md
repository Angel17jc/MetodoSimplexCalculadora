# Guía de contribución

## Regla principal

Cada cambio, por mínimo que sea, va en **su propio commit**. Un commit hace una sola cosa y el proyecto debe seguir funcionando después de cada uno. El orden de los commits de cada sprint está en [PLAN.md](PLAN.md#plan-de-commits).

## Ramas

| Rama | Uso |
|---|---|
| `main` | Versión estable. Solo recibe merges de `develop` al terminar un sprint. |
| `develop` | Integración de lo terminado. |
| `feature/sprint-N-tema` | Trabajo diario. Se crea desde `develop` y vuelve a `develop` con Pull Request. |

```bash
git switch develop
git pull
git switch -c feature/sprint-1-simplex-normal
```

## Mensajes de commit

Se usa [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/) en español:

```
tipo(ámbito): descripción corta
```

- Descripción en **imperativo** (“agregar”, “corregir”), en minúsculas y **sin punto final**.
- Máximo 72 caracteres en la primera línea.
- Si hace falta explicar el porqué, se deja una línea en blanco y se escribe el cuerpo.

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
| `style` | Formato sin cambiar código |

**Ámbitos:** `backend`, `frontend`, `simplex`, `explicador`, `exportacion`, `api`, `db`. Sin ámbito cuando afecta a todo el repositorio.

**Ejemplos**

```
feat(simplex): agregar prueba de razón mínima excluyendo ceros y negativos
test(simplex): probar prueba de razón mínima
fix(frontend): corregir foco al pasar a la siguiente restricción
docs: agregar guía de despliegue
```

## Antes de cada commit

**Backend** (desde `backend/`):

```bash
ruff check .
ruff format --check .
mypy app
pytest
```

**Frontend** (desde `frontend/`):

```bash
npm run lint
npm run test
npm run build
```

## Registro de avance

Cada vez que subas trabajo a `develop` o `main`, actualiza [docs/avance.md](docs/avance.md): marca los pasos terminados con tu usuario y el hash del commit, el siguiente paso y una línea en el historial. Va en su propio commit:

```
docs: actualizar registro de avance
```

Así el equipo sabe siempre hasta dónde se llegó sin tener que revisar el historial de Git.

## Pull Requests

- Título con el mismo formato que un commit.
- Descripción: qué cambia, cómo probarlo y capturas si hay cambios visuales.
- Debe pasar la integración continua (GitHub Actions) antes de hacer merge.
- Al menos una revisión de otro integrante.
