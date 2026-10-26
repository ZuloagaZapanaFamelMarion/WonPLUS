package pe.edu.utp.wonplus.servicio;

import com.google.common.base.Preconditions;
import com.google.common.collect.ImmutableList;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.CalculoVenta;
import pe.edu.utp.wonplus.model.LineaCalculada;
import pe.edu.utp.wonplus.model.LineaPedido;
import pe.edu.utp.wonplus.model.Producto;

public final class CalculadoraVenta {
    public CalculoVenta calcular(List<Producto> catalogo, List<LineaPedido> pedido) {
        Preconditions.checkNotNull(catalogo, "El catálogo es obligatorio");
        Preconditions.checkArgument(pedido != null && !pedido.isEmpty(), "Agrega al menos un producto");

        Map<Integer, Producto> porId = new LinkedHashMap<>();
        for (Producto producto : catalogo) {
            porId.put(producto.id(), producto);
        }

        Map<Integer, Integer> cantidades = new LinkedHashMap<>();
        for (LineaPedido linea : pedido) {
            if (linea.cantidad() <= 0) {
                throw new ReglaNegocioException("La cantidad debe ser mayor que cero");
            }
            cantidades.merge(linea.idProducto(), linea.cantidad(), Integer::sum);
        }

        ImmutableList.Builder<LineaCalculada> lineas = ImmutableList.builder();
        BigDecimal total = BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
        BigDecimal ganancia = BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);

        for (Map.Entry<Integer, Integer> entrada : cantidades.entrySet()) {
            Producto producto = porId.get(entrada.getKey());
            if (producto == null) {
                throw new ReglaNegocioException("Hay un producto que ya no existe");
            }
            int cantidad = entrada.getValue();
            if (producto.stock() < cantidad) {
                throw new ReglaNegocioException("Stock insuficiente de " + producto.nombre());
            }
            BigDecimal subtotal = producto.precio()
                    .multiply(BigDecimal.valueOf(cantidad))
                    .setScale(2, RoundingMode.HALF_UP);
            BigDecimal margen = producto.precio()
                    .subtract(producto.costo())
                    .multiply(BigDecimal.valueOf(cantidad))
                    .setScale(2, RoundingMode.HALF_UP);
            total = total.add(subtotal);
            ganancia = ganancia.add(margen);
            lineas.add(new LineaCalculada(
                    producto.id(),
                    producto.nombre(),
                    cantidad,
                    producto.precio(),
                    producto.costo(),
                    producto.stock() - cantidad,
                    subtotal
            ));
        }
        return new CalculoVenta(total, ganancia, lineas.build());
    }
}
