package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSpinner;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SpinnerNumberModel;
import javax.swing.table.DefaultTableModel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.LineaPedido;
import pe.edu.utp.wonplus.model.Producto;

public final class VentaVista extends Vista {
    private final ControladorPrincipal controlador;
    private final Navegacion navegacion;
    private final DefaultTableModel catalogo = modelo("Id", "Producto", "Precio", "Stock");
    private final DefaultTableModel carrito = modelo("Id", "Producto", "Cantidad", "Precio", "Subtotal");
    private final JTable tablaCatalogo = tabla(catalogo);
    private final JTable tablaCarrito = tabla(carrito);
    private final JTextField busqueda = new JTextField(16);
    private final JSpinner cantidad = new JSpinner(new SpinnerNumberModel(1, 1, 999, 1));
    private final JLabel total = new JLabel("Total: S/ 0.00");
    private final List<Producto> visibles = new ArrayList<>();

    public VentaVista(ControladorPrincipal controlador, Navegacion navegacion) {
        this.controlador = controlador;
        this.navegacion = navegacion;
        add(encabezado("Registrar venta", "El stock se descuenta al confirmar y queda guardado"), BorderLayout.NORTH);

        JPanel cuerpo = new JPanel(new java.awt.GridLayout(1, 2, 16, 0));
        cuerpo.setOpaque(false);
        JPanel izquierda = new JPanel(new BorderLayout(0, 8));
        izquierda.setOpaque(false);
        JPanel busca = new JPanel(new FlowLayout(FlowLayout.LEFT));
        busca.setOpaque(false);
        var filtrar = Estilo.primario("Buscar");
        filtrar.addActionListener(event -> cargarCatalogo());
        busca.add(busqueda);
        busca.add(filtrar);
        izquierda.add(busca, BorderLayout.NORTH);
        izquierda.add(new JScrollPane(tablaCatalogo), BorderLayout.CENTER);
        JPanel agregarFila = new JPanel(new FlowLayout(FlowLayout.LEFT));
        agregarFila.setOpaque(false);
        var agregar = Estilo.primario("Agregar");
        agregar.addActionListener(event -> agregar());
        agregarFila.add(new JLabel("Cantidad"));
        agregarFila.add(cantidad);
        agregarFila.add(agregar);
        izquierda.add(agregarFila, BorderLayout.SOUTH);

        JPanel derecha = new JPanel(new BorderLayout(0, 8));
        derecha.setOpaque(false);
        derecha.add(new JScrollPane(tablaCarrito), BorderLayout.CENTER);
        JPanel confirmar = new JPanel(new FlowLayout(FlowLayout.LEFT));
        confirmar.setOpaque(false);
        total.setFont(Estilo.BOTON);
        var cobrar = Estilo.primario("Confirmar venta");
        var quitar = Estilo.primario("Quitar");
        cobrar.addActionListener(event -> confirmar());
        quitar.addActionListener(event -> quitar());
        confirmar.add(total);
        confirmar.add(quitar);
        confirmar.add(cobrar);
        derecha.add(confirmar, BorderLayout.SOUTH);

        cuerpo.add(izquierda);
        cuerpo.add(derecha);
        add(cuerpo, BorderLayout.CENTER);
    }

    @Override
    public void alMostrar() {
        carrito.setRowCount(0);
        actualizarTotal();
        cargarCatalogo();
    }

    private void cargarCatalogo() {
        catalogo.setRowCount(0);
        visibles.clear();
        for (Producto producto : controlador.buscarProductos(busqueda.getText())) {
            visibles.add(producto);
            catalogo.addRow(new Object[]{
                    producto.id(),
                    producto.nombre(),
                    Formatos.dinero(producto.precio()),
                    producto.stock()
            });
        }
    }

    private void agregar() {
        int fila = tablaCatalogo.getSelectedRow();
        if (fila < 0) {
            Mensajes.info(this, "Selecciona un producto");
            return;
        }
        Producto producto = visibles.get(fila);
        int pedida = (int) cantidad.getValue();
        int ya = cantidadEnCarrito(producto.id());
        if (producto.stock() < ya + pedida) {
            Mensajes.info(this, "Stock insuficiente de " + producto.nombre());
            return;
        }
        if (ya == 0) {
            carrito.addRow(new Object[]{
                    producto.id(),
                    producto.nombre(),
                    pedida,
                    producto.precio(),
                    producto.precio().multiply(java.math.BigDecimal.valueOf(pedida))
            });
        } else {
            for (int i = 0; i < carrito.getRowCount(); i++) {
                if ((int) carrito.getValueAt(i, 0) == producto.id()) {
                    int nueva = (int) carrito.getValueAt(i, 2) + pedida;
                    carrito.setValueAt(nueva, i, 2);
                    carrito.setValueAt(producto.precio().multiply(java.math.BigDecimal.valueOf(nueva)), i, 4);
                }
            }
        }
        actualizarTotal();
    }

    private int cantidadEnCarrito(int idProducto) {
        for (int i = 0; i < carrito.getRowCount(); i++) {
            if ((int) carrito.getValueAt(i, 0) == idProducto) {
                return (int) carrito.getValueAt(i, 2);
            }
        }
        return 0;
    }

    private void quitar() {
        int fila = tablaCarrito.getSelectedRow();
        if (fila >= 0) {
            carrito.removeRow(fila);
            actualizarTotal();
        }
    }

    private void actualizarTotal() {
        java.math.BigDecimal suma = java.math.BigDecimal.ZERO;
        for (int i = 0; i < carrito.getRowCount(); i++) {
            suma = suma.add((java.math.BigDecimal) carrito.getValueAt(i, 4));
        }
        total.setText("Total: " + Formatos.dinero(suma));
    }

    private void confirmar() {
        if (carrito.getRowCount() == 0) {
            Mensajes.info(this, "Agrega al menos un producto");
            return;
        }
        List<LineaPedido> pedido = new ArrayList<>();
        for (int i = 0; i < carrito.getRowCount(); i++) {
            pedido.add(new LineaPedido((int) carrito.getValueAt(i, 0), (int) carrito.getValueAt(i, 2)));
        }
        try {
            controlador.registrarVenta(pedido);
            navegacion.ir("ticket");
        } catch (RuntimeException e) {
            Mensajes.error(this, e);
        }
    }
}
