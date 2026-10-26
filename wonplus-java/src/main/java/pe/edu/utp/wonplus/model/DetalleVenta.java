package pe.edu.utp.wonplus.model;

import java.math.BigDecimal;

public record DetalleVenta(
        int id,
        int idProducto,
        String nombreProducto,
        int cantidad,
        BigDecimal precioUnitario,
        BigDecimal costoUnitario
) {
    public BigDecimal subtotal() {
        return precioUnitario.multiply(BigDecimal.valueOf(cantidad));
    }
}
