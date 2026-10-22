"""Genera el sprite SVG de la selva (hojas, helechos, monstera, palma) y la gráfica
secundaria a mano alzada (garabatos, zigzag, asteriscos) para la landing.
Uso: python3 scripts/generar-hojas.py  ->  scripts/_sprite.svg (se incrusta en index.html)
Todas las hojas apuntan hacia arriba con la base abajo al centro, para que el vaivén
gire desde el tallo."""
import math, os, random

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(7)
f = lambda v: ("%.1f" % v).rstrip("0").rstrip(".")


def lente(x0, y0, x1, y1, ancho, curva=0.0):
    """Folíolo en forma de lente entre dos puntos."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    mx, my = x0 + dx * .45 + nx * curva, y0 + dy * .45 + ny * curva
    a = (mx + nx * ancho, my + ny * ancho)
    b = (mx - nx * ancho * .7, my - ny * ancho * .7)
    return "M%s %sQ%s %s %s %sQ%s %s %s %sZ" % (f(x0), f(y0), f(a[0]), f(a[1]), f(x1), f(y1), f(b[0]), f(b[1]), f(x0), f(y0))


def bez(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def pinnada(nombre, n, largo, ancho, caida, curva_raquis=10, h=200):
    """Hoja pinnada (palma o helecho). viewBox 0 0 120 h."""
    p0, p1, p2 = (60, h), (60 + curva_raquis, h * .5), (60 - curva_raquis * .4, 6)
    partes = []
    for i in range(n):
        t = .1 + .86 * i / (n - 1)
        x, y = bez(p0, p1, p2, t)
        # dirección del raquis
        x2, y2 = bez(p0, p1, p2, min(1, t + .01))
        ang = math.atan2(y2 - y, x2 - x)
        env = math.sin(math.pi * (t * .92 + .04)) ** .8
        for lado in (-1, 1):
            a = ang + lado * (math.pi / 2 - .55) - lado * caida * (1 - t) * .3
            l = largo * env * random.uniform(.9, 1.05)
            ex, ey = x + math.cos(a) * l, y + math.sin(a) * l + caida * l * .25
            partes.append(lente(x, y, ex, ey, ancho * env + 1, curva=lado * -2))
    hojas = "".join(partes)
    raquis = "M%s %sQ%s %s %s %s" % (f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1]), f(p2[0]), f(p2[1]))
    return ('<symbol id="%s" viewBox="0 0 120 %d"><path class="h-l" style="fill:var(--r,#0E6B48)" d="%s"/>'
            '<path class="h-n" style="stroke:var(--n,rgba(255,255,255,.28))" d="%s" fill="none" stroke-width="1.6"/></symbol>') % (nombre, h, hojas, raquis)


def lanza(nombre, ancho=34, asim=4):
    """Hoja entera alargada, tipo heliconia o bijao. viewBox 0 0 100 200."""
    c = 50
    contorno = ("M{c} 200C{a1} 186 {a2} 150 {a3} 104C{a4} 62 {a5} 26 {c} 3"
                "C{b5} 26 {b4} 62 {b3} 104C{b2} 150 {b1} 186 {c} 200Z").format(
        c=c, a1=f(c - ancho * .35), a2=f(c - ancho - asim), a3=f(c - ancho - asim * .6), a4=f(c - ancho * .95), a5=f(c - ancho * .25),
        b1=f(c + ancho * .35), b2=f(c + ancho + asim * .3), b3=f(c + ancho), b4=f(c + ancho * .9), b5=f(c + ancho * .2))
    venas = []
    for i in range(1, 12):
        y = 192 - i * 16
        w = ancho * math.sin(math.pi * (1 - (y - 4) / 196)) ** .7 * .86
        for lado in (-1, 1):
            venas.append("M%s %sQ%s %s %s %s" % (f(c), f(y), f(c + lado * w * .5), f(y - 6), f(c + lado * w), f(y - 18)))
    return ('<symbol id="%s" viewBox="0 0 100 200"><path class="h-l" style="fill:var(--r,#0E6B48)" d="%s"/>'
            '<path class="h-n" style="stroke:var(--n,rgba(255,255,255,.28))" d="M50 199Q53 110 50 8" fill="none" stroke-width="1.8"/>'
            '<path class="h-v" style="stroke:var(--v,rgba(255,255,255,.14))" d="%s" fill="none" stroke-width=".9"/></symbol>') % (nombre, contorno, "".join(venas))


def monstera(nombre):
    """Hoja de monstera con lóbulos y agujeros. viewBox 0 0 200 220."""
    cx, cy, R = 100, 104, 96
    pts = []
    N = 360
    muescas = [math.radians(a) for a in (-50, -14, 18, 50, 76, 104, 130, 162, 194, 230)]
    for k in range(N + 1):
        th = -math.pi / 2 + 2 * math.pi * k / N   # empieza arriba
        # forma de corazón: más ancha arriba, con hendidura abajo
        r = R * (1 - .1 * math.cos(th) ** 2) * (1 + .06 * math.cos(th + math.pi / 2))
        for m in muescas:
            d = math.atan2(math.sin(th - m), math.cos(th - m))
            r *= 1 - .48 * math.exp(-(d / .028) ** 2)
        # hendidura del pecíolo (abajo, th = pi/2)
        d = math.atan2(math.sin(th - math.pi / 2), math.cos(th - math.pi / 2))
        r *= 1 - .55 * math.exp(-(d / .12) ** 2)
        pts.append((cx + r * math.cos(th) * .92, cy + r * math.sin(th)))
    d = "M" + "L".join("%s %s" % (f(x), f(y)) for x, y in pts) + "Z"
    agujeros = ""
    for (ax, ay, rx, ry, rot) in ((70, 80, 6, 13, 35), (130, 82, 6, 13, -35), (64, 120, 5, 11, 60), (136, 122, 5, 11, -60), (84, 52, 4, 9, 20), (116, 52, 4, 9, -20)):
        # elipse como dos arcos, en sentido contrario para recortar (evenodd)
        agujeros += '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" transform="rotate(%d %d %d)"/>' % (ax, ay, rx, ry, rot, ax, ay)
    venas = "".join("M100 %dL%s %s" % (180 - i * 8, f(100 + math.cos(math.radians(a)) * 80), f(98 - math.sin(math.radians(a)) * 72))
                    for i, a in enumerate((20, 160, 45, 135, 70, 110)))
    return ('<symbol id="%s" viewBox="0 0 200 220"><mask id="%s-m"><rect width="200" height="220" fill="#fff"/><g fill="#000">%s</g></mask>'
            '<g mask="url(#%s-m)"><path class="h-l" style="fill:var(--r,#0E6B48)" d="%s"/><path class="h-v" style="stroke:var(--v,rgba(255,255,255,.14))" d="%s" fill="none" stroke-width="1.4"/></g>'
            '<path class="h-n" style="stroke:var(--n,rgba(255,255,255,.28))" d="M100 220Q101 160 100 30" fill="none" stroke-width="2.4"/></symbol>') % (nombre, nombre, agujeros, nombre, d, venas)


def flor(nombre):
    """Heliconia estilizada: brácteas en zigzag. viewBox 0 0 80 200."""
    partes = []
    for i in range(6):
        y = 170 - i * 26
        lado = 1 if i % 2 else -1
        x0 = 40 + lado * 2
        partes.append("M%s %sQ%s %s %s %sQ%s %s %s %sZ" % (f(x0), f(y), f(40 + lado * 30), f(y + 2), f(40 + lado * 36), f(y - 34), f(40 + lado * 12), f(y - 16), f(x0), f(y - 20)))
    return ('<symbol id="%s" viewBox="0 0 80 200"><path class="h-n" style="stroke:var(--n,rgba(255,255,255,.28))" d="M40 200Q42 110 40 20" fill="none" stroke-width="2.4"/>'
            '<path class="h-f" style="fill:url(#g-flor)" d="%s"/></symbol>') % (nombre, "".join(partes))


def garabato(nombre, vueltas=2.3, rx=44, ry=36, ruido=2.2):
    pts = []
    n = int(vueltas * 48)
    for i in range(n + 1):
        t = i / 48
        a = 2.4 + t * 2 * math.pi
        k = 1 + .07 * t
        pts.append((50 + rx * k * math.cos(a) + random.uniform(-ruido, ruido), 50 + ry * k * math.sin(a) + random.uniform(-ruido, ruido)))
    # suavizado
    s = []
    for i in range(len(pts)):
        v = pts[max(0, i - 3):i + 4]
        s.append((sum(p[0] for p in v) / len(v), sum(p[1] for p in v) / len(v)))
    d = "M" + " ".join("%s %s" % (f(x), f(y)) for x, y in s)
    return '<symbol id="%s" viewBox="-8 -8 116 116"><path d="%s" pathLength="1"/></symbol>' % (nombre, d)


def zigzag(nombre, pasos=8):
    pts = ["%s %s" % (f(4 + i * (112 / pasos)), f(24 + (-14 if i % 2 else 14) + random.uniform(-2, 2))) for i in range(pasos + 1)]
    return '<symbol id="%s" viewBox="0 0 120 48"><path d="M%s" pathLength="1"/></symbol>' % (nombre, " L".join(pts))


def asterisco(nombre):
    trazos = []
    for k in range(4):
        a = k * math.pi / 4 + random.uniform(-.08, .08)
        trazos.append("M%s %sL%s %s" % (f(50 - 42 * math.cos(a)), f(50 - 42 * math.sin(a)), f(50 + 42 * math.cos(a)), f(50 + 42 * math.sin(a))))
    return '<symbol id="%s" viewBox="0 0 100 100"><path d="%s" pathLength="1"/></symbol>' % (nombre, "".join(trazos))


GRADIENTES = """
<linearGradient id="g-sombra" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0A2E3A"/><stop offset=".55" stop-color="#16154F"/><stop offset="1" stop-color="#1B4D5C"/></linearGradient>
<linearGradient id="g-selva" x1="0" y1="1" x2=".3" y2="0"><stop offset="0" stop-color="#073D2B"/><stop offset=".6" stop-color="#0E6B48"/><stop offset="1" stop-color="#1FA38A"/></linearGradient>
<linearGradient id="g-brote" x1="0" y1="1" x2=".4" y2="0"><stop offset="0" stop-color="#0E6B48"/><stop offset=".5" stop-color="#3FAE5C"/><stop offset="1" stop-color="#7ED36B"/></linearGradient>
<linearGradient id="g-luz" x1="0" y1="1" x2=".5" y2="0"><stop offset="0" stop-color="#3FAE5C"/><stop offset=".55" stop-color="#9BDD6E"/><stop offset="1" stop-color="#D9F08C"/></linearGradient>
<linearGradient id="g-agua" x1="0" y1="1" x2=".4" y2="0"><stop offset="0" stop-color="#0B4F58"/><stop offset=".6" stop-color="#1FA38A"/><stop offset="1" stop-color="#8EE3C8"/></linearGradient>
<linearGradient id="g-flor" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FF6A3D"/><stop offset=".6" stop-color="#FF4F9A"/><stop offset="1" stop-color="#F7D84A"/></linearGradient>
"""

simbolos = [
    lanza("hoja-lanza"), lanza("hoja-ancha", ancho=42, asim=7),
    pinnada("hoja-palma", 15, 54, 5.5, .9), pinnada("hoja-helecho", 22, 30, 3.2, .4, curva_raquis=14),
    monstera("hoja-monstera"), flor("flor-heliconia"),
    garabato("g-garabato"), garabato("g-garabato-2", vueltas=1.6, rx=40, ry=30), zigzag("g-zigzag"), asterisco("g-asterisco"),
]
sprite = ('<svg class="sprite" aria-hidden="true" focusable="false" width="0" height="0" style="position:absolute">'
          '<defs>%s</defs>%s</svg>') % (GRADIENTES.strip(), "".join(simbolos))
out = os.path.join(RAIZ, "scripts", "_sprite.svg")  # se incrusta en site/index.html
open(out, "w", encoding="utf-8").write(sprite)
print("sprite", len(sprite), "bytes")
