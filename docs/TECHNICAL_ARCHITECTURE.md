# Arquitectura técnica y publicación

## Decisión
HTML, CSS y JavaScript sin dependencias, publicado en Cloudflare Pages (plan gratuito).

- **Por qué no Astro:** el entorno de desarrollo de Claude no tiene acceso a npm. Además, para una sola página, HTML estático da el menor peso posible, algo clave para las conexiones de la Amazonía. Si el sitio crece (blog, casos), se puede migrar a Astro reutilizando el mismo HTML y CSS.
- **Fuentes:** Outfit desde Google Fonts, con `display=swap`.
- **Sin rastreadores.** Cada botón de WhatsApp envía un mensaje inicial distinto, así Gabriela sabe desde qué sección le escriben.

## Publicación actual
El conector de Cloudflare no permite subir archivos estáticos sueltos. Por eso `scripts/construir.mjs` empaqueta todo `site/` dentro de un único `dist/_worker.js`, en «modo avanzado» de Pages. Ese worker:
- sirve cada archivo con su tipo de contenido;
- comprime el texto con gzip dentro del paquete;
- añade cabeceras de seguridad (CSP, HSTS, nosniff, Referrer-Policy y Permissions-Policy);
- define la caché: el HTML siempre se revalida y los recursos se guardan una hora.

Pasos:
1. `node scripts/construir.mjs`
2. Crear el despliegue de producción del proyecto `gabrielajimenez-consultoria` con `dist/_worker.js` y un `manifest` vacío. Se hace con la API de Cloudflare (POST `/accounts/{id}/pages/projects/gabrielajimenez-consultoria/deployments`, multipart).

## Publicación recomendada a futuro
Cuando Claude tenga permiso de escritura en `gjconsultoria/landing` (app de Claude para GitHub instalada en esa cuenta):
1. Conectar el proyecto de Pages al repositorio, con rama `main` y carpeta de salida `site`, sin comando de compilación.
2. Cada cambio aprobado se guarda en GitHub y Cloudflare lo publica solo.

## Calidad
- **Accesibilidad:** HTML semántico, enlace para saltar al contenido, foco visible y botones reales. Las pestañas de talleres se manejan con el teclado y los módulos son casillas de verificación reales. El texto principal tiene contraste de 17:1.
- **Movimiento:** se respeta `prefers-reduced-motion`. El parallax solo funciona con mouse, y las animaciones se pausan fuera de pantalla.
- **Diseño adaptable:** se probó a 1440 y 390 px sin desplazamiento horizontal. En celular aparece una barra fija con WhatsApp y Agendar.
- **SEO:** título, descripción, canonical, Open Graph con imagen de 1200×630, datos estructurados, robots.txt y sitemap.xml.

## Dominio
- **Actual:** `gabrielajimenez-consultoria.pages.dev`, gratis.
- **A futuro:** un dominio propio, si Gabriela decide comprarlo; `gabrielajimenez.com` ya está tomado. Se agrega en Pages → Custom domains.
