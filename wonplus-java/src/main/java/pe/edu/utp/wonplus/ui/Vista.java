package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import javax.swing.BorderFactory;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;

public abstract class Vista extends JPanel {
    protected Vista() {
        setLayout(new BorderLayout(0, 16));
        setBackground(Estilo.FONDO);
        setBorder(BorderFactory.createEmptyBorder(24, 24, 24, 24));
    }

    public void alMostrar() {
    }

    protected JPanel encabezado(String titulo, String subtitulo) {
        JPanel panel = new JPanel(new BorderLayout(0, 4));
        panel.setOpaque(false);
        JLabel tituloLabel = new JLabel(titulo);
        tituloLabel.setFont(Estilo.TITULO);
        tituloLabel.setForeground(Estilo.TEXTO);
        JLabel subtituloLabel = new JLabel(subtitulo);
        subtituloLabel.setFont(Estilo.SUBTITULO);
        subtituloLabel.setForeground(Estilo.SUAVE);
        panel.add(tituloLabel, BorderLayout.NORTH);
        panel.add(subtituloLabel, BorderLayout.SOUTH);
        return panel;
    }

    protected DefaultTableModel modelo(String... columnas) {
        return new DefaultTableModel(columnas, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
    }

    protected JPanel tarjeta(JComponent contenido) {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        panel.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(0xE8E0F0)),
                BorderFactory.createEmptyBorder(16, 16, 16, 16)
        ));
        panel.add(contenido, BorderLayout.CENTER);
        return panel;
    }

    protected JTable tabla(DefaultTableModel modelo) {
        JTable tabla = new JTable(modelo);
        tabla.setRowHeight(28);
        tabla.setFont(Estilo.TEXTO_NORMAL);
        tabla.getTableHeader().setFont(Estilo.BOTON);
        tabla.setSelectionBackground(new Color(0xE8E0F0));
        tabla.getTableHeader().setBackground(Estilo.ACENTO);
        tabla.getTableHeader().setForeground(Color.WHITE);
        tabla.getTableHeader().setOpaque(true);
        tabla.setFillsViewportHeight(true);
        return tabla;
    }
}
