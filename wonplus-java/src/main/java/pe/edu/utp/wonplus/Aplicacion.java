package pe.edu.utp.wonplus;

import pe.edu.utp.wonplus.config.ConexionBd;
import pe.edu.utp.wonplus.config.ConfiguracionBd;
import pe.edu.utp.wonplus.config.InicializadorBd;
import pe.edu.utp.wonplus.dao.jdbc.CategoriaJdbcDao;
import pe.edu.utp.wonplus.dao.jdbc.ProductoJdbcDao;
import pe.edu.utp.wonplus.dao.jdbc.UsuarioJdbcDao;
import pe.edu.utp.wonplus.dao.jdbc.VentaJdbcDao;
import pe.edu.utp.wonplus.reporte.ExportadorExcel;
import pe.edu.utp.wonplus.servicio.AuthService;
import pe.edu.utp.wonplus.servicio.CalculadoraVenta;
import pe.edu.utp.wonplus.servicio.CategoriaService;
import pe.edu.utp.wonplus.servicio.PeriodoConsulta;
import pe.edu.utp.wonplus.servicio.ProductoService;
import pe.edu.utp.wonplus.servicio.ReporteService;
import pe.edu.utp.wonplus.servicio.UsuarioService;
import pe.edu.utp.wonplus.servicio.VentaService;

public final class Aplicacion {
    public final AuthService auth;
    public final UsuarioService usuarios;
    public final CategoriaService categorias;
    public final ProductoService productos;
    public final VentaService ventas;
    public final ReporteService reportes;

    private Aplicacion(
            AuthService auth,
            UsuarioService usuarios,
            CategoriaService categorias,
            ProductoService productos,
            VentaService ventas,
            ReporteService reportes
    ) {
        this.auth = auth;
        this.usuarios = usuarios;
        this.categorias = categorias;
        this.productos = productos;
        this.ventas = ventas;
        this.reportes = reportes;
    }

    public static Aplicacion iniciar() {
        ConexionBd conexiones = new ConexionBd(ConfiguracionBd.cargar());
        new InicializadorBd(conexiones).preparar();
        AuthService auth = new AuthService(new UsuarioJdbcDao(conexiones));
        VentaService ventas = new VentaService(
                new ProductoJdbcDao(conexiones),
                new VentaJdbcDao(conexiones),
                new CalculadoraVenta(),
                PeriodoConsulta.lima(),
                auth
        );
        return new Aplicacion(
                auth,
                new UsuarioService(new UsuarioJdbcDao(conexiones), auth),
                new CategoriaService(new CategoriaJdbcDao(conexiones), auth),
                new ProductoService(new ProductoJdbcDao(conexiones), auth),
                ventas,
                new ReporteService(ventas, new ExportadorExcel())
        );
    }
}
