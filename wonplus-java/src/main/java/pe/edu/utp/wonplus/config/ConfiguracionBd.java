package pe.edu.utp.wonplus.config;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

public final class ConfiguracionBd {
    private final String url;
    private final String usuario;
    private final String clave;

    private ConfiguracionBd(String url, String usuario, String clave) {
        this.url = url;
        this.usuario = usuario;
        this.clave = clave;
    }

    public static ConfiguracionBd cargar() {
        Properties propiedades = new Properties();
        Path externo = Path.of("db.properties");
        try {
            if (Files.exists(externo)) {
                try (InputStream entrada = Files.newInputStream(externo)) {
                    propiedades.load(entrada);
                }
            } else {
                try (InputStream entrada = ConfiguracionBd.class.getResourceAsStream("/db.properties")) {
                    if (entrada == null) {
                        throw new IllegalStateException("No se encontró db.properties");
                    }
                    propiedades.load(entrada);
                }
            }
        } catch (IOException e) {
            throw new IllegalStateException("No se pudo leer la configuración de la base de datos", e);
        }

        String url = System.getenv().getOrDefault("WONPLUS_JDBC_URL", propiedades.getProperty("jdbc.url"));
        String usuario = System.getenv().getOrDefault("WONPLUS_JDBC_USER", propiedades.getProperty("jdbc.user"));
        String clave = System.getenv().getOrDefault("WONPLUS_JDBC_PASSWORD", propiedades.getProperty("jdbc.password", ""));
        return new ConfiguracionBd(url, usuario, clave);
    }

    public String url() {
        return url;
    }

    public String usuario() {
        return usuario;
    }

    public String clave() {
        return clave;
    }
}
