package pe.edu.utp.wonplus.model;

import java.math.BigDecimal;
import java.util.List;

public record CalculoVenta(BigDecimal total, BigDecimal ganancia, List<LineaCalculada> lineas) {
}
