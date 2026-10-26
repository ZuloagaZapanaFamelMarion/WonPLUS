package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.Categoria;
import pe.edu.utp.wonplus.model.Producto;

public final class ProductosVista extends Vista {
    private final ControladorPrincipal controlador;
    private final DefaultTableModel modelo = modelo("Id", "Producto", "Categoría", "Precio", "Costo", "Stock", "Mínimo", "Estado");
    private final JTable tabla = tabla(modelo);

    public ProductosVista(ControladorPrincipal controlador) {
        this.controlador = controlador;
        add(encabezado("Productos", "Alta y edición de productos. El stock bajo se marca en rojo"), BorderLayout.NORTH);
        tabla.setDefaultRenderer(Object.class, new DefaultTableCellRenderer() {
            @Override
            public Component getTableCellRendererComponent(JTable table, Object value, boolean selected, boolean focus, int row, int column) {
                Component celda = super.getTableCellRendererComponent(table, value, selected, focus, row, column);
                String estado = String.valueOf(table.getModel().getValueAt(row, 7));
                if (!selected && "Stock bajo".equals(estado)) {
                    celda.setBackground(Estilo.PELIGRO);
                } else if (!selected) {
                    celda.setBackground(Color.WHITE);
                }
                return celda;
            }
        });
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        JPanel acciones = new JPanel(new FlowLayout(FlowLayout.LEFT));
        acciones.setOpaque(false);
        var nuevo = Estilo.primario("Nuevo producto");
        var editar = Estilo.primario("Editar");
        nuevo.addActionListener(event -> abrir(null));
        editar.addActionListener(event -> editarSeleccion());
        acciones.add(nuevo);
        acciones.add(editar);
        add(acciones, BorderLayout.SOUTH);
    }

    @Override
    public void alMostrar() {
        modelo.setRowCount(0);
        for (Producto producto : controlador.productos()) {
            modelo.addRow(fila(producto));
        }
    }

    private Object[] fila(Producto producto) {
        return new Object[]{
                producto.id(),
                producto.nombre(),
                producto.categoria(),
                Formatos.dinero(producto.precio()),
                Formatos.dinero(producto.costo()),
                producto.stock(),
                producto.stockMinimo(),
                producto.stockBajo() ? "Stock bajo" : "Disponible"
        };
    }

    private void editarSeleccion() {
        int fila = tabla.getSelectedRow();
        if (fila < 0) {
            Mensajes.info(this, "Selecciona un producto");
            return;
        }
        int id = (int) modelo.getValueAt(fila, 0);
        Producto producto = controlador.productos().stream().filter(item -> item.id() == id).findFirst().orElseThrow();
        abrir(producto);
    }

    private void abrir(Producto producto) {
        JDialog dialogo = new JDialog(javax.swing.SwingUtilities.getWindowAncestor(this),
                producto == null ? "Nuevo producto" : "Editar producto");
        JTextField nombre = new JTextField(producto == null ? "" : producto.nombre(), 18);
        JTextField precio = new JTextField(producto == null ? "" : producto.precio().toPlainString(), 18);
        JTextField costo = new JTextField(producto == null ? "" : producto.costo().toPlainString(), 18);
        JTextField stock = new JTextField(producto == null ? "" : String.valueOf(producto.stock()), 18);
        JTextField minimo = new JTextField(producto == null ? "5" : String.valueOf(producto.stockMinimo()), 18);
        JComboBox<Categoria> categorias = new JComboBox<>();
        for (Categoria categoria : controlador.categorias()) {
            categorias.addItem(categoria);
        }
        categorias.setRenderer((list, value, index, selected, focus) -> new JLabel(value == null ? "" : value.nombre()));
        if (producto != null) {
            for (int i = 0; i < categorias.getItemCount(); i++) {
                if (categorias.getItemAt(i).id() == producto.idCategoria()) {
                    categorias.setSelectedIndex(i);
                }
            }
        }
        JPanel form = new JPanel(new GridLayout(0, 1, 6, 6));
        form.setBorder(javax.swing.BorderFactory.createEmptyBorder(16, 16, 16, 16));
        form.add(new JLabel("Nombre"));
        form.add(nombre);
        form.add(new JLabel("Categoría"));
        form.add(categorias);
        form.add(new JLabel("Precio"));
        form.add(precio);
        form.add(new JLabel("Costo"));
        form.add(costo);
        form.add(new JLabel("Stock"));
        form.add(stock);
        form.add(new JLabel("Stock mínimo"));
        form.add(minimo);
        var guardar = Estilo.primario("Guardar");
        guardar.addActionListener(event -> {
            Categoria categoria = (Categoria) categorias.getSelectedItem();
            try {
                controlador.guardarProducto(
                        producto == null ? 0 : producto.id(),
                        nombre.getText(),
                        precio.getText(),
                        costo.getText(),
                        stock.getText(),
                        minimo.getText(),
                        categoria == null ? 0 : categoria.id(),
                        categoria == null ? "" : categoria.nombre()
                );
                dialogo.dispose();
                alMostrar();
            } catch (RuntimeException e) {
                Mensajes.error(dialogo, e);
            }
        });
        form.add(guardar);
        dialogo.setContentPane(form);
        dialogo.pack();
        dialogo.setLocationRelativeTo(this);
        dialogo.setModal(true);
        dialogo.setVisible(true);
    }
}
