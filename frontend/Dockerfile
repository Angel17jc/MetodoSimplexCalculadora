# Producción: compila el frontend y lo sirve con Nginx, que además reenvía /api al backend.
FROM node:24-alpine AS compilacion

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=compilacion /app/dist /usr/share/nginx/html

EXPOSE 80
