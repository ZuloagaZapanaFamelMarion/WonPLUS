package pe.edu.utp.wonplus.servicio;

import com.google.common.base.Preconditions;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pe.edu.utp.wonplus.dao.ProductoDao;
import pe.edu.utp.wonplus.dao.VentaDao;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.CalculoVenta;
import pe.edu.utp.wonplus.model.LineaPedido;
import pe.edu.utp.wonplus.model.Periodo;
import pe.edu.utp.wonplus.model.RangoFechas;
import pe.edu.utp.wonplus.model.ResumenDia;
import pe.edu.utp.wonplus.model.TotalesPeriodo;
import pe.edu.utp.wonplus.model.Usuario;
import pe.edu.utp.wonplus.model.Venta;

public final class VentaService {
    private static final Logger LOG = LoggerFactory.getLogger(VentaService.class);
    private final ProductoDao productos;
    private final VentaDao ventas;
    private final CalculadoraVenta calculadora;
    private final PeriodoConsulta periodos;
    private final AuthService auth;

    public VentaService(
            ProductoDao productos,
            VentaDao ventas,
            CalculadoraVenta calculadora,
            PeriodoConsulta periodos,
            AuthService auth
    ) {
        this.productos = productos;
        this.ventas = ventas;
        this.calculadora = calculadora;
        this.periodos = periodos;
        this.auth = auth;
    }

    public ResumenDia resumen(Usuario sesion) {
        auth.exigirSesion(sesion);
        RangoFechas hoy = periodos.rango(Periodo.HOY);
        TotalesPeriodo totales = ventas.totales(hoy.desde(), hoy.hasta());
        return new ResumenDia(
                totales.total(),
                totales.operaciones(),
                totales.ganancia(),
                productos.contarStockBajo()
        );
    }

    public Venta registrar(Usuario sesion, List<LineaPedido> pedido) {
        auth.exigirSesion(sesion);
        try {
            Preconditions.checkArgument(pedido != null && !pedido.isEmpty(), "Agrega al menos un producto");
            CalculoVenta calculo = calculadora.calcular(productos.listar(), pedido);
            Venta venta = ventas.registrar(sesion.id(), calculo);
            LOG.info("VENTA registrada id={} total={} usuario={}", venta.id(), venta.total(), sesion.email());
            return venta;
        } catch (ReglaNegocioException | IllegalArgumentException e) {
            LOG.warn("VENTA rechazada: {}", e.getMessage());
            if (e instanceof ReglaNegocioException regla) {
                throw regla;
            }
            throw new ReglaNegocioException(e.getMessage());
        }
    }

    public List<Venta> historial(Usuario sesion, Periodo periodo) {
        auth.exigirSesion(sesion);
        RangoFechas rango = periodos.rango(periodo);
        return ventas.listar(rango.desde(), rango.hasta());
    }

    public Venta detalle(Usuario sesion, int id) {
        auth.exigirSesion(sesion);
        return ventas.buscar(id);
    }
}
