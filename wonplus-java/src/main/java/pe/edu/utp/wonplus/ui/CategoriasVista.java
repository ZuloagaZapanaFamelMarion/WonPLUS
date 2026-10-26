package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.Categoria;

public final class CategoriasVista extends Vista {
    private final ControladorPrincipal controlador;
    private final DefaultTableModel modelo = modelo("Id", "Categoría");
    private final JTable tabla = tabla(modelo);
    private final JTextField nombre = new JTextField(18);
    private int editando;

    public CategoriasVista(ControladorPrincipal controlador) {
        this.controlador = controlador;
        add(encabezado("Categorías", "Agrupan los productos del inventario"), BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        JPanel acciones = new JPanel(new FlowLayout(FlowLayout.LEFT));
        acciones.setOpaque(false);
        var guardar = Estilo.primario("Guardar");
        var editar = Estilo.primario("Cargar selección");
        var eliminar = Estilo.primario("Eliminar");
        guardar.addActionListener(event -> guardar());
        editar.addActionListener(event -> cargar());
        eliminar.addActionListener(event -> eliminar());
        acciones.add(nombre);
        acciones.add(guardar);
        acciones.add(editar);
        acciones.add(eliminar);
        add(acciones, BorderLayout.SOUTH);
    }

    @Override
    public void alMostrar() {
        modelo.setRowCount(0);
        for (Categoria categoria : controlador.categorias()) {
            modelo.addRow(new Object[]{categoria.id(), categoria.nombre()});
        }
    }

    private void guardar() {
        try {
            controlador.guardarCategoria(editando, nombre.getText());
            editando = 0;
            nombre.setText("");
            alMostrar();
        } catch (RuntimeException e) {
            Mensajes.error(this, e);
        }
    }

    private void cargar() {
        int fila = tabla.getSelectedRow();
        if (fila < 0) {
            Mensajes.info(this, "Selecciona una categoría");
            return;
        }
        editando = (int) modelo.getValueAt(fila, 0);
        nombre.setText(String.valueOf(modelo.getValueAt(fila, 1)));
    }

    private void eliminar() {
        int fila = tabla.getSelectedRow();
        if (fila < 0) {
            Mensajes.info(this, "Selecciona una categoría");
            return;
        }
        try {
            controlador.eliminarCategoria((int) modelo.getValueAt(fila, 0));
            nombre.setText("");
            alMostrar();
        } catch (RuntimeException e) {
            Mensajes.error(this, e);
        }
    }
}
