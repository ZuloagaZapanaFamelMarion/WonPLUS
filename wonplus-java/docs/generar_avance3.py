#!/usr/bin/env python3
"""Informe del Avance 3 de WonPLUS, formato A4."""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    FrameBreak,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
    Flowable,
)
from reportlab.platypus.tableofcontents import TableOfContents

OUT = str(
    Path(__file__).resolve().parents[1] / "avance-3" / "Avance_3_WonPLUS.pdf"
)

NAVY = HexColor("#1B3A4B")
BURG = HexColor("#7A2E36")
SAND = HexColor("#F6F3EC")
CREAM = HexColor("#EFE8DC")
LINE = HexColor("#C9C2B4")
INK = HexColor("#1C1C1C")
MUTED = HexColor("#5C564E")
GREEN = HexColor("#2C6B4A")
GREEN_SOFT = HexColor("#E5F0EA")
AMBER = HexColor("#8A5A12")
AMBER_SOFT = HexColor("#F8EFD9")
BLUE_SOFT = HexColor("#E7EEF2")

W = A4[0] - 5 * cm


def S(name, **kw):
    base = dict(
        fontName="Times-Roman",
        fontSize=12,
        leading=16,
        textColor=INK,
        alignment=TA_JUSTIFY,
    )
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    "cover_uni": S("cover_uni", fontName="Times-Bold", fontSize=12, leading=15, alignment=TA_CENTER, textColor=NAVY),
    "cover_course": S("cover_course", fontName="Times-Bold", fontSize=11, leading=14, alignment=TA_CENTER, textColor=BURG),
    "cover_title": S("cover_title", fontName="Times-Bold", fontSize=18, leading=22, alignment=TA_CENTER, textColor=NAVY),
    "cover_sub": S("cover_sub", fontName="Times-Italic", fontSize=12, leading=16, alignment=TA_CENTER, textColor=INK),
    "cover_meta": S("cover_meta", fontName="Times-Roman", fontSize=12, leading=16, alignment=TA_CENTER),
    "h1": S("H1", fontName="Times-Bold", fontSize=14, leading=18, alignment=TA_LEFT, textColor=NAVY, spaceBefore=14, spaceAfter=8),
    "h2": S("H2", fontName="Times-Bold", fontSize=12, leading=16, alignment=TA_LEFT, textColor=NAVY, spaceBefore=12, spaceAfter=4),
    "h3": S("H3", fontName="Times-Bold", fontSize=12, leading=16, alignment=TA_LEFT, textColor=BURG, spaceBefore=8, spaceAfter=3),
    "body": S("body", firstLineIndent=0.6 * cm, spaceAfter=8),
    "body0": S("body0", firstLineIndent=0, spaceAfter=8),
    "bullet": S("bullet", leftIndent=14, firstLineIndent=0, spaceAfter=2, leading=15),
    "caption": S("caption", fontName="Times-Italic", fontSize=10, leading=13, alignment=TA_CENTER, textColor=MUTED, spaceBefore=3, spaceAfter=10),
    "note": S("note", fontSize=10, leading=13, textColor=MUTED, spaceAfter=8),
    "cell": S("cell", fontSize=9, leading=11, alignment=TA_LEFT),
    "cellc": S("cellc", fontSize=9, leading=11, alignment=TA_CENTER),
    "th": S("th", fontName="Times-Bold", fontSize=9, leading=11, alignment=TA_CENTER, textColor=white),
    "thl": S("thl", fontName="Times-Bold", fontSize=9, leading=11, alignment=TA_LEFT, textColor=white),
    "src": S("src", fontName="Times-Roman", fontSize=11, leading=15, leftIndent=1.25 * cm, firstLineIndent=-1.25 * cm, spaceAfter=6),
    "code": S("code", fontName="Courier", fontSize=8, leading=10, alignment=TA_LEFT),
    "footer": S("footer", fontSize=9, alignment=TA_CENTER, textColor=NAVY),
}


class Lienzo(Flowable):
    def __init__(self, width, height, painter):
        super().__init__()
        self.box_w = width
        self.box_h = height
        self.painter = painter

    def wrap(self, aw, ah):
        self.width = min(self.box_w, aw)
        self.height = self.box_h
        return self.width, self.height

    def draw(self):
        self.painter(self.canv, self.width, self.height)


class Doc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ("H1", "H2"):
            level = 0 if flowable.style.name == "H1" else 1
            text = flowable.getPlainText()
            if text == "Índice":
                return
            key = f"k{self.page}-{level}-{abs(hash(text)) % 100000}"
            self.canv.bookmarkPage(key)
            try:
                self.canv.addOutlineEntry(text, key, level, 0)
            except Exception:
                pass
            self.notify("TOCEntry", (level, text, self.page))


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(NAVY)
        canvas.setLineWidth(0.8)
        canvas.line(2.5 * cm, A4[1] - 1.6 * cm, A4[0] - 2.5 * cm, A4[1] - 1.6 * cm)
        canvas.setFillColor(NAVY)
        canvas.setFont("Times-Italic", 9)
        canvas.drawString(2.5 * cm, A4[1] - 1.45 * cm, "WonPLUS — Avance 3 del proyecto final")
        canvas.drawRightString(A4[0] - 2.5 * cm, A4[1] - 1.45 * cm, "Curso Integrador I")
        canvas.line(2.5 * cm, 1.5 * cm, A4[0] - 2.5 * cm, 1.5 * cm)
        canvas.setFont("Times-Roman", 10)
        canvas.drawCentredString(A4[0] / 2, 1.05 * cm, str(doc.page))
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 1.3 * cm, A4[0], 1.3 * cm, fill=1, stroke=0)
    canvas.rect(0, 0, A4[0], 1.1 * cm, fill=1, stroke=0)
    canvas.setFillColor(BURG)
    canvas.rect(0, A4[1] - 1.5 * cm, A4[0], 0.2 * cm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Times-Roman", 9)
    canvas.drawCentredString(A4[0] / 2, 0.45 * cm, "Universidad Tecnológica del Perú  ·  2026")
    canvas.restoreState()


def P(text, style="body"):
    return Paragraph(text, ST[style])


def H(text, level=1):
    return Paragraph(text, ST["h1" if level == 1 else "h2" if level == 2 else "h3"])


def bullets(items):
    out = []
    for item in items:
        out.append(Paragraph("•  " + item, ST["bullet"]))
    out.append(Spacer(1, 6))
    return out


def tabla(headers, rows, col_widths):
    head = [Paragraph(h, ST["th"]) for h in headers]
    data = [head]
    for row in rows:
        data.append([Paragraph(str(c), ST["cell"]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 1), (-1, -1), white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, SAND]),
                ("GRID", (0, 0), (-1, -1), 0.3, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def caption(text):
    return Paragraph(text, ST["caption"])


def bloque(c, x, y, w, h, titulo, cuerpo, fill):
    c.setFillColor(fill)
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Times-Bold", 8)
    c.drawString(x + 5, y + h - 11, titulo)
    estilo = ParagraphStyle(
        "mini",
        fontName="Times-Roman",
        fontSize=7.5,
        leading=9.2,
        textColor=INK,
    )
    Frame(x + 4, y + 3, w - 8, h - 16, showBoundary=0).addFromList(
        [Paragraph(cuerpo, estilo)], c
    )


def pintar_canvas(c, w, h):
    gap = 4
    bottom_h = 78
    top_h = h - bottom_h - gap
    cols = 5
    cw = (w - gap * (cols - 1)) / cols
    y_top = bottom_h + gap
    xs = [i * (cw + gap) for i in range(cols)]
    mid = top_h / 2 - 2
    bloque(
        c, xs[0], y_top, cw, top_h, "Socios clave",
        "Proveedor de base de datos y equipo de desarrollo. Docente del curso como revisor del alcance. Posible aliado de capacitación para MYPES.",
        CREAM,
    )
    bloque(
        c, xs[1], y_top + mid + 4, cw, top_h - mid - 4, "Actividades clave",
        "Desarrollar el aplicativo, mantener el inventario coherente con la venta y validar el uso con el negocio.",
        BLUE_SOFT,
    )
    bloque(
        c, xs[1], y_top, cw, mid, "Recursos clave",
        "Java 21, Maven, Swing, PostgreSQL, repositorio GitHub y la documentación del proyecto.",
        BLUE_SOFT,
    )
    bloque(
        c, xs[2], y_top, cw, top_h, "Propuesta de valor",
        "Un solo sistema, sencillo y local, para registrar la venta, descontar el stock y consultar la ganancia sin rehacer cálculos a mano.",
        HexColor("#F3E4E6"),
    )
    bloque(
        c, xs[3], y_top + mid + 4, cw, top_h - mid - 4, "Relación",
        "Acompañamiento inicial, cuentas de administrador y vendedor, y soporte sobre el flujo de venta.",
        GREEN_SOFT,
    )
    bloque(
        c, xs[3], y_top, cw, mid, "Canales",
        "Demostración directa del programa, repositorio del código y canales digitales del negocio.",
        GREEN_SOFT,
    )
    bloque(
        c, xs[4], y_top, cw, top_h, "Segmentos",
        "Micro y pequeñas empresas y emprendedores que venden productos y hoy controlan caja y stock en cuaderno u hoja de cálculo.",
        CREAM,
    )
    half = (w - gap) / 2
    bloque(
        c, 0, 0, half, bottom_h, "Estructura de costos",
        "Tiempo de desarrollo, equipo con JDK y PostgreSQL, mantenimiento del código y documentación. En esta etapa el costo es académico.",
        AMBER_SOFT,
    )
    bloque(
        c, half + gap, 0, half, bottom_h, "Fuentes de ingresos",
        "El MVP no se comercializa todavía. Una etapa posterior puede evaluar licencia, suscripción o soporte, solo después de validar la utilidad.",
        AMBER_SOFT,
    )


def pintar_barras(c, w, h, titulo, pares, colores):
    c.setFillColor(SAND)
    c.setStrokeColor(LINE)
    c.roundRect(0, 0, w, h, 4, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Times-Bold", 10)
    c.drawString(10, h - 16, titulo)
    max_v = max(v for _, v in pares) or 1
    bar_w = w - 170
    y = h - 38
    for i, (nombre, valor) in enumerate(pares):
        c.setFillColor(INK)
        c.setFont("Times-Roman", 9)
        c.drawString(10, y + 2, nombre)
        c.setFillColor(HexColor("#E6E1D8"))
        c.roundRect(145, y, bar_w, 12, 2, fill=1, stroke=0)
        c.setFillColor(colores[i % len(colores)])
        c.roundRect(145, y, bar_w * (valor / max_v), 12, 2, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Times-Bold", 8)
        c.drawRightString(w - 10, y + 2, str(valor))
        y -= 22


def ventana(c, x, y, w, h, numero, titulo, zonas, estado):
    c.setStrokeColor(NAVY)
    c.setFillColor(HexColor("#FBF9F5"))
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.rect(x, y + h - 16, w, 16, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Times-Bold", 8)
    c.drawString(x + 6, y + h - 11, f"{numero}   {titulo}")
    c.setFillColor(GREEN if estado == "Construida" else AMBER)
    c.roundRect(x + w - 68, y + h - 13, 60, 10, 2, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Times-Bold", 6)
    c.drawCentredString(x + w - 38, y + h - 10.5, estado.upper())
    yy = y + h - 30
    for zona in zonas:
        c.setFillColor(white)
        c.setStrokeColor(LINE)
        c.roundRect(x + 8, yy - 2, w - 16, 16, 2, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Times-Roman", 8)
        c.drawString(x + 14, yy + 2, zona)
        yy -= 20


def pintar_pantallas(c, w, h, pantallas):
    cols = 2
    gap = 8
    cw = (w - gap) / cols
    rows = (len(pantallas) + 1) // 2
    ch = (h - gap * (rows - 1)) / rows
    for i, pantalla in enumerate(pantallas):
        col = i % cols
        row = i // cols
        x = col * (cw + gap)
        y = h - (row + 1) * ch - row * gap
        ventana(c, x, y, cw, ch - 2, *pantalla)


def pintar_gantt(c, w, h, fases):
    left = 158
    legend = 18
    top = h - 14
    c.setFillColor(NAVY)
    c.setFont("Times-Bold", 8)
    c.drawString(4, top, "Fase")
    weeks = 18
    gw = (w - left - 6) / weeks
    for i in range(weeks):
        c.setFillColor(MUTED)
        c.setFont("Times-Roman", 6)
        c.drawCentredString(left + gw * i + gw / 2, top, str(i + 1))
    usable = top - 16 - legend
    row_h = usable / len(fases)
    for i, (nombre, inicio, fin, hecho) in enumerate(fases):
        y = legend + 8 + usable - (i + 1) * row_h
        if i % 2 == 0:
            c.setFillColor(SAND)
            c.rect(0, y, w, row_h, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Times-Roman", 7)
        c.drawString(4, y + row_h / 2 - 3, nombre)
        ancho = max(gw * (fin - inicio + 1) - 2, 3)
        c.setFillColor(GREEN if hecho else HexColor("#E4C98A"))
        c.setStrokeColor(NAVY)
        c.setLineWidth(0.4)
        c.roundRect(left + gw * (inicio - 1), y + 4, ancho, row_h - 8, 2, fill=1, stroke=0)
    c.setFillColor(white)
    c.rect(0, 0, w, legend - 1, fill=1, stroke=0)
    c.setFont("Times-Roman", 7)
    c.setFillColor(GREEN)
    c.rect(4, 4, 10, 8, fill=1, stroke=0)
    c.setFillColor(INK)
    c.drawString(18, 5, "Hecho")
    c.setFillColor(HexColor("#E4C98A"))
    c.rect(62, 4, 10, 8, fill=1, stroke=0)
    c.setFillColor(INK)
    c.drawString(76, 5, "Pendiente")
    c.setFillColor(MUTED)
    c.drawRightString(w - 2, 5, "Eje: semanas 1 a 18")


def caja_uml(c, x, y, w, h, titulo, campos):
    head = 16
    c.setStrokeColor(NAVY)
    c.setFillColor(BLUE_SOFT)
    c.rect(x, y + h - head, w, head, fill=1, stroke=1)
    c.setFillColor(white)
    c.rect(x, y, w, h - head, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Times-Bold", 8)
    c.drawCentredString(x + w / 2, y + h - 11, titulo)
    c.setFillColor(INK)
    c.setFont("Times-Roman", 7.5)
    yy = y + h - head - 12
    for campo in campos:
        c.drawString(x + 5, yy, campo)
        yy -= 11


def pintar_clases(c, w, h):
    gap = 12
    bw = (w - 2 * gap) / 3
    bot_h = 96
    caja_uml(c, 0, 6, bw, bot_h, "Producto", [
        "id, nombre",
        "precio, costo",
        "stock, stockMinimo",
        "idCategoria, categoria",
        "stockBajo()",
    ])
    caja_uml(c, bw + gap, 6, bw, bot_h, "Venta", [
        "id, fecha",
        "total, ganancia",
        "idUsuario, vendedor",
        "detalles : List",
    ])
    caja_uml(c, 2 * (bw + gap), 6, bw, bot_h, "DetalleVenta", [
        "id, idProducto",
        "nombreProducto",
        "cantidad",
        "precioUnitario",
        "costoUnitario",
        "subtotal()",
    ])
    top_y = bot_h + 22
    caja_uml(c, 0, top_y, bw, h - top_y - 4, "Usuario", [
        "id, nombre, email",
        "passwordHash",
        "rol : Rol",
        "activo : boolean",
    ])
    caja_uml(c, bw + gap, top_y + 18, bw, h - top_y - 22, "Rol", [
        "ADMIN",
        "VENDEDOR",
        "etiqueta()",
    ])
    caja_uml(c, 2 * (bw + gap), top_y + 18, bw, h - top_y - 22, "Categoria", [
        "id : int",
        "nombre : String",
    ])


def pintar_er(c, w, h):
    bw = 124
    gap = (w - 3 * bw) / 2

    def ent(x, y, bh, titulo, attrs):
        caja_uml(c, x, y, bw, bh, titulo, attrs)

    def flecha(x1, x2, y, texto):
        c.setStrokeColor(BURG)
        c.setLineWidth(0.9)
        c.line(x1, y, x2, y)
        mid = (x1 + x2) / 2
        c.setFillColor(white)
        c.roundRect(mid - 12, y - 5, 24, 11, 2, fill=1, stroke=0)
        c.setFillColor(BURG)
        c.setFont("Times-Bold", 7)
        c.drawCentredString(mid, y - 2, texto)

    ent(0, h - 118, 108, "usuario", [
        "PK  id_usuario", "nombre", "email  UK",
        "password_hash", "rol", "activo",
    ])
    ent(bw + gap, h - 100, 90, "venta", [
        "PK  id_venta", "fecha", "total", "FK  id_usuario",
    ])
    ent(2 * (bw + gap), h - 128, 118, "detalle_venta", [
        "PK  id_detalle", "cantidad", "precio_unitario",
        "costo_unitario", "FK  id_venta", "FK  id_producto",
    ])
    flecha(bw, bw + gap, h - 70, "1:N")
    flecha(2 * bw + gap, 2 * (bw + gap), h - 70, "1:N")
    ent(0, 8, 78, "categoria", [
        "PK  id_categoria", "nombre  UK",
    ])
    ent(bw + gap, 8, 108, "producto", [
        "PK  id_producto", "nombre", "precio", "costo",
        "stock", "stock_minimo", "FK  id_categoria",
    ])
    flecha(bw, bw + gap, 46, "1:N")
    c.setFillColor(MUTED)
    c.setFont("Times-Italic", 8)
    c.drawString(2 * (bw + gap), 36, "producto 1:N")
    c.drawString(2 * (bw + gap), 24, "detalle_venta")


def pintar_proceso(c, w, h, pasos, titulo, color):
    c.setFillColor(NAVY)
    c.setFont("Times-Bold", 10)
    c.drawString(0, h - 12, titulo)
    n = len(pasos)
    gap = 14
    bw = (w - (n - 1) * gap) / n
    box_h = h - 28
    for i, paso in enumerate(pasos):
        x = i * (bw + gap)
        c.setFillColor(color)
        c.setStrokeColor(NAVY)
        c.setLineWidth(0.8)
        c.roundRect(x, 6, bw, box_h, 4, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Times-Bold", 8)
        c.drawCentredString(x + bw / 2, 6 + box_h / 2 - 3, paso)
        if i < n - 1:
            c.setFillColor(BURG)
            c.setFont("Times-Bold", 9)
            c.drawCentredString(x + bw + gap / 2, 6 + box_h / 2 - 3, ">")


def pintar_capas(c, w, h):
    capas = [
        ("Vista", "11 pantallas Swing. Solo muestran datos y envían la acción.", SAND),
        ("Controlador", "ControladorPrincipal recibe la acción y llama al servicio.", CREAM),
        ("Servicio", "Reglas de venta, stock, usuarios, periodos y sesión.", BLUE_SOFT),
        ("DAO", "Interfaces Usuario, Categoria, Producto y Venta. JDBC aparte.", GREEN_SOFT),
        ("PostgreSQL", "usuario, categoria, producto, venta y detalle_venta.", AMBER_SOFT),
    ]
    gap = 6
    ch = (h - gap * (len(capas) - 1)) / len(capas)
    y = h - ch
    for nombre, texto, fill in capas:
        c.setFillColor(fill)
        c.setStrokeColor(NAVY)
        c.roundRect(70, y, w - 140, ch - 1, 3, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Times-Bold", 9)
        c.drawCentredString(w / 2, y + ch - 14, nombre)
        c.setFillColor(INK)
        c.setFont("Times-Roman", 8)
        c.drawCentredString(w / 2, y + 8, texto)
        y -= ch + gap


def code_block(text):
    return Preformatted(text, ST["code"])


def pantallas_sol1():
    return [
        ("1", "Inicio de sesión", ["Correo", "Contraseña", "Botón Ingresar"], "Construida"),
        ("2", "Panel", ["Ventas del día", "Ganancia del día", "Productos con stock bajo"], "Construida"),
        ("3", "Registrar venta", ["Producto y cantidad", "Líneas del pedido", "Total y confirmar"], "Construida"),
        ("4", "Ticket", ["Número y fecha", "Detalle y total", "Vendedor de la sesión"], "Construida"),
        ("5", "Historial", ["Periodo de consulta", "Lista de ventas", "Acceso al detalle"], "Construida"),
        ("6", "Detalle de venta", ["Líneas vendidas", "Cantidad y precio", "Subtotal de la línea"], "Construida"),
        ("7", "Alertas de stock", ["Producto en el mínimo", "Stock actual", "Stock mínimo"], "Construida"),
        ("8", "Reportes", ["Día, semana o mes", "Totales del periodo", "Exportar a Excel"], "Construida"),
        ("9", "Productos", ["Nombre, precio y costo", "Stock y stock mínimo", "Categoría. Solo admin."], "Construida"),
        ("10", "Categorías", ["Alta de categoría", "Edición", "Eliminación. Solo admin."], "Construida"),
        ("11", "Usuarios", ["Nombre y correo", "Rol y clave", "Activo o inactivo. Solo admin."], "Construida"),
    ]


def pantallas_sol2():
    return [
        ("1", "Acceso web", ["Correo y contraseña", "Rol al ingresar", "Sesión del navegador"], "Diseño"),
        ("2", "Panel web", ["Ventas del día", "Ganancia", "Aviso de stock"], "Diseño"),
        ("3", "Punto de venta", ["Buscar producto", "Cantidad", "Confirmar venta"], "Diseño"),
        ("4", "Comprobante", ["Datos de la venta", "Líneas", "Total"], "Diseño"),
        ("5", "Historial web", ["Filtro de fechas", "Ventas del periodo", "Ver detalle"], "Diseño"),
        ("6", "Detalle web", ["Productos vendidos", "Cantidades", "Importes"], "Diseño"),
        ("7", "Catálogo", ["Alta de producto", "Precio, costo y stock", "Solo administrador"], "Diseño"),
        ("8", "Categorías web", ["Listado", "Crear y editar", "Eliminar"], "Diseño"),
        ("9", "Usuarios web", ["Rol administrador", "Rol vendedor", "Estado de la cuenta"], "Diseño"),
        ("10", "Reportes web", ["Periodo", "Totales", "Descarga Excel"], "Diseño"),
    ]


def pantallas_sol3():
    return [
        ("1", "Inicio de sesión", ["Correo", "Contraseña", "Ingreso local"], "Diseño"),
        ("2", "Panel", ["Venta del día", "Stock crítico", "Último correo enviado"], "Diseño"),
        ("3", "Correo del negocio", ["Servidor SMTP", "Cuenta remitente", "Prueba de envío"], "Diseño"),
        ("4", "Registrar venta", ["Pedido", "Control de stock", "Confirmar"], "Diseño"),
        ("5", "Ticket", ["Comprobante local", "Opción de reenvío", "Total"], "Diseño"),
        ("6", "Productos", ["Precio y costo", "Stock mínimo", "Categoría"], "Diseño"),
        ("7", "Alertas", ["Productos bajo mínimo", "Destinatario", "Enviar aviso"], "Diseño"),
        ("8", "Reporte programado", ["Hora de envío", "Periodo del resumen", "Activar o pausar"], "Diseño"),
        ("9", "Bandeja de envíos", ["Fecha del correo", "Resultado", "Reintento"], "Diseño"),
        ("10", "Usuarios", ["Administrador", "Vendedor", "Quién recibe alertas"], "Diseño"),
    ]


def rejilla(pantallas):
    cols = 2
    rows = (len(pantallas) + cols - 1) // cols
    row_h = 108
    gap = 8
    height = rows * row_h + (rows - 1) * gap
    return Lienzo(W, height, lambda c, w, h: pintar_pantallas(c, w, h, pantallas))


def build_story():
    story = []
    story.append(Spacer(1, 2.2 * cm))
    story.append(P("UNIVERSIDAD TECNOLÓGICA DEL PERÚ", "cover_uni"))
    story.append(P("FACULTAD DE INGENIERÍA", "cover_uni"))
    story.append(P("CARRERA PROFESIONAL DE INGENIERÍA DE", "cover_uni"))
    story.append(P("SISTEMAS E INFORMÁTICA", "cover_uni"))
    story.append(Spacer(1, 0.45 * cm))
    story.append(P("CURSO INTEGRADOR I: SISTEMAS SOFTWARE", "cover_course"))
    story.append(Spacer(1, 1.1 * cm))
    story.append(P("AVANCE 3 DEL PROYECTO FINAL", "cover_title"))
    story.append(Spacer(1, 0.25 * cm))
    story.append(P("WonPLUS", "cover_title"))
    story.append(Spacer(1, 0.3 * cm))
    story.append(P("Sistema de gestión de ventas e inventarios para MYPES", "cover_sub"))
    story.append(Spacer(1, 0.25 * cm))
    story.append(P("Informe del avance de proyecto final 4 (proyecto 2)", "cover_sub"))
    story.append(Spacer(1, 1.5 * cm))
    story.append(P("Alumna: Famel Marion Zuloaga Zapana", "cover_meta"))
    story.append(P("Docente: Irani Guillen Gómez", "cover_meta"))
    story.append(Spacer(1, 1.2 * cm))
    story.append(P("Lima — Perú", "cover_meta"))
    story.append(P("2026", "cover_meta"))
    story.append(NextPageTemplate("interior"))
    story.append(PageBreak())

    story.append(H("Índice"))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC1", fontName="Times-Bold", fontSize=12, leading=16, leftIndent=0, firstLineIndent=0, spaceBefore=7, textColor=NAVY),
        ParagraphStyle("TOC2", fontName="Times-Roman", fontSize=11, leading=14, leftIndent=14, firstLineIndent=0, spaceBefore=1, textColor=INK),
    ]
    story.append(toc)
    story.append(PageBreak())

    story.append(H("1. Introducción"))
    story.append(P(
        "Este informe es el avance 3 de WonPLUS. Recoge el análisis ya presentado en el avance 2 "
        "y le agrega el trabajo construido después: la aplicación de escritorio, su arquitectura, "
        "las pruebas, las librerías, los diagramas alineados al código y la publicación del "
        "repositorio. El documento responde a la consigna del avance de proyecto final 4, "
        "en el que el equipo actúa como consultor y entrega una solución informática para un "
        "proceso concreto de la empresa."
    ))
    story.append(P(
        "La solución elegida y construida es una aplicación de escritorio en Java 21, con Maven, "
        "Swing y PostgreSQL. Cubre el alcance comprometido desde el avance 2: usuarios, productos, "
        "ventas, actualización de inventario y reportes básicos. El código está en "
        "https://github.com/ZuloagaZapanaFamelMarion/WonPLUS, dentro de la carpeta wonplus-java."
    ))
    story.append(P(
        "El avance 2 describía un prototipo de cuatro pantallas y dejaba las alternativas 2 y 3 "
        "ilustradas con productos comerciales ajenos al equipo. Este avance corrige esa distancia: "
        "documenta las once pantallas que ya funcionan, reemplaza esas referencias externas por "
        "dos diseños propios en Java y completa el Project Charter, el Gantt y los diagramas "
        "con los datos reales del programa."
    ))

    story.append(H("2. Contexto de la empresa"))
    story.append(P(
        "WonPLUS es una propuesta para micro y pequeñas empresas del Perú que necesitan controlar "
        "ventas e inventario con una herramienta sencilla. El proyecto nace de la dificultad para "
        "registrar operaciones a mano, seguir el stock y consultar el resultado del negocio."
    ))
    story.append(P(
        "La solución es un sistema de gestión de ventas e inventarios con arquitectura "
        "modelo–vista–controlador y base de datos relacional PostgreSQL. Prioriza una interfaz "
        "directa, el registro de la venta, la actualización del inventario y reportes sencillos, "
        "incluido el archivo Excel del periodo."
    ))
    story.append(P(
        "El usuario principal es el emprendedor o el responsable de una MYPE. El sistema distingue "
        "dos roles. El administrador gestiona productos, categorías y usuarios. El vendedor registra "
        "ventas y consulta panel, historial, alertas y reportes. El menú oculta la administración "
        "cuando la sesión pertenece a un vendedor."
    ))

    story.append(H("3. Identificación del problema"))
    story.append(P(
        "El problema es la dificultad de algunas MYPES para disponer de un sistema sencillo que "
        "registre ventas, controle inventario y deje consultar la información básica del negocio. "
        "El cuaderno y la hoja de cálculo producen errores, pérdida de datos y poca claridad sobre "
        "la ganancia."
    ))
    story.append(P(
        "También existe una barrera de acceso: varias herramientas de gestión tienen un costo o "
        "una complejidad que no corresponden a un negocio pequeño. WonPLUS se limita a las "
        "operaciones esenciales de ese negocio y se ejecuta en el equipo local."
    ))

    story.append(H("4. Descripción del problema"))
    story.append(P(
        "En el proceso manual, la venta se anota en papel o en un registro informal. Después esa "
        "información se transcribe a un cuaderno o a una hoja de cálculo, los totales se calculan "
        "a mano, el comprobante se guarda en físico y la ganancia se estima revisando lo anotado."
    ))
    story.append(P(
        "Ese recorrido afecta tres puntos: el control del inventario, la consulta de las ventas y "
        "la decisión que depende de datos registrados de la misma manera cada vez. La solución "
        "concentra esas operaciones en un solo flujo: autenticar al usuario, registrar la venta, "
        "descontar el stock y consultar el resultado."
    ))

    story.append(H("5. Alcance de la solución"))
    story.append(P(
        "El alcance comprende cinco operaciones: gestión de usuarios con roles, gestión de "
        "categorías y productos, registro de ventas con ticket, actualización del inventario al "
        "confirmar la venta, con alerta de stock bajo, y reportes por periodo con exportación a Excel."
    ))
    story.append(P(
        "Esta versión trabaja en el equipo local o en una red básica. Quedan para una etapa "
        "posterior la facturación electrónica, la conexión con SUNAT, el lector físico de código "
        "de barras, los respaldos automatizados y el despliegue en la nube. El tamaño del alcance "
        "corresponde al problema descrito en el avance 2 y al esfuerzo de la solución ya construida."
    ))

    story.append(H("5.1 Visión", 2))
    story.append(P(
        "Ser una solución de gestión sencilla para MYPES que facilite el registro de ventas y el "
        "control de inventario, reduzca la dependencia de procesos manuales y ofrezca información "
        "clara para la gestión cotidiana del negocio."
    ))
    story.append(H("5.2 Misión", 2))
    story.append(P(
        "Desarrollar y mantener una herramienta accesible para que el pequeño negocio registre sus "
        "operaciones, controle sus productos y consulte las ventas mediante una interfaz simple."
    ))
    story.append(H("5.3 Entorno", 2))
    story.append(tabla(
        ["Factor", "Descripción"],
        [
            ["Interno", "Aplicación Java 21, Maven, Swing, PostgreSQL y JDBC. Alcance académico centrado en las cinco operaciones."],
            ["Clientes", "MYPES y emprendedores que requieren controlar ventas, productos y stock."],
            ["Tecnológico", "Escritorio Java, base relacional, consultas preparadas y exportación con Apache POI."],
            ["Competitivo", "Software comercial de gestión y métodos manuales, como el cuaderno y la hoja de cálculo."],
            ["Legal", "Referencia de la Ley N.° 29733, Ley de Protección de Datos Personales, aplicada al tratamiento de la cuenta de usuario."],
        ],
        [3.2 * cm, W - 3.2 * cm],
    ))
    story.append(Spacer(1, 8))
    story.append(H("5.4 Estrategias", 2))
    story.extend(bullets([
        "Priorizar productos, ventas, stock y reportes antes que funciones de una etapa posterior.",
        "Mantener textos claros y una operación directa en cada pantalla.",
        "Separar vista, controlador, servicio y acceso a datos.",
        "Guardar la información en PostgreSQL con consultas preparadas y la contraseña cifrada.",
        "Verificar las reglas de negocio con pruebas JUnit y ampliar después la validación con más MYPES.",
    ]))
    story.append(H("5.5 Planes", 2))
    story.append(tabla(
        ["Horizonte", "Plan"],
        [
            ["Corto plazo", "Cerrar el MVP: venta con descuento de stock, administración por roles, reporte y Excel. Entregar este informe y sustentar."],
            ["Mediano plazo", "Mejorar la experiencia de uso, ampliar la validación con MYPES y evaluar una versión web con el mismo alcance."],
            ["Largo plazo", "Estudiar facturación electrónica, respaldos y nuevas funciones solo cuando el uso del MVP esté comprobado."],
        ],
        [3.2 * cm, W - 3.2 * cm],
    ))
    story.append(Spacer(1, 8))

    story.append(H("5.6 Modelo de negocio en Canvas", 2))
    story.append(P(
        "El avance 2 presentaba el modelo de negocio en una tabla y el Lean Canvas en el anexo. "
        "Este avance agrega el lienzo de nueve bloques, que es la herramienta pedida para graficar "
        "el análisis. Los bloques usan el mismo contenido del avance 2, actualizado con la "
        "tecnología que ya está en el programa."
    ))
    story.append(Lienzo(W, 300, pintar_canvas))
    story.append(caption("Figura 1. Lienzo de modelo de negocio de WonPLUS."))
    story.append(P(
        "La propuesta de valor queda en el centro: registrar la venta y conocer el stock y la "
        "ganancia en el mismo sistema. Los segmentos son MYPES con control todavía manual. Los "
        "costos de esta etapa son de desarrollo académico. Los ingresos de una comercialización "
        "futura se dejan condicionados a una validación posterior, para no prometer un modelo "
        "que el MVP todavía no comprueba."
    ))

    story.append(H("5.7 Análisis del negocio", 2))
    story.append(P(
        "La encuesta piloto del avance 2 se aplicó a 6 emprendedores de MYPES en Lima. Por el "
        "tamaño de la muestra, los resultados son una primera lectura del problema y no una "
        "representación de todas las MYPES del país."
    ))
    story.append(Lienzo(W, 120, lambda c, w, h: pintar_barras(
        c, w, h, "¿Cómo controla ingresos y egresos? (n = 6)",
        [("Cuaderno o libreta", 3), ("Software", 2), ("Excel", 1)],
        [NAVY, GREEN, AMBER],
    )))
    story.append(caption("Figura 2. Método de control reportado por los seis encuestados."))
    story.append(P(
        "Tres de seis usan cuaderno o libreta, dos usan algún software y uno usa Excel. En la "
        "muestra, cuatro de seis no usan un software dedicado a esta actividad."
    ))
    story.append(Lienzo(W, 120, lambda c, w, h: pintar_barras(
        c, w, h, "¿Sabe cuánto ganó el último mes? (n = 6)",
        [("Sí", 3), ("Más o menos", 2), ("No", 1)],
        [GREEN, AMBER, BURG],
    )))
    story.append(caption("Figura 3. Claridad declarada sobre la ganancia mensual."))
    story.append(P(
        "La mitad de la muestra afirmó conocer la ganancia del último mes. Dos de seis la conocen "
        "de forma aproximada y uno indicó que no la tiene clara."
    ))
    story.append(Lienzo(W, 110, lambda c, w, h: pintar_barras(
        c, w, h, "Interés en probar la solución (n = 6)",
        [("Interés en probar", 3), ("Sin interés inmediato", 3)],
        [NAVY, HexColor("#8D8378")],
    )))
    story.append(caption("Figura 4. Interés inicial ante la propuesta."))
    story.append(P(
        "Tres emprendedores manifestaron interés en probar la propuesta y tres prefirieron seguir "
        "con su método actual. Ese resultado obliga a mantener el sistema simple y a seguir "
        "validando la aceptación, en lugar de ampliar funciones."
    ))
    story.extend(bullets([
        "Problema principal: el control sigue en procesos manuales o en herramientas no especializadas.",
        "Necesidad: información de ventas e inventario ordenada y fácil de consultar.",
        "Oportunidad: concentrar productos, ventas, stock y reportes en un único sistema.",
        "Riesgo: la muestra es pequeña y la mitad no mostró interés inmediato.",
        "Indicador del MVP: registrar una venta, actualizar el stock y consultar el resultado sin cálculo manual.",
    ]))

    story.append(H("6. Tres alternativas de solución"))
    story.append(P(
        "La consigna pide tres alternativas propias, cada una con al menos diez pantallas y al "
        "menos un 50 % de Java, de modo que cualquiera de ellas pueda cubrir el mismo alcance. "
        "Las tres propuestas de este avance son del proyecto. La alternativa 1 está construida "
        "y es la que se sustenta. Las alternativas 2 y 3 son diseños evaluados para comparar "
        "esfuerzo, acceso y alcance; no están codificadas y el informe no las presenta como "
        "parte del programa entregado."
    ))
    story.append(tabla(
        ["Alternativa", "Tecnología", "Java", "Pantallas", "Estado"],
        [
            ["1. WonPLUS Escritorio", "Java 21, Swing, Maven, JDBC y PostgreSQL", "100 %", "11", "Construida y publicada"],
            ["2. WonPLUS Web", "Backend Java con Spring Boot y PostgreSQL; interfaz en el navegador", "Más del 50 %: reglas, seguridad y persistencia en Java", "10", "Diseño"],
            ["3. WonPLUS Correo", "Java de escritorio, PostgreSQL y JavaMail para avisos y resumen", "100 % de la aplicación; el correo es una librería Java", "10", "Diseño"],
        ],
        [3.3 * cm, 4.6 * cm, 3.6 * cm, 2.0 * cm, 2.6 * cm],
    ))
    story.append(Spacer(1, 8))
    story.append(P(
        "Se eligió la alternativa 1 porque cubre el alcance con el menor despliegue: no exige "
        "servidor web ni correo externo para cumplir la venta, el stock y el reporte. El Excel "
        "se genera en el equipo con Apache POI. Las otras dos siguen siendo caminos válidos si "
        "más adelante se necesita acceso desde el navegador o aviso por correo."
    ))

    story.append(H("6.1 Alternativa 1: WonPLUS Escritorio", 2))
    story.append(P(
        "Es la solución del repositorio. El usuario entra con correo y contraseña. Según el rol, "
        "el menú muestra o reserva la administración. Una venta confirma cantidades, calcula el "
        "total y la ganancia, graba la operación y descuenta el stock en la misma transacción. "
        "Si no hay stock suficiente, la venta se rechaza. El reporte del periodo se exporta a "
        "un archivo .xlsx."
    ))
    story.append(rejilla(pantallas_sol1()))
    story.append(caption("Figura 5. Once pantallas de la alternativa 1, construidas en Swing."))
    story.append(P(
        "El vendedor usa inicio de sesión, panel, venta, ticket, historial, detalle, alertas y "
        "reportes. El administrador usa esas mismas pantallas y, además, productos, categorías "
        "y usuarios. El ticket y el detalle se abren desde el flujo de la venta y del historial; "
        "por eso no aparecen como botones fijos del menú lateral, pero son pantallas propias del sistema."
    ))

    story.append(H("6.2 Alternativa 2: WonPLUS Web", 2))
    story.append(P(
        "Misma empresa, mismo problema y mismo alcance, con acceso desde el navegador. El backend "
        "sería Java, con Spring Boot, la misma base PostgreSQL y las mismas reglas de rol, stock "
        "y reporte. La interfaz web consumiría esa API. La parte Java —autenticación, reglas, "
        "persistencia y generación del Excel— supera la mitad de la solución. Esta alternativa "
        "sirve si el negocio necesita consultar desde más de un equipo. Aumenta el trabajo de "
        "despliegue, sesión web y mantenimiento, y por eso quedó como diseño y no como el MVP."
    ))
    story.append(rejilla(pantallas_sol2()))
    story.append(caption("Figura 6. Diez pantallas diseñadas para la alternativa web con backend Java."))

    story.append(H("6.3 Alternativa 3: WonPLUS Correo", 2))
    story.append(P(
        "También es una aplicación Java de escritorio con PostgreSQL. Agrega JavaMail para avisar "
        "el stock bajo y enviar un resumen del día. Cubre el alcance y suma la comunicación hacia "
        "el responsable que no está mirando la pantalla. Exige una cuenta de correo, un servidor "
        "SMTP y el cuidado de esas credenciales. Como el alcance aprobado se cumple con la consulta "
        "en el programa y con el Excel, el correo quedó fuera de la versión construida. Apache POI, "
        "que sí está integrado, cubre el requisito de librería de reportes de la consigna."
    ))
    story.append(rejilla(pantallas_sol3()))
    story.append(caption("Figura 7. Diez pantallas diseñadas para la alternativa Java con correo."))

    story.append(H("6.4 Comparación y decisión", 2))
    story.append(tabla(
        ["Criterio", "Escritorio", "Web", "Correo"],
        [
            ["Cubre usuarios, productos, venta, stock y reporte", "Sí, en el código", "Sí, en el diseño", "Sí, en el diseño"],
            ["Porcentaje Java", "100 %", "Más del 50 %", "100 %"],
            ["Pantallas", "11 construidas", "10 diseñadas", "10 diseñadas"],
            ["Qué necesita para funcionar", "JDK, Maven y PostgreSQL", "Servidor y navegador", "JDK, PostgreSQL y SMTP"],
            ["Riesgo principal", "Uso en un solo equipo", "Más despliegue", "Credenciales de correo"],
            ["Decisión", "Seleccionada", "Evolución posible", "Evolución posible"],
        ],
        [5.4 * cm, 3.6 * cm, 3.5 * cm, 3.6 * cm],
    ))
    story.append(Spacer(1, 8))

    story.append(H("7. Gestión del proyecto"))
    story.append(H("7.1 Project Charter", 2))
    story.append(P(
        "El avance 2 incluía un charter básico. Esta versión lo completa con interesados, hitos, "
        "riesgos, supuestos, esfuerzo y criterios de éxito ligados a los objetivos del alcance."
    ))
    story.append(tabla(
        ["Elemento", "Definición"],
        [
            ["Nombre", "WonPLUS — Sistema de gestión de ventas e inventarios para MYPES."],
            ["Patrocinio académico", "Curso Integrador I: Sistemas Software. Docente: Irani Guillen Gómez."],
            ["Responsable", "Famel Marion Zuloaga Zapana. Elabora, publica y sustenta el entregable."],
            ["Propósito", "Reducir el registro manual mediante la venta digital, el control de stock y la consulta del resultado."],
            ["Objetivo general", "Entregar un sistema de ventas e inventarios en Java, con MVC, que cubra el alcance del avance 2."],
            ["Objetivos específicos", "OE1. Registrar la venta y descontar el stock. OE2. Administrar productos, categorías y usuarios por rol. OE3. Consultar el periodo y exportar Excel. OE4. Publicar código e informe sobre el mismo alcance."],
            ["Alcance", "Usuarios, categorías, productos, venta, ticket, historial, detalle, alerta de stock y reporte."],
            ["Fuera de alcance", "Facturación electrónica, SUNAT, lector de barras, correo automático y nube."],
            ["Entregables", "Informe de este avance, diagramas, charter, Gantt, aplicativo Java y repositorio GitHub."],
            ["Interesados", "Docente, que evalúa; alumna, que construye; administrador y vendedor de la MYPE, que operarían el sistema; emprendedor, que usa el resultado para decidir."],
            ["Hitos", "H1. Problema y alcance aprobados en el avance 2. H2. Modelo de datos y núcleo Java. H3. Once pantallas operativas. H4. Informe del avance 3 y código publicado. H5. Sustentación oral de 10 minutos."],
            ["Riesgos", "Muestra de seis personas; crecimiento del alcance hacia SUNAT; credenciales locales de la base; exceso de tiempo en la sustentación."],
            ["Supuestos", "El alcance del avance 2 se mantiene. Hay JDK 21, Maven y PostgreSQL en el equipo de la sustentación. La demostración usa datos de prueba."],
            ["Restricciones", "Calendario del curso, una solución de alcance acotado y diez minutos de exposición."],
            ["Esfuerzo", "Estimación académica: análisis 20 h, diseño 24 h, núcleo y seguridad 40 h, pantallas 40 h, pruebas 12 h, informe 20 h y sustentación 8 h."],
            ["Criterios de éxito", "La venta confirmada descuenta stock y rechaza cantidades imposibles. El vendedor no administra el catálogo ni los usuarios. El reporte del periodo genera un .xlsx. La contraseña no se guarda en texto plano. El informe y el código describen las mismas cinco operaciones."],
        ],
        [3.6 * cm, W - 3.6 * cm],
    ))
    story.append(caption("Tabla 1. Project Charter de WonPLUS."))

    story.append(H("7.2 Diagrama de Gantt", 2))
    story.append(P(
        "El cronograma conserva las 18 semanas del avance 2. Lo verde ya está en el código "
        "o en este informe. La sustentación queda para el cierre."
    ))
    fases = [
        ("Análisis y alcance", 1, 3, True),
        ("Canvas, visión y planes", 3, 5, True),
        ("Alternativas y charter", 5, 7, True),
        ("Datos, MVC y seguridad", 6, 10, True),
        ("Pruebas de reglas", 8, 11, True),
        ("Once pantallas y Excel", 10, 14, True),
        ("Diagramas e informe", 14, 16, True),
        ("GitHub al día", 14, 16, True),
        ("Sustentación oral", 16, 17, False),
        ("Validación con más MYPES", 17, 18, False),
    ]
    story.append(Lienzo(W, 268, lambda c, w, h: pintar_gantt(c, w, h, fases)))
    story.append(caption("Figura 8. Gantt de 18 semanas. El eje horizontal indica la semana."))
    story.append(tabla(
        ["Id", "Tarea", "Semanas", "Depende de", "Estado"],
        [
            ["A1", "Contexto, problema y alcance", "1-3", "—", "Hecho en el avance 2"],
            ["A2", "Visión, misión, entorno, estrategias y planes", "3-4", "A1", "Hecho"],
            ["A3", "Canvas gráfico y lectura de la encuesta", "4-5", "A1", "Hecho en este informe"],
            ["B1", "Tres alternativas de al menos 10 pantallas", "5-6", "A3", "Hecho en este informe"],
            ["B2", "Project Charter profesional", "6-7", "B1", "Hecho en este informe"],
            ["C1", "Esquema PostgreSQL", "6-8", "B1", "Hecho"],
            ["C2", "Capas MVC, servicios y DAO", "7-10", "C1", "Hecho"],
            ["C3", "Cifrado, roles y validación", "8-10", "C2", "Hecho"],
            ["C4", "Pruebas JUnit de reglas, periodo, clave y Excel", "8-11", "C2", "Hecho"],
            ["D1", "Venta, ticket, historial, detalle, stock y reportes", "10-14", "C3", "Hecho"],
            ["D2", "Productos, categorías y usuarios", "12-14", "C3", "Hecho"],
            ["E1", "Diagramas alineados al código", "14-16", "D2", "Hecho en este informe"],
            ["E2", "Publicación del código en GitHub", "14-16", "D2", "Hecho"],
            ["E3", "Informe del avance 3", "15-16", "E1", "Este documento"],
            ["E4", "Sustentación de 10 minutos", "16-17", "E3", "Pendiente"],
            ["F1", "Validación con una muestra mayor", "17-18", "E4", "Pendiente"],
        ],
        [1.2 * cm, 6.6 * cm, 2.0 * cm, 2.2 * cm, 4.1 * cm],
    ))
    story.append(caption("Tabla 2. Tareas, dependencia y estado del cronograma."))

    story.append(H("8. Diseño de la solución elegida"))
    story.append(P(
        "La consigna pide al menos tres piezas entre charter, Gantt, proceso, clases y "
        "entidad–relación, además de Maven y una librería entre Apache POI, JavaMail y "
        "JasperReports. Este avance incluye las cinco piezas. La librería integrada en el "
        "código es Apache POI. Maven administra la construcción y las dependencias."
    ))

    story.append(H("8.1 Diagramas de proceso", 2))
    story.append(P(
        "El proceso manual obliga a transcribir y a calcular fuera del registro de la venta. "
        "El proceso con WonPLUS deja esa secuencia dentro del sistema: la confirmación graba "
        "la venta y actualiza el stock, y el reporte lee lo ya guardado."
    ))
    story.append(Lienzo(W, 70, lambda c, w, h: pintar_proceso(
        c, w, h,
        ["Anotar", "Transcribir", "Calcular", "Archivar", "Estimar"],
        "Proceso actual",
        HexColor("#F6E6E4"),
    )))
    story.append(Spacer(1, 4))
    story.append(Lienzo(W, 70, lambda c, w, h: pintar_proceso(
        c, w, h,
        ["Ingresar", "Armar venta", "Validar", "Confirmar", "Exportar"],
        "Proceso con WonPLUS",
        GREEN_SOFT,
    )))
    story.append(caption("Figura 9. Proceso manual y proceso propuesto."))

    story.append(H("8.2 Diagrama de clases", 2))
    story.append(P(
        "Las clases de dominio están en el paquete pe.edu.utp.wonplus.model y coinciden con el "
        "código. Respecto del diagrama del avance 2, aquí aparecen el rol, el estado activo, "
        "el hash de la contraseña, el costo, el stock mínimo, la ganancia y el costo de la línea. "
        "Producto conoce si está en stock bajo. DetalleVenta calcula su subtotal."
    ))
    story.append(Lienzo(W, 230, pintar_clases))
    story.append(caption("Figura 10. Clases de dominio alineadas al código."))
    story.append(P(
        "Alrededor de esas clases, el programa separa responsabilidades. CalculadoraVenta obtiene "
        "el total, la ganancia y el stock resultante antes de persistir. Los servicios de "
        "autenticación, usuario, categoría, producto, venta y reporte aplican las reglas y exigen "
        "sesión. Las interfaces UsuarioDao, CategoriaDao, ProductoDao y VentaDao definen el acceso "
        "a datos; las clases de dao.jdbc las implementan. La vista no escribe SQL."
    ))

    story.append(H("8.3 Diagrama entidad–relación", 2))
    story.append(P(
        "La base tiene cinco tablas, definidas en src/main/resources/schema.sql. Un usuario "
        "registra varias ventas. Una venta tiene varias líneas. Cada línea apunta a un producto "
        "y cada producto pertenece a una categoría. El rol solo admite ADMIN o VENDEDOR. El "
        "correo y el nombre de categoría son únicos. Precio, costo, stock y total no admiten "
        "valores negativos, y la cantidad de la línea debe ser mayor que cero."
    ))
    story.append(Lienzo(W, 250, pintar_er))
    story.append(caption("Figura 11. Modelo entidad–relación de la base wonplus."))

    story.append(H("9. Arquitectura de la solución construida"))
    story.append(P(
        "La rúbrica pide construir la arquitectura aplicando al menos tres principios entre MVC, "
        "TDD, DAO y SOLID, y considerar la seguridad. La solución aplica los cuatro y documenta "
        "la seguridad por separado, para que el informe y el código describan la misma estructura."
    ))
    story.append(Lienzo(W, 210, pintar_capas))
    story.append(caption("Figura 12. Capas de WonPLUS. La dependencia baja de la vista hacia la base."))

    story.append(H("9.1 MVC", 2))
    story.append(P(
        "Cada pantalla implementa la interfaz Vista y vive en pe.edu.utp.wonplus.ui. "
        "ControladorPrincipal recibe la acción, por ejemplo iniciar sesión o confirmar una venta, "
        "y llama al servicio correspondiente. El controlador no calcula totales ni decide el stock. "
        "Esas reglas están en CalculadoraVenta y en VentaService. Aplicacion crea las capas e "
        "inyecta cada DAO en su servicio."
    ))
    story.append(H("9.2 DAO", 2))
    story.append(P(
        "El servicio depende de la interfaz, no de PostgreSQL. Cambiar una consulta no obliga a "
        "cambiar la pantalla. Las implementaciones JDBC usan PreparedStatement. Al descontar "
        "stock, VentaJdbcDao bloquea la fila del producto dentro de la transacción y rechaza la "
        "venta si la cantidad supera el disponible. Así la venta y el inventario quedan consistentes."
    ))
    story.append(H("9.3 SOLID", 2))
    story.extend(bullets([
        "Responsabilidad única: cada servicio atiende un grupo de operaciones. La exportación a Excel está en ExportadorExcel y no en la pantalla de reportes.",
        "Abierto-cerrado: una regla nueva de cálculo se concentra en CalculadoraVenta, sin reescribir las pantallas.",
        "Sustitución e inversión de dependencia: los servicios reciben las interfaces DAO por el constructor. La vista y el controlador no eligen el motor de base.",
        "Segregación: existen cuatro interfaces DAO pequeñas, una por agregado, en lugar de un único acceso a datos.",
    ]))
    story.append(H("9.4 Pruebas", 2))
    story.append(P(
        "Las reglas que no necesitan base de datos se verifican con JUnit 5, ejecutadas con "
        "mvn test. Las pruebas fijan el comportamiento esperado de la venta, del periodo, del "
        "cifrado y del archivo Excel. No reemplazan una prueba de cada pantalla ni de cada DAO; "
        "cubren el núcleo que decide si una venta es válida y si el reporte se puede generar."
    ))
    story.append(tabla(
        ["Clase de prueba", "Qué comprueba"],
        [
            ["CalculadoraVentaTest", "Suma total y ganancia, junta cantidades del mismo producto, rechaza stock insuficiente y rechaza una venta vacía."],
            ["PeriodoConsultaTest", "El periodo de un día cubre solo la fecha consultada."],
            ["SeguridadTest", "El hash coincide solo con la clave original, no guarda la clave en claro y rechaza correo vacío, clave corta y precio negativo."],
            ["ExportadorExcelTest", "La exportación genera un archivo .xlsx con contenido."],
        ],
        [4.4 * cm, W - 4.4 * cm],
    ))
    story.append(caption("Tabla 3. Pruebas automáticas del núcleo."))

    story.append(H("9.5 Seguridad", 2))
    story.append(P(
        "La contraseña no se almacena en texto plano. CifradorClave la deriva con PBKDF2-HMAC-SHA256, "
        "sal aleatoria de 16 bytes y 65536 iteraciones. El ingreso compara el resultado con "
        "comparación de tiempo constante. Un usuario marcado como inactivo no entra. Las operaciones "
        "de usuarios, productos y categorías exigen, además de la sesión, el rol administrador."
    ))
    story.append(P(
        "ValidadorEntrada revisa correo, longitud de contraseña, nombres, montos y cantidades "
        "antes de llegar a la base. Las consultas van parametrizadas. La cadena de conexión no "
        "viaja en el repositorio: GitHub publica db.properties.example y cada equipo copia ese "
        "archivo a db.properties, que queda fuera de Git. La sustentación usa solo datos de "
        "demostración."
    ))
    story.append(P(
        "En relación con la Ley N.° 29733, el dato personal que el sistema trata es la cuenta "
        "de quien opera el negocio: nombre, correo, rol y clave cifrada. El sistema no pide "
        "datos de clientes finales ni de comprobantes tributarios, porque ese tratamiento está "
        "fuera del alcance."
    ))

    story.append(H("10. Librerías y construcción con Maven"))
    story.append(P(
        "El proyecto es Maven, grupo pe.edu.utp, artefacto wonplus, versión 1.0.0, compilado "
        "para Java 21. La rúbrica pide incorporar Google Guava, Apache POI, Apache Commons y "
        "Logback, con cuidado básico de la información. Las cuatro están declaradas en pom.xml "
        "y el código las usa. PostgreSQL JDBC y JUnit 5 completan la construcción; JUnit queda "
        "limitado a las pruebas."
    ))
    story.append(tabla(
        ["Librería", "Dónde se usa", "Para qué"],
        [
            ["Google Guava 33.3.1", "ValidadorEntrada, ProductoService, CalculadoraVenta y VentaService", "Limpiar textos, rechazar nulos y armar listas que la venta no pueda alterar después."],
            ["Apache POI 5.4.0", "ExportadorExcel", "Generar el .xlsx del reporte de ventas. Cumple la librería pedida entre POI, JavaMail y JasperReports."],
            ["Apache Commons Lang y IO", "ValidadorEntrada, UsuarioService y ExportadorExcel", "Validar textos y normalizar el nombre del archivo Excel."],
            ["Logback 1.5.16", "logback.xml, servicios y DAO", "Registrar ingresos, ventas rechazadas y errores de base en logs/wonplus.log, sin escribir la contraseña."],
        ],
        [3.8 * cm, 5.5 * cm, W - 9.3 * cm],
    ))
    story.append(caption("Tabla 4. Librerías exigidas por la rúbrica y su uso real."))
    story.append(P(
        "El empaquetado usa maven-shade-plugin y deja un ejecutable cuya clase principal es "
        "pe.edu.utp.wonplus.Main. En el equipo de desarrollo también existe ejecutar.sh, que "
        "levanta la aplicación con Maven. Las pruebas se lanzan con mvn test."
    ))

    story.append(H("11. Interfaces y cobertura del alcance"))
    story.append(P(
        "La rúbrica pide que las interfaces cubran el 100 % del alcance comprometido. El alcance "
        "sigue siendo el del avance 2. La tabla siguiente cruza cada operación con la pantalla, "
        "el servicio y la tabla de base que la sostienen."
    ))
    story.append(tabla(
        ["Alcance", "Pantalla", "Servicio", "Persistencia"],
        [
            ["Ingreso según rol", "Inicio de sesión", "AuthService", "usuario.password_hash y usuario.activo"],
            ["Consulta rápida del día", "Panel", "ReporteService", "venta y producto"],
            ["Registrar la venta", "Registrar venta y ticket", "VentaService y CalculadoraVenta", "venta, detalle_venta y stock de producto"],
            ["Consultar operaciones", "Historial y detalle", "VentaService", "venta y detalle_venta"],
            ["Controlar el mínimo", "Alertas de stock", "ProductoService", "producto.stock y stock_minimo"],
            ["Ver el resultado", "Reportes y Excel", "ReporteService y ExportadorExcel", "venta del periodo"],
            ["Mantener el catálogo", "Productos y categorías", "ProductoService y CategoriaService", "producto y categoria"],
            ["Mantener las cuentas", "Usuarios", "UsuarioService", "usuario, con rol ADMIN o VENDEDOR"],
        ],
        [3.3 * cm, 3.6 * cm, 4.2 * cm, W - 11.1 * cm],
    ))
    story.append(caption("Tabla 5. Trazabilidad del alcance comprometido."))
    story.append(P(
        "El flujo de demostración del vendedor es: iniciar sesión, revisar el panel, registrar "
        "una venta, ver el ticket y comprobar que el stock bajó. El flujo del administrador "
        "agrega el alta de una categoría, un producto y un usuario vendedor. El reporte cierra "
        "la demostración al exportar el Excel del periodo."
    ))

    story.append(H("12. Control de versiones"))
    story.append(P(
        "El repositorio público es https://github.com/ZuloagaZapanaFamelMarion/WonPLUS, rama main. "
        "El historial publicado incluye el trabajo previo del proyecto y los avances de la "
        "solución Java que este informe describe. Los commits de la aplicación de escritorio, "
        "a nombre de Marion Zuloaga, son los siguientes."
    ))
    story.append(tabla(
        ["Commit", "Contenido publicado"],
        [
            ["d5f89b3", "Núcleo Java de WonPLUS con PostgreSQL, DAO y pruebas."],
            ["726ea8f", "Pantallas de ventas, inventario, usuarios y reportes."],
            ["94e5349", "Documento de arquitectura y de las pantallas."],
            ["c44b754", "README del repositorio actualizado a la aplicación Java."],
            ["avance-3/", "Informe de este avance, como continuación del avance 2, junto con el código publicado."],
        ],
        [2.4 * cm, W - 2.4 * cm],
    ))
    story.append(caption("Tabla 6. Commits que dejan en GitHub el avance de la solución elegida."))
    story.append(P(
        "Con esos commits, GitHub contiene el código de las once pantallas, el esquema de la base, "
        "las pruebas, el POM con las cuatro librerías, la descripción de la arquitectura y este "
        "informe en wonplus-java/avance-3/Avance_3_WonPLUS.pdf. La clave de PostgreSQL no está "
        "en el historial nuevo: el repositorio deja db.properties.example. El informe y el "
        "programa describen el mismo sistema, el del avance 2 ya construido."
    ))

    story.append(H("13. Correspondencia con la rúbrica"))
    story.append(P(
        "La tabla resume dónde queda evidenciado cada criterio del avance. Sirve como guía de "
        "la sustentación y como control de que el informe no promete funciones distintas de las "
        "que el programa ya tiene."
    ))
    story.append(tabla(
        ["Criterio", "Dónde se cumple"],
        [
            ["Arquitectura con MVC, DAO, SOLID y pruebas, más seguridad", "Capítulo 9. Vistas Swing, ControladorPrincipal, servicios, interfaces DAO, JUnit 5 y cifrado PBKDF2."],
            ["Guava, Apache POI, Apache Commons y Logback", "Capítulo 10 y pom.xml. POI exporta el Excel; Logback escribe el registro de operación."],
            ["Git con el avance publicado en GitHub", "Capítulo 12. Repositorio WonPLUS, rama main: núcleo, pantallas, arquitectura, README e informe en wonplus-java/avance-3/Avance_3_WonPLUS.pdf."],
            ["Interfaces del 100 % del alcance", "Capítulo 11 y figura 5. Ocho operaciones del alcance cruzadas con pantalla, servicio y tabla."],
            ["Solución completa", "Las cinco operaciones del avance 2 están en el programa. Lo dejado fuera se declara en el alcance y en el charter."],
            ["Solución coherente", "Este informe describe la aplicación Java de escritorio. Las alternativas 2 y 3 se marcan como diseño."],
            ["Buenas prácticas", "Maven, capas, DAO, consultas preparadas, pruebas y control de versiones."],
            ["Autoría", "El código y los commits están en el repositorio de la alumna, que puede recorrer el flujo en la sustentación."],
            ["Canvas, charter y Gantt", "Figura 1, tabla 1 y figura 8."],
            ["Tres alternativas con 10 pantallas y mayoría Java", "Capítulo 6. La elegida tiene 11 pantallas construidas."],
        ],
        [5.2 * cm, W - 5.2 * cm],
    ))
    story.append(caption("Tabla 7. Criterios de la rúbrica y evidencia en este avance."))

    story.append(H("14. Recomendaciones"))
    story.extend(bullets([
        "Ampliar la encuesta a una muestra mayor y más diversa de MYPES antes de agregar funciones.",
        "Hacer una prueba de uso con una persona en rol administrador y otra en rol vendedor.",
        "Mantener el alcance del MVP en ventas, productos, stock y reportes durante la sustentación.",
        "Preparar la exposición en diez minutos con el orden del anexo C.",
        "En el equipo de la sustentación, crear la base wonplus y revisar la conexión antes de empezar.",
        "Dejar db.properties fuera de cualquier copia pública y usar datos de demostración.",
        "Evaluar la alternativa web solo después de comprobar que el escritorio resuelve el proceso.",
        "Estudiar la facturación electrónica como un proyecto aparte, con su propio alcance.",
        "Programar una copia de la base antes de usar el sistema con datos reales de un negocio.",
    ]))

    story.append(H("15. Conclusiones"))
    story.extend(bullets([
        "WonPLUS mantiene el problema y el alcance del avance 2: una MYPE necesita registrar ventas, controlar stock y consultar el resultado sin depender del cuaderno.",
        "De las tres alternativas Java, se construyó la de escritorio. Tiene once pantallas y cubre usuarios, catálogo, venta, inventario y reporte. Las alternativas web y de correo quedan diseñadas para una evolución.",
        "La arquitectura separa vista, controlador, servicio y DAO. Las pruebas automáticas fijan el cálculo de la venta, el periodo, el cifrado y la exportación. La contraseña se guarda como hash PBKDF2 y el rol limita la administración.",
        "Maven integra Guava, Apache POI, Apache Commons y Logback. POI es la librería de reportes usada para el Excel.",
        "El lienzo de nueve bloques, el charter profesional y el Gantt de 18 semanas planifican el mismo alcance que el código ya implementa. La sustentación oral y una validación con más usuarios siguen pendientes.",
        "El repositorio GitHub publica el código y este informe en wonplus-java/avance-3, de modo que el documento y el programa describen el mismo sistema.",
    ]))

    story.append(H("16. Referencias"))
    refs = [
        "Apache Software Foundation. (2024). Apache POI: The Java API for Microsoft documents. https://poi.apache.org/",
        "Beck, K. (2003). Test-driven development: By example. Addison-Wesley.",
        "Congreso de la República del Perú. (2011). Ley N.° 29733, Ley de protección de datos personales. Diario Oficial El Peruano. https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733",
        "Gamma, E., Helm, R., Johnson, R. y Vlissides, J. (1995). Design patterns: Elements of reusable object-oriented software. Addison-Wesley.",
        "Instituto Nacional de Estadística e Informática. (2025). Perú: estructura empresarial. https://www.inei.gob.pe",
        "Nielsen, J. (1994). Usability engineering. Morgan Kaufmann.",
        "Obe, R. O. y Hsu, L. S. (2017). PostgreSQL: Up and running (3.ª ed.). O’Reilly Media.",
        "Oracle. (2026). Java platform, standard edition documentation (Java 21). https://docs.oracle.com/en/java/javase/21/",
        "Osterwalder, A. y Pigneur, Y. (2011). Generación de modelos de negocio. Deusto.",
        "Project Management Institute. (2021). A guide to the project management body of knowledge (PMBOK® guide) (7.ª ed.). Project Management Institute.",
        "QOS.ch. (2024). Logback manual. https://logback.qos.ch/manual/",
        "Sommerville, I. (2016). Ingeniería de software (10.ª ed.). Pearson Educación.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, ST["src"]))

    story.append(PageBreak())
    story.append(H("Anexo A. Lean Canvas"))
    story.append(P(
        "Se conserva el Lean Canvas del avance 2, porque complementa el lienzo de nueve bloques "
        "con el problema, la métrica y la ventaja que la MYPE reconocería."
    , "body0"))
    story.append(tabla(
        ["Bloque", "Contenido"],
        [
            ["Problema", "Registro manual de ventas, dificultad para controlar el stock y poca claridad de la ganancia."],
            ["Segmentos", "MYPES y emprendedores que venden y necesitan un control básico."],
            ["Propuesta única de valor", "Gestión sencilla de ventas e inventario en un solo sistema."],
            ["Solución", "Usuarios, productos, ventas, stock y reportes, con la alternativa de escritorio ya construida."],
            ["Canales", "Demostración directa, contacto con el negocio y repositorio del proyecto."],
            ["Ventaja", "Operaciones esenciales, ejecución local y adaptación al tamaño de una MYPE."],
            ["Métricas", "Ventas registradas, productos gestionados, alertas de stock y reportes exportados."],
            ["Costos", "Desarrollo, equipo, mantenimiento y, más adelante, infraestructura si se migra a web."],
            ["Ingresos", "En una etapa futura: licencia, suscripción o soporte, solo con validación previa."],
        ],
        [4.2 * cm, W - 4.2 * cm],
    ))

    story.append(H("Anexo B. Encuesta piloto"))
    story.append(P(
        "Instrumento usado en el avance 2. Los gráficos del capítulo 5 resumen las respuestas "
        "de seis participantes a las preguntas 3, 5 y 9."
    , "body0"))
    story.append(tabla(
        ["N.°", "Pregunta", "Respuesta"],
        [
            ["1", "¿A qué rubro pertenece su negocio?", "Abierta o selección"],
            ["2", "¿Cuál es el rango aproximado de ventas mensuales?", "Rangos"],
            ["3", "¿Cómo controla actualmente sus ingresos y egresos?", "Cuaderno, Excel, software u otro"],
            ["4", "¿Con qué frecuencia registra sus movimientos?", "Diario, interdiario, semanal, mensual u otro"],
            ["5", "¿Sabe exactamente cuánto ganó el mes pasado?", "Sí, más o menos, no"],
            ["6", "¿Con qué frecuencia tiene problemas para conocer su stock?", "Nunca, a veces, frecuentemente"],
            ["7", "¿Qué dificultad encuentra al controlar sus productos?", "Abierta"],
            ["8", "¿Qué función considera más útil?", "Ventas, inventario, reportes, usuarios u otra"],
            ["9", "¿Le interesaría probar una herramienta sencilla para ventas y stock?", "Sí, no, tal vez"],
            ["10", "¿Qué característica considera indispensable?", "Abierta"],
        ],
        [1.2 * cm, 9.5 * cm, W - 10.7 * cm],
    ))

    story.append(H("Anexo C. Guion de la sustentación"))
    story.append(P(
        "La exposición dispone de 10 minutos. El orden sigue la consigna: problema, alcance, "
        "lienzo, tres alternativas, charter, Gantt, arquitectura, librerías y demostración."
    , "body0"))
    story.append(tabla(
        ["Minuto", "Qué se dice", "Apoyo"],
        [
            ["0:00-1:00", "La MYPE anota la venta, transcribe y calcula la ganancia aparte.", "Figura 9, proceso manual"],
            ["1:00-2:00", "El alcance son usuarios, productos, venta, stock y reporte. Quedan fuera SUNAT y la nube.", "Capítulo 5"],
            ["2:00-3:00", "El lienzo concentra la propuesta: un sistema local para vender y conocer el stock.", "Figura 1"],
            ["3:00-4:30", "Hay tres alternativas Java. Se construyó el escritorio, con 11 pantallas. Web y correo son diseño.", "Figuras 5, 6 y 7"],
            ["4:30-5:30", "El charter fija objetivos, hitos y criterios: la venta descuenta stock y el Excel se genera.", "Tabla 1"],
            ["5:30-6:30", "El Gantt muestra hecho el desarrollo y pendiente la sustentación y la validación.", "Figura 8"],
            ["6:30-8:00", "Capas MVC y DAO, cuatro librerías, cifrado y roles. Demostración: venta, stock y Excel.", "Figura 12 y el programa"],
            ["8:00-10:00", "Cierre con la trazabilidad del alcance y preguntas.", "Tabla 5"],
        ],
        [2.5 * cm, 8.4 * cm, W - 10.9 * cm],
    ))
    story.append(caption("Tabla 8. Secuencia sugerida para los 10 minutos."))

    story.append(H("Anexo D. Estructura del código entregado"))
    story.append(P(
        "El aplicativo está en wonplus-java. La clase principal es pe.edu.utp.wonplus.Main. "
        "El detalle de capas también está en docs/arquitectura.md del mismo módulo."
    , "body0"))
    story.append(code_block(
        "wonplus-java/\n"
        "  pom.xml\n"
        "  src/main/java/pe/edu/utp/wonplus/\n"
        "    Main.java\n"
        "    Aplicacion.java\n"
        "    model/          Usuario, Rol, Categoria, Producto, Venta, DetalleVenta\n"
        "    ui/             Login, Panel, Venta, Ticket, Historial, Detalle,\n"
        "                    Stock, Reportes, Productos, Categorias, Usuarios\n"
        "    controlador/    ControladorPrincipal.java\n"
        "    servicio/       Auth, Usuario, Categoria, Producto, Venta, Reporte\n"
        "    dao/            interfaces y dao/jdbc con PreparedStatement\n"
        "    seguridad/      CifradorClave, ValidadorEntrada\n"
        "    reporte/        ExportadorExcel.java\n"
        "  src/main/resources/schema.sql\n"
        "  src/main/resources/logback.xml\n"
        "  src/test/java/    CalculadoraVenta, Periodo, Seguridad, Excel\n"
    ))
    story.append(Spacer(1, 8))
    story.append(P(
        "Para ejecutar en un equipo con JDK 21, Maven y la base wonplus creada, desde la carpeta "
        "wonplus-java se usa mvn test para las pruebas y el script ejecutar.sh, o mvn package, "
        "para la aplicación. Las cuentas de la demostración están descritas en el README del "
        "módulo y entran por la pantalla de inicio de sesión."
    ))
    story.append(P(
        "Fragmento de referencia del cifrado, tal como está en CifradorClave. La clave no se "
        "guarda: se derivan 256 bits con PBKDF2 y una sal distinta en cada alta."
    ))
    story.append(code_block(
        "private static final int ITERACIONES = 65536;\n"
        "private static final int BYTES_SAL = 16;\n"
        "private static final int BITS_HASH = 256;\n"
        "// resultado: iteraciones $ sal $ hash\n"
    ))
    return story


def main():
    doc = Doc(
        OUT,
        pagesize=A4,
        title="Avance 3 — WonPLUS",
        author="Famel Marion Zuloaga Zapana",
        subject="Curso Integrador I: Sistemas Software",
    )
    frame_cover = Frame(2.5 * cm, 1.8 * cm, W, A4[1] - 3.6 * cm, id="cover")
    frame = Frame(2.5 * cm, 1.9 * cm, W, A4[1] - 4.0 * cm, id="normal")
    doc.addPageTemplates([
        PageTemplate(id="portada", frames=[frame_cover], onPage=cover_page),
        PageTemplate(id="interior", frames=[frame], onPage=header_footer),
    ])
    doc.multiBuild(build_story())
    print(OUT)


if __name__ == "__main__":
    main()
