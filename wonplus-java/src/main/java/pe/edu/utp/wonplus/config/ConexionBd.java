package pe.edu.utp.wonplus.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pe.edu.utp.wonplus.excepcion.PersistenciaException;

public final class ConexionBd {
    private static final Logger LOG = LoggerFactory.getLogger(ConexionBd.class);

    private final ConfiguracionBd configuracion;

    public ConexionBd(ConfiguracionBd configuracion) {
        this.configuracion = configuracion;
    }

    public Connection abrir() {
        try {
            return DriverManager.getConnection(
                    configuracion.url(),
                    configuracion.usuario(),
                    configuracion.clave()
            );
        } catch (SQLException e) {
            LOG.error("Error de base de datos al abrir la conexión", e);
            throw new PersistenciaException(
                    "No se pudo conectar a PostgreSQL. Revisa que el servicio esté activo y que exista la base wonplus.",
                    e
            );
        }
    }
}
