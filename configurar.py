#!/usr/bin/env python3
"""Personaliza el sitio de IM-PULSO antes de publicarlo.

Uso:
  python3 configurar.py --dominio midominio.com --donar https://ko-fi.com/usuario --idioma auto

  --dominio  Dirección final del sitio, sin https:// ni barra final (para la vista previa al compartir).
  --donar    Enlace de donación (debe empezar por https://). Opcional.
  --idioma   auto (según el dispositivo), es o en. Por defecto: auto.
  --carpeta  Carpeta del sitio. Por defecto: ./sitio
"""
import argparse, re, sys, pathlib

p = argparse.ArgumentParser(description="Personaliza IM-PULSO")
p.add_argument("--dominio", required=True)
p.add_argument("--donar", default="")
p.add_argument("--idioma", default="auto", choices=["auto", "es", "en"])
p.add_argument("--carpeta", default="sitio")
a = p.parse_args()

dom = a.dominio.strip().replace("https://", "").replace("http://", "").strip("/")
if not re.fullmatch(r"[A-Za-z0-9.-]+(:[0-9]+)?(/[A-Za-z0-9._~/-]*)?", dom):
    sys.exit("Dominio no válido: " + a.dominio)
if a.donar and not a.donar.startswith("https://"):
    sys.exit("El enlace de donación debe empezar por https://")
if '"' in a.donar or "\\" in a.donar or "<" in a.donar:
    sys.exit("El enlace de donación contiene caracteres no permitidos")

f = pathlib.Path(a.carpeta) / "index.html"
h = f.read_text(encoding="utf-8")
n = h.count("TU-DOMINIO")
h = h.replace("TU-DOMINIO", dom)
h, c1 = re.subn(r'var DONATE_URL = "[^"]*";', lambda m: 'var DONATE_URL = "%s";' % a.donar, h, count=1)
h, c2 = re.subn(r'var DEFAULT_LANG = "[^"]*";', lambda m: 'var DEFAULT_LANG = "%s";' % a.idioma, h, count=1)
if c1 != 1 or c2 != 1:
    sys.exit("No se encontraron las variables DONATE_URL / DEFAULT_LANG en index.html")
f.write_text(h, encoding="utf-8")
print("Listo: %d referencias de dominio actualizadas; donación: %s; idioma por defecto: %s" % (n, a.donar or "(vacía: muestra 'link en bio')", a.idioma))
