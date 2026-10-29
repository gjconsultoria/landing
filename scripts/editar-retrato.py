"""Preedición del retrato de «Sobre mí».
Busca el acabado de una cámara profesional: separación del fondo con
desenfoque suave, piel suavizada sin perder los rasgos, y un revelado de
contraste, color y viñeta discretos.

Uso: python3 scripts/editar-retrato.py <foto-original>
Salida: site/assets/gabriela-920.webp y -560.webp
"""
import os, sys
import numpy as np
import cv2

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "site", "assets")
ANCHOS = (920, 560)


def buscar_cara(bgr):
    """Ubica la cara por tono de piel: la mancha más grande de la mitad
    superior, cerca del centro. Esta compilación de OpenCV no trae el
    detector de rostros, y para un retrato de medio cuerpo basta."""
    h, w = bgr.shape[:2]
    ycrcb = cv2.cvtColor(cv2.GaussianBlur(bgr, (0, 0), w * 0.004), cv2.COLOR_BGR2YCrCb)
    piel = cv2.inRange(ycrcb, (40, 135, 80), (245, 178, 125))
    piel[int(h * .62):, :] = 0                      # abajo van el torso y los brazos
    piel = cv2.morphologyEx(piel, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    piel = cv2.morphologyEx(piel, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))

    n, _, stats, cent = cv2.connectedComponentsWithStats(piel, 8)
    mejor, puntaje = None, -1.0
    for i in range(1, n):
        x, y, bw, bh, area = stats[i]
        if area < (w * h) * 0.004 or bh == 0:
            continue
        prop = bw / bh
        if prop < 0.45 or prop > 1.9:               # una cara no es ni muy ancha ni muy larga
            continue
        centrado = 1.0 - abs(cent[i][0] - w / 2) / (w / 2)
        p = area * (0.45 + 0.55 * centrado)
        if p > puntaje:
            puntaje, mejor = p, (x, y, bw, bh)
    return mejor


def mascara_sujeto(bgr):
    """Separa a la persona del fondo. Arranca con GrabCut sembrado por la
    cara y por una franja central donde va el cuerpo."""
    h, w = bgr.shape[:2]
    gris = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    caja = buscar_cara(bgr)
    if caja is not None:
        fx, fy, fw, fh = caja
    else:  # si no la encuentra, asume cara en el tercio superior central
        fw = fh = int(w * .26)
        fx, fy = int(w * .37), int(h * .16)

    # Semillas: seguro fondo en los bordes, seguro sujeto en cara y torso
    marca = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
    marca[:, :int(w * .05)] = cv2.GC_BGD
    marca[:, int(w * .95):] = cv2.GC_BGD
    marca[:int(h * .04), :] = cv2.GC_BGD

    cx = fx + fw // 2
    # Cara
    cv2.ellipse(marca, (cx, fy + fh // 2), (int(fw * .42), int(fh * .52)), 0, 0, 360, cv2.GC_FGD, -1)
    # Cuello y torso: un trapecio que se abre hacia abajo
    torso = np.array([
        [cx - int(fw * .45), fy + fh],
        [cx + int(fw * .45), fy + fh],
        [cx + int(fw * 1.55), h - 1],
        [cx - int(fw * 1.55), h - 1],
    ], np.int32)
    cv2.fillPoly(marca, [torso], cv2.GC_FGD)
    # Zona probable del sujeto, más ancha
    probable = np.array([
        [cx - int(fw * 1.0), max(0, fy - int(fh * .5))],
        [cx + int(fw * 1.0), max(0, fy - int(fh * .5))],
        [cx + int(fw * 2.3), h - 1],
        [cx - int(fw * 2.3), h - 1],
    ], np.int32)
    capa = np.zeros((h, w), np.uint8)
    cv2.fillPoly(capa, [probable], 1)
    marca[(capa == 1) & (marca == cv2.GC_PR_BGD)] = cv2.GC_PR_FGD

    fondo = np.zeros((1, 65), np.float64)
    frente = np.zeros((1, 65), np.float64)
    try:
        cv2.grabCut(bgr, marca, None, fondo, frente, 4, cv2.GC_INIT_WITH_MASK)
    except cv2.error:
        pass

    m = np.where((marca == cv2.GC_FGD) | (marca == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((11, 11), np.uint8))
    m = cv2.GaussianBlur(m, (0, 0), w * 0.012)
    return m.astype(np.float32) / 255.0, (fx, fy, fw, fh)


def mascara_piel(bgr, cara):
    """Piel dentro de la zona de la cara y el cuello, sin los rasgos."""
    h, w = bgr.shape[:2]
    fx, fy, fw, fh = cara
    ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    piel = cv2.inRange(ycrcb, (0, 133, 77), (255, 180, 127))

    # Solo alrededor de la cara y el cuello
    zona = np.zeros((h, w), np.uint8)
    cv2.ellipse(zona, (fx + fw // 2, fy + int(fh * .58)),
                (int(fw * .78), int(fh * 1.05)), 0, 0, 360, 255, -1)
    piel = cv2.bitwise_and(piel, zona)

    # Quitar los rasgos: donde hay mucho detalle (ojos, cejas, boca, pelo)
    gris = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    detalle = cv2.Laplacian(cv2.GaussianBlur(gris, (0, 0), 1.2), cv2.CV_32F)
    detalle = cv2.GaussianBlur(np.abs(detalle), (0, 0), 3)
    umbral = np.percentile(detalle[piel > 0], 82) if np.any(piel > 0) else 1e9
    piel[detalle > umbral] = 0

    piel = cv2.morphologyEx(piel, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    piel = cv2.GaussianBlur(piel, (0, 0), fw * 0.05)
    return piel.astype(np.float32) / 255.0


def suavizar_piel(bgr, piel, fuerza=0.62):
    """Separación de frecuencias: aplana el tono y devuelve parte del detalle."""
    base = cv2.bilateralFilter(bgr, 0, 42, 14)
    base = cv2.bilateralFilter(base, 0, 34, 12)
    detalle = bgr.astype(np.float32) - base.astype(np.float32)
    suave = base.astype(np.float32) + detalle * (1.0 - fuerza)
    m = piel[..., None]
    return (bgr.astype(np.float32) * (1 - m) + suave * m)


def revelar(img):
    """Contraste en S, un punto de calidez y color, sin quemar."""
    lab = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # Luminancia: abre sombras y da cuerpo a los medios
    clahe = cv2.createCLAHE(clipLimit=1.25, tileGridSize=(8, 8))
    l = cv2.addWeighted(l, 0.55, clahe.apply(l), 0.45, 0)
    x = l.astype(np.float32) / 255.0
    x = np.clip(x + 0.11 * np.sin(np.pi * x) * (0.5 - x) * -2.0, 0, 1)  # S suave
    l = (x * 255).astype(np.uint8)
    img = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR).astype(np.float32)

    hsv = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.09, 0, 255)
    img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    img[..., 2] = np.clip(img[..., 2] * 1.015, 0, 255)   # R
    img[..., 0] = np.clip(img[..., 0] * 0.988, 0, 255)   # B
    return img


def vineta(img, fuerza=0.2):
    h, w = img.shape[:2]
    y, x = np.mgrid[0:h, 0:w]
    d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    v = np.clip(1 - fuerza * np.clip((d - 0.55) / 0.85, 0, 1) ** 1.5, 0, 1)
    return img * v[..., None]


def main():
    origen = sys.argv[1]
    bgr = cv2.imread(origen)
    if bgr is None:
        raise SystemExit("no pude abrir " + origen)
    h, w = bgr.shape[:2]

    sujeto, cara = mascara_sujeto(bgr)

    # Fondo: desenfoque progresivo, como una apertura abierta
    fondo = cv2.GaussianBlur(bgr, (0, 0), w * 0.011)
    fondo = cv2.GaussianBlur(fondo, (0, 0), w * 0.006)
    m = sujeto[..., None]
    img = fondo.astype(np.float32) * (1 - m) + bgr.astype(np.float32) * m

    # Piel
    piel = mascara_piel(bgr, cara)
    img = suavizar_piel(np.clip(img, 0, 255).astype(np.uint8), piel)

    # Revelado y viñeta
    img = revelar(img)
    img = vineta(img, 0.22)

    # Nitidez solo sobre el sujeto (los rasgos, no el fondo)
    base = cv2.GaussianBlur(img, (0, 0), 1.6)
    nitido = np.clip(img + (img - base) * 0.55, 0, 255)
    img = img * (1 - m) + nitido * m

    final = np.clip(img, 0, 255).astype(np.uint8)
    os.makedirs(DESTINO, exist_ok=True)

    # Encuadre vertical 4:5 centrado en la cara, con aire arriba
    fx, fy, fw, fh = cara
    cx = fx + fw // 2
    alto = h
    ancho = int(alto * 0.8)
    if ancho > w:
        ancho = w
        alto = int(ancho / 0.8)
    x0 = int(np.clip(cx - ancho // 2, 0, w - ancho))
    y0 = int(np.clip(fy - fh * 0.75, 0, h - alto))
    recorte = final[y0:y0 + alto, x0:x0 + ancho]

    for ancho_sal in ANCHOS:
        esc = ancho_sal / recorte.shape[1]
        chico = cv2.resize(recorte, (ancho_sal, int(recorte.shape[0] * esc)), interpolation=cv2.INTER_AREA)
        ruta = os.path.join(DESTINO, f"gabriela-{ancho_sal}.webp")
        cv2.imwrite(ruta, chico, [cv2.IMWRITE_WEBP_QUALITY, 86])
        print(f"{os.path.basename(ruta)}  {chico.shape[1]}x{chico.shape[0]}  {os.path.getsize(ruta)//1024} KB")

    cv2.imwrite("/tmp/claude-0/-home-claude/e25420f1-890b-596a-bb6c-070532ca213a/scratchpad/retrato-mascara.jpg",
                (sujeto * 255).astype(np.uint8))
    print("cara detectada en", cara)


if __name__ == "__main__":
    main()
