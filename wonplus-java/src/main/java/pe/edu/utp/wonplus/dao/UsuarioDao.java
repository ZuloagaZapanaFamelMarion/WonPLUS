package pe.edu.utp.wonplus.dao;

import java.util.List;
import java.util.Optional;
import pe.edu.utp.wonplus.model.Usuario;

public interface UsuarioDao {
    Optional<Usuario> buscarPorEmail(String email);

    List<Usuario> listar();

    void guardar(Usuario usuario);
}
