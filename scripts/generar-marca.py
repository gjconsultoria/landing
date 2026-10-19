"""Genera los logos de la marca (PNG y JPG) y la foto de la firma de correo.
Uso: python3 scripts/generar-marca.py [ruta/a/foto.jpg]
Salida: brand/logos/{png,jpg}/ y site/firma/foto-firma.png
Nota: Outfit no está instalada en este equipo; el texto se dibuja con Poppins (geométrica, muy parecida)."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = "/usr/share/fonts/truetype/google-fonts/"
TINTA = (18, 26, 22)
GRIS = (61, 72, 66)
# Mismos degradados del logo aprobado (favicon.svg): x, y, radio, paradas (posición, color, opacidad)
CAPAS = [
    (0.26, 0.30, 0.40, [(0, (217, 240, 140), .9), (1, (217, 240, 140), 0)]),
    (0.30, 0.74, 0.44, [(0, (255, 246, 184), 1), (.4, (247, 216, 74), .95), (1, (247, 216, 74), 0)]),
    (0.52, 0.50, 0.46, [(0, (11, 111, 120), 1), (.45, (31, 163, 138), .9), (1, (31, 163, 138), 0)]),
    (0.70, 0.42, 0.46, [(0, (22, 21, 79), 1), (.45, (43, 45, 143), .95), (1, (43, 45, 143), 0)]),
]

def fuente(peso, tam):
    return ImageFont.truetype(FUENTES + "Poppins-%s.ttf" % peso, int(tam))

def _gradiente(n, cx, cy, r, paradas, esc):
    y, x = np.mgrid[0:n, 0:n]
    t = np.clip(np.sqrt(((x + .5) / n - cx) ** 2 + ((y + .5) / n - cy) ** 2) / (r * esc), 0, 1)
    offs = [p[0] for p in paradas]
    col = np.stack([np.interp(t, offs, [p[1][k] for p in paradas]) for k in range(3)], -1)
    alfa = np.interp(t, offs, [p[2] for p in paradas])
    return col, alfa[..., None]

def campo(n, grano=0.10, escala=1.0, relleno=(244, 248, 236)):
    """Campo de color cuadrado con los degradados del logo."""
    img = np.zeros((n, n, 3)) + np.array(relleno, float)
    for cx, cy, r, paradas in CAPAS:
        col, a = _gradiente(n, cx, cy, r, paradas, escala)
        img = img * (1 - a) + col * a
    out = Image.fromarray(np.clip(img, 0, 255).astype("uint8"))
    if grano:
        rng = np.random.default_rng(7)
        r = np.clip(1 - np.abs(rng.normal(0, 1, (n, n))) * grano * .6, 0, 1)
        out = ImageChops.multiply(out, Image.fromarray((r * 255).astype("uint8")).convert("RGB"))
    return out

def aura(n, grano=0.10, nitido=False):
    """Aura circular RGBA (fondo transparente)."""
    ss = 2
    base = campo(n, grano).convert("RGBA")
    m = Image.new("L", (n * ss, n * ss), 0)
    ImageDraw.Draw(m).ellipse([n * ss * .016, n * ss * .016, n * ss * .984, n * ss * .984], fill=255)
    base.putalpha(m.resize((n, n), Image.LANCZOS))
    return base

def monograma(n, grano=0.10, completo=False):
    """Aura con un círculo de vidrio y las letras GJ."""
    if completo:
        img = campo(n, grano, escala=1.7).convert("RGBA")
    else:
        img = aura(n, grano)
    c = n / 2
    r = n * (0.255 if completo else 0.235)
    sombra = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse([c - r, c - r + n * .012, c + r, c + r + n * .012], fill=(22, 21, 79, 70))
    img = Image.alpha_composite(img, sombra.filter(ImageFilter.GaussianBlur(n * 0.02)))
    vidrio = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(vidrio)
    d.ellipse([c - r, c - r, c + r, c + r], fill=(255, 255, 255, 232), outline=(255, 255, 255, 255), width=max(2, int(n * .006)))
    img = Image.alpha_composite(img, vidrio)
    f = fuente("Light", r * 1.05)
    txt = "GJ"
    d = ImageDraw.Draw(img)
    b = d.textbbox((0, 0), txt, font=f)
    w, h = b[2] - b[0], b[3] - b[1]
    d.text((c - w / 2 - b[0], c - h / 2 - b[1]), txt, font=f, fill=TINTA + (255,))
    return img

def sobre_blanco(rgba):
    fondo = Image.new("RGB", rgba.size, (255, 255, 255))
    fondo.paste(rgba, mask=rgba.split()[3])
    return fondo

def texto_bloque(ancho_aura, color_nombre, color_sub):
    """Devuelve (nombre, subtítulo) ya dibujados como capa RGBA."""
    f1, f2 = fuente("Regular", ancho_aura * 0.30), fuente("Light", ancho_aura * 0.165)
    t1, t2 = "Gabriela Jiménez", "Consultoría en comunicación"
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    w1 = tmp.textlength(t1, font=f1); w2 = tmp.textlength(t2, font=f2)
    w = int(max(w1, w2)) + 4; h = int(ancho_aura * 0.62)
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.text((0, 0), t1, font=f1, fill=color_nombre + (255,))
    d.text((0, ancho_aura * 0.36), t2, font=f2, fill=color_sub + (255,))
    return capa

def horizontal(marca, claro=True, ancho_marca=420):
    n = ancho_marca
    m = marca.resize((n, n), Image.LANCZOS)
    t = texto_bloque(n, TINTA if claro else (255, 255, 255), GRIS if claro else (225, 232, 228))
    pad = int(n * .12)
    lienzo = Image.new("RGBA", (n + t.width + pad * 3, n + pad * 2), (0, 0, 0, 0))
    lienzo.alpha_composite(m, (pad, pad))
    lienzo.alpha_composite(t, (pad * 2 + n, (lienzo.height - t.height) // 2 - int(n * .01)))
    return lienzo

def vertical(marca, claro=True, ancho_marca=600):
    n = ancho_marca
    m = marca.resize((n, n), Image.LANCZOS)
    t = texto_bloque(n * 0.9, TINTA if claro else (255, 255, 255), GRIS if claro else (225, 232, 228))
    pad = int(n * .1)
    lienzo = Image.new("RGBA", (max(n, t.width) + pad * 2, n + t.height + pad * 3), (0, 0, 0, 0))
    lienzo.alpha_composite(m, ((lienzo.width - n) // 2, pad))
    lienzo.alpha_composite(t, ((lienzo.width - t.width) // 2, pad * 2 + n))
    return lienzo

def solo_texto(claro=True, tam=420):
    t = texto_bloque(tam, TINTA if claro else (255, 255, 255), GRIS if claro else (225, 232, 228))
    pad = 40
    l = Image.new("RGBA", (t.width + pad * 2, t.height + pad * 2), (0, 0, 0, 0))
    l.alpha_composite(t, (pad, pad))
    return l

def guardar(rgba, carpeta_base, nombre, jpg_sobre=(255, 255, 255)):
    os.makedirs(os.path.join(carpeta_base, "png"), exist_ok=True)
    os.makedirs(os.path.join(carpeta_base, "jpg"), exist_ok=True)
    rgba.save(os.path.join(carpeta_base, "png", nombre + ".png"), optimize=True)
    fondo = Image.new("RGB", rgba.size, jpg_sobre)
    fondo.paste(rgba, mask=rgba.split()[3])
    fondo.save(os.path.join(carpeta_base, "jpg", nombre + ".jpg"), quality=92, optimize=True, subsampling=0)

def anillo_foto(ruta, salida, n=480):
    """Foto circular con anillo de aura (índigo, verde agua, amarillo, lima)."""
    foto = Image.open(ruta).convert("RGB")
    cx, cy, lado = 440, 395, 640  # recorte sobre el rostro y los hombros
    foto = foto.crop((cx - lado // 2, cy - lado // 2 - 40, cx + lado // 2, cy + lado // 2 - 40))
    ss = 3  # supermuestreo para bordes suaves
    N = n * ss
    ring = 0.035
    interior = int(N * (1 - 2 * (ring + 0.022)))
    foto = foto.resize((interior, interior), Image.LANCZOS)
    y, x = np.mgrid[0:N, 0:N]
    ang = (np.arctan2(y - N / 2, x - N / 2) / (2 * math.pi)) % 1.0
    pts = [(0.0, (43, 45, 143)), (0.28, (31, 163, 138)), (0.55, (247, 216, 74)), (0.78, (217, 240, 140)), (1.0, (43, 45, 143))]
    g = np.zeros((N, N, 3))
    for (a0, c0), (a1, c1) in zip(pts, pts[1:]):
        m = (ang >= a0) & (ang <= a1)
        t = ((ang - a0) / (a1 - a0))[m][:, None]
        g[m] = np.array(c0) * (1 - t) + np.array(c1) * t
    capa = Image.fromarray(g.astype("uint8")).convert("RGBA")
    d = np.sqrt((x - N / 2) ** 2 + (y - N / 2) ** 2)
    mask = ((d <= N / 2 - 1) & (d >= N / 2 * (1 - ring * 2))).astype("uint8") * 255
    capa.putalpha(Image.fromarray(mask))
    lienzo = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    lienzo.alpha_composite(capa)
    fm = Image.new("L", (interior, interior), 0)
    ImageDraw.Draw(fm).ellipse([0, 0, interior - 1, interior - 1], fill=255)
    off = (N - interior) // 2
    lienzo.paste(foto, (off, off), fm)
    lienzo = lienzo.resize((n, n), Image.LANCZOS)
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    lienzo.save(salida, optimize=True)

if __name__ == "__main__":
    base = os.path.join(RAIZ, "brand", "logos")
    foto = sys.argv[1] if len(sys.argv) > 1 else None
    if foto:
        anillo_foto(foto, os.path.join(RAIZ, "site", "firma", "foto-firma.png"))
    G = 2400
    guardar(aura(1600), os.path.join(base, "1-aura"), "aura-con-grano")
    guardar(aura(1600, grano=0), os.path.join(base, "1-aura"), "aura-sin-grano-para-iconos")
    pequenos = os.path.join(base, "1-aura", "png")
    for t in (512, 256, 64):
        aura(1600, grano=0).resize((t, t), Image.LANCZOS).save(os.path.join(pequenos, "aura-icono-%d.png" % t))
    mg = monograma(1600)
    guardar(mg, os.path.join(base, "2-perfil-GJ"), "perfil-GJ-circular")
    cuadrado = monograma(1600, completo=True).convert("RGB")
    carp = os.path.join(base, "2-perfil-GJ")
    cuadrado.save(os.path.join(carp, "png", "perfil-GJ-cuadrado-para-llamadas.png"), optimize=True)
    cuadrado.save(os.path.join(carp, "jpg", "perfil-GJ-cuadrado-para-llamadas.jpg"), quality=93, optimize=True, subsampling=0)
    cuadrado.resize((400, 400), Image.LANCZOS).save(os.path.join(carp, "png", "perfil-GJ-cuadrado-400.png"), optimize=True)
    cuadrado.resize((400, 400), Image.LANCZOS).save(os.path.join(carp, "jpg", "perfil-GJ-cuadrado-400.jpg"), quality=93, subsampling=0)
    h = os.path.join(base, "3-horizontal")
    guardar(horizontal(aura(1600)), h, "horizontal-aura-fondo-claro")
    guardar(horizontal(aura(1600), claro=False), h, "horizontal-aura-fondo-oscuro", jpg_sobre=(18, 26, 22))
    guardar(horizontal(mg), h, "horizontal-GJ-fondo-claro")
    guardar(horizontal(mg, claro=False), h, "horizontal-GJ-fondo-oscuro", jpg_sobre=(18, 26, 22))
    v = os.path.join(base, "4-vertical")
    guardar(vertical(aura(1600)), v, "vertical-aura-fondo-claro")
    guardar(vertical(aura(1600), claro=False), v, "vertical-aura-fondo-oscuro", jpg_sobre=(18, 26, 22))
    guardar(vertical(mg), v, "vertical-GJ-fondo-claro")
    guardar(vertical(mg, claro=False), v, "vertical-GJ-fondo-oscuro", jpg_sobre=(18, 26, 22))
    t = os.path.join(base, "5-solo-texto")
    guardar(solo_texto(True), t, "nombre-solo-fondo-claro")
    guardar(solo_texto(False), t, "nombre-solo-fondo-oscuro", jpg_sobre=(18, 26, 22))
    print("ok")
