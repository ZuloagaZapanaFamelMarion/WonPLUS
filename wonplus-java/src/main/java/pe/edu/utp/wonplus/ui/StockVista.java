package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.Producto;

public final class StockVista extends Vista {
    private final ControladorPrincipal controlador;
    private final DefaultTableModel modelo = modelo("Producto", "Categoría", "Stock", "Mínimo", "Estado");
    private final JTable tabla = tabla(modelo);

    public StockVista(ControladorPrincipal controlador) {
        this.controlador = controlador;
        add(encabezado("Alertas de stock", "Productos que llegaron al mínimo y necesitan reposición"), BorderLayout.NORTH);
        tabla.setDefaultRenderer(Object.class, new DefaultTableCellRenderer() {
            @Override
            public Component getTableCellRendererComponent(JTable table, Object value, boolean selected, boolean focus, int row, int column) {
                Component celda = super.getTableCellRendererComponent(table, value, selected, focus, row, column);
                if (!selected) {
                    celda.setBackground(Estilo.PELIGRO);
                    celda.setForeground(new Color(0x7A1A14));
                }
                return celda;
            }
        });
        add(new JScrollPane(tabla), BorderLayout.CENTER);
    }

    @Override
    public void alMostrar() {
        modelo.setRowCount(0);
        for (Producto producto : controlador.stockBajo()) {
            modelo.addRow(new Object[]{
                    producto.nombre(),
                    producto.categoria(),
                    producto.stock(),
                    producto.stockMinimo(),
                    "Stock bajo"
            });
        }
    }
}
