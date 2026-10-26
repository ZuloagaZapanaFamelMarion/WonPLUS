package pe.edu.utp.wonplus.model;

import java.math.BigDecimal;

public record Producto(
        int id,
        String nombre,
        BigDecimal precio,
        BigDecimal costo,
        int stock,
        int stockMinimo,
        int idCategoria,
        String categoria
) {
    public boolean stockBajo() {
        return stock <= stockMinimo;
    }
}
