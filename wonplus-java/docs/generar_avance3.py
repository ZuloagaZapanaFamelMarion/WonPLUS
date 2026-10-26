#!/usr/bin/env python3
"""Arma el Avance 3: el Avance 2 completo, más el capítulo de la rúbrica."""

from pathlib import Path

import fitz
from reportlab.lib.colors import Color, black, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Arial", f"{FONT_DIR}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", f"{FONT_DIR}/Arial Bold.ttf"))

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "avance-3" / "Avance_3_WonPLUS.pdf"
CAPITULO = BASE / "avance-3" / "_capitulo3.pdf"
AVANCE2 = Path(
    "/Users/marionzuloagazapana/.cursor/projects/"
    "Users-marionzuloagazapana-Desktop-wonplus-java/attachments/"
    "55a545cb-e9cb-4729-a3ad-e26507f7e308/"
    "Avance_2_WonPLUS_curso_integrador_sistemas_1.pdf"
)
LOGO = BASE / "docs" / "bocetos" / "logo_utp.png"
ARIAL = f"{FONT_DIR}/Arial.ttf"
ARIAL_BOLD = f"{FONT_DIR}/Arial Bold.ttf"

VERDE = Color(0.886, 0.937, 0.851)
GRIS = Color(0.349, 0.376, 0.459)
LINEA = Color(0.835, 0.863, 0.890)
W = A4[0] - 4.4 * cm
PAGINAS_AVANCE2 = 25


def estilo(nombre, **kw):
    base = dict(fontName="Arial", fontSize=11, leading=14, textColor=black, alignment=TA_JUSTIFY)
    base.update(kw)
    return ParagraphStyle(nombre, **base)


ST = {
    "cap": estilo("cap", fontName="Arial-Bold", fontSize=15, leading=18, alignment=TA_LEFT, spaceAfter=10),
    "sec": estilo("sec", fontName="Arial-Bold", fontSize=12, leading=15, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6),
    "body": estilo("body", spaceAfter=8),
    "th": estilo("th", fontName="Arial-Bold", fontSize=9, leading=11, alignment=TA_LEFT),
    "td": estilo("td", fontSize=9, leading=11, alignment=TA_LEFT),
}


def pagina(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(black)
    canvas.setLineWidth(0.8)
    canvas.rect(24, 24, A4[0] - 48, A4[1] - 48, stroke=1, fill=0)
    canvas.drawImage(str(LOGO), 63, A4[1] - 78, width=94, height=36, mask="auto")
    canvas.setStrokeColor(LINEA)
    canvas.setLineWidth(1)
    canvas.line(42, 36, A4[0] - 42, 36)
    canvas.setFillColor(GRIS)
    canvas.setFont("Arial", 7)
    numero = doc.page + PAGINAS_AVANCE2
    canvas.drawString(63, 22, f"WonPLUS — Curso Integrador I: Sistemas SoftwarePágina {numero}")
    canvas.restoreState()


def P(texto, nombre="body"):
    return Paragraph(texto, ST[nombre])


def tabla(headers, filas, anchos):
    data = [[Paragraph(h, ST["th"]) for h in headers]]
    for fila in filas:
        data.append([Paragraph(str(c), ST["td"]) for c in fila])
    t = Table(data, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERDE),
        ("GRID", (0, 0), (-1, -1), 0.4, black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND", (0, 1), (-1, -1), white),
    ]))
    return t


def capitulo():
    s = []
    s.append(P("CAPÍTULO 3", "cap"))
    s.append(P("Lo agregado en este avance", "sec"))
    s.append(P(
        "Este capítulo se agrega al avance 2. El índice, el contexto, el problema, el alcance, "
        "las tres alternativas, el charter, el Gantt, los procesos, las clases, el modelo "
        "entidad–relación, el prototipo y los anexos quedan como fueron entregados. Las "
        "pantallas que se ven en las secciones 5.1 y 7 son los bocetos de WonPLUS y no se "
        "reemplazan."
    ))
    s.append(P(
        "Lo que se suma aquí es la construcción de la solución 1, la de escritorio en Java. "
        "El alcance no cambia: usuarios, productos, ventas, actualización del inventario y "
        "reportes básicos. La aplicación está en la carpeta wonplus-java del repositorio "
        "https://github.com/ZuloagaZapanaFamelMarion/WonPLUS."
    ))

    s.append(P("1. Arquitectura de la solución construida", "sec"))
    s.append(P(
        "La solución aplica los cuatro criterios pedidos entre MVC, TDD, DAO y SOLID, y "
        "además trata la seguridad de la información. La vista no escribe SQL. "
        "ControladorPrincipal recibe la acción de la pantalla y llama al servicio. El "
        "servicio aplica la regla y usa una interfaz DAO. Aplicacion crea esas capas e "
        "inyecta cada DAO en su servicio."
    ))
    s.append(tabla(
        ["Principio", "Dónde queda en el código"],
        [
            ["MVC", "Las pantallas están en pe.edu.utp.wonplus.ui e implementan Vista. ControladorPrincipal coordina. Las reglas de la venta están en CalculadoraVenta y en VentaService, no en la pantalla."],
            ["DAO", "UsuarioDao, CategoriaDao, ProductoDao y VentaDao definen el acceso. Las clases de dao.jdbc los implementan con JDBC y PreparedStatement. El servicio no depende de PostgreSQL de forma directa."],
            ["SOLID", "Cada servicio atiende un grupo: autenticación, usuarios, categorías, productos, ventas y reportes. La exportación a Excel está en ExportadorExcel. Los servicios reciben la interfaz DAO por el constructor."],
            ["TDD", "JUnit 5 fija el comportamiento del núcleo. CalculadoraVentaTest cubre total, ganancia, stock insuficiente y venta vacía. PeriodoConsultaTest cubre el día consultado. SeguridadTest cubre el hash y la validación. ExportadorExcelTest comprueba el archivo .xlsx. Se ejecutan con mvn test."],
        ],
        [3.2 * cm, W - 3.2 * cm],
    ))
    s.append(Spacer(1, 8))
    s.append(P(
        "La contraseña no se guarda en texto plano. CifradorClave la deriva con "
        "PBKDF2-HMAC-SHA256, sal aleatoria de 16 bytes y 65536 iteraciones. El ingreso "
        "compara el resultado en tiempo constante. Un usuario inactivo no entra. Productos, "
        "categorías y usuarios exigen el rol administrador, además de la sesión. "
        "ValidadorEntrada revisa correo, contraseña, nombres, montos y cantidades antes de "
        "llegar a la base. Al descontar stock, VentaJdbcDao bloquea la fila del producto y "
        "rechaza la venta si la cantidad supera el disponible. La clave de PostgreSQL no va "
        "en el repositorio: el archivo público es db.properties.example y cada equipo copia "
        "ese archivo a db.properties."
    ))
    s.append(P(
        "En relación con la Ley N.° 29733, ya citada en el avance 2, el dato personal que "
        "el sistema trata es la cuenta de quien opera el negocio: nombre, correo, rol y "
        "clave cifrada. No se piden datos de clientes finales ni de comprobantes tributarios, "
        "porque eso sigue fuera del alcance."
    ))

    s.append(P("2. Librerías de apoyo y seguridad de la información", "sec"))
    s.append(P(
        "Maven declara y el código usa las cuatro librerías pedidas. PostgreSQL JDBC conecta "
        "la base y JUnit 5 queda limitado a las pruebas."
    ))
    s.append(tabla(
        ["Librería", "Dónde se usa", "Para qué"],
        [
            ["Google Guava 33.3.1", "ValidadorEntrada, ProductoService, CalculadoraVenta y VentaService", "Limpiar textos, rechazar nulos y armar la lista de la venta."],
            ["Apache POI 5.4.0", "ExportadorExcel", "Generar el Excel del reporte del periodo."],
            ["Apache Commons Lang 3.17.0 y Commons IO 2.18.0", "ValidadorEntrada, UsuarioService y ExportadorExcel", "Validar textos y normalizar el nombre del archivo."],
            ["Logback 1.5.16", "logback.xml, servicios y DAO", "Registrar ingresos, ventas rechazadas y errores de base en logs/wonplus.log, sin escribir la contraseña."],
        ],
        [4.4 * cm, 5.4 * cm, W - 9.8 * cm],
    ))
    s.append(Spacer(1, 8))
    s.append(P(
        "El tratamiento de la información sigue las precauciones del avance 2 y las concreta "
        "en el programa: consultas con parámetros, clave cifrada, rol de administrador para "
        "el catálogo y las cuentas, y la cadena de conexión fuera del historial público."
    ))

    s.append(P("3. Control de versiones en GitHub", "sec"))
    s.append(P(
        "El repositorio público es https://github.com/ZuloagaZapanaFamelMarion/WonPLUS, "
        "rama main. Ahí está el código de wonplus-java y este informe, en "
        "wonplus-java/avance-3/Avance_3_WonPLUS.pdf. Los commits de la aplicación, a nombre "
        "de Marion Zuloaga, dejan el avance de la solución."
    ))
    s.append(tabla(
        ["Commit", "Contenido publicado"],
        [
            ["d5f89b3", "Núcleo Java de WonPLUS con PostgreSQL, DAO y pruebas."],
            ["726ea8f", "Pantallas de ventas, inventario, usuarios y reportes."],
            ["94e5349", "Documento de arquitectura y de las pantallas."],
            ["c44b754", "README del repositorio actualizado a la aplicación Java."],
            ["b1e3c2b", "Conexión de ejemplo. La clave de la base queda fuera de Git."],
        ],
        [2.6 * cm, W - 2.6 * cm],
    ))
    s.append(Spacer(1, 8))
    s.append(P(
        "Con esos commits, GitHub contiene las pantallas, el esquema de la base, las pruebas, "
        "el POM con las cuatro librerías, la arquitectura y este informe. El avance 2 se "
        "conserva en el documento y el código implementa el mismo alcance."
    ))

    s.append(P("4. Interfaces y cobertura del alcance", "sec"))
    s.append(P(
        "Las interfaces son los bocetos ya incluidos en este documento. La sección 5.1 muestra "
        "el inicio de sesión, el panel, el registro de venta, la gestión de productos y el "
        "historial. La sección 7 repite el flujo del prototipo: inicio de sesión, panel "
        "principal, registro de venta y gestión de productos. No se agregan dibujos distintos."
    ))
    s.append(P(
        "El funcionamiento construido cubre el 100 % del alcance comprometido en el punto 4 "
        "del avance 2. La tabla cruza cada operación con el boceto que ya está en el informe "
        "y con la clase que la ejecuta."
    ))
    s.append(tabla(
        ["Alcance del avance 2", "Boceto ya entregado", "Implementación"],
        [
            ["Ingreso según el rol", "Inicio de sesión, secciones 5.1 y 7", "LoginVista y AuthService. El vendedor no administra el catálogo ni las cuentas."],
            ["Gestión de usuarios", "Mismo ingreso, con rol Administrador o Vendedor", "UsuariosVista y UsuarioService. La contraseña se guarda cifrada."],
            ["Gestión de productos", "Pantalla 4, Gestión de productos", "ProductosVista, CategoriasVista, ProductoService y CategoriaService."],
            ["Registro de ventas", "Pantalla 3, Registrar venta", "VentaVista, TicketVista, VentaService y CalculadoraVenta."],
            ["Actualización del inventario", "Alerta de stock bajo en productos y en el panel", "Al confirmar, se descuenta el stock. StockVista lista el mínimo."],
            ["Consulta de resultados", "Panel principal e historial", "PanelVista, HistorialVista y DetalleVista."],
            ["Reportes básicos", "Panel, historial y exportación", "ReportesVista y ExportadorExcel generan el .xlsx del periodo."],
        ],
        [3.6 * cm, 4.6 * cm, W - 8.2 * cm],
    ))
    s.append(Spacer(1, 8))
    s.append(P(
        "El flujo del vendedor es el del prototipo: iniciar sesión, revisar el panel, "
        "registrar una venta y comprobar que el stock bajó. El flujo del administrador agrega "
        "el mantenimiento de productos y de usuarios. El historial y el Excel cierran la "
        "consulta de resultados que el alcance ya pedía."
    ))

    s.append(P("5. Solución completa, coherente y de autoría", "sec"))
    s.append(tabla(
        ["Criterio", "Cómo se cumple"],
        [
            ["Completa", "Cubre usuarios, productos, ventas, stock y reportes. Facturación electrónica, SUNAT y lector de barras siguen fuera de alcance, como en el charter del avance 2."],
            ["Coherente", "Este informe conserva el texto, el índice y los bocetos del avance 2. El código de wonplus-java implementa esas mismas cinco operaciones."],
            ["Buenas prácticas", "Maven, MVC, DAO, pruebas JUnit, consultas preparadas, clave cifrada y Git."],
            ["Autoría", "Los commits están a nombre de Marion Zuloaga, en el repositorio de la alumna. El flujo se puede recorrer desde el inicio de sesión hasta el reporte."],
        ],
        [3.4 * cm, W - 3.4 * cm],
    ))
    s.append(Spacer(1, 8))
    s.append(tabla(
        ["Criterio de la rúbrica", "Dónde está"],
        [
            ["Arquitectura con MVC, TDD, DAO y SOLID, y seguridad", "Sección 1 de este capítulo. Las pantallas, el controlador, los servicios, los DAO, las pruebas y el cifrado PBKDF2."],
            ["Guava, Apache POI, Apache Commons y Logback", "Sección 2 de este capítulo y el archivo pom.xml."],
            ["Git con el avance publicado en GitHub", "Sección 3 de este capítulo. Repositorio WonPLUS, rama main."],
            ["Interfaces del 100 % del alcance", "Secciones 5.1 y 7 de este documento, y la sección 4 de este capítulo."],
            ["Solución completa, coherente, con buenas prácticas y autoría", "Sección 5 de este capítulo, sobre el mismo alcance del avance 2."],
        ],
        [5.4 * cm, W - 5.4 * cm],
    ))
    s.append(Spacer(1, 8))
    s.append(P(
        "Para ejecutar, con JDK 21, Maven y la base wonplus creada, se copia "
        "db.properties.example a db.properties y se usa ejecutar.sh, o mvn test para las "
        "pruebas. Las cuentas de demostración están en el README: administrador "
        "admin@wonplus.pe y vendedor vendedor@wonplus.pe."
    ))
    return s


def escribir_capitulo():
    doc = BaseDocTemplate(
        str(CAPITULO),
        pagesize=A4,
        title="Avance 3 — WonPLUS",
        author="Famel Marion Zuloaga Zapana",
    )
    frame = Frame(63, 48, W, A4[1] - 168, id="normal", showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="interior", frames=[frame], onPage=pagina)])
    doc.build(capitulo())


def linea_indice(titulo, pagina, sangria=0):
    puntos = "." * 40
    return f"{titulo} {puntos} {pagina}", sangria


def sellar_portada(page):
    rects = page.search_for("AVANCE 2 DEL PROYECTO FINAL - WonPLUS")
    if not rects:
        raise SystemExit("No se encontró el título del avance 2 en la portada.")
    rect = rects[0]
    page.add_redact_annot(rect, fill=(1, 1, 1))
    page.apply_redactions()
    page.insert_font(fontname="ArialAv", fontfile=ARIAL)
    page.insert_text(
        (rect.x0, rect.y1 - 1),
        "AVANCE 3 DEL PROYECTO FINAL - WonPLUS",
        fontname="ArialAv",
        fontsize=12,
        color=(0, 0, 0),
    )


def sellar_indice(page, entradas):
    page.insert_font(fontname="ArialAv", fontfile=ARIAL)
    page.insert_font(fontname="ArialAv-Bold", fontfile=ARIAL_BOLD)
    y = 175
    page.insert_text((71.3, y), "CAPÍTULO 3", fontname="ArialAv-Bold", fontsize=11, color=(0, 0, 0))
    y += 22
    for titulo, numero in entradas:
        texto = f"{titulo} {'.' * 36} {numero}"
        page.insert_text((72, y), texto, fontname="ArialAv", fontsize=9.5, color=(0, 0, 0))
        y += 21.5


def armar():
    if not AVANCE2.exists():
        raise SystemExit(f"No está el PDF del avance 2: {AVANCE2}")
    escribir_capitulo()
    base = fitz.open(AVANCE2)
    extra = fitz.open(CAPITULO)
    sellar_portada(base[0])

    buscadas = [
        "1. Arquitectura de la solución construida",
        "2. Librerías de apoyo y seguridad de la información",
        "3. Control de versiones en GitHub",
        "4. Interfaces y cobertura del alcance",
        "5. Solución completa, coherente y de autoría",
    ]
    entradas = []
    for titulo in buscadas:
        for i, page in enumerate(extra):
            if page.search_for(titulo):
                entradas.append((titulo, PAGINAS_AVANCE2 + i + 1))
                break
        else:
            raise SystemExit(f"No apareció en el capítulo: {titulo}")

    sellar_indice(base[2], entradas)
    base.insert_pdf(extra)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUT)
    extra.close()
    base.close()
    CAPITULO.unlink(missing_ok=True)
    print(OUT)


if __name__ == "__main__":
    armar()
