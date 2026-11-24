# IM-PULSO: instrucciones para el webmaster

IM-PULSO es una aplicación web **estática** (HTML, CSS y JavaScript en un solo archivo). No necesita servidor propio,
base de datos, compilación ni librerías externas. Todo el procesamiento de audio ocurre en el navegador del visitante.

- Tamaño total de la carpeta `sitio/`: unos 450 KB (el `index.html` pesa unos 107 KB e incluye las tipografías).
- Peticiones a terceros: **ninguna**. No hay CDNs, fuentes externas, analítica ni cookies.
- Autoría: Creado por DJ CAS. Powered by Waro Labs.

## 1. Publicar en 3 pasos

1. **Personaliza** (desde esta carpeta, requiere Python 3):

       python3 configurar.py --dominio TU-DIRECCION.com --donar https://enlace-de-donacion --idioma auto

   - `--dominio`: la dirección final, sin https:// ni barra final. Si va en una subcarpeta, inclúyela:
     `--dominio midominio.com/impulso`.
   - `--donar`: enlace de donación (opcional, solo https). Si se omite, el botón muestra "link en bio".
   - `--idioma`: `auto` (según el dispositivo del visitante), `es` o `en`.
   - Sin Python: abre `sitio/index.html` con un editor, cambia las 4 apariciones de `TU-DOMINIO`, la línea
     `var DONATE_URL = "";` y, si quieres, `var DEFAULT_LANG = "auto";`.

2. **Sube el contenido de la carpeta `sitio/`** (incluidos los archivos ocultos `.htaccess` y `_headers`) a la raíz del sitio
   o a la subcarpeta elegida.
3. **Comprueba** con la lista del apartado 5.

Se recomienda **HTTPS** (necesario para instalar la app en pantalla de inicio y para que algunos navegadores no restrinjan funciones).

## 2. Archivos

- `index.html`: la aplicación completa (código, estilos y tipografías).
- `og.png` (1200 × 630): imagen de vista previa al compartir en WhatsApp, redes y mensajería.
- `icon-180.png`, `icon-192.png`, `icon-512.png`, `manifest.webmanifest`: icono y "añadir a pantalla de inicio".
- `_headers`: cabeceras de seguridad para Netlify y Cloudflare Pages.
- `.htaccess`: las mismas cabeceras para Apache, además del tipo MIME del manifiesto, compresión y caché.
- `404.html` y `robots.txt`.
- Fuera de `sitio/`: `configurar.py` (personalización) y `LICENCIAS-TERCEROS.txt`.

## 3. Cabeceras de seguridad (recomendadas)

La política de contenido está pensada para que la app **no pueda** conectarse a internet:

    Content-Security-Policy: default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; font-src data:; img-src 'self' data:; media-src blob: data:; connect-src 'none'; manifest-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'
    X-Content-Type-Options: nosniff
    Referrer-Policy: strict-origin-when-cross-origin
    Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
    X-Frame-Options: DENY

Ya están listas en `_headers` (Netlify, Cloudflare Pages) y en `.htaccess` (Apache). Para **Nginx**:

    location / {
      add_header Content-Security-Policy "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; font-src data:; img-src 'self' data:; media-src blob: data:; connect-src 'none'; manifest-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'" always;
      add_header X-Content-Type-Options nosniff always;
      add_header Referrer-Policy strict-origin-when-cross-origin always;
      add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()" always;
      add_header X-Frame-Options DENY always;
    }
    types { application/manifest+json webmanifest; }

GitHub Pages no permite cabeceras propias: la app funciona igual, solo se pierde esta capa extra.
Si el servidor devuelve el manifiesto con otro tipo MIME, el icono de instalación puede no aparecer.

## 4. Personalización

- **Enlace de donación:** `var DONATE_URL` (solo se acepta https; cualquier otro valor se ignora).
- **Idioma por defecto:** `var DEFAULT_LANG`. El visitante puede cambiarlo con el selector ES / EN, y se recuerda en su dispositivo.
  También se puede forzar con la dirección: `https://tusitio/#en` o `https://tusitio/#es`.
- **Textos:** el objeto `TR` dentro del script contiene todos los textos en español e inglés.
- **Colores:** variables CSS al inicio de `<style>` (`--blue`, `--lime`, `--ink`).
- **Datos guardados en el dispositivo (localStorage):** solo `impulso-lang` (idioma) e `impulso-how` (guía ya vista). No hay cookies.

## 5. Lista de verificación (10 minutos)

- [ ] Abre la página en un **teléfono** y en una **computadora**.
- [ ] Toca **"Probar con un beat de ejemplo"**: debe detectar 90 BPM. Pulsa **Reproducir**: las barras avanzan y el BPM sube.
- [ ] Carga un MP3 y un WAV propios: muestra el BPM y las opciones de BPM alternativas.
- [ ] Cambia ES / EN, y comprueba que el botón **?** reabre la guía "Así funciona".
- [ ] Comprueba el botón **Donar** (abre el enlace configurado en otra pestaña).
- [ ] Pega la dirección en WhatsApp: debe aparecer la imagen `og.png`. Si no, usa el depurador de enlaces de Facebook y pulsa "Scrape again".
- [ ] En el navegador, consola de desarrollador: no debe haber errores ni violaciones de CSP.
- [ ] En el celular: menú del navegador > "Añadir a pantalla de inicio".
- [ ] `curl -I https://tusitio/` debe mostrar las cabeceras de la sección 3.
- [ ] Prueba en **Safari (iPhone y Mac)**, ver el apartado 6.

## 6. Compatibilidad y puntos a vigilar

- **Probado:** Chromium (escritorio y vista móvil), con archivos WAV de 8 a 24 bits y 32 bits flotante de 8 a 96 kHz, MP3, OGG, FLAC; análisis de accesibilidad (axe) con 0 problemas; pruebas aleatorias de estrés sin errores; bloqueo máximo de pantalla medido de 99 ms.
- **No probado por falta de entorno:** Safari / iOS, Firefox, teléfonos Android reales y M4A/AAC. Revisa sobre todo Safari: la reproducción con "Mantener tono" a velocidades por debajo de 0,5× o por encima de 2× podría comportarse distinto.
- **Navegadores mínimos recomendados:** Chrome y Edge 90 o más, Safari 15.4 o más, Firefox 90 o más (usa Web Audio, async/await, CSS grid y `:focus-visible`).
- **Importante para el visitante:** si cambia de pestaña o bloquea el teléfono, algunos navegadores móviles pausan la página y la subida de tempo se detiene.

## 7. Incrustarla dentro de otra página (opcional)

Es mejor **enlazar** a una página dedicada. Si hace falta un iframe, hay que cambiar `frame-ancestors 'none'` por tu dominio
(`frame-ancestors https://tusitio.com`) y quitar `X-Frame-Options`, y usar algo así (sin atributo `sandbox`, no probado):

    <iframe src="https://app.tusitio.com/" title="IM-PULSO" style="width:100%;min-height:900px;border:0" allow="autoplay"></iframe>

## 8. Analítica (opcional)

La CSP actual bloquea cualquier conexión externa a propósito. Si añades una herramienta de estadísticas (por ejemplo
Plausible o GoatCounter), amplía `script-src` y `connect-src` solo para su dominio. Eventos útiles: clic en "Probar con un beat de ejemplo",
carga de un beat propio y clic en Donar. Recuerda actualizar el aviso de privacidad del sitio.

## 9. Actualizaciones

Para publicar una nueva versión basta con reemplazar `index.html` (y los demás archivos si cambian) y volver a ejecutar `configurar.py`.
Si cambias el contenido, limpia la caché de la red de distribución (CDN) si usas una.
