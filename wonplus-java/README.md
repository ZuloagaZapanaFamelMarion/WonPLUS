# WonPLUS — aplicación de escritorio

Sistema de ventas e inventario en Java 21, Maven, Swing y PostgreSQL.

## Requisitos

- JDK 21
- Maven
- PostgreSQL con la base `wonplus`

La conexión no se versiona. Copie el ejemplo y ponga la clave local:

```bash
cp db.properties.example db.properties
```

## Ejecutar

```bash
chmod +x ejecutar.sh
./ejecutar.sh
```

Cuentas de demostración:

- Administrador: `admin@wonplus.pe` / `Admin123`
- Vendedor: `vendedor@wonplus.pe` / `Venta123`

El vendedor no ve usuarios, productos ni categorías. Las pruebas se ejecutan con `mvn test`.

La arquitectura, las once pantallas, la seguridad y las librerías están descritas en [docs/arquitectura.md](docs/arquitectura.md). El informe del avance 3, continuación del avance 2, está en [avance-3/Avance_3_WonPLUS.pdf](avance-3/Avance_3_WonPLUS.pdf).
