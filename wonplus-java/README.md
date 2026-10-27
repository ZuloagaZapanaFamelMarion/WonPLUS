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

## Archivos

- Informe del avance 3: [avance-3/Avance_3_WonPLUS.pdf](avance-3/Avance_3_WonPLUS.pdf)
- Presentación: [avance-3/WonPLUS_Avance_3_Presentacion.pdf](avance-3/WonPLUS_Avance_3_Presentacion.pdf)

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
| `399b65b` | Interfaz en el morado de los bocetos | [399b65b](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS/commit/399b65b0ea609863cf3a950ac6eea61f5fec2358) |

## Rúbrica

| Criterio | Puntos | Dónde está |
|---|---|---|
| Arquitectura con MVC, DAO, SOLID y pruebas, más seguridad | 3 | Pantallas en `src/main/java/pe/edu/utp/wonplus/ui`, `ControladorPrincipal` y los DAO. Pruebas en `src/test/java` (`mvn test`). La clave se guarda con PBKDF2 y el vendedor no administra usuarios ni productos. |
| Guava, Apache POI, Apache Commons y Logback | 2 | Las cuatro están en `pom.xml`. Guava valida, POI genera el Excel, Commons revisa textos y Logback escribe `logs/wonplus.log`. En el repositorio solo está `db.properties.example`. |
| Git, con los avances en GitHub | 3 | Repositorio [WonPLUS](https://github.com/ZuloagaZapanaFamelMarion/WonPLUS), rama `main`. Los commits de arriba incluyen el código, el informe y la presentación. |
| Interfaces que cubren el alcance | 6 | Usuarios, productos, ventas, stock y reportes. Esas pantallas están en el PDF del avance 2 y funcionan en el programa. |
| Solución completa, coherente y propia | 4 | El programa hace esas cinco operaciones. El PDF y el código describen lo mismo. No entra SUNAT ni la facturación electrónica. Los commits están a nombre de Marion Zuloaga. |
