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

public final class TicketVista extends Vista {
    private final ControladorPrincipal controlador;
    private final DefaultTableModel modelo = modelo("Producto", "Cantidad", "Precio", "Subtotal");
    private final JLabel resumen = new JLabel(" ");

    public TicketVista(ControladorPrincipal controlador, Navegacion navegacion) {
        this.controlador = controlador;
        add(encabezado("Venta cobrada", "Comprobante de la operación que acaba de registrarse"), BorderLayout.NORTH);
        add(new JScrollPane(tabla(modelo)), BorderLayout.CENTER);
        JPanel sur = new JPanel(new FlowLayout(FlowLayout.LEFT));
        sur.setOpaque(false);
        resumen.setFont(Estilo.BOTON);
        var volver = Estilo.primario("Volver al panel");
        volver.addActionListener(event -> navegacion.ir("panel"));
        sur.add(resumen);
        sur.add(volver);
        add(sur, BorderLayout.SOUTH);
    }

    @Override
    public void alMostrar() {
        modelo.setRowCount(0);
        Venta venta = controlador.ultimaVenta();
        if (venta == null) {
            resumen.setText("No hay una venta reciente");
            return;
        }
        for (DetalleVenta detalle : venta.detalles()) {
            modelo.addRow(new Object[]{
                    detalle.nombreProducto(),
                    detalle.cantidad(),
                    Formatos.dinero(detalle.precioUnitario()),
                    Formatos.dinero(detalle.subtotal())
            });
        }
        resumen.setText("Venta " + venta.id() + "  ·  Total " + Formatos.dinero(venta.total())
                + "  ·  Ganancia " + Formatos.dinero(venta.ganancia()));
    }
}
