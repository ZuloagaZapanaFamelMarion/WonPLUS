package pe.edu.utp.wonplus.config;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pe.edu.utp.wonplus.excepcion.PersistenciaException;
import pe.edu.utp.wonplus.seguridad.CifradorClave;
import pe.edu.utp.wonplus.servicio.PeriodoConsulta;

public final class InicializadorBd {
    private static final Logger LOG = LoggerFactory.getLogger(InicializadorBd.class);
    private final ConexionBd conexiones;

    public InicializadorBd(ConexionBd conexiones) {
        this.conexiones = conexiones;
    }

    public void preparar() {
        try (Connection cn = conexiones.abrir()) {
            crearTablas(cn);
            sembrar(cn);
        } catch (SQLException | IOException e) {
            LOG.error("Error de base de datos al preparar el esquema", e);
            throw new PersistenciaException("No se pudo preparar la base de datos wonplus", e);
        }
        LOG.info("Base de datos lista");
    }

    private void crearTablas(Connection cn) throws IOException, SQLException {
        String sql;
        try (var entrada = InicializadorBd.class.getResourceAsStream("/schema.sql")) {
            if (entrada == null) {
                throw new IOException("No se encontró schema.sql");
            }
            sql = new String(entrada.readAllBytes(), StandardCharsets.UTF_8);
        }
        for (String sentencia : sql.split(";")) {
            String limpia = sentencia.trim();
            if (!limpia.isEmpty()) {
                try (var ps = cn.createStatement()) {
                    ps.execute(limpia);
                }
            }
        }
    }

    private void sembrar(Connection cn) throws SQLException {
        cn.setAutoCommit(false);
        try {
            if (contar(cn, "usuario") > 0) {
                cn.rollback();
                return;
            }
            int admin = insertarUsuario(cn, "Administrador WonPLUS", "admin@wonplus.pe", "Admin123", "ADMIN");
            insertarUsuario(cn, "Vendedor de tienda", "vendedor@wonplus.pe", "Venta123", "VENDEDOR");
            int bebidas = insertarCategoria(cn, "Bebidas");
            int papeleria = insertarCategoria(cn, "Papelería");
            int merch = insertarCategoria(cn, "Merchandising");
            int cafe = insertarProducto(cn, "Café premium", "8.50", "4.00", 3, 5, bebidas);
            int cuaderno = insertarProducto(cn, "Cuaderno emprendedor", "12.00", "6.00", 14, 5, papeleria);
            insertarProducto(cn, "Kit de branding", "45.00", "22.00", 2, 5, merch);
            int camiseta = insertarProducto(cn, "Camiseta WonPLUS", "35.00", "18.00", 22, 5, merch);
            insertarProducto(cn, "Pack de stickers", "8.00", "2.50", 4, 5, papeleria);

            LocalDateTime ahora = LocalDateTime.now(PeriodoConsulta.ZONA);
            int venta1 = insertarVenta(cn, ahora.withHour(9).withMinute(20).withSecond(0), "17.00", admin);
            insertarDetalle(cn, venta1, cafe, 2, "8.50", "4.00");
            int venta2 = insertarVenta(cn, ahora.withHour(11).withMinute(5).withSecond(0), "35.00", admin);
            insertarDetalle(cn, venta2, camiseta, 1, "35.00", "18.00");
            int venta3 = insertarVenta(cn, ahora.minusDays(2).withHour(16).withMinute(10).withSecond(0), "12.00", admin);
            insertarDetalle(cn, venta3, cuaderno, 1, "12.00", "6.00");
            cn.commit();
            LOG.info("Datos iniciales cargados. Admin: admin@wonplus.pe / Vendedor: vendedor@wonplus.pe");
        } catch (SQLException e) {
            cn.rollback();
            throw e;
        }
    }

    private int contar(Connection cn, String tabla) throws SQLException {
        try (var ps = cn.createStatement();
             ResultSet rs = ps.executeQuery("SELECT COUNT(*) FROM " + tabla)) {
            rs.next();
            return rs.getInt(1);
        }
    }

    private int insertarUsuario(Connection cn, String nombre, String email, String clave, String rol) throws SQLException {
        String sql = """
                INSERT INTO usuario (nombre, email, password_hash, rol, activo)
                VALUES (?, ?, ?, ?, TRUE)
                RETURNING id_usuario
                """;
        try (PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setString(1, nombre);
            ps.setString(2, email);
            ps.setString(3, CifradorClave.cifrar(clave));
            ps.setString(4, rol);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getInt(1);
            }
        }
    }

    private int insertarCategoria(Connection cn, String nombre) throws SQLException {
        try (PreparedStatement ps = cn.prepareStatement(
                "INSERT INTO categoria (nombre) VALUES (?) RETURNING id_categoria")) {
            ps.setString(1, nombre);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getInt(1);
            }
        }
    }

    private int insertarProducto(
            Connection cn,
            String nombre,
            String precio,
            String costo,
            int stock,
            int minimo,
            int categoria
    ) throws SQLException {
        String sql = """
                INSERT INTO producto (nombre, precio, costo, stock, stock_minimo, id_categoria)
                VALUES (?, ?, ?, ?, ?, ?)
                RETURNING id_producto
                """;
        try (PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setString(1, nombre);
            ps.setBigDecimal(2, new BigDecimal(precio));
            ps.setBigDecimal(3, new BigDecimal(costo));
            ps.setInt(4, stock);
            ps.setInt(5, minimo);
            ps.setInt(6, categoria);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getInt(1);
            }
        }
    }

    private int insertarVenta(Connection cn, LocalDateTime fecha, String total, int usuario) throws SQLException {
        try (PreparedStatement ps = cn.prepareStatement(
                "INSERT INTO venta (fecha, total, id_usuario) VALUES (?, ?, ?) RETURNING id_venta")) {
            ps.setTimestamp(1, Timestamp.valueOf(fecha));
            ps.setBigDecimal(2, new BigDecimal(total));
            ps.setInt(3, usuario);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getInt(1);
            }
        }
    }

    private void insertarDetalle(
            Connection cn,
            int venta,
            int producto,
            int cantidad,
            String precio,
            String costo
    ) throws SQLException {
        String sql = """
                INSERT INTO detalle_venta (cantidad, precio_unitario, costo_unitario, id_venta, id_producto)
                VALUES (?, ?, ?, ?, ?)
                """;
        try (PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setInt(1, cantidad);
            ps.setBigDecimal(2, new BigDecimal(precio));
            ps.setBigDecimal(3, new BigDecimal(costo));
            ps.setInt(4, venta);
            ps.setInt(5, producto);
            ps.executeUpdate();
        }
    }
}
