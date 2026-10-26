package pe.edu.utp.wonplus.dao;

import java.util.List;
import pe.edu.utp.wonplus.model.Categoria;

public interface CategoriaDao {
    List<Categoria> listar();

    void guardar(Categoria categoria);

    void eliminar(int id);
}
