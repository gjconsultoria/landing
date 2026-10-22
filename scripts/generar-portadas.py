"""Genera la portada de WhatsApp Business (16:9), dos fondos de Meet (claro/oscuro)
y los iconos de la firma. Uso: python3 scripts/generar-portadas.py
Salida: brand/portadas/ y site/firma/ic-*.png"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
_spec = importlib.util.spec_from_file_location("marca", os.path.join(os.path.dirname(os.path.abspath(__file__)), "generar-marca.py"))
M = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(M)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TINTA, GRIS, BLANCO = (18, 26, 22), (61, 72, 66), (255, 255, 255)
INDIGO, INDIGO_P, AGUA, AMARILLO, LIMA, SELVA = (43, 45, 143), (22, 21, 79), (31, 163, 138), (247, 216, 74), (217, 240, 140), (14, 107, 72)

def fondo(W, H, base, capas, grano=0.03):
    """capas: (cx, cy, rx, ry, [(pos, color, alpha)]) con fracciones de W/H."""
    y, x = np.mgrid[0:H, 0:W]
    img = np.zeros((H, W, 3), float) + np.array(base, float)
    for cx, cy, rx, ry, paradas in capas:
        t = np.clip(np.sqrt(((x + .5) / W - cx) ** 2 / (rx ** 2) + ((y + .5) / H - cy) ** 2 / (ry ** 2)), 0, 1)
        offs = [p[0] for p in paradas]
        col = np.stack([np.interp(t, offs, [p[1][k] for p in paradas]) for k in range(3)], -1)
        a = np.interp(t, offs, [p[2] for p in paradas])[..., None]
        img = img * (1 - a) + col * a
    out = Image.fromarray(np.clip(img, 0, 255).astype("uint8"))
    if grano:
        rng = np.random.default_rng(5)
        r = np.clip(1 - np.abs(rng.normal(0, 1, (H, W))) * grano * .6, 0, 1)
        out = ImageChops.multiply(out, Image.fromarray((r * 255).astype("uint8")).convert("RGB"))
    return out

def texto_centrado(d, cx, y, txt, f, fill, anchor="mm"):
    d.text((cx, y), txt, font=f, fill=fill, anchor=anchor)

# ---------- 1. Portada de WhatsApp Business (16:9, alta resolución) ----------
def whatsapp_cover():
    W, H = 1920, 1080
    capas = [
        (0.20, 0.78, 0.42, 0.62, [(0, (255, 246, 184), .95), (.4, AMARILLO, .9), (1, AMARILLO, 0)]),
        (0.12, 0.30, 0.40, 0.55, [(0, LIMA, .8), (1, LIMA, 0)]),
        (0.52, 0.50, 0.40, 0.72, [(0, (11, 111, 120), .9), (.45, AGUA, .8), (1, AGUA, 0)]),
        (0.80, 0.34, 0.42, 0.7, [(0, INDIGO_P, .95), (.45, INDIGO, .9), (1, INDIGO, 0)]),
    ]
    img = fondo(W, H, (246, 249, 240), capas).convert("RGBA")
    # Monograma GJ centrado-arriba
    mg = M.monograma(520).resize((360, 360), Image.LANCZOS)
    img.alpha_composite(mg, ((W - 360) // 2, 150))
    d = ImageDraw.Draw(img)
    texto_centrado(d, W/2, 620, "Gabriela Jiménez", M.fuente("Medium", 118), TINTA + (255,))
    texto_centrado(d, W/2, 712, "Consultoría en comunicación estratégica", M.fuente("Light", 54), TINTA + (255,))
    texto_centrado(d, W/2, 770, "para la Amazonía colombiana", M.fuente("Light", 54), TINTA + (255,))
    # Línea fina + frase (zona superior-media, lejos del borde inferior que tapa la foto de perfil)
    d.line([W/2 - 300, 858, W/2 + 300, 858], fill=TINTA + (255,), width=3)
    texto_centrado(d, W/2, 905, "Lo que la Amazonía hace merece llegar más lejos", M.fuente("LightItalic", 42), GRIS + (255,))
    out = os.path.join(RAIZ, "brand", "portadas")
    os.makedirs(out, exist_ok=True)
    rgb = img.convert("RGB")
    rgb.save(os.path.join(out, "whatsapp-business-portada-1920x1080.png"), optimize=True)
    rgb.save(os.path.join(out, "whatsapp-business-portada-1920x1080.jpg"), quality=92, optimize=True, subsampling=0)

# ---------- 2. Fondos de Google Meet (1920x1080) ----------
def lockup(n, color_txt, color_sub):
    """Logo (aura) + nombre + bajada, en una capa RGBA compacta."""
    a = M.aura(620).resize((n, n), Image.LANCZOS)
    f1, f2 = M.fuente("Medium", n * 0.46), M.fuente("Light", n * 0.26)
    t1, t2a, t2b = "Gabriela Jiménez", "Consultoría en comunicación estratégica", "Amazonía colombiana"
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(max(tmp.textlength(t1, font=f1), tmp.textlength(t2a, font=f2)))
    gap = int(n * 0.26)
    w = n + gap + tw + 8
    h = max(n, int(n * 1.5))
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    capa.alpha_composite(a, (0, (h - n) // 2))
    d = ImageDraw.Draw(capa)
    tx, cy = n + gap, h / 2
    d.text((tx, cy - n * 0.52), t1, font=f1, fill=color_txt + (255,), anchor="lm")
    d.text((tx, cy + n * 0.02), t2a, font=f2, fill=color_sub + (255,), anchor="lm")
    d.text((tx, cy + n * 0.42), t2b, font=f2, fill=color_sub + (255,), anchor="lm")
    return capa

def meet_fondo(oscuro):
    W, H = 1920, 1080
    if oscuro:
        base = (16, 18, 42)
        capas = [
            (0.16, 0.22, 0.5, 0.6, [(0, INDIGO, .55), (1, INDIGO, 0)]),
            (0.86, 0.26, 0.45, 0.6, [(0, AGUA, .4), (1, AGUA, 0)]),
            (0.90, 0.86, 0.5, 0.6, [(0, AMARILLO, .3), (1, AMARILLO, 0)]),
            (0.12, 0.9, 0.5, 0.55, [(0, (11, 90, 78), .45), (1, (11, 90, 78), 0)]),
        ]
        img = fondo(W, H, base, capas, grano=0.02).convert("RGBA")
        # Velo para que el centro quede limpio detrás del rostro
        velo = Image.new("RGBA", (W, H), (16, 18, 42, 0)); vd = ImageDraw.Draw(velo)
        vd.ellipse([W*0.28, H*0.1, W*0.72, H*1.15], fill=(16, 18, 42, 150))
        img = Image.alpha_composite(img, velo.filter(ImageFilter.GaussianBlur(120)))
        lk = lockup(132, BLANCO, (206, 214, 235))
    else:
        base = (247, 249, 242)
        capas = [
            (0.14, 0.2, 0.46, 0.55, [(0, LIMA, .6), (1, LIMA, 0)]),
            (0.9, 0.22, 0.44, 0.6, [(0, INDIGO, .4), (1, INDIGO, 0)]),
            (0.9, 0.85, 0.5, 0.6, [(0, AMARILLO, .55), (1, AMARILLO, 0)]),
            (0.1, 0.88, 0.5, 0.55, [(0, AGUA, .4), (1, AGUA, 0)]),
        ]
        img = fondo(W, H, base, capas, grano=0.025).convert("RGBA")
        velo = Image.new("RGBA", (W, H), (0, 0, 0, 0)); vd = ImageDraw.Draw(velo)
        vd.ellipse([W*0.26, H*0.08, W*0.74, H*1.15], fill=(250, 251, 246, 170))
        img = Image.alpha_composite(img, velo.filter(ImageFilter.GaussianBlur(130)))
        lk = lockup(132, TINTA, GRIS)
    # Lockup arriba a la izquierda (zona que el rostro no tapa)
    img.alpha_composite(lk, (70, 60))
    out = os.path.join(RAIZ, "brand", "portadas"); os.makedirs(out, exist_ok=True)
    nombre = "meet-fondo-oscuro-1920x1080" if oscuro else "meet-fondo-claro-1920x1080"
    rgb = img.convert("RGB")
    rgb.save(os.path.join(out, nombre + ".png"), optimize=True)
    rgb.save(os.path.join(out, nombre + ".jpg"), quality=92, optimize=True, subsampling=0)

# ---------- 3. Iconos de la firma ----------
def icono_pill(nombre, color_fondo, dibujo):
    """Crea un icono cuadrado con fondo de color (para la firma)."""
    N = 192
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rad = N * 0.26
    d.rounded_rectangle([0, 0, N-1, N-1], radius=rad, fill=color_fondo + (255,))
    dibujo(d, N)
    img.resize((96, 96), Image.LANCZOS).save(os.path.join(RAIZ, "site", "firma", "ic-" + nombre + ".png"), optimize=True)

def dib_whatsapp(d, N):
    w = (255, 255, 255, 255)
    cx, cy, r = N*0.5, N*0.47, N*0.3
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=w, width=int(N*0.082))
    d.polygon([(cx-r*0.92, cy+r*0.28), (cx-r*0.15, cy+r*1.08), (cx-r*0.02, cy+r*0.45)], fill=w)
    x1, y1 = cx-r*0.42, cy-r*0.4
    x2, y2 = cx+r*0.38, cy+r*0.4
    bw = int(N*0.11)
    d.line([(x1, y1), (x2, y2)], fill=w, width=bw)
    br = bw*0.95
    d.ellipse([x1-br, y1-br, x1+br, y1+br], fill=w)
    d.ellipse([x2-br, y2-br, x2+br, y2+br], fill=w)

def dib_linkedin(d, N):
    f = M.fuente("Bold", N*0.5)
    d.text((N*0.5, N*0.54), "in", font=f, fill=(255, 255, 255, 255), anchor="mm")

if __name__ == "__main__":
    whatsapp_cover()
    meet_fondo(True)
    meet_fondo(False)
    icono_pill("whatsapp", (37, 211, 102), dib_whatsapp)
    icono_pill("linkedin", (10, 102, 194), dib_linkedin)
    print("ok")
