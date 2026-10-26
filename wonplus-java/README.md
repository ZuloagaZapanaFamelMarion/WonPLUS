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

La arquitectura, las once pantallas, la seguridad y las librerías están descritas en [docs/arquitectura.md](docs/arquitectura.md).

## Archivos del repositorio

- PDF del avance 3: [avance-3/Avance_3_WonPLUS.pdf](avance-3/Avance_3_WonPLUS.pdf). Es el avance 2 completo más lo construido en esta entrega.
- PPT explicativo: se agrega a esta lista cuando el archivo esté en el repositorio.
- Commits con evidencia: cada enlace abre el cambio en GitHub.

| Commit | Qué deja publicado | Evidencia |
|---|---|---|
| `d5f89b3` | Núcleo Java, PostgreSQL, DAO y pruebas | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/d5f89b3ceca7af4e3e61e793c012f8e7b1baec77) |
| `726ea8f` | Pantallas de ventas, inventario, usuarios y reportes | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/726ea8f198825d78269156d352947ab591f944a7) |
| `94e5349` | Documento de arquitectura y de las pantallas | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/94e53493d45c1e02774f1d44cda0f11f79664eff) |
| `c44b754` | README de la aplicación Java | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/c44b754f677539b7c04bdfc0c44b3004e8ca1e77) |
| `b1e3c2b` | Informe del avance y conexión de ejemplo, sin la clave de la base | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/b1e3c2babc4ac9b35542fb60b8b3492dcb54e5ed) |
| `bc62e5e` | PDF del avance 3 con las páginas del avance 2 y lo agregado | [ver commit](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/bc62e5e93fab817ae065b1be2123ccbfe415018a) |

## Tabla comparativa con la rúbrica

Esta sección queda al final del README. La tabla se pega aquí cuando esté la rúbrica completa.
