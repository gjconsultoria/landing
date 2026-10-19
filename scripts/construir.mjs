// Empaqueta la carpeta site/ en un único dist/_worker.js para Cloudflare Pages.
// Sin dependencias: node scripts/construir.mjs
//
// Por qué un _worker.js: el conector de Cloudflare publica despliegues sin acceso a la
// carga de archivos estáticos, así que el sitio viaja dentro del worker. Cuando el
// repositorio esté conectado a Cloudflare Pages por Git, se puede publicar site/ tal cual.
import { readFileSync, readdirSync, statSync, mkdirSync, writeFileSync } from "node:fs";
import { join, relative, extname } from "node:path";
import { gzipSync } from "node:zlib";

const RAIZ = new URL("..", import.meta.url).pathname;
const SITIO = join(RAIZ, "site");
const SALIDA = join(RAIZ, "dist");

const TIPOS = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".webmanifest": "application/manifest+json",
};
const TEXTO = new Set([".html", ".css", ".js", ".svg", ".xml", ".txt", ".webmanifest"]);

function recorrer(dir) {
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? recorrer(p) : [p];
  });
}

const archivos = {};
for (const ruta of recorrer(SITIO)) {
  const ext = extname(ruta);
  if (!TIPOS[ext]) continue;
  const bytes = readFileSync(ruta);
  const web = "/" + relative(SITIO, ruta).split("\\").join("/");
  const gz = TEXTO.has(ext);
  archivos[web] = { t: TIPOS[ext], z: gz, d: (gz ? gzipSync(bytes, { level: 9 }) : bytes).toString("base64") };
}

const worker = `// Generado por scripts/construir.mjs. No editar a mano: edita site/ y vuelve a construir.
const ARCHIVOS = ${JSON.stringify(archivos)};
const cache = new Map();
const SEGURIDAD = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "X-Frame-Options": "SAMEORIGIN",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=(), interest-cohort=()",
  "Strict-Transport-Security": "max-age=31536000",
  "Content-Security-Policy": "default-src 'self'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://cloudflareinsights.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self'"
};
function aBytes(b64) { const s = atob(b64); const u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return u; }
async function contenido(ruta) {
  if (cache.has(ruta)) return cache.get(ruta);
  const a = ARCHIVOS[ruta];
  let bytes = aBytes(a.d);
  if (a.z) bytes = new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"))).arrayBuffer());
  cache.set(ruta, bytes);
  return bytes;
}
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (request.method !== "GET" && request.method !== "HEAD") return new Response("Método no permitido", { status: 405 });
    let ruta = decodeURIComponent(url.pathname);
    if (ruta.endsWith("/")) ruta += "index.html";
    if (!ARCHIVOS[ruta] && ARCHIVOS[ruta + ".html"]) ruta += ".html";
    const existe = !!ARCHIVOS[ruta];
    if (!existe) ruta = "/index.html";
    const a = ARCHIVOS[ruta];
    const cuerpo = await contenido(ruta);
    const esHtml = a.t.startsWith("text/html");
    const cabeceras = new Headers(SEGURIDAD);
    cabeceras.set("Content-Type", a.t);
    cabeceras.set("Cache-Control", esHtml ? "public, max-age=0, must-revalidate" : "public, max-age=3600, stale-while-revalidate=86400");
    return new Response(request.method === "HEAD" ? null : cuerpo, { status: existe ? 200 : 404, headers: cabeceras });
  }
};
`;

mkdirSync(SALIDA, { recursive: true });
writeFileSync(join(SALIDA, "_worker.js"), worker);
const kb = (Buffer.byteLength(worker) / 1024).toFixed(1);
console.log(`dist/_worker.js listo: ${Object.keys(archivos).length} archivos, ${kb} KB`);
