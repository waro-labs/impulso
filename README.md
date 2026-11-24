# IM-PULSO — Battle Tempo Ramp Tool

App web estática (HTML+CSS+JS single-file) — detecta BPM y hace ramp de tempo paso a paso para batallas de freestyle. Sin backend, sin CDNs.

> Creado por DJ CAS. Powered by Waro Labs.

## Sitio
- `sitio/index.html` — app completa
- `sitio/og.png`, `icon-*.png`, `manifest.webmanifest` — PWA

## Deploy rápido
```bash
python3 configurar.py --dominio impulso.warolabs.com --donar https://... --idioma auto
# subir contenido de sitio/ al server/nginx/docker
```

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Licencia

**Código:** MIT — libre uso comercial, ver [`LICENSE`](LICENSE) (`Copyright (c) 2026 DJ CAS / Waro Labs`).

**Tipografías embebidas:** [Anton](https://fonts.google.com/specimen/Anton) y [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) — SIL Open Font License 1.1, ver [`LICENCIAS-TERCEROS.txt`](LICENCIAS-TERCEROS.txt).

`SPDX-License-Identifier: MIT AND OFL-1.1`

## Docker

Imagen estática `nginx:alpine` sirviendo `sitio/` en `127.0.0.1:4000` (puerto libre verificado en `warolabs-hostinger`, evita `3000`).

```bash
# local
docker build -t ghcr.io/waro-labs/impulso:latest .
docker run --rm -p 127.0.0.1:4001:80 ghcr.io/waro-labs/impulso:latest
curl -I http://127.0.0.1:4001/ # CSP + X-Frame-Options

# compose (prod, alistado — no ejecuta en server aquí)
docker compose up -d
curl -I http://127.0.0.1:4000/
```

> Infra `nginx/sites-available/impulso.warolabs.com.conf → :4000` + `cloudfront/impulso` + `bin/deploy-impulso-prod.sh` vive en `uno0uno/warolabs-server-infra#25` (no en este repo). Este compose solo alista.
