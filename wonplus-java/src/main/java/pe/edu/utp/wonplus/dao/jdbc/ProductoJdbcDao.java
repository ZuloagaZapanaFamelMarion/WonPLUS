package pe.edu.utp.wonplus.dao.jdbc;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pe.edu.utp.wonplus.config.ConexionBd;
import pe.edu.utp.wonplus.dao.ProductoDao;
import pe.edu.utp.wonplus.excepcion.PersistenciaException;
import pe.edu.utp.wonplus.model.Producto;

public final class ProductoJdbcDao implements ProductoDao {
    private static final Logger LOG = LoggerFactory.getLogger(ProductoJdbcDao.class);
    private static final String SELECT = """
            SELECT p.id_producto, p.nombre, p.precio, p.costo, p.stock, p.stock_minimo,
                   p.id_categoria, c.nombre AS categoria
            FROM producto p
            JOIN categoria c ON c.id_categoria = p.id_categoria
            """;
    private final ConexionBd conexiones;

    public ProductoJdbcDao(ConexionBd conexiones) {
        this.conexiones = conexiones;
    }

    @Override
    public List<Producto> listar() {
        try (Connection cn = conexiones.abrir();
             PreparedStatement ps = cn.prepareStatement(SELECT + " ORDER BY p.nombre");
             ResultSet rs = ps.executeQuery()) {
            List<Producto> productos = new ArrayList<>();
            while (rs.next()) {
                productos.add(mapear(rs));
            }
            return productos;
        } catch (SQLException e) {
            LOG.error("Error de base de datos al listar productos", e);
            throw new PersistenciaException("No se pudo listar los productos", e);
        }
    }

    @Override
    public void guardar(Producto producto) {
        try (Connection cn = conexiones.abrir()) {
            if (producto.id() == 0) {
                String sql = """
                        INSERT INTO producto (nombre, precio, costo, stock, stock_minimo, id_categoria)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """;
                try (PreparedStatement ps = cn.prepareStatement(sql)) {
                    llenar(ps, producto);
                    ps.executeUpdate();
                }
            } else {
                String sql = """
                        UPDATE producto
                        SET nombre = ?, precio = ?, costo = ?, stock = ?, stock_minimo = ?, id_categoria = ?
                        WHERE id_producto = ?
                        """;
                try (PreparedStatement ps = cn.prepareStatement(sql)) {
                    llenar(ps, producto);
                    ps.setInt(7, producto.id());
                    ps.executeUpdate();
                }
            }
        } catch (SQLException e) {
            LOG.error("Error de base de datos al guardar el producto", e);
            throw new PersistenciaException("No se pudo guardar el producto", e);
        }
    }

    @Override
    public int contarStockBajo() {
        String sql = "SELECT COUNT(*) FROM producto WHERE stock <= stock_minimo";
        try (Connection cn = conexiones.abrir();
             PreparedStatement ps = cn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            rs.next();
            return rs.getInt(1);
        } catch (SQLException e) {
            LOG.error("Error de base de datos al contar el stock bajo", e);
            throw new PersistenciaException("No se pudo consultar el stock", e);
        }
    }

    private void llenar(PreparedStatement ps, Producto producto) throws SQLException {
        ps.setString(1, producto.nombre());
        ps.setBigDecimal(2, producto.precio());
        ps.setBigDecimal(3, producto.costo());
        ps.setInt(4, producto.stock());
        ps.setInt(5, producto.stockMinimo());
        ps.setInt(6, producto.idCategoria());
    }

    private Producto mapear(ResultSet rs) throws SQLException {
        return new Producto(
                rs.getInt("id_producto"),
                rs.getString("nombre"),
                rs.getBigDecimal("precio"),
                rs.getBigDecimal("costo"),
                rs.getInt("stock"),
                rs.getInt("stock_minimo"),
                rs.getInt("id_categoria"),
                rs.getString("categoria")
        );
    }
}
