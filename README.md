# WonPLUS

Sistema de escritorio para que una micro o pequeña empresa registre ventas, controle su inventario y consulte resultados. La aplicación actual está en [`wonplus-java`](wonplus-java) y está hecha en Java 21, con Maven, Swing y PostgreSQL.

## Qué hace

- Ingreso con dos roles: administrador y vendedor.
- Registro y edición de usuarios, categorías y productos.
- Registro de ventas, con ticket, historial y detalle.
- Descuento automático del stock al confirmar una venta y alerta cuando un producto llega al mínimo.
- Reportes por periodo y exportación a Excel.

El vendedor registra ventas y consulta reportes. El administrador, además, gestiona usuarios, categorías y productos. Quedan fuera de esta versión la facturación electrónica, la conexión con SUNAT y el lector de código de barras.

La arquitectura, las pantallas, la seguridad y las librerías están descritas en [`wonplus-java/docs/arquitectura.md`](wonplus-java/docs/arquitectura.md).

## Cómo está organizado

Las pantallas Swing se comunican con `ControladorPrincipal`. El controlador llama a los servicios y los servicios usan interfaces DAO para guardar la información en PostgreSQL. Las contraseñas se almacenan con PBKDF2 y las consultas usan parámetros, no texto armado.

El proyecto usa Google Guava, Apache POI, Apache Commons y Logback. Apache POI genera el Excel de reportes.

## Requisitos

- JDK 21
- Maven
- PostgreSQL en `localhost:5432`, con la base y el usuario `wonplus`

La conexión se lee de `wonplus-java/db.properties`. Al iniciar, la aplicación crea las tablas y carga datos de demostración si la base está vacía.

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
