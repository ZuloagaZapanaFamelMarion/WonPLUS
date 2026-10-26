# Arquitectura de WonPLUS

Sistema de escritorio para que una MYPE registre ventas, controle productos y consulte resultados. Está desarrollado en Java 21, con Maven, Swing y PostgreSQL.

## Alcance

El sistema cubre cinco operaciones:

- Gestión de usuarios, con roles administrador y vendedor.
- Gestión de categorías y productos.
- Registro de ventas y emisión del ticket.
- Actualización del inventario al confirmar una venta, con alerta de stock bajo.
- Reportes por periodo y exportación a Excel.

Quedan fuera de esta versión la facturación electrónica, la conexión con SUNAT y el lector físico de código de barras.

## Pantallas

| Pantalla | Clase | Quién la usa | Qué hace |
|---|---|---|---|
| Inicio de sesión | `LoginVista` | Ambos | Valida correo y contraseña |
| Panel | `PanelVista` | Ambos | Muestra ventas del día, ganancia y productos con stock bajo |
| Registrar venta | `VentaVista` | Ambos | Arma el pedido y confirma la venta |
| Ticket | `TicketVista` | Ambos | Muestra el comprobante de la última venta |
| Historial | `HistorialVista` | Ambos | Lista las ventas de un periodo |
| Detalle | `DetalleVista` | Ambos | Muestra las líneas de una venta |
| Alertas de stock | `StockVista` | Ambos | Lista productos que llegaron al mínimo |
| Reportes | `ReportesVista` | Ambos | Consulta ventas y exporta el Excel |
| Productos | `ProductosVista` | Administrador | Registra y edita precio, costo, stock y stock mínimo |
| Categorías | `CategoriasVista` | Administrador | Crea, edita y elimina categorías |
| Usuarios | `UsuariosVista` | Administrador | Crea y edita usuarios, rol y estado activo |

El menú de `MarcoPrincipal` oculta productos, categorías y usuarios cuando la sesión pertenece a un vendedor.

## Capas

La solución separa la presentación, la coordinación, las reglas de negocio y la persistencia.

- **Modelo.** Entidades en `pe.edu.utp.wonplus.model`: `Usuario`, `Rol`, `Categoria`, `Producto`, `Venta` y `DetalleVenta`.
- **Vista.** Pantallas Swing en `pe.edu.utp.wonplus.ui`. Cada pantalla implementa `Vista` y solo muestra datos.
- **Controlador.** `ControladorPrincipal` recibe la acción de la pantalla y llama al servicio correspondiente.
- **Servicio.** `AuthService`, `UsuarioService`, `CategoriaService`, `ProductoService`, `VentaService` y `ReporteService` aplican las reglas y exigen sesión.
- **DAO.** Las interfaces `UsuarioDao`, `CategoriaDao`, `ProductoDao` y `VentaDao` definen el acceso a datos. Las clases de `dao.jdbc` las implementan con JDBC.

`Aplicacion` construye esas capas e inyecta cada DAO en su servicio. La vista no abre conexiones ni escribe SQL.

## Principios aplicados

- **MVC.** Las pantallas no contienen SQL. El controlador no calcula totales ni decide el stock. Esas reglas viven en `CalculadoraVenta` y en los servicios.
- **DAO.** El servicio depende de la interfaz. Cambiar el detalle de una consulta no obliga a cambiar la pantalla.
- **SOLID.** Cada servicio atiende un solo grupo de operaciones. Las interfaces DAO son pequeñas. Los servicios reciben esas interfaces por el constructor, así que no dependen de PostgreSQL de forma directa.
- **Pruebas.** JUnit 5 cubre las reglas que no necesitan base de datos: `CalculadoraVentaTest`, `PeriodoConsultaTest`, `SeguridadTest` y `ExportadorExcelTest`. Se ejecutan con `mvn test`.

## Seguridad

- La contraseña no se guarda en texto plano. `CifradorClave` la deriva con PBKDF2-HMAC-SHA256, sal aleatoria y 65536 iteraciones. El login compara el resultado con `MessageDigest.isEqual`.
- `AuthService` exige una sesión activa. Las operaciones de usuarios, productos y categorías exigen además el rol administrador.
- Un usuario marcado como inactivo no puede ingresar.
- `ValidadorEntrada` revisa correo, longitud de contraseña, nombres, montos y cantidades antes de llegar a la base.
- Las consultas usan `PreparedStatement`. Al descontar stock, `VentaJdbcDao` bloquea la fila del producto con `FOR UPDATE` y rechaza la venta si la cantidad supera el stock disponible.

## Librerías

Maven declara y el código usa estas cuatro librerías:

| Librería | Dónde se usa | Para qué |
|---|---|---|
| Google Guava | `ValidadorEntrada`, `ProductoService`, `CalculadoraVenta`, `VentaService` | Limpiar textos, rechazar nulos y armar listas inmutables |
| Apache POI | `ExportadorExcel` | Generar el archivo `.xlsx` de reportes |
| Apache Commons | `ValidadorEntrada`, `UsuarioService`, `ExportadorExcel` | Validar textos y normalizar el nombre del Excel |
| Logback | `src/main/resources/logback.xml` y los servicios y DAO | Registrar ingresos, ventas rechazadas y errores de base en `logs/wonplus.log` |

## Datos

La conexión se lee de `db.properties` en el equipo local. El repositorio solo publica `db.properties.example`; el archivo con la clave no entra a Git.

PostgreSQL guarda cinco tablas, definidas en `src/main/resources/schema.sql`.

- `usuario`: nombre, correo único, `password_hash`, rol (`ADMIN` o `VENDEDOR`) y `activo`.
- `categoria`: nombre único.
- `producto`: nombre, precio, costo, stock, stock mínimo y categoría.
- `venta`: fecha, total y usuario que la registró.
- `detalle_venta`: cantidad, precio, costo, venta y producto.

Un usuario registra varias ventas. Una venta tiene varias líneas. Cada línea apunta a un producto y cada producto pertenece a una categoría.
