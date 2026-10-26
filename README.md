# WonPLUS

Sistema de escritorio para que una micro o pequeña empresa registre ventas, controle su inventario y consulte resultados. La aplicación actual está en [`wonplus-java`](wonplus-java) y está hecha en Java 21, con Maven, Swing y PostgreSQL.

## Qué hace

- Ingreso con dos roles: administrador y vendedor.
- Registro y edición de usuarios, categorías y productos.
- Registro de ventas, con ticket, historial y detalle.
- Descuento automático del stock al confirmar una venta y alerta cuando un producto llega al mínimo.
- Reportes por periodo y exportación a Excel.

El vendedor registra ventas y consulta reportes. El administrador, además, gestiona usuarios, categorías y productos. Quedan fuera de esta versión la facturación electrónica, la conexión con SUNAT y el lector de código de barras.

La arquitectura, las pantallas, la seguridad y las librerías están descritas en [`wonplus-java/docs/arquitectura.md`](wonplus-java/docs/arquitectura.md). El informe del avance 3, continuación del avance 2, está en [`wonplus-java/avance-3/Avance_3_WonPLUS.pdf`](wonplus-java/avance-3/Avance_3_WonPLUS.pdf).

## Cómo está organizado

Las pantallas Swing se comunican con `ControladorPrincipal`. El controlador llama a los servicios y los servicios usan interfaces DAO para guardar la información en PostgreSQL. Las contraseñas se almacenan con PBKDF2 y las consultas usan parámetros, no texto armado.

El proyecto usa Google Guava, Apache POI, Apache Commons y Logback. Apache POI genera el Excel de reportes.

## Requisitos

- JDK 21
- Maven
- PostgreSQL en `localhost:5432`, con la base `wonplus`

La clave de la base no está en Git. Copie el ejemplo y complete la clave local:

```bash
cd wonplus-java
cp db.properties.example db.properties
```

Al iniciar, la aplicación crea las tablas y carga datos de demostración si la base está vacía.

## Ejecutar

```bash
cd wonplus-java
chmod +x ejecutar.sh
./ejecutar.sh
```

También se puede construir y abrir el programa con Maven:

```bash
cd wonplus-java
mvn -q package
java -jar target/wonplus-1.0.0.jar
```

Cuentas de demostración:

- Administrador: `admin@wonplus.pe` / `Admin123`
- Vendedor: `vendedor@wonplus.pe` / `Venta123`

## Pruebas

```bash
cd wonplus-java
mvn test
```

Las pruebas cubren el cálculo de la venta, los periodos de consulta, el cifrado de contraseñas y la exportación a Excel.

## Archivos del repositorio

- PDF del avance 3: [`wonplus-java/avance-3/Avance_3_WonPLUS.pdf`](wonplus-java/avance-3/Avance_3_WonPLUS.pdf). Es el avance 2 completo más lo construido en esta entrega.
- PPT explicativo: [`wonplus-java/avance-3/WonPLUS_Avance_3_Presentacion.pptx`](wonplus-java/avance-3/WonPLUS_Avance_3_Presentacion.pptx).
- Commits con evidencia: la tabla de abajo. Cada enlace abre el commit en GitHub.
- Tabla comparativa con la rúbrica: va al final de este archivo.

## Commits con evidencia

Cada fila es un commit de la rama `main`. El enlace muestra el cambio publicado.

| Commit | Qué deja publicado | Evidencia |
|---|---|---|
| `d5f89b3` | Núcleo Java, PostgreSQL, DAO y pruebas | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/d5f89b3ceca7af4e3e61e793c012f8e7b1baec77) |
| `726ea8f` | Pantallas de ventas, inventario, usuarios y reportes | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/726ea8f198825d78269156d352947ab591f944a7) |
| `94e5349` | Documento de arquitectura y de las pantallas | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/94e53493d45c1e02774f1d44cda0f11f79664eff) |
| `c44b754` | README de la aplicación Java | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/c44b754f677539b7c04bdfc0c44b3004e8ca1e77) |
| `b1e3c2b` | Informe del avance y conexión de ejemplo, sin la clave de la base | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/b1e3c2babc4ac9b35542fb60b8b3492dcb54e5ed) |
| `bc62e5e` | PDF del avance 3 con las páginas del avance 2 y lo agregado | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/bc62e5e93fab817ae065b1be2123ccbfe415018a) |

## Tabla comparativa con la rúbrica

| Qué pide la rúbrica | Puntos | Cómo se cumplió |
|---|---|---|
| Diseñar y desarrollar la arquitectura inicial, aplicando al menos 3 de MVC, TDD, DAO y SOLID, y considerando la seguridad. | 3 | Se aplican los cuatro. Las pantallas están en `wonplus-java/src/main/java/pe/edu/utp/wonplus/ui`, `ControladorPrincipal` coordina y los servicios reciben los DAO por el constructor. Las pruebas JUnit están en `src/test/java` y se ejecutan con `mvn test`. La contraseña se guarda con PBKDF2, el rol limita la administración y las consultas usan parámetros. |
| Incorporar Google Guava, Apache POI, Apache Commons y Logback, con cuidado básico de la información. | 2 | Las cuatro están en `wonplus-java/pom.xml` y el código las usa: Guava en la validación y el cálculo, Apache POI en el Excel, Apache Commons en los textos y Logback en `logback.xml`. La clave de PostgreSQL no está en Git: el repositorio publica `db.properties.example`. |
| Usar Git y dejar en GitHub el 100 % de los avances y de las actualizaciones de los entregables. | 3 | El repositorio es [WonPLUS](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS), rama `main`. La tabla de commits de arriba enlaza el núcleo, las pantallas, la arquitectura, el README, el PDF y la presentación. |
| Implementar las interfaces gráficas y que su funcionamiento cubra el 100 % del alcance comprometido. | 6 | El alcance del avance 2 es usuarios, productos, ventas, inventario y reportes. Los bocetos de ese avance siguen en el PDF y el programa los ejecuta: ingreso por rol, panel, venta, productos, historial y exportación a Excel. |
| Construir una solución completa, coherente, con buenas prácticas y de autoría propia. | 4 | Completa: cubre esas cinco operaciones y deja fuera SUNAT, la facturación electrónica y el lector de barras. Coherente: el PDF conserva el avance 2 y el código de `wonplus-java` implementa ese alcance. Buenas prácticas: Maven, MVC, DAO, pruebas y Git. Autoría: los commits están a nombre de Marion Zuloaga. |
