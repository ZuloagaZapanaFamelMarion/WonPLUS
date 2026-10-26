package pe.edu.utp.wonplus.servicio;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pe.edu.utp.wonplus.dao.UsuarioDao;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.Rol;
import pe.edu.utp.wonplus.model.Usuario;
import pe.edu.utp.wonplus.seguridad.CifradorClave;
import pe.edu.utp.wonplus.seguridad.ValidadorEntrada;

public final class AuthService {
    private static final Logger LOG = LoggerFactory.getLogger(AuthService.class);
    private final UsuarioDao usuarios;

    public AuthService(UsuarioDao usuarios) {
        this.usuarios = usuarios;
    }

    public Usuario ingresar(String email, String clave) {
        String correo;
        try {
            correo = ValidadorEntrada.correo(email);
            ValidadorEntrada.clave(clave);
        } catch (ReglaNegocioException e) {
            LOG.warn("LOGIN rechazo: {}", e.getMessage());
            throw e;
        }

        Usuario usuario = usuarios.buscarPorEmail(correo).orElse(null);
        if (usuario == null || !usuario.activo() || !CifradorClave.coincide(clave, usuario.passwordHash())) {
            LOG.warn("LOGIN rechazo: credenciales inválidas para {}", correo);
            throw new ReglaNegocioException("Correo o contraseña incorrectos");
        }
        LOG.info("LOGIN resultado: ingreso aceptado usuario={}", usuario.email());
        return usuario;
    }

    public void exigirSesion(Usuario sesion) {
        if (sesion == null) {
            throw new ReglaNegocioException("Inicia sesión para continuar");
        }
    }

    public void exigirAdmin(Usuario sesion) {
        exigirSesion(sesion);
        if (sesion.rol() != Rol.ADMIN) {
            throw new ReglaNegocioException("Solo el administrador puede realizar esta acción");
        }
    }
}
