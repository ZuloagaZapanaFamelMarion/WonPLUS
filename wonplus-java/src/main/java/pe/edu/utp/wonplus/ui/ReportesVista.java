package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.nio.file.Path;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableModel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.Periodo;
import pe.edu.utp.wonplus.model.Venta;

public final class ReportesVista extends Vista {
    private final ControladorPrincipal controlador;
    private final JComboBox<Periodo> periodo = new JComboBox<>(Periodo.values());
    private final DefaultTableModel modelo = modelo("Id", "Fecha", "Vendedor", "Total", "Ganancia");

    public ReportesVista(ControladorPrincipal controlador) {
        this.controlador = controlador;
        add(encabezado("Reportes", "El Excel se genera con Apache POI"), BorderLayout.NORTH);
        add(new JScrollPane(tabla(modelo)), BorderLayout.CENTER);
        JPanel acciones = new JPanel(new FlowLayout(FlowLayout.LEFT));
        acciones.setOpaque(false);
        var consultar = Estilo.primario("Consultar");
        var exportar = Estilo.primario("Exportar Excel");
        consultar.addActionListener(event -> alMostrar());
        exportar.addActionListener(event -> exportar());
        acciones.add(periodo);
        acciones.add(consultar);
        acciones.add(exportar);
        add(acciones, BorderLayout.SOUTH);
    }

    @Override
    public void alMostrar() {
        modelo.setRowCount(0);
        for (Venta venta : controlador.reporte((Periodo) periodo.getSelectedItem())) {
            modelo.addRow(new Object[]{
                    venta.id(),
                    Formatos.fecha(venta.fecha()),
                    venta.vendedor(),
                    Formatos.dinero(venta.total()),
                    Formatos.dinero(venta.ganancia())
            });
        }
    }

    private void exportar() {
        JFileChooser selector = new JFileChooser();
        selector.setSelectedFile(new java.io.File("wonplus-ventas.xlsx"));
        selector.setFileFilter(new FileNameExtensionFilter("Excel", "xlsx"));
        if (selector.showSaveDialog(this) != JFileChooser.APPROVE_OPTION) {
            return;
        }
        try {
            Path archivo = controlador.exportar(
                    (Periodo) periodo.getSelectedItem(),
                    selector.getSelectedFile().toPath()
            );
            Mensajes.info(this, "Reporte guardado en " + archivo.toAbsolutePath());
        } catch (RuntimeException e) {
            Mensajes.error(this, e);
        }
    }
}
