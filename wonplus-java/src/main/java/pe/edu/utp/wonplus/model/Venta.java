package pe.edu.utp.wonplus.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

public record Venta(
        int id,
        LocalDateTime fecha,
        BigDecimal total,
        BigDecimal ganancia,
        int idUsuario,
        String vendedor,
        List<DetalleVenta> detalles
) {
}
