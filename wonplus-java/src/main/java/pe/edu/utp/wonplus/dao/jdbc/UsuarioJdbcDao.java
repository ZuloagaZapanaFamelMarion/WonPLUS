package pe.edu.utp.wonplus.dao.jdbc;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pe.edu.utp.wonplus.config.ConexionBd;
import pe.edu.utp.wonplus.dao.UsuarioDao;
import pe.edu.utp.wonplus.excepcion.PersistenciaException;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.Rol;
import pe.edu.utp.wonplus.model.Usuario;

public final class UsuarioJdbcDao implements UsuarioDao {
    private static final Logger LOG = LoggerFactory.getLogger(UsuarioJdbcDao.class);
    private final ConexionBd conexiones;

    public UsuarioJdbcDao(ConexionBd conexiones) {
        this.conexiones = conexiones;
    }

    @Override
    public Optional<Usuario> buscarPorEmail(String email) {
        String sql = """
                SELECT id_usuario, nombre, email, password_hash, rol, activo
                FROM usuario
                WHERE email = ?
                """;
        try (Connection cn = conexiones.abrir();
             PreparedStatement ps = cn.prepareStatement(sql)) {
            ps.setString(1, email);
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    return Optional.empty();
                }
                return Optional.of(mapear(rs));
            }
        } catch (SQLException e) {
            LOG.error("Error de base de datos al buscar el usuario", e);
            throw new PersistenciaException("No se pudo consultar el usuario", e);
        }
    }

    @Override
    public List<Usuario> listar() {
        String sql = """
                SELECT id_usuario, nombre, email, password_hash, rol, activo
                FROM usuario
                ORDER BY nombre
                """;
        try (Connection cn = conexiones.abrir();
             PreparedStatement ps = cn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            List<Usuario> usuarios = new ArrayList<>();
            while (rs.next()) {
                usuarios.add(mapear(rs));
            }
            return usuarios;
        } catch (SQLException e) {
            LOG.error("Error de base de datos al listar usuarios", e);
            throw new PersistenciaException("No se pudo listar los usuarios", e);
        }
    }

    @Override
    public void guardar(Usuario usuario) {
        try (Connection cn = conexiones.abrir()) {
            if (usuario.id() == 0) {
                insertar(cn, usuario);
            } else {
                actualizar(cn, usuario);
            }
        } catch (SQLException e) {
            if ("23505".equals(e.getSQLState())) {
                throw new ReglaNegocioException("Ya existe un usuario con ese correo");
            }
            LOG.error("Error de base de datos al guardar el usuario", e);
            throw new PersistenciaException("No se pudo guardar el usuario", e);
        }
    }

    private void insertar(Connection cn, Usuario usuario) throws SQLException {
        String sql = """
                INSERT INTO usuario (nombre, email, password_hash, rol, activo)
                VALUES (?, ?, ?, ?, ?)
                """;
        try (PreparedStatement ps = cn.prepareStatement(sql)) {
            llenar(ps, usuario);
            ps.executeUpdate();
        }
    }

    private void actualizar(Connection cn, Usuario usuario) throws SQLException {
        String sql = """
                UPDATE usuario
                SET nombre = ?, email = ?, password_hash = ?, rol = ?, activo = ?
                WHERE id_usuario = ?
                """;
        try (PreparedStatement ps = cn.prepareStatement(sql)) {
            llenar(ps, usuario);
            ps.setInt(6, usuario.id());
            ps.executeUpdate();
        }
    }

    private void llenar(PreparedStatement ps, Usuario usuario) throws SQLException {
        ps.setString(1, usuario.nombre());
        ps.setString(2, usuario.email());
        ps.setString(3, usuario.passwordHash());
        ps.setString(4, usuario.rol().name());
        ps.setBoolean(5, usuario.activo());
    }

    private Usuario mapear(ResultSet rs) throws SQLException {
        return new Usuario(
                rs.getInt("id_usuario"),
                rs.getString("nombre"),
                rs.getString("email"),
                rs.getString("password_hash"),
                Rol.desde(rs.getString("rol")),
                rs.getBoolean("activo")
        );
    }
}
