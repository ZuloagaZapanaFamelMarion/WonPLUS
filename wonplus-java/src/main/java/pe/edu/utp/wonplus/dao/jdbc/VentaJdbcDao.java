package pe.edu.utp.wonplus.dao.jdbc;

import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pe.edu.utp.wonplus.config.ConexionBd;
import pe.edu.utp.wonplus.dao.VentaDao;
import pe.edu.utp.wonplus.excepcion.PersistenciaException;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.CalculoVenta;
import pe.edu.utp.wonplus.model.DetalleVenta;
import pe.edu.utp.wonplus.model.LineaCalculada;
import pe.edu.utp.wonplus.model.TotalesPeriodo;
import pe.edu.utp.wonplus.model.Venta;
import pe.edu.utp.wonplus.servicio.PeriodoConsulta;

public final class VentaJdbcDao implements VentaDao {
    private static final Logger LOG = LoggerFactory.getLogger(VentaJdbcDao.class);
    private final ConexionBd conexiones;

    public VentaJdbcDao(ConexionBd conexiones) {
        this.conexiones = conexiones;
    }

    @Override
    public Venta registrar(int idUsuario, CalculoVenta calculo) {
        int idVenta = 0;
        try (Connection cn = conexiones.abrir()) {
            cn.setAutoCommit(false);
            try {
                for (LineaCalculada linea : calculo.lineas()) {
                    descontarStock(cn, linea);
                }
                idVenta = insertarVenta(cn, idUsuario, calculo);
                for (LineaCalculada linea : calculo.lineas()) {
                    insertarDetalle(cn, idVenta, linea);
                }
                cn.commit();
            } catch (Exception e) {
                cn.rollback();
                if (e instanceof ReglaNegocioException regla) {
                    throw regla;
                }
                if (e instanceof SQLException sql) {
                    throw sql;
                }
                throw new PersistenciaException("No se pudo registrar la venta", e);
            }
        } catch (SQLException e) {
            LOG.error("Error de base de datos al registrar la venta", e);
            throw new PersistenciaException("No se pudo registrar la venta", e);
        }
        return buscar(idVenta);
    }

    @Override
    public TotalesPeriodo totales(LocalDateTime desde, LocalDateTime hasta) {
        String sql = """
                SELECT COUNT(*) AS operaciones,
                       COALESCE(SUM(v.total), 0) AS total,
                       COALESCE((
                           SELECT SUM((d.precio_unitario - d.costo_unitario) * d.cantidad)
                           FROM detalle_venta d
                           JOIN venta v2 ON v2.id_venta = d.id_venta
                           WHERE v2.fecha >= ? AND v2.fecha < ?
                       ), 0) AS ganancia
                FROM venta v
                WHERE v.fecha >= ? AND v.fecha < ?
                """;
        try (Connection cn = conexiones.abrir();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            marcarRango(ps, desde, hasta);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return new TotalesPeriodo(
                        rs.getBigDecimal("total"),
                        rs.getInt("operaciones"),
                        rs.getBigDecimal("ganancia")
                );
            }
        } catch (SQLException e) {
            LOG.error("Error de base de datos al calcular los totales", e);
            throw new PersistenciaException("No se pudo calcular el resumen", e);
        }
    }

    @Override
    public List<Venta> listar(LocalDateTime desde, LocalDateTime hasta) {
        String sql = """
                SELECT v.id_venta, v.fecha, v.total, v.id_usuario, u.nombre,
                       COALESCE(SUM((d.precio_unitario - d.costo_unitario) * d.cantidad), 0) AS ganancia
                FROM venta v
                JOIN usuario u ON u.id_usuario = v.id_usuario
                LEFT JOIN detalle_venta d ON d.id_venta = v.id_venta
                WHERE v.fecha >= ? AND v.fecha < ?
                GROUP BY v.id_venta, v.fecha, v.total, v.id_usuario, u.nombre
                ORDER BY v.fecha DESC
                """;
        try (Connection cn = conexiones.abrir();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setTimestamp(1, Timestamp.valueOf(desde));
            ps.setTimestamp(2, Timestamp.valueOf(hasta));
            try (ResultSet rs = ps.executeQuery()) {
                List<Venta> ventas = new ArrayList<>();
                while (rs.next()) {
                    ventas.add(mapearResumen(rs));
                }
                return ventas;
            }
        } catch (SQLException e) {
            LOG.error("Error de base de datos al listar ventas", e);
            throw new PersistenciaException("No se pudo consultar el historial", e);
        }
    }

    @Override
    public Venta buscar(int id) {
        String sql = """
                SELECT v.id_venta, v.fecha, v.total, v.id_usuario, u.nombre,
                       COALESCE(SUM((d.precio_unitario - d.costo_unitario) * d.cantidad), 0) AS ganancia
                FROM venta v
                JOIN usuario u ON u.id_usuario = v.id_usuario
                LEFT JOIN detalle_venta d ON d.id_venta = v.id_venta
                WHERE v.id_venta = ?
                GROUP BY v.id_venta, v.fecha, v.total, v.id_usuario, u.nombre
                """;
        try (Connection cn = conexiones.abrir();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setInt(1, id);
            Venta resumen;
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    throw new ReglaNegocioException("La venta no existe");
                }
                resumen = mapearResumen(rs);
            }
            return new Venta(
                    resumen.id(),
                    resumen.fecha(),
                    resumen.total(),
                    resumen.ganancia(),
                    resumen.idUsuario(),
                    resumen.vendedor(),
                    detalles(cn, id)
            );
        } catch (SQLException e) {
            LOG.error("Error de base de datos al buscar la venta", e);
            throw new PersistenciaException("No se pudo abrir el detalle de la venta", e);
        }
    }

    private void descontarStock(Connection cn, LineaCalculada linea) throws SQLException {
        int stock;
        try (PreparedStatement ps = cn.prepareStatement(
                "SELECT stock FROM producto WHERE id_producto = ? FOR UPDATE")) {
            ps.setInt(1, linea.idProducto());
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    throw new ReglaNegocioException("Hay un producto que ya no existe");
                }
                stock = rs.getInt("stock");
            }
        }
        if (stock < linea.cantidad()) {
            throw new ReglaNegocioException("Stock insuficiente de " + linea.nombre());
        }
        try (PreparedStatement ps = cn.prepareStatement(
                "UPDATE producto SET stock = ? WHERE id_producto = ?")) {
            ps.setInt(1, stock - linea.cantidad());
            ps.setInt(2, linea.idProducto());
            ps.executeUpdate();
        }
    }

    private int insertarVenta(Connection cn, int idUsuario, CalculoVenta calculo) throws SQLException {
        String sql = """
                INSERT INTO venta (fecha, total, id_usuario)
                VALUES (?, ?, ?)
                RETURNING id_venta
                """;
        try (PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setTimestamp(1, Timestamp.valueOf(LocalDateTime.now(PeriodoConsulta.ZONA)));
            ps.setBigDecimal(2, calculo.total());
            ps.setInt(3, idUsuario);
            try (ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getInt("id_venta");
            }
        }
    }

    private void insertarDetalle(Connection cn, int idVenta, LineaCalculada linea) throws SQLException {
        String sql = """
                INSERT INTO detalle_venta
                    (cantidad, precio_unitario, costo_unitario, id_venta, id_producto)
                VALUES (?, ?, ?, ?, ?)
                """;
        try (PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setInt(1, linea.cantidad());
            ps.setBigDecimal(2, linea.precioUnitario());
            ps.setBigDecimal(3, linea.costoUnitario());
            ps.setInt(4, idVenta);
            ps.setInt(5, linea.idProducto());
            ps.executeUpdate();
        }
    }

    private List<DetalleVenta> detalles(Connection cn, int idVenta) throws SQLException {
        String sql = """
                SELECT d.id_detalle, d.id_producto, p.nombre, d.cantidad, d.precio_unitario, d.costo_unitario
                FROM detalle_venta d
                JOIN producto p ON p.id_producto = d.id_producto
                WHERE d.id_venta = ?
                ORDER BY d.id_detalle
                """;
        try (PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setInt(1, idVenta);
            try (ResultSet rs = ps.executeQuery()) {
                List<DetalleVenta> detalles = new ArrayList<>();
                while (rs.next()) {
                    detalles.add(new DetalleVenta(
                            rs.getInt("id_detalle"),
                            rs.getInt("id_producto"),
                            rs.getString("nombre"),
                            rs.getInt("cantidad"),
                            rs.getBigDecimal("precio_unitario"),
                            rs.getBigDecimal("costo_unitario")
                    ));
                }
                return detalles;
            }
        }
    }

    private void marcarRango(PreparedStatement ps, LocalDateTime desde, LocalDateTime hasta) throws SQLException {
        Timestamp inicio = Timestamp.valueOf(desde);
        Timestamp fin = Timestamp.valueOf(hasta);
        ps.setTimestamp(1, inicio);
        ps.setTimestamp(2, fin);
        ps.setTimestamp(3, inicio);
        ps.setTimestamp(4, fin);
    }

    private Venta mapearResumen(ResultSet rs) throws SQLException {
        BigDecimal ganancia = rs.getBigDecimal("ganancia");
        return new Venta(
                rs.getInt("id_venta"),
                rs.getTimestamp("fecha").toLocalDateTime(),
                rs.getBigDecimal("total"),
                ganancia == null ? BigDecimal.ZERO : ganancia,
                rs.getInt("id_usuario"),
                rs.getString("nombre"),
                List.of()
        );
    }
}
