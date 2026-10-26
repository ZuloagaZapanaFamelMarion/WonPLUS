package pe.edu.utp.wonplus.servicio;

import com.google.common.base.CharMatcher;
import com.google.common.base.Strings;
import java.math.BigDecimal;
import java.util.List;
import java.util.Locale;
import pe.edu.utp.wonplus.dao.ProductoDao;
import pe.edu.utp.wonplus.model.Producto;
import pe.edu.utp.wonplus.model.Usuario;
import pe.edu.utp.wonplus.seguridad.ValidadorEntrada;

public final class ProductoService {
    private final ProductoDao productos;
    private final AuthService auth;

    public ProductoService(ProductoDao productos, AuthService auth) {
        this.productos = productos;
        this.auth = auth;
    }

    public List<Producto> listar(Usuario sesion) {
        auth.exigirSesion(sesion);
        return productos.listar();
    }

    public List<Producto> buscar(Usuario sesion, String texto) {
        String termino = CharMatcher.whitespace()
                .trimFrom(Strings.nullToEmpty(texto))
                .toLowerCase(Locale.ROOT);
        return listar(sesion).stream()
                .filter(producto -> producto.nombre().toLowerCase(Locale.ROOT).contains(termino))
                .toList();
    }

    public List<Producto> stockBajo(Usuario sesion) {
        return listar(sesion).stream().filter(Producto::stockBajo).toList();
    }

    public void guardar(
            Usuario sesion,
            int id,
            String nombre,
            String precio,
            String costo,
            String stock,
            String stockMinimo,
            int idCategoria,
            String categoria
    ) {
        auth.exigirAdmin(sesion);
        String limpio = ValidadorEntrada.nombre(nombre, "el nombre del producto");
        BigDecimal precioValor = ValidadorEntrada.dinero(precio, "El precio");
        BigDecimal costoValor = ValidadorEntrada.dinero(costo, "El costo");
        int stockValor = ValidadorEntrada.enteroNoNegativo(stock, "El stock");
        int minimoValor = ValidadorEntrada.enteroNoNegativo(stockMinimo, "El stock mínimo");
        if (idCategoria <= 0) {
            throw new pe.edu.utp.wonplus.excepcion.ReglaNegocioException("Selecciona una categoría");
        }
        productos.guardar(new Producto(
                id,
                limpio,
                precioValor,
                costoValor,
                stockValor,
                minimoValor,
                idCategoria,
                categoria
        ));
    }
}
