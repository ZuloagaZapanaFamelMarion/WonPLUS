package pe.edu.utp.wonplus.dao;

import java.util.List;
import pe.edu.utp.wonplus.model.Producto;

public interface ProductoDao {
    List<Producto> listar();

    void guardar(Producto producto);

    int contarStockBajo();
}
