# Guía de despliegue

Cómo instalar Simplex Paso a Paso en el servidor de la facultad. Hay dos caminos: **con Docker** (recomendado) y **sin Docker**.

La base de datos es **opcional**. Sin ella funcionan resolver, el paso a paso, exportar/importar JSON, el PDF, el historial del navegador y los ejemplos; solo se desactiva *Compartir enlace*.

---

## 0. Antes de empezar: datos que hay que pedir a la facultad

- [ ] Usuario y clave, y forma de acceso (SSH, panel web o FTP).
- [ ] ¿Docker disponible? Si no: ¿Python 3.11+ y permiso para dejar un proceso corriendo?
- [ ] ¿PostgreSQL o MySQL? (opcional)
- [ ] Dominio o dirección asignada (ej. `simplex.facultad.edu` o `facultad.edu/simplex`).
- [ ] ¿HTTPS lo pone la facultad o lo configuramos nosotros?
- [ ] Puertos disponibles (80/443 o uno interno detrás de su proxy).

Si solo ofrecen hosting **PHP**, el backend en Python no funciona allí: avisar al equipo antes de seguir.

---

## 1. Con Docker (recomendado)

### Requisitos

- Docker Engine y Docker Compose v2.
- Git.

### Instalación

```bash
git clone https://github.com/Angel17jc/MetodoSimplexCalculadora.git
cd MetodoSimplexCalculadora
git switch main
cp .env.example .env
```

Editar `.env`:

```dotenv
ENTORNO=produccion
WEB_PORT=80

# Solo si se usa base de datos:
POSTGRES_USER=simplex
POSTGRES_PASSWORD=una-clave-segura
POSTGRES_DB=simplex
DATABASE_URL=postgresql+psycopg://simplex:una-clave-segura@db:5432/simplex
```

Sin base de datos, borrar la línea `DATABASE_URL`.

### Levantar

**Sin base de datos**

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

**Con base de datos** (crea PostgreSQL y aplica las migraciones)

```bash
docker compose -f docker-compose.prod.yml --profile db up -d --build
```

### Verificar

```bash
curl http://localhost/api/v1/health
# {"estado":"ok"}
```

Abrir `http://<servidor>/` en el navegador. En producción Nginx solo publica el frontend y `/api/`; la documentación Swagger (`/docs`) queda disponible únicamente en desarrollo.

### Actualizar a una nueva versión

```bash
git pull
docker compose -f docker-compose.prod.yml --profile db up -d --build
```

(Omitir `--profile db` si no se usa base de datos.)

### Ver registros

```bash
docker compose -f docker-compose.prod.yml logs -f api
docker compose -f docker-compose.prod.yml logs -f web
```

### Respaldo de la base de datos

```bash
docker compose -f docker-compose.prod.yml exec db pg_dump -U simplex simplex > respaldo.sql
```

Restaurar:

```bash
docker compose -f docker-compose.prod.yml exec -T db psql -U simplex simplex < respaldo.sql
```

---

## 2. Sin Docker

### Requisitos

- Python 3.11 o superior.
- Node.js 24 (solo para compilar el frontend; puede hacerse en otra computadora).
- Nginx.
- PostgreSQL (opcional).

### Backend

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install ".[db]"          # sin base de datos: pip install .
cp ../.env.example .env      # ajustar DATABASE_URL a localhost o borrarla
alembic upgrade head         # solo con base de datos
```

Servicio `systemd` en `/etc/systemd/system/simplex-api.service`:

```ini
[Unit]
Description=Simplex Paso a Paso - API
After=network.target

[Service]
WorkingDirectory=/opt/simplex/backend
EnvironmentFile=/opt/simplex/backend/.env
ExecStart=/opt/simplex/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2 --proxy-headers
Restart=always
User=simplex

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now simplex-api
```

### Frontend

```bash
cd frontend
npm ci
npm run build                # genera frontend/dist
```

Copiar `frontend/dist` al servidor (ej. `/opt/simplex/web`).

### Nginx

Usar `frontend/nginx.conf` como base, cambiando:

- `root /usr/share/nginx/html;` → `root /opt/simplex/web;`
- `proxy_pass http://api:8000;` → `proxy_pass http://127.0.0.1:8000;`

```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## 3. Casos especiales

### La facultad asigna una subruta (`facultad.edu/simplex`)

Hay que compilar el frontend con esa base y ajustar Nginx:

1. En `frontend/vite.config.ts` agregar `base: '/simplex/'`.
2. En React Router usar `basename: '/simplex'`.
3. En Nginx cambiar `location /` por `location /simplex/` y `location /api/` por `location /simplex/api/`.

Registrar el cambio con un commit: `build: ajustar docker-compose.prod.yml al servidor de la facultad`.

### HTTPS

- Si la facultad tiene un proxy con certificado, apuntarlo al puerto `WEB_PORT`.
- Si no, instalar Certbot en el servidor y usar su configuración para Nginx.

---

## 4. Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| La página carga pero *Resolver* falla | Nginx no llega a la API | Revisar `logs api` y que el servicio `api` esté arriba |
| `port is already allocated` | El puerto 80 está ocupado | Cambiar `WEB_PORT` en `.env` |
| *Compartir enlace* no aparece | No hay `DATABASE_URL` | Es lo esperado sin base de datos |
| Error `POSTGRES_PASSWORD` al levantar con `--profile db` | Falta la clave en `.env` | Definir `POSTGRES_PASSWORD` |
| La API responde 503 al guardar | La base de datos no está configurada o no responde | Revisar `DATABASE_URL` y `logs db` |
