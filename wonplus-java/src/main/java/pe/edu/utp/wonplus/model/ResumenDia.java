package pe.edu.utp.wonplus.model;

import java.math.BigDecimal;

public record ResumenDia(
        BigDecimal totalVentas,
        int operaciones,
        BigDecimal ganancia,
        int productosStockBajo
) {
}
