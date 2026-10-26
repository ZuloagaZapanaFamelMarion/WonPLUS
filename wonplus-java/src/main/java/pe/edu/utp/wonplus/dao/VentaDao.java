package pe.edu.utp.wonplus.dao;

import java.time.LocalDateTime;
import java.util.List;
import pe.edu.utp.wonplus.model.CalculoVenta;
import pe.edu.utp.wonplus.model.TotalesPeriodo;
import pe.edu.utp.wonplus.model.Venta;

public interface VentaDao {
    Venta registrar(int idUsuario, CalculoVenta calculo);

    TotalesPeriodo totales(LocalDateTime desde, LocalDateTime hasta);

    List<Venta> listar(LocalDateTime desde, LocalDateTime hasta);

    Venta buscar(int id);
}
