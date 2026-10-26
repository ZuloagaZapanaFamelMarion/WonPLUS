#!/usr/bin/env python3
"""Avance 3 de WonPLUS, con el formato y los bocetos del avance 2."""

from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

FONT = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Arial", f"{FONT}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", f"{FONT}/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", f"{FONT}/Arial Italic.ttf"))

BASE = Path(__file__).resolve().parents[1]
BOC = BASE / "docs" / "bocetos"
OUT = str(BASE / "avance-3" / "Avance_3_WonPLUS.pdf")

VERDE = Color(0.886, 0.937, 0.851)
GRIS = Color(0.349, 0.376, 0.459)
LINEA = Color(0.835, 0.863, 0.890)
W = A4[0] - 4.4 * cm


def S(name, **kw):
    base = dict(fontName="Arial", fontSize=11, leading=14, textColor=black, alignment=TA_JUSTIFY)
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    "cover": S("cover", fontSize=12, leading=16, alignment=TA_CENTER, spaceAfter=10),
    "coverb": S("coverb", fontName="Arial-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=12),
    "cap": S("cap", fontName="Arial-Bold", fontSize=15, leading=18, alignment=TA_LEFT, spaceBefore=4, spaceAfter=10),
    "sec": S("sec", fontName="Arial-Bold", fontSize=12, leading=15, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6),
    "sub": S("sub", fontName="Arial-Bold", fontSize=11, leading=14, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4),
    "body": S("body", spaceAfter=8),
    "capfig": S("capfig", fontName="Arial-Italic", fontSize=10, leading=13, alignment=TA_CENTER, spaceBefore=2, spaceAfter=8),
    "th": S("th", fontName="Arial-Bold", fontSize=9, leading=11, alignment=TA_CENTER),
    "td": S("td", fontSize=9, leading=11, alignment=TA_LEFT),
    "toc1": S("toc1", fontName="Arial-Bold", fontSize=11, leading=15, alignment=TA_LEFT, spaceBefore=6),
    "toc2": S("toc2", fontSize=10, leading=13, alignment=TA_LEFT, leftIndent=12),
}


class Doc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ("cap", "sec"):
            level = 0 if flowable.style.name == "cap" else 1
            text = flowable.getPlainText()
            if text == "Índice":
                return
            self.notify("TOCEntry", (level, text, self.page))


def pagina(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(black)
    canvas.setLineWidth(0.8)
    canvas.rect(24, 24, A4[0] - 48, A4[1] - 48, stroke=1, fill=0)
    canvas.drawImage(str(BOC / "logo_utp.png"), 63, A4[1] - 78, width=94, height=36, mask="auto")
    canvas.setStrokeColor(LINEA)
    canvas.setLineWidth(1)
    canvas.line(42, 36, A4[0] - 42, 36)
    canvas.setFillColor(GRIS)
    canvas.setFont("Arial", 7)
    canvas.drawString(63, 22, f"WonPLUS — Curso Integrador I: Sistemas Software    Página {doc.page}")
    canvas.restoreState()


def P(text, style="body"):
    return Paragraph(text, ST[style])


def H(text, style):
    return Paragraph(text, ST[style])


def figura(nombre, ancho=None):
    path = str(BOC / nombre)
    img = Image(path)
    ancho = ancho or W
    alto = img.imageHeight * (ancho / float(img.imageWidth))
    img.drawWidth = ancho
    img.drawHeight = alto
    img.hAlign = "CENTER"
    return img


def bloque(imagen, texto):
    return KeepTogether([figura(imagen), P(texto, "capfig")])


def tabla(headers, rows, widths):
    data = [[Paragraph(h, ST["th"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), ST["td"]) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1)
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


def viñetas(items):
    return ListFlowable(
        [ListItem(Paragraph(item, ST["body"]), leftIndent=12) for item in items],
        bulletType="bullet",
        start="•",
        leftIndent=16,
        bulletFontName="Arial",
        bulletFontSize=11,
        spaceBefore=2,
        spaceAfter=6,
    )


def build():
    story = []
    story.append(Spacer(1, 2.4 * cm))
    story.append(figura("logo_utp_grande.png", 280))
    story.append(Spacer(1, 0.6 * cm))
    story.append(P("UNIVERSIDAD TECNOLÓGICA DEL PERÚ", "coverb"))
    story.append(P("FACULTAD DE INGENIERÍA", "coverb"))
    story.append(P("CARRERA PROFESIONAL DE INGENIERÍA DE SISTEMAS E INFORMÁTICA", "coverb"))
    story.append(Spacer(1, 0.3 * cm))
    story.append(P("CURSO INTEGRADOR I: SISTEMAS SOFTWARE", "cover"))
    story.append(P("AVANCE 3 DEL PROYECTO FINAL - WonPLUS", "cover"))
    story.append(P("Proyecto: Sistema de gestión de ventas e inventarios para MYPES", "cover"))
    story.append(P("Alumna: Famel Marion Zuloaga Zapana", "cover"))
    story.append(P("Docente: Irani Guillen Gómez", "cover"))
    story.append(P("Perú — 2026", "cover"))
    story.append(NextPageTemplate("interior"))
    story.append(PageBreak())

    story.append(H("Índice", "cap"))
    toc = TableOfContents()
    toc.levelStyles = [ST["toc1"], ST["toc2"]]
    story.append(toc)
    story.append(PageBreak())

    story.append(H("CAPÍTULO 1", "cap"))
    story.append(H("1. Contexto de la empresa", "sec"))
    story.append(P(
        "WonPLUS es una propuesta de solución tecnológica orientada a las micro y pequeñas "
        "empresas (MYPES) del Perú que necesitan controlar sus ventas e inventario mediante una "
        "herramienta sencilla y accesible. El proyecto surge de la identificación de dificultades en el "
        "registro manual de operaciones, el seguimiento del stock y la consulta de resultados del negocio."
    ))
    story.append(P(
        "La solución se plantea como un sistema de gestión de ventas e inventarios desarrollado en "
        "Java, con arquitectura Modelo–Vista–Controlador (MVC) y una base de datos relacional "
        "PostgreSQL. Su enfoque prioriza una interfaz intuitiva, operaciones básicas de venta y "
        "actualización de inventario, así como reportes sencillos."
    ))
    story.append(P(
        "El usuario principal es el emprendedor o responsable de una MYPE. El sistema considera dos "
        "roles operativos: Administrador y Vendedor. El Administrador gestiona productos y usuarios, "
        "mientras que el Vendedor registra las operaciones de venta."
    ))
    story.append(P(
        "Este avance 3 continúa el avance 2. No cambia el problema, el alcance ni los bocetos de "
        "WonPLUS ya presentados. Agrega la construcción de esa misma solución: la aplicación Java, "
        "sus pruebas, sus librerías y la publicación en GitHub."
    ))

    story.append(H("2. Identificación del problema", "sec"))
    story.append(P(
        "La problemática identificada es la dificultad de algunas MYPES para disponer de un sistema "
        "sencillo y accesible que permita registrar ventas, controlar inventario y consultar información "
        "básica del negocio. Los métodos manuales pueden generar errores, pérdida de información "
        "y poca claridad sobre la rentabilidad."
    ))
    story.append(P(
        "El proyecto también identifica una barrera de acceso cuando las herramientas de gestión "
        "presentan costos o complejidad que no se ajustan a las necesidades de un negocio pequeño. "
        "WonPLUS se plantea como una alternativa de alcance acotado, enfocada en las operaciones esenciales."
    ))

    story.append(H("3. Descripción del problema", "sec"))
    story.append(P(
        "El proceso manual descrito en el proyecto inicia con el registro de la venta en papel o mediante "
        "anotaciones informales. Posteriormente, la información puede transcribirse a un cuaderno o "
        "una hoja de cálculo, realizar cálculos manuales, almacenar comprobantes físicamente y "
        "finalmente estimar la ganancia revisando la información disponible."
    ))
    story.append(P(
        "La situación afecta principalmente tres aspectos: el control del inventario, la disponibilidad de "
        "información para consultar las ventas y la toma de decisiones basada en datos registrados "
        "de manera consistente. La solución propuesta busca centralizar estas operaciones en un único sistema."
    ))

    story.append(H("4. Alcance de la solución", "sec"))
    story.append(P(
        "El alcance de WonPLUS comprende gestión de usuarios, gestión de productos, registro de "
        "ventas, actualización del inventario y generación de reportes básicos. La primera versión no "
        "contempla facturación electrónica, conexión con SUNAT ni lectores físicos de códigos de "
        "barras. El funcionamiento previsto para esta etapa es local o dentro de una red básica."
    ))

    story.append(H("4.1 Visión", "sub"))
    story.append(P(
        "Ser una solución de gestión sencilla para MYPES que facilite el registro de ventas y el control "
        "de inventario, reduciendo la dependencia de procesos manuales y ofreciendo información "
        "clara para la gestión cotidiana del negocio."
    ))
    story.append(H("4.2 Misión", "sub"))
    story.append(P(
        "Desarrollar y mantener una herramienta tecnológica accesible que permita a los pequeños "
        "negocios registrar sus operaciones comerciales, controlar sus productos y consultar "
        "información básica de ventas mediante una interfaz simple y fácil de utilizar."
    ))
    story.append(H("4.3 Entorno", "sub"))
    story.append(tabla(
        ["Factor", "Descripción"],
        [
            ["Interno", "Solución Java con MVC, PostgreSQL y JDBC; alcance académico centrado en funciones esenciales."],
            ["Clientes", "MYPES y emprendedores que requieren controlar ventas, productos y stock."],
            ["Tecnológico", "Java, PostgreSQL, JDBC e interfaz orientada a operaciones simples."],
            ["Competitivo", "Herramientas de gestión empresarial y alternativas manuales como cuadernos y hojas de cálculo."],
            ["Legal", "Se considera como referencia la Ley N.° 29733 de Protección de Datos Personales."],
        ],
        [3.2 * cm, W - 3.2 * cm],
    ))
    story.append(Spacer(1, 8))

    story.append(H("4.4 Estrategias", "sub"))
    story.append(viñetas([
        "Priorizar productos, ventas, stock y reportes.",
        "Mantener una interfaz simple, con textos claros y operaciones directas.",
        "Aplicar arquitectura MVC y separación de responsabilidades.",
        "Usar PostgreSQL y consultas preparadas para gestionar la información.",
        "Validar la solución mediante pruebas y una muestra mayor de usuarios en futuras iteraciones.",
    ]))

    story.append(H("4.5 Planes de la empresa", "sub"))
    story.append(tabla(
        ["Horizonte", "Plan"],
        [
            ["Corto plazo", "Completar el MVP académico, validar productos y ventas, comprobar la actualización del stock y generar reportes básicos."],
            ["Mediano plazo", "Mejorar la experiencia de usuario, ampliar la validación con MYPES y evaluar la migración a una aplicación web."],
            ["Largo plazo", "Evaluar facturación electrónica, nube, respaldos automatizados y nuevas funciones de gestión."],
        ],
        [3.2 * cm, W - 3.2 * cm],
    ))
    story.append(Spacer(1, 8))

    story.append(H("4.6 Modelo de negocios en Canvas", "sub"))
    story.append(P(
        "Se conserva el lienzo ya elaborado para WonPLUS. Los bloques no se reemplazan."
    ))
    story.append(bloque("lienzo_canvas.png", "Lienzo de modelo de negocio de WonPLUS, el mismo del avance 2."))
    story.append(tabla(
        ["Bloque", "Propuesta para WonPLUS"],
        [
            ["Socios clave", "Proveedores de infraestructura, alojamiento, soporte técnico y posibles aliados para capacitación de MYPES."],
            ["Actividades clave", "Desarrollo, mantenimiento, soporte, validación con usuarios y mejora continua."],
            ["Recursos clave", "Aplicación Java, PostgreSQL, infraestructura, documentación y conocimiento técnico."],
            ["Propuesta de valor", "Sistema sencillo para registrar ventas y controlar inventario, orientado a MYPES que necesitan reducir procesos manuales."],
            ["Relación con clientes", "Acompañamiento inicial, soporte y orientación básica."],
            ["Canales", "Contacto directo, demostraciones, redes sociales y canales digitales."],
            ["Segmentos", "Micro y pequeñas empresas con necesidades básicas de control de ventas e inventario."],
            ["Costos", "Desarrollo, infraestructura, dominio, seguridad, mantenimiento y promoción."],
            ["Ingresos", "Para una futura comercialización: licencia, suscripción o soporte, sujeto a validación."],
        ],
        [4.2 * cm, W - 4.2 * cm],
    ))
    story.append(Spacer(1, 8))

    story.append(H("4.7 Gráficos y análisis de negocio", "sub"))
    story.append(P(
        "La encuesta piloto incluida en el avance previo fue aplicada a 6 emprendedores de MYPES "
        "en Lima. Por su tamaño reducido, los resultados se interpretan como una validación inicial y "
        "no como una representación estadística de todas las MYPES."
    ))
    story.append(bloque(
        "grafico_control.png",
        "Figura 1. Distribución de los métodos de control reportados por los 6 encuestados.",
    ))
    story.append(P(
        "Tres de seis encuestados utilizan cuaderno o libreta, uno utiliza Excel y dos cuentan con algún "
        "software. En la muestra, cuatro de seis no utilizan un software dedicado para esta actividad."
    ))
    story.append(bloque(
        "grafico_ganancia.png",
        "Figura 2. Nivel de claridad sobre la ganancia mensual.",
    ))
    story.append(P(
        "La mitad de la muestra afirmó conocer exactamente cuánto ganó el último mes; dos de seis "
        "lo conocen aproximadamente y uno indicó no tener claridad."
    ))
    story.append(bloque(
        "grafico_interes.png",
        "Figura 3. Distribución del interés inicial ante la propuesta.",
    ))
    story.append(P(
        "Tres de seis emprendedores manifestaron interés en probar la propuesta y tres prefirieron "
        "mantener sus métodos actuales o no mostraron interés inmediato."
    ))
    story.append(H("Análisis de negocio", "sub"))
    story.append(viñetas([
        "Problema principal: registro y control mediante procesos manuales o herramientas no especializadas.",
        "Necesidad: disponer de información de ventas e inventario ordenada y sencilla.",
        "Oportunidad: concentrar productos, ventas, stock y reportes en un único sistema.",
        "Riesgo: la muestra piloto es pequeña y existe un grupo sin interés inmediato.",
        "Indicador del MVP: registrar una venta, actualizar stock y consultar el resultado sin cálculos manuales.",
    ]))

    story.append(H("5. Alternativas para la solución del problema", "sec"))
    story.append(tabla(
        ["Alternativa", "Descripción", "Ventajas", "Limitaciones"],
        [
            ["Solución 1: WonPLUS de escritorio", "Aplicación Java con MVC y PostgreSQL para usuarios, productos, ventas, stock y reportes.", "Control del desarrollo, interfaz simple y alcance adecuado al proyecto.", "Funcionamiento local o en red básica; sin facturación electrónica en la primera versión."],
            ["Solución 2: Sistema web", "Aplicación web con backend Java y PostgreSQL, accesible desde navegador.", "Mayor accesibilidad y posibilidad de trabajo multiusuario.", "Mayor complejidad de desarrollo, despliegue y mantenimiento."],
            ["Solución 3: Plataforma existente", "Uso de un software comercial de gestión ya disponible.", "Implementación potencialmente rápida y funciones ya desarrolladas.", "Costos recurrentes y menor adaptación al alcance específico."],
        ],
        [3.3 * cm, 4.4 * cm, 3.6 * cm, W - 11.3 * cm],
    ))
    story.append(Spacer(1, 8))
    story.append(H("5.1 Solución 1", "sub"))
    story.append(P(
        "Corresponde a la propuesta desarrollada en el proyecto. Se organiza en autenticación, "
        "productos, ventas, inventario y reportes, con MVC, PostgreSQL y JDBC. Las pantallas son "
        "los bocetos de WonPLUS ya definidos."
    ))
    story.append(H("Pantallas de solución — Inicio de sesión", "sub"))
    story.append(figura("boceto_login.png"))
    story.append(Spacer(1, 6))
    story.append(H("Dashboard inicial", "sub"))
    story.append(figura("boceto_panel.png"))
    story.append(Spacer(1, 6))
    story.append(H("Registro de venta", "sub"))
    story.append(figura("boceto_venta.png"))
    story.append(Spacer(1, 6))
    story.append(H("Gestión de productos", "sub"))
    story.append(figura("boceto_productos.png"))
    story.append(Spacer(1, 6))
    story.append(H("Historial", "sub"))
    story.append(figura("boceto_historial.png"))
    story.append(Spacer(1, 8))

    story.append(H("5.2 Solución 2", "sub"))
    story.append(P(
        "Se considera como una evolución futura de WonPLUS, especialmente si se requiere acceso "
        "multiusuario desde diferentes ubicaciones. En el avance 2 se ilustró con pantallas de referencia "
        "de un producto comercial. Este avance no agrega bocetos nuevos: la solución construida sigue siendo la 1."
    ))
    story.append(H("5.3 Solución 3", "sub"))
    story.append(P(
        "Constituye una alternativa externa al desarrollo propio. Puede reducir el tiempo de "
        "implementación, pero limita el control de la arquitectura y de la adaptación al proyecto. "
        "Tampoco se redibuja: permanece como la alternativa ya descrita en el avance 2."
    ))

    story.append(H("6. Diseños de las estructuras de las soluciones", "sec"))
    story.append(H("6.1 Project Charter", "sub"))
    story.append(P(
        "Se mantiene el charter del avance 2 y se precisan los entregables que este avance ya tiene construidos."
    ))
    story.append(tabla(
        ["Elemento", "Definición del proyecto WonPLUS"],
        [
            ["Nombre", "WonPLUS — Sistema de gestión de ventas e inventarios para MYPES."],
            ["Propósito", "Reducir la dependencia de procesos manuales mediante el registro digital de ventas, productos e inventario."],
            ["Objetivo general", "Desarrollar un sistema de gestión de ventas e inventarios en Java bajo arquitectura MVC."],
            ["Alcance", "Usuarios, productos, ventas, actualización de stock y reportes básicos."],
            ["Fuera de alcance", "Facturación electrónica, conexión con SUNAT, lectores físicos de códigos de barras y funciones avanzadas en la nube."],
            ["Entregables", "Documentación, modelos, diagramas, prototipo, aplicación Java y repositorio GitHub."],
            ["Usuarios", "Administrador y Vendedor; como segmento, MYPES y emprendedores."],
            ["Tecnología", "Java 21, MVC, PostgreSQL, JDBC, Maven, Guava, Apache POI, Apache Commons y Logback."],
            ["Restricciones", "Tiempo académico, alcance del MVP, recursos limitados y necesidad de ampliar la validación."],
            ["Criterios de éxito", "Registrar ventas, actualizar stock, guardar información y consultar reportes básicos."],
        ],
        [3.6 * cm, W - 3.6 * cm],
    ))
    story.append(Spacer(1, 8))

    story.append(H("6.2 Diagrama de Gantt Chart", "sub"))
    story.append(P("Cronograma general — 18 semanas. Es el mismo cronograma del avance 2.", "body"))
    story.append(bloque("gantt.png", "Figura 4. Cronograma general de 18 semanas."))

    story.append(H("6.3 Diagramas de proceso", "sub"))
    story.append(P("Proceso actual: gestión manual.", "body"))
    story.append(bloque("proceso_manual.png", "Figura 5. Flujo del proceso manual."))
    story.append(P("Proceso propuesto: gestión con WonPLUS.", "body"))
    story.append(bloque(
        "proceso_propuesto.png",
        "Figura 6. Flujo propuesto con WonPLUS. Elimina la transcripción manual y centraliza la actualización del stock.",
    ))

    story.append(H("6.4 Diagramas de clase", "sub"))
    story.append(bloque("diagrama_clases.png", "Figura 7. Diagrama de clases UML del avance 2."))
    story.append(P(
        "Las clases principales son Usuario, Producto, Categoría, Venta y DetalleVenta. La estructura "
        "se basa en las entidades y métodos definidos en el proyecto."
    ))

    story.append(H("6.5 Diagramas de Entidad–Relación", "sub"))
    story.append(bloque("diagrama_er.png", "Figura 8. Modelo conceptual simplificado de la base de datos."))
    story.append(P(
        "El modelo relaciona usuarios con ventas, ventas con detalles, detalles con productos y "
        "productos con categorías. El diseño lógico contempla las tablas usuario, categoria, "
        "producto, venta y detalle_venta, con claves primarias y foráneas."
    ))

    story.append(H("7. Prototipo funcional de la solución propuesta", "sec"))
    story.append(P(
        "El prototipo representa el flujo principal de uso del sistema y organiza las pantallas ya "
        "descritas. En este avance esas pantallas siguen siendo la referencia visual de WonPLUS."
    ))
    story.append(H("Pantalla 1 — Inicio de sesión", "sub"))
    story.append(figura("boceto_inicio.png"))
    story.append(Spacer(1, 6))
    story.append(figura("boceto_login.png"))
    story.append(P("Permite ingresar las credenciales del usuario según el rol asignado."))
    story.append(H("Pantalla 2 — Panel principal", "sub"))
    story.append(figura("boceto_panel.png"))
    story.append(P("Concentra indicadores básicos para consultar rápidamente ventas e inventario."))
    story.append(H("Pantalla 3 — Registrar venta", "sub"))
    story.append(figura("boceto_venta.png"))
    story.append(P(
        "Permite seleccionar productos, indicar cantidades y registrar la operación. Al confirmar, el "
        "stock debe actualizarse en la base de datos."
    ))
    story.append(H("Pantalla 4 — Gestión de productos", "sub"))
    story.append(figura("boceto_productos.png"))
    story.append(P(
        "Permite registrar, consultar y editar productos, además de visualizar alertas cuando el stock "
        "se encuentre bajo."
    ))
    story.append(P(
        "Flujo funcional del prototipo: Inicio de sesión → Panel principal → Registro de venta → "
        "Actualización de stock → Consulta de resultados. Para administración: Inicio de sesión → "
        "Panel principal → Gestión de productos → Actualización de información."
    ))

    story.append(H("8. Construcción sobre el mismo alcance", "sec"))
    story.append(P(
        "La aplicación está en la carpeta wonplus-java del repositorio "
        "https://github.com/ZuloagaZapanaFamelMarion/WonPLUS. Usa Java 21, Maven, Swing y "
        "PostgreSQL. Las pantallas de la solución siguen los bocetos de este documento: inicio de "
        "sesión, panel, registro de venta, productos e historial."
    ))
    story.append(tabla(
        ["Boceto de WonPLUS", "Qué cubre del alcance", "Dónde está en el código"],
        [
            ["Inicio de sesión", "Ingreso del administrador o del vendedor", "LoginVista y AuthService"],
            ["Panel principal", "Ventas del día, ganancia y stock bajo", "PanelVista y ReporteService"],
            ["Registrar venta", "Pedido, total y descuento de stock", "VentaVista y VentaService"],
            ["Gestión de productos", "Alta, edición y alerta de stock bajo", "ProductosVista y ProductoService"],
            ["Historial", "Consulta de las ventas registradas", "HistorialVista y VentaService"],
        ],
        [4.2 * cm, 5.6 * cm, W - 9.8 * cm],
    ))
    story.append(Spacer(1, 6))
    story.append(P(
        "El mismo programa atiende, dentro de ese flujo, la cuenta de usuario, la categoría del "
        "producto, el ticket de la venta, el detalle, la alerta de stock y el Excel del periodo. No se "
        "dibujan pantallas distintas de los bocetos ya entregados."
    ))

    story.append(H("8.1 Arquitectura", "sub"))
    story.append(P(
        "La vista está en pe.edu.utp.wonplus.ui. ControladorPrincipal recibe la acción y llama al "
        "servicio. Los servicios aplican las reglas. Las interfaces UsuarioDao, CategoriaDao, "
        "ProductoDao y VentaDao separan el acceso a PostgreSQL. Cada servicio recibe su DAO por "
        "el constructor. CalculadoraVenta calcula el total y la ganancia. Las pruebas JUnit cubren "
        "ese cálculo, el periodo, el cifrado de la clave y el archivo Excel."
    ))
    story.append(P(
        "La contraseña se guarda con PBKDF2-HMAC-SHA256, sal aleatoria y 65536 iteraciones. "
        "Un usuario inactivo no ingresa. Productos, categorías y usuarios quedan reservados al "
        "administrador. Las consultas usan parámetros. La clave de la base no está en el repositorio: "
        "se copia db.properties.example a db.properties en el equipo local."
    ))

    story.append(H("8.2 Librerías", "sub"))
    story.append(tabla(
        ["Librería", "Dónde se usa", "Para qué"],
        [
            ["Google Guava", "ValidadorEntrada, ProductoService, CalculadoraVenta y VentaService", "Limpiar textos, rechazar nulos y armar la lista de la venta."],
            ["Apache POI", "ExportadorExcel", "Generar el Excel del reporte."],
            ["Apache Commons", "ValidadorEntrada, UsuarioService y ExportadorExcel", "Validar textos y el nombre del archivo."],
            ["Logback", "logback.xml, servicios y DAO", "Registrar la operación en logs/wonplus.log, sin escribir la contraseña."],
        ],
        [3.4 * cm, 6.2 * cm, W - 9.6 * cm],
    ))
    story.append(Spacer(1, 8))

    story.append(H("8.3 Control de versiones", "sub"))
    story.append(P(
        "El repositorio es https://github.com/ZuloagaZapanaFamelMarion/WonPLUS, rama main. "
        "El código de esta solución y este informe están publicados."
    ))
    story.append(tabla(
        ["Commit", "Contenido publicado"],
        [
            ["d5f89b3", "Núcleo Java de WonPLUS con PostgreSQL, DAO y pruebas."],
            ["726ea8f", "Pantallas de ventas, inventario, usuarios y reportes."],
            ["94e5349", "Documento de arquitectura y de las pantallas."],
            ["c44b754", "README del repositorio actualizado a la aplicación Java."],
            ["b1e3c2b", "Informe del avance 3 y ejemplo de conexión, sin la clave de la base."],
        ],
        [2.6 * cm, W - 2.6 * cm],
    ))
    story.append(Spacer(1, 8))

    story.append(H("CAPÍTULO 2", "cap"))
    story.append(H("1. Recomendaciones", "sec"))
    story.append(viñetas([
        "Ampliar la encuesta a una muestra mayor y más diversa de MYPES.",
        "Realizar pruebas de usabilidad con usuarios que representen Administrador y Vendedor.",
        "Mantener controlado el alcance del MVP y priorizar ventas, productos, stock y reportes.",
        "Evaluar una migración futura a una arquitectura web con Java y Spring Boot.",
        "Implementar copias de seguridad periódicas y mecanismos de recuperación.",
        "Investigar la integración con facturación electrónica antes de incorporar esta función.",
        "Documentar pruebas, errores y correcciones para facilitar el mantenimiento.",
    ]))
    story.append(H("2. Conclusiones", "sec"))
    story.append(viñetas([
        "WonPLUS plantea una solución tecnológica centrada en facilitar a las MYPES el registro de ventas y el control de inventario mediante una herramienta sencilla.",
        "El análisis del proceso manual muestra puntos de intervención claros: registro de operaciones, actualización de stock, almacenamiento y consulta de resultados.",
        "La arquitectura MVC, Java, PostgreSQL y JDBC proporcionan la estructura técnica definida para el MVP. El modelo de datos contempla usuarios, productos, categorías, ventas y detalles de venta.",
        "La encuesta piloto aporta evidencia inicial, pero la muestra de seis participantes es reducida y no representa a todas las MYPES del Perú.",
        "Los bocetos del avance 2 siguen siendo la interfaz de referencia. La aplicación Java, las pruebas, las librerías y el repositorio GitHub continúan ese mismo alcance.",
    ]))
    story.append(H("3. Bibliografía", "sec"))
    refs = [
        "Congreso de la República del Perú. (2011). Ley N.° 29733: Ley de Protección de Datos Personales. Diario Oficial El Peruano.",
        "Instituto Nacional de Estadística e Informática. (2025). Reporte de empresas en el Perú: Micro y pequeñas empresas. https://www.inei.gob.pe",
        "Nielsen, J. (1994). Usability Engineering. Morgan Kaufmann.",
        "Obe, R. O., y Hsu, L. S. (2017). PostgreSQL: Up and Running (3rd ed.). O’Reilly Media.",
        "Oracle Corporation. (2023). Java Platform, Standard Edition Documentation. https://docs.oracle.com/javase/",
        "Sommerville, I. (2016). Ingeniería de software (10.ª ed.). Pearson Educación.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, S("ref", fontSize=10, leading=13, leftIndent=14, firstLineIndent=-14, spaceAfter=4)))

    story.append(H("4. Anexos", "sec"))
    story.append(H("4.1 Modelo Lean Canvas", "sub"))
    story.append(figura("lienzo_canvas.png"))
    story.append(Spacer(1, 6))
    story.append(tabla(
        ["Problema", "Segmentos", "Propuesta única de valor"],
        [[
            "Registro manual de ventas; dificultad para controlar stock; poca claridad de resultados.",
            "MYPES y emprendedores que realizan ventas y necesitan control básico.",
            "Gestión sencilla de ventas e inventario en un solo sistema.",
        ]],
        [W / 3, W / 3, W / 3],
    ))
    story.append(Spacer(1, 4))
    story.append(tabla(
        ["Solución", "Canales", "Ventaja especial"],
        [[
            "Usuarios, productos, ventas, stock y reportes.",
            "Demostraciones, contacto directo y canales digitales.",
            "Simplicidad, operaciones esenciales y adaptación al contexto de una MYPE.",
        ]],
        [W / 3, W / 3, W / 3],
    ))
    story.append(Spacer(1, 4))
    story.append(tabla(
        ["Métricas clave", "Estructura de costos", "Fuentes de ingresos"],
        [[
            "Ventas registradas, productos gestionados, operaciones de stock y uso de reportes.",
            "Desarrollo, infraestructura, dominio, seguridad, mantenimiento y promoción.",
            "Para una futura etapa: licencia, suscripción o soporte, previa validación.",
        ]],
        [W / 3, W / 3, W / 3],
    ))
    story.append(Spacer(1, 8))
    story.append(H("4.2 Modelo de encuesta", "sub"))
    story.append(tabla(
        ["N.°", "Pregunta", "Tipo de respuesta"],
        [
            ["1", "¿A qué rubro pertenece su negocio?", "Respuesta abierta o selección"],
            ["2", "¿Cuál es el rango aproximado de ventas mensuales?", "Selección por rangos"],
            ["3", "¿Cómo controla actualmente sus ingresos y egresos?", "Cuaderno, Excel, software u otro"],
            ["4", "¿Con qué frecuencia registra sus movimientos?", "Diario, interdiario, semanal, mensual u otro"],
            ["5", "¿Sabe exactamente cuánto ganó el mes pasado?", "Sí, más o menos, no"],
            ["6", "¿Con qué frecuencia tiene problemas para conocer su stock disponible?", "Nunca, a veces, frecuentemente"],
            ["7", "¿Qué dificultad encuentra al controlar sus productos?", "Respuesta abierta"],
            ["8", "¿Qué función considera más útil en un sistema de gestión?", "Ventas, inventario, reportes, usuarios u otra"],
            ["9", "¿Le interesaría probar una herramienta sencilla para registrar ventas y controlar stock?", "Sí, no, tal vez"],
            ["10", "¿Qué característica considera indispensable para utilizar un sistema de este tipo?", "Respuesta abierta"],
        ],
        [1.2 * cm, 9.2 * cm, W - 10.4 * cm],
    ))
    story.append(Spacer(1, 6))
    story.append(P(
        "La encuesta se plantea como instrumento de validación del problema y de las necesidades "
        "del usuario. Los resultados utilizados en el cuerpo del documento corresponden a la encuesta "
        "piloto de seis participantes descrita en el avance base."
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
    frame = Frame(63, 48, W, A4[1] - 168, id="normal", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="portada", frames=[frame], onPage=pagina),
        PageTemplate(id="interior", frames=[frame], onPage=pagina),
    ])
    doc.multiBuild(build())
    print(OUT)


if __name__ == "__main__":
    main()
