"""Genera el ícono para dispositivos (180x180) y la imagen para compartir (1200x630)
con el aura del logo (índigo, verde agua y amarillo). Uso: python3 scripts/generar-imagenes.py"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

def aura(n, grano=0.10):
    base = Image.new("RGB", (n, n), (250, 251, 244))
    capas = [  # x, y, radio (fracción), color, opacidad
        (0.64, 0.44, 0.36, (43, 45, 143), 0.95),
        (0.70, 0.42, 0.16, (22, 21, 79), 0.85),
        (0.48, 0.52, 0.30, (31, 163, 138), 0.85),
        (0.30, 0.70, 0.28, (247, 216, 74), 0.95),
        (0.28, 0.72, 0.12, (255, 246, 184), 0.9),
        (0.30, 0.30, 0.20, (217, 240, 140), 0.6),
    ]
    for cx, cy, r, color, op in capas:
        R = r * n
        mask = Image.new("L", (n, n), 0)
        ImageDraw.Draw(mask).ellipse([cx * n - R, cy * n - R, cx * n + R, cy * n + R], fill=int(255 * op))
        mask = mask.filter(ImageFilter.GaussianBlur(R * 0.6))
        base = Image.composite(Image.new("RGB", (n, n), color), base, mask)
    # Forma circular que se desvanece en los bordes
    borde = Image.new("L", (n, n), 0)
    ImageDraw.Draw(borde).ellipse([n * 0.1, n * 0.1, n * 0.9, n * 0.9], fill=255)
    borde = borde.filter(ImageFilter.GaussianBlur(n * 0.05))
    ruido = Image.effect_noise((n, n), 70).convert("L").point(lambda v: 255 - int((255 - v) * grano))
    con_grano = ImageChops.multiply(base, ruido.convert("RGB"))
    return Image.composite(con_grano, Image.new("RGB", (n, n), (255, 255, 255)), borde)

icono = aura(180, grano=0.05)
icono.save("site/apple-touch-icon.png", optimize=True)

og = Image.new("RGB", (1200, 630), (255, 255, 255))
og.paste(aura(640, grano=0.12), (600, -5))
d = ImageDraw.Draw(og)
try:
    f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
except OSError:
    f1 = f2 = ImageFont.load_default()
for i, linea in enumerate(["Lo que la Amazonía", "hace merece", "llegar más lejos"]):
    d.text((80, 170 + i * 76), linea, font=f1, fill=(18, 26, 22))
d.text((80, 455), "Gabriela Jiménez · Consultoría en comunicación", font=f2, fill=(61, 72, 66))
og.save("site/og-image.jpg", quality=84, optimize=True, progressive=True)
print("ok")
