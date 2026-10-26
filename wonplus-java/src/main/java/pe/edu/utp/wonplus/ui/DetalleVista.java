package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.table.DefaultTableModel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.DetalleVenta;
import pe.edu.utp.wonplus.model.Venta;

public final class DetalleVista extends Vista {
    private final ControladorPrincipal controlador;
    private final DefaultTableModel modelo = modelo("Producto", "Cantidad", "Precio", "Subtotal");
    private final JLabel resumen = new JLabel(" ");

    public DetalleVista(ControladorPrincipal controlador, Navegacion navegacion) {
        this.controlador = controlador;
        add(encabezado("Detalle de venta", "Productos, cantidades y montos de la operación"), BorderLayout.NORTH);
        add(new JScrollPane(tabla(modelo)), BorderLayout.CENTER);
        JPanel sur = new JPanel(new FlowLayout(FlowLayout.LEFT));
        sur.setOpaque(false);
        var volver = Estilo.primario("Volver al historial");
        volver.addActionListener(event -> navegacion.ir("historial"));
        sur.add(resumen);
        sur.add(volver);
        add(sur, BorderLayout.SOUTH);
    }

    @Override
    public void alMostrar() {
        modelo.setRowCount(0);
        try {
            Venta venta = controlador.detalleSeleccionado();
            resumen.setText(Formatos.fecha(venta.fecha()) + "  ·  " + venta.vendedor()
                    + "  ·  Total " + Formatos.dinero(venta.total()));
            for (DetalleVenta detalle : venta.detalles()) {
                modelo.addRow(new Object[]{
                        detalle.nombreProducto(),
                        detalle.cantidad(),
                        Formatos.dinero(detalle.precioUnitario()),
                        Formatos.dinero(detalle.subtotal())
                });
            }
        } catch (RuntimeException e) {
            resumen.setText(e.getMessage());
        }
    }
}
