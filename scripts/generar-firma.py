"""Genera la franja de la firma de correo (1500x450, se muestra a 600x180).
Uso: python3 scripts/generar-firma.py ruta/a/foto.jpg
Salida: site/firma/firma-banner.png"""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("marca", os.path.join(os.path.dirname(os.path.abspath(__file__)), "generar-marca.py"))
marca = importlib.util.module_from_spec(spec); spec.loader.exec_module(marca)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, S = 1500, 450, 2          # lienzo base y supermuestreo
TINTA, GRIS = (18, 26, 22), (61, 72, 66)
random.seed(11)

def blob(size, color, alpha, blur):
    c = Image.new("RGBA", (S * W, S * H), (0, 0, 0, 0))
    x0, y0, x1, y1 = [v * S for v in size]
    ImageDraw.Draw(c).ellipse([x0, y0, x1, y1], fill=color + (int(255 * alpha),))
    return c.filter(ImageFilter.GaussianBlur(blur * S))

def arco(caja, radio):
    x0, y0, x1, y1 = [v * S for v in caja]
    m = Image.new("L", (S * W, S * H), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([x0, y0, x1, y0 + 2 * radio * S], fill=255)
    d.rectangle([x0, y0 + radio * S, x1, y1], fill=255)
    return m

def trazo(puntos, color, ancho, alfa=235):
    c = Image.new("RGBA", (S * W, S * H), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    pts = [(x * S, y * S) for x, y in puntos]
    d.line(pts, fill=color + (alfa,), width=int(ancho * S), joint="curve")
    for x, y in (pts[0], pts[-1]):
        r = ancho * S / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (alfa,))
    return c

def garabato(cx, cy, rx, ry, vueltas, color, ancho, ruido=16, ang0=0.0):
    pts = []
    n = int(vueltas * 60)
    for i in range(n + 1):
        t = i / 60
        a = ang0 + t * 2 * math.pi
        k = 1 + 0.08 * t
        pts.append((cx + (rx * k) * math.cos(a) + random.uniform(-ruido, ruido),
                    cy + (ry * k) * math.sin(a) + random.uniform(-ruido, ruido)))
    k = 6
    suave = [(sum(p[0] for p in pts[max(0, i - k):i + k + 1]) / len(pts[max(0, i - k):i + k + 1]),
              sum(p[1] for p in pts[max(0, i - k):i + k + 1]) / len(pts[max(0, i - k):i + k + 1])) for i in range(len(pts))]
    return trazo(suave, color, ancho)

def zigzag(x0, y0, x1, y1, pasos, amp, color, ancho):
    pts = []
    for i in range(pasos + 1):
        t = i / pasos
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + (amp if i % 2 else -amp) + random.uniform(-4, 4)
        pts.append((x, y))
    return trazo(pts, color, ancho)

def estrella(cx, cy, r, color, ancho):
    c = Image.new("RGBA", (S * W, S * H), (0, 0, 0, 0))
    for k in range(4):
        a = k * math.pi / 4 + random.uniform(-.1, .1)
        c = Image.alpha_composite(c, trazo([(cx - r * math.cos(a), cy - r * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))], color, ancho))
    return c

def fuente(peso, tam, cursiva=False):
    n = "Poppins-%s%s.ttf" % (peso, "Italic" if cursiva else "")
    return ImageFont.truetype(marca.FUENTES + n, int(tam * S))

def construir(ruta_foto, salida):
    lienzo = Image.new("RGBA", (S * W, S * H), (255, 255, 255, 255))
    # Lavados de color suaves, como en los referentes
    for c in (blob((-260, 230, 420, 760), (247, 216, 74), .50, 90),
              blob((-120, -330, 380, 120), (217, 240, 140), .34, 90),
              blob((780, -160, 1500, 520), (31, 163, 138), .10, 110),
              blob((1060, 120, 1700, 700), (43, 45, 143), .10, 110)):
        lienzo = Image.alpha_composite(lienzo, c)
    # Aura del logo detrás de la foto
    a = marca.aura(900).resize((S * 560, S * 560), Image.LANCZOS)
    cap = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); cap.alpha_composite(a, (S * 890, S * -70))
    lienzo = Image.alpha_composite(lienzo, cap)
    # Foto a color dentro de un arco
    foto = Image.open(ruta_foto).convert("RGB").crop((95, 40, 805, 920))
    foto = ImageOps.autocontrast(foto, cutoff=1)
    caja = (1010, 36, 1340, 450)
    fw, fh = (caja[2] - caja[0]) * S, (caja[3] - caja[1]) * S
    foto = foto.resize((fw, int(fw * 880 / 710)), Image.LANCZOS)
    foto = foto.crop((0, 0, fw, fh))
    capa = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); capa.paste(foto, (caja[0] * S, caja[1] * S))
    mascara = arco(caja, 165)
    capa.putalpha(ImageChops.multiply(mascara, capa.split()[3]))
    sombra = capa.filter(ImageFilter.GaussianBlur(14 * S))
    sombra = Image.merge("RGBA", (Image.new("L", lienzo.size, 22), Image.new("L", lienzo.size, 26), Image.new("L", lienzo.size, 22), sombra.split()[3].point(lambda v: int(v * .28))))
    desp = Image.new('RGBA', lienzo.size, (0, 0, 0, 0)); desp.paste(sombra, (10 * S, 14 * S)); lienzo = Image.alpha_composite(lienzo, desp)
    lienzo = Image.alpha_composite(lienzo, capa)
    # Línea fina del arco desplazada
    cont = Image.new("RGBA", lienzo.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cont)
    x0, y0, x1 = (caja[0] - 22) * S, (caja[1] - 18) * S, (caja[2] - 22) * S
    r = 165 * S
    d.arc([x0, y0, x1, y0 + 2 * r], 180, 360, fill=TINTA + (255,), width=3 * S)
    d.line([x0, y0 + r, x0, H * S], fill=TINTA + (255,), width=3 * S)
    d.line([x1, y0 + r, x1, H * S], fill=TINTA + (255,), width=3 * S)
    lienzo = Image.alpha_composite(lienzo, cont)
    # Trazos de marcador (gráfica secundaria)
    lienzo = Image.alpha_composite(lienzo, garabato(1060, 372, 92, 78, 1.6, (247, 216, 74), 15, ang0=2.4))
    lienzo = Image.alpha_composite(lienzo, garabato(1060, 372, 70, 58, 1.1, (31, 163, 138), 9, ang0=3.4))
    lienzo = Image.alpha_composite(lienzo, zigzag(1290, 392, 1450, 340, 9, 16, (43, 45, 143), 11))
    lienzo = Image.alpha_composite(lienzo, estrella(1385, 92, 40, (247, 216, 74), 11))
    lienzo = Image.alpha_composite(lienzo, estrella(1440, 150, 17, (31, 163, 138), 8))
    # Texto
    d = ImageDraw.Draw(lienzo)
    OFF = 33  # recentra el bloque verticalmente tras quitar la frase inferior
    m = marca.aura(500).resize((S * 78, S * 78), Image.LANCZOS)
    lienzo.alpha_composite(m, (S * 66, S * (52 + OFF)))
    d.text((S * 164, S * (72 + OFF)), "Consultoría en comunicación", font=fuente("Light", 25), fill=GRIS + (255,))
    d.text((S * 66, S * (150 + OFF)), "Gabriela Jiménez", font=fuente("Medium", 76), fill=TINTA + (255,))
    d.text((S * 70, S * (250 + OFF)), "Comunicación estratégica", font=fuente("Light", 36), fill=TINTA + (255,))
    d.text((S * 70, S * (296 + OFF)), "para la Amazonía colombiana", font=fuente("Light", 36), fill=TINTA + (255,))
    # Grano de película
    rng = np.random.default_rng(3)
    r = np.clip(1 - np.abs(rng.normal(0, 1, (S * H, S * W))) * .028, 0, 1)
    gr = Image.fromarray((r * 255).astype("uint8")).convert("RGB")
    rgb = ImageChops.multiply(lienzo.convert("RGB"), gr)
    out = rgb.resize((W, H), Image.LANCZOS)
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    out.save(salida, optimize=True)
    return out

if __name__ == "__main__":
    construir(sys.argv[1], os.path.join(RAIZ, "site", "firma", "firma-banner.png"))
    print("ok")
