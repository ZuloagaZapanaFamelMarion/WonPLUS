package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import javax.swing.JComboBox;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.Periodo;
import pe.edu.utp.wonplus.model.Venta;

public final class HistorialVista extends Vista {
    private final ControladorPrincipal controlador;
    private final Navegacion navegacion;
    private final JComboBox<Periodo> periodo = new JComboBox<>(Periodo.values());
    private final DefaultTableModel modelo = modelo("Id", "Fecha", "Vendedor", "Total", "Ganancia");
    private final JTable tabla = tabla(modelo);

    public HistorialVista(ControladorPrincipal controlador, Navegacion navegacion) {
        this.controlador = controlador;
        this.navegacion = navegacion;
        add(encabezado("Historial de ventas", "Consulta las operaciones guardadas por periodo"), BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        JPanel acciones = new JPanel(new FlowLayout(FlowLayout.LEFT));
        acciones.setOpaque(false);
        var consultar = Estilo.primario("Consultar");
        var detalle = Estilo.primario("Ver detalle");
        consultar.addActionListener(event -> alMostrar());
        detalle.addActionListener(event -> abrirDetalle());
        acciones.add(periodo);
        acciones.add(consultar);
        acciones.add(detalle);
        add(acciones, BorderLayout.SOUTH);
    }

    @Override
    public void alMostrar() {
        modelo.setRowCount(0);
        for (Venta venta : controlador.historial((Periodo) periodo.getSelectedItem())) {
            modelo.addRow(new Object[]{
                    venta.id(),
                    Formatos.fecha(venta.fecha()),
                    venta.vendedor(),
                    Formatos.dinero(venta.total()),
                    Formatos.dinero(venta.ganancia())
            });
        }
    }

    private void abrirDetalle() {
        int fila = tabla.getSelectedRow();
        if (fila < 0) {
            Mensajes.info(this, "Selecciona una venta");
            return;
        }
        controlador.seleccionarVenta((int) modelo.getValueAt(fila, 0));
        navegacion.ir("detalle");
    }
}
