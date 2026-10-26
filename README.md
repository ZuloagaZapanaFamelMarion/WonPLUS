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

## Archivos

- Informe del avance 3: [`wonplus-java/avance-3/Avance_3_WonPLUS.pdf`](wonplus-java/avance-3/Avance_3_WonPLUS.pdf)
- Presentación: [`wonplus-java/avance-3/WonPLUS_Avance_3_Presentacion.pdf`](wonplus-java/avance-3/WonPLUS_Avance_3_Presentacion.pdf)

## Commits

| Commit | Cambio | Enlace |
|---|---|---|
| `d5f89b3` | Núcleo del programa, base de datos y pruebas | [d5f89b3](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/d5f89b3ceca7af4e3e61e793c012f8e7b1baec77) |
| `726ea8f` | Pantallas de ventas, inventario, usuarios y reportes | [726ea8f](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/726ea8f198825d78269156d352947ab591f944a7) |
| `94e5349` | Arquitectura del proyecto | [94e5349](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/94e53493d45c1e02774f1d44cda0f11f79664eff) |
| `c44b754` | README de la aplicación | [c44b754](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/c44b754f677539b7c04bdfc0c44b3004e8ca1e77) |
| `b1e3c2b` | Informe del avance, sin la clave de la base | [b1e3c2b](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/b1e3c2babc4ac9b35542fb60b8b3492dcb54e5ed) |
| `bc62e5e` | PDF del avance 3 | [bc62e5e](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/bc62e5e93fab817ae065b1be2123ccbfe415018a) |
| `4a9a0d9` | Presentación del avance 3 | [4a9a0d9](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/4a9a0d9fdfbfdc439d498e602dd071905014e2c1) |

## Rúbrica

| Criterio | Puntos | Dónde está |
|---|---|---|
| Arquitectura con MVC, DAO, SOLID y pruebas, más seguridad | 3 | Pantallas en `wonplus-java/src/main/java/pe/edu/utp/wonplus/ui`, `ControladorPrincipal` y los DAO. Pruebas en `src/test/java` (`mvn test`). La clave se guarda con PBKDF2 y el vendedor no administra usuarios ni productos. |
| Guava, Apache POI, Apache Commons y Logback | 2 | Las cuatro están en `wonplus-java/pom.xml`. Guava valida, POI genera el Excel, Commons revisa textos y Logback escribe `logs/wonplus.log`. En el repositorio solo está `db.properties.example`. |
| Git, con los avances en GitHub | 3 | Repositorio [WonPLUS](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS), rama `main`. Los commits de arriba incluyen el código, el informe y la presentación. |
| Interfaces que cubren el alcance | 6 | Usuarios, productos, ventas, stock y reportes. Esas pantallas están en el PDF del avance 2 y funcionan en el programa. |
| Solución completa, coherente y propia | 4 | El programa hace esas cinco operaciones. El PDF y el código describen lo mismo. No entra SUNAT ni la facturación electrónica. Los commits están a nombre de Marion Zuloaga. |
