package pe.edu.utp.wonplus.controlador;

import java.nio.file.Path;
import java.util.List;
import pe.edu.utp.wonplus.Aplicacion;
import pe.edu.utp.wonplus.model.Categoria;
import pe.edu.utp.wonplus.model.LineaPedido;
import pe.edu.utp.wonplus.model.Periodo;
import pe.edu.utp.wonplus.model.Producto;
import pe.edu.utp.wonplus.model.ResumenDia;
import pe.edu.utp.wonplus.model.Rol;
import pe.edu.utp.wonplus.model.Usuario;
import pe.edu.utp.wonplus.model.Venta;

public final class ControladorPrincipal {
    private final Aplicacion aplicacion;
    private Usuario sesion;
    private Venta ultimaVenta;
    private int ventaSeleccionada;

    public ControladorPrincipal(Aplicacion aplicacion) {
        this.aplicacion = aplicacion;
    }

    public Usuario ingresar(String email, String clave) {
        sesion = aplicacion.auth.ingresar(email, clave);
        return sesion;
    }

    public void cerrarSesion() {
        sesion = null;
        ultimaVenta = null;
        ventaSeleccionada = 0;
    }

    public Usuario sesion() {
        return sesion;
    }

    public boolean esAdmin() {
        return sesion != null && sesion.rol() == Rol.ADMIN;
    }

    public ResumenDia resumen() {
        return aplicacion.ventas.resumen(sesion);
    }

    public List<Producto> productos() {
        return aplicacion.productos.listar(sesion);
    }

    public List<Producto> buscarProductos(String texto) {
        return aplicacion.productos.buscar(sesion, texto);
    }

    public List<Producto> stockBajo() {
        return aplicacion.productos.stockBajo(sesion);
    }

    public void guardarProducto(
            int id,
            String nombre,
            String precio,
            String costo,
            String stock,
            String minimo,
            int idCategoria,
            String categoria
    ) {
        aplicacion.productos.guardar(sesion, id, nombre, precio, costo, stock, minimo, idCategoria, categoria);
    }

    public List<Categoria> categorias() {
        return aplicacion.categorias.listar(sesion);
    }

    public void guardarCategoria(int id, String nombre) {
        aplicacion.categorias.guardar(sesion, id, nombre);
    }

    public void eliminarCategoria(int id) {
        aplicacion.categorias.eliminar(sesion, id);
    }

    public List<Usuario> usuarios() {
        return aplicacion.usuarios.listar(sesion);
    }

    public void guardarUsuario(int id, String nombre, String email, String clave, Rol rol, boolean activo) {
        aplicacion.usuarios.guardar(sesion, id, nombre, email, clave, rol, activo);
    }

    public Venta registrarVenta(List<LineaPedido> pedido) {
        ultimaVenta = aplicacion.ventas.registrar(sesion, pedido);
        return ultimaVenta;
    }

    public Venta ultimaVenta() {
        return ultimaVenta;
    }

    public List<Venta> historial(Periodo periodo) {
        return aplicacion.ventas.historial(sesion, periodo);
    }

    public void seleccionarVenta(int id) {
        ventaSeleccionada = id;
    }

    public Venta detalleSeleccionado() {
        return aplicacion.ventas.detalle(sesion, ventaSeleccionada);
    }

    public List<Venta> reporte(Periodo periodo) {
        return aplicacion.reportes.consultar(sesion, periodo);
    }

    public Path exportar(Periodo periodo, Path destino) {
        return aplicacion.reportes.exportar(sesion, periodo, destino);
    }
}
