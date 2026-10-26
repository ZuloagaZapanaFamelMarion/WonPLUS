package pe.edu.utp.wonplus.model;

import java.math.BigDecimal;

public record LineaCalculada(
        int idProducto,
        String nombre,
        int cantidad,
        BigDecimal precioUnitario,
        BigDecimal costoUnitario,
        int stockResultante,
        BigDecimal subtotal
) {
}
