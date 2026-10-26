package pe.edu.utp.wonplus.servicio;

import java.util.List;
import pe.edu.utp.wonplus.dao.CategoriaDao;
import pe.edu.utp.wonplus.model.Categoria;
import pe.edu.utp.wonplus.model.Usuario;
import pe.edu.utp.wonplus.seguridad.ValidadorEntrada;

public final class CategoriaService {
    private final CategoriaDao categorias;
    private final AuthService auth;

    public CategoriaService(CategoriaDao categorias, AuthService auth) {
        this.categorias = categorias;
        this.auth = auth;
    }

    public List<Categoria> listar(Usuario sesion) {
        auth.exigirSesion(sesion);
        return categorias.listar();
    }

    public void guardar(Usuario sesion, int id, String nombre) {
        auth.exigirAdmin(sesion);
        String limpio = ValidadorEntrada.nombre(nombre, "el nombre de la categoría");
        categorias.guardar(new Categoria(id, limpio));
    }

    public void eliminar(Usuario sesion, int id) {
        auth.exigirAdmin(sesion);
        categorias.eliminar(id);
    }
}
