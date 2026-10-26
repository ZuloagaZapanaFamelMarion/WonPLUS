# WonPLUS — aplicación de escritorio

Sistema de ventas e inventario en Java 21, Maven, Swing y PostgreSQL.

## Requisitos

- JDK 21
- Maven
- PostgreSQL con la base `wonplus` y el usuario `wonplus` / `wonplus`

La conexión se lee de `db.properties`.

## Ejecutar

```bash
chmod +x ejecutar.sh
./ejecutar.sh
```

Cuentas de demostración:

- Administrador: `admin@wonplus.pe` / `Admin123`
- Vendedor: `vendedor@wonplus.pe` / `Venta123`

El vendedor no ve usuarios, productos ni categorías. Las pruebas se ejecutan con `mvn test`.
