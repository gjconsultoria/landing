# Universo visual «Dosel»

Rediseño visual de la landing (22 oct 2026). Los textos no cambiaron: solo el arte, la maquetación y la interacción. Este universo es el referente para llevar la marca a redes (entradas, salidas y piezas en movimiento).

## Idea
Una caminata desde la luz del dosel hasta el río al anochecer. Blanco y tinta para leer; la selva, el aura del logo y los trazos a mano llevan el color.

| Momento | Sección | Lenguaje |
|---|---|---|
| Luz del dosel | Hero | La selva se abre y aparece el aura (el sol). Hojas en tres capas de profundidad que se apartan del cursor, polen flotando, rayos de luz. |
| Sotobosque | Qué necesitas resolver | Helechos bajos; cada situación lleva una hoja que se abre al elegirla. |
| Liana | Cómo trabajo | Una liana que se dibuja sola, con hojas que brotan; el paso activo saca un brote. |
| Claro | Servicios | Acordeón horizontal: cada servicio conserva su arte de marca (cintas, holográfico, multitud, luces, mosaico), ahora en verdes. |
| Hojas de archivo | Talleres | Carpetas arriba, los 4 módulos en una fila (carrusel en celular). |
| Retrato | Sobre mí | Foto en arco con aura y los garabatos de la firma (amarillo, agua, zigzag índigo, asteriscos). Un río une Leticia, Puerto Nariño y Guainía. |
| Noche de selva | Contacto | Fondo selva-índigo, aura del logo, luciérnagas que esquivan el cursor. |

## Paleta en uso
Tinta #121A16 · Niebla #F4F6F3 · Selva #0E6B48 · Brote #7ED36B · Lima #D9F08C · Agua #1FA38A · Polen #F7D84A · Índigo #2B2D8F. Heliconia #FF4F9A y Atardecer #FF6A3D solo como flor o acento puntual.

## Piezas reutilizables para redes
- **Apertura (close in):** «la selva se abre». Las hojas parten del centro hacia los bordes y aparece el aura. En la web: carga del hero.
- **Transición / salida (close out):** «cortina de hojas». Dos paños de selva con borde orgánico se cierran, el aura del logo late en el centro y se abren. En la web: al saltar entre secciones desde el menú, el pie o el riel.
- **Logo animado:** el aura respira y un brillo gira por encima; al pasar el cursor da un pequeño salto.
- **Gráfica secundaria:** garabatos, zigzag y asteriscos a mano alzada que se dibujan solos (los mismos de la firma de correo).
- **Hojas:** lanza, ancha, palma, helecho, monstera y heliconia, generadas en `scripts/generar-hojas.py` (vectoriales, reutilizables en cualquier tamaño).

## Interacción y rendimiento
- Solo con mouse: hojas que se apartan, luciérnaga de luz, botones magnéticos, reflejo en tarjetas.
- Navegación: cabecera flotante con marcador de sección, riel lateral con nudos por sección, botón de volver arriba.
- Todo se apaga con «reducir movimiento». Las animaciones y los lienzos se pausan fuera de pantalla.
- Sin librerías. Foto en WebP de 28 KB. Las hojas van en un solo sprite SVG incrustado.
