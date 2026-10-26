package pe.edu.utp.wonplus.servicio;

import java.util.List;
import org.apache.commons.lang3.StringUtils;
import pe.edu.utp.wonplus.dao.UsuarioDao;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.Rol;
import pe.edu.utp.wonplus.model.Usuario;
import pe.edu.utp.wonplus.seguridad.CifradorClave;
import pe.edu.utp.wonplus.seguridad.ValidadorEntrada;

public final class UsuarioService {
    private final UsuarioDao usuarios;
    private final AuthService auth;

    public UsuarioService(UsuarioDao usuarios, AuthService auth) {
        this.usuarios = usuarios;
        this.auth = auth;
    }

    public List<Usuario> listar(Usuario sesion) {
        auth.exigirAdmin(sesion);
        return usuarios.listar();
    }

    public void guardar(Usuario sesion, int id, String nombre, String email, String clave, Rol rol, boolean activo) {
        auth.exigirAdmin(sesion);
        String nombreLimpio = ValidadorEntrada.nombre(nombre, "el nombre");
        String correo = ValidadorEntrada.correo(email);
        if (rol == null) {
            throw new ReglaNegocioException("Selecciona un rol");
        }
        String hash;
        if (id == 0 || !StringUtils.isBlank(clave)) {
            ValidadorEntrada.clave(clave);
            hash = CifradorClave.cifrar(clave);
        } else {
            hash = usuarios.listar().stream()
                    .filter(usuario -> usuario.id() == id)
                    .map(Usuario::passwordHash)
                    .findFirst()
                    .orElseThrow(() -> new ReglaNegocioException("El usuario no existe"));
        }
        usuarios.guardar(new Usuario(id, nombreLimpio, correo, hash, rol, activo));
    }
}
