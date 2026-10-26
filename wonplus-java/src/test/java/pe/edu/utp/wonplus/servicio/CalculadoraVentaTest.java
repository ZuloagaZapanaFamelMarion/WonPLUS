package pe.edu.utp.wonplus.servicio;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.Test;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.LineaPedido;
import pe.edu.utp.wonplus.model.Producto;

class CalculadoraVentaTest {
    private final CalculadoraVenta calculadora = new CalculadoraVenta();

    @Test
    void sumaElTotalYLaGananciaDeVariasLineas() {
        var calculo = calculadora.calcular(List.of(cafe(), cuaderno()), List.of(
                new LineaPedido(1, 2),
                new LineaPedido(2, 1)
        ));

        assertEquals(0, new BigDecimal("29.00").compareTo(calculo.total()));
        assertEquals(0, new BigDecimal("15.00").compareTo(calculo.ganancia()));
        assertEquals(1, calculo.lineas().get(0).stockResultante());
    }

    @Test
    void juntaCantidadesDelMismoProducto() {
        var calculo = calculadora.calcular(List.of(cafe()), List.of(
                new LineaPedido(1, 1),
                new LineaPedido(1, 1)
        ));

        assertEquals(1, calculo.lineas().size());
        assertEquals(2, calculo.lineas().get(0).cantidad());
        assertEquals(1, calculo.lineas().get(0).stockResultante());
    }

    @Test
    void rechazaLaVentaSiNoAlcanzaElStock() {
        ReglaNegocioException error = assertThrows(ReglaNegocioException.class, () ->
                calculadora.calcular(List.of(cafe()), List.of(new LineaPedido(1, 4)))
        );

        assertEquals("Stock insuficiente de Café premium", error.getMessage());
    }

    @Test
    void rechazaUnaVentaVacia() {
        assertThrows(IllegalArgumentException.class, () -> calculadora.calcular(List.of(cafe()), List.of()));
    }

    private Producto cafe() {
        return new Producto(1, "Café premium", new BigDecimal("8.50"), new BigDecimal("4.00"), 3, 5, 1, "Bebidas");
    }

    private Producto cuaderno() {
        return new Producto(2, "Cuaderno emprendedor", new BigDecimal("12.00"), new BigDecimal("6.00"), 14, 5, 2, "Papelería");
    }
}
