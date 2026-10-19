# Landing · Gabriela Jiménez, consultoría en comunicación

Sitio de una sola página para la consultoría en comunicación estratégica de Gabriela Jiménez, enfocada en la Amazonía colombiana (Amazonas, Caquetá, Putumayo, Guaviare, Guainía y Vaupés).

- **Dirección:** https://gabrielajimenez-consultoria.pages.dev
- **Alojamiento:** Cloudflare Pages, plan gratuito.
- **Código:** HTML, CSS y JavaScript sin dependencias.

## Resumen del proyecto

| Tema | Estado |
|---|---|
| Objetivo | Presentar a Gabriela, generar confianza y facilitar el contacto por agenda, WhatsApp o correo. Sin formularios. |
| Público | Organizaciones locales de la Amazonía, y fundaciones o proyectos de cooperación que trabajan allí. |
| Mensaje central | «Lo que la Amazonía hace merece llegar más lejos». |
| Contacto | WhatsApp +57 321 930 0818 · gabrielajimenez.consultoria@gmail.com · conversación gratuita de 30 minutos, de lunes a viernes de 10 a 12 y de 2 a 4. |
| Identidad visual | Ver `docs/BRAND_GUIDELINES.md`. |
| Contenido, servicios y talleres | Ver `docs/CONTENT_STRATEGY.md`. |
| Arquitectura y publicación | Ver `docs/TECHNICAL_ARCHITECTURE.md`. |
| Decisiones | Ver `docs/DECISION_LOG.md`. |
| Pendientes | Ver `docs/ROADMAP.md`. |

## Estructura

```
site/                 Lo que se publica
  index.html          Toda la página: textos, secciones y enlaces
  assets/styles.css   Estilos, colores, tipografía y animaciones
  assets/main.js      Interacciones (menú, selectores, talleres, parallax)
  favicon.svg         Ícono del navegador
  apple-touch-icon.png  Ícono para celulares
  og-image.jpg        Imagen al compartir el enlace (WhatsApp, redes)
  robots.txt, sitemap.xml
scripts/
  construir.mjs       Empaqueta site/ en dist/_worker.js para Cloudflare
  generar-imagenes.py Regenera el ícono y la imagen para compartir
docs/                 Documentación del proyecto
```

## Cómo cambiar un texto

1. Abre `site/index.html` y busca el texto con Ctrl+F.
2. Cámbialo sin tocar las etiquetas que lo rodean.
3. Los textos que cambian al hacer clic («¿Te suena alguna…?» y «Cómo trabajo») están en `site/assets/main.js`, en los bloques `necesidades` y `pasos`.
4. Publica de nuevo (ver abajo).

## Cómo activar el botón de agenda

Cuando exista la página de citas de Google Calendar, pega su enlace en `site/assets/main.js`:

```js
var AGENDA_URL = "https://calendar.app.google/...";
```

Mientras esté vacío, los botones de «Agendar» abren WhatsApp con un mensaje para proponer horario.

## Cómo publicar

```bash
node scripts/construir.mjs     # crea dist/_worker.js
```

Luego se sube `dist/_worker.js` como despliegue de Cloudflare Pages. Los detalles están en `docs/TECHNICAL_ARCHITECTURE.md`.

## Ver la página en tu computador

```bash
cd site && python3 -m http.server 8000
```

Después abre http://localhost:8000.
