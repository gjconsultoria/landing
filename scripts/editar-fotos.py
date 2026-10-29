"""Preedición de las fotos de territorio y generación de las versiones web.
Uso: python3 scripts/editar-fotos.py
Entrada: fotos-origen/*.webp   Salida: site/assets/fotos/<nombre>-<ancho>.webp
"""
import os, glob
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEN = os.path.join(RAIZ, "fotos-origen")
DESTINO = os.path.join(RAIZ, "site", "assets", "fotos")
ANCHOS = (1400, 900, 600)

# Ajustes por foto: (recorte_negros, luz_sombras, saturación, contraste, calidez)
# recorte_negros: % de píxeles que se llevan a negro puro (quita la neblina)
# luz_sombras: 0 = sin cambio; sube las zonas oscuras sin tocar las altas
AJUSTES = {
    "gua-mavecure-rio":  (0.5, 0.10, 1.22, 1.12, 0.00),
    "gua-cerro-cielo":   (0.5, 0.08, 1.20, 1.12, 0.00),
    "gua-espejo-rio":    (0.4, 0.06, 1.18, 1.10, 0.01),
    "gua-selva-espejo":  (0.15, 0.26, 1.16, 1.03, 0.00),
    "ama-dosel-arbol":   (0.3, 0.16, 1.18, 1.10, 0.00),
    "ama-ceiba-abajo":   (0.3, 0.20, 1.16, 1.10, 0.00),
    "ama-raices-ceiba":  (0.3, 0.26, 1.14, 1.08, 0.02),
    "ama-victoria":      (0.5, 0.12, 1.22, 1.12, 0.00),
    "ama-bote-rio":      (0.5, 0.10, 1.20, 1.12, 0.01),
    "ama-casa-rio":      (0.5, 0.08, 1.20, 1.12, 0.01),
    "ama-orilla-bote":   (0.2, 0.24, 1.14, 1.04, 0.03),
    "ama-escuela":       (0.5, 0.08, 1.18, 1.10, 0.00),
    "ama-chiguiro-pollitos": (0.3, 0.22, 1.20, 1.08, 0.02),
    "ama-perro-canoa":       (0.2, 0.34, 1.12, 1.06, 0.04),
}
POR_DEFECTO = (0.4, 0.10, 1.18, 1.10, 0.00)

# Encuadre por foto: (izq, arriba, der, abajo) como fracción 0-1 del original.
# Se recorta antes de editar, para llevar cada foto a una composición más
# cerrada en vez de dejar que el navegador decida qué recorta.
ENCUADRE = {
    "ama-chiguiro-pollitos": (0.02, 0.03, 0.86, 1.00),
    "ama-perro-canoa":       (0.00, 0.08, 1.00, 0.56),
}


def recortar(img, caja):
    if not caja:
        return img
    w, h = img.size
    l, t, r, b = caja
    return img.crop((round(l * w), round(t * h), round(r * w), round(b * h)))


def niveles(img, recorte):
    """Lleva el punto negro y el blanco a los extremos, por canal, sin quemar."""
    a = np.asarray(img, dtype=np.float32)
    for c in range(3):
        canal = a[..., c]
        lo = np.percentile(canal, recorte)
        hi = np.percentile(canal, 100 - recorte * 0.6)
        if hi - lo < 1:
            continue
        a[..., c] = np.clip((canal - lo) * (255.0 / (hi - lo)), 0, 255)
    return Image.fromarray(a.astype("uint8"))


def sombras(img, fuerza):
    """Abre las sombras con una curva que deja intactas las luces."""
    if fuerza <= 0:
        return img
    a = np.asarray(img, dtype=np.float32) / 255.0
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    mascara = np.clip(1.0 - lum * 1.6, 0, 1) ** 1.5
    subida = (np.power(a, 1.0 / (1.0 + fuerza * 1.8)) - a) * mascara[..., None]
    return Image.fromarray((np.clip(a + subida, 0, 1) * 255).astype("uint8"))


def vibrancia(img, factor):
    """Sube la saturación más donde hay poco color, para no quemar los verdes."""
    if factor == 1.0:
        return img
    a = np.asarray(img, dtype=np.float32)
    gris = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    dif = a - gris[..., None]
    sat = np.abs(dif).max(axis=2) / 255.0
    peso = (1.0 - sat * 0.55)[..., None]
    return Image.fromarray(np.clip(gris[..., None] + dif * (1 + (factor - 1) * peso), 0, 255).astype("uint8"))


def calidez(img, fuerza):
    if fuerza <= 0:
        return img
    a = np.asarray(img, dtype=np.float32)
    a[..., 0] = np.clip(a[..., 0] * (1 + fuerza), 0, 255)
    a[..., 2] = np.clip(a[..., 2] * (1 - fuerza * 0.6), 0, 255)
    return Image.fromarray(a.astype("uint8"))


def editar(img, ajuste):
    rec, som, sat, con, cal = ajuste
    img = niveles(img, rec)
    img = sombras(img, som)
    img = vibrancia(img, sat)
    img = ImageEnhance.Contrast(img).enhance(con)
    img = calidez(img, cal)
    return img


def main():
    os.makedirs(DESTINO, exist_ok=True)
    total = 0
    for ruta in sorted(glob.glob(os.path.join(ORIGEN, "*.webp"))):
        nombre = os.path.splitext(os.path.basename(ruta))[0]
        img = Image.open(ruta).convert("RGB")
        img = recortar(img, ENCUADRE.get(nombre))
        img = editar(img, AJUSTES.get(nombre, POR_DEFECTO))
        # El tamaño manda sobre el lado largo: así una foto vertical no
        # termina pesando el triple que una horizontal.
        largo = max(img.width, img.height)
        for ancho in ANCHOS:
            if ancho > largo:
                continue
            esc = ancho / largo
            chico = img.resize((round(img.width * esc), round(img.height * esc)), Image.LANCZOS)
            # Enfoque suave, proporcional al tamaño final
            chico = chico.filter(ImageFilter.UnsharpMask(radius=1.1, percent=58, threshold=3))
            salida = os.path.join(DESTINO, f"{nombre}-{ancho}.webp")
            chico.save(salida, "WEBP", quality=80, method=6)
            total += 1
            print(f"{os.path.basename(salida):34s} {os.path.getsize(salida)//1024:4d} KB")
    print(f"\n{total} archivos en site/assets/fotos/")


if __name__ == "__main__":
    main()
