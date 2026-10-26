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
import pe.edu.utp.wonplus.dao.CategoriaDao;
import pe.edu.utp.wonplus.excepcion.PersistenciaException;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.Categoria;

public final class CategoriaJdbcDao implements CategoriaDao {
    private static final Logger LOG = LoggerFactory.getLogger(CategoriaJdbcDao.class);
    private final ConexionBd conexiones;

    public CategoriaJdbcDao(ConexionBd conexiones) {
        this.conexiones = conexiones;
    }

    @Override
    public List<Categoria> listar() {
        String sql = "SELECT id_categoria, nombre FROM categoria ORDER BY nombre";
        try (Connection cn = conexiones.abrir();
             PreparedStatement ps = cn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            List<Categoria> categorias = new ArrayList<>();
            while (rs.next()) {
                categorias.add(new Categoria(rs.getInt("id_categoria"), rs.getString("nombre")));
            }
            return categorias;
        } catch (SQLException e) {
            LOG.error("Error de base de datos al listar categorías", e);
            throw new PersistenciaException("No se pudo listar las categorías", e);
        }
    }

    @Override
    public void guardar(Categoria categoria) {
        try (Connection cn = conexiones.abrir()) {
            if (categoria.id() == 0) {
                try (PreparedStatement ps = cn.prepareStatement(
                        "INSERT INTO categoria (nombre) VALUES (?)")) {
                    ps.setString(1, categoria.nombre());
                    ps.executeUpdate();
                }
            } else {
                try (PreparedStatement ps = cn.prepareStatement(
                        "UPDATE categoria SET nombre = ? WHERE id_categoria = ?")) {
                    ps.setString(1, categoria.nombre());
                    ps.setInt(2, categoria.id());
                    ps.executeUpdate();
                }
            }
        } catch (SQLException e) {
            if ("23505".equals(e.getSQLState())) {
                throw new ReglaNegocioException("Ya existe una categoría con ese nombre");
            }
            LOG.error("Error de base de datos al guardar la categoría", e);
            throw new PersistenciaException("No se pudo guardar la categoría", e);
        }
    }

    @Override
    public void eliminar(int id) {
        String conteo = "SELECT COUNT(*) FROM producto WHERE id_categoria = ?";
        String borrar = "DELETE FROM categoria WHERE id_categoria = ?";
        try (Connection cn = conexiones.abrir();
             PreparedStatement contar = cn.prepareStatement(conteo)) {
            contar.setInt(1, id);
            try (ResultSet rs = contar.executeQuery()) {
                rs.next();
                if (rs.getInt(1) > 0) {
                    throw new ReglaNegocioException("No se puede eliminar una categoría con productos");
                }
            }
            try (PreparedStatement ps = cn.prepareStatement(borrar)) {
                ps.setInt(1, id);
                ps.executeUpdate();
            }
        } catch (SQLException e) {
            LOG.error("Error de base de datos al eliminar la categoría", e);
            throw new PersistenciaException("No se pudo eliminar la categoría", e);
        }
    }
}
