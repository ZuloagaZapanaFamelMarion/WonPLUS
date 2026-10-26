package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableModel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.Rol;
import pe.edu.utp.wonplus.model.Usuario;

public final class UsuariosVista extends Vista {
    private final ControladorPrincipal controlador;
    private final DefaultTableModel modelo = modelo("Id", "Nombre", "Correo", "Rol", "Activo");
    private final JTable tabla = tabla(modelo);

    public UsuariosVista(ControladorPrincipal controlador) {
        this.controlador = controlador;
        add(encabezado("Usuarios", "El administrador crea cuentas y asigna el rol"), BorderLayout.NORTH);
        add(new JScrollPane(tabla), BorderLayout.CENTER);
        JPanel acciones = new JPanel(new FlowLayout(FlowLayout.LEFT));
        acciones.setOpaque(false);
        var nuevo = Estilo.primario("Nuevo usuario");
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
        for (Usuario usuario : controlador.usuarios()) {
            modelo.addRow(new Object[]{
                    usuario.id(),
                    usuario.nombre(),
                    usuario.email(),
                    usuario.rol().etiqueta(),
                    usuario.activo() ? "Sí" : "No"
            });
        }
    }

    private void editarSeleccion() {
        int fila = tabla.getSelectedRow();
        if (fila < 0) {
            Mensajes.info(this, "Selecciona un usuario");
            return;
        }
        int id = (int) modelo.getValueAt(fila, 0);
        Usuario usuario = controlador.usuarios().stream()
                .filter(item -> item.id() == id)
                .findFirst()
                .orElseThrow();
        abrir(usuario);
    }

    private void abrir(Usuario usuario) {
        JDialog dialogo = new JDialog(javax.swing.SwingUtilities.getWindowAncestor(this),
                usuario == null ? "Nuevo usuario" : "Editar usuario");
        JTextField nombre = new JTextField(usuario == null ? "" : usuario.nombre(), 20);
        JTextField email = new JTextField(usuario == null ? "" : usuario.email(), 20);
        JPasswordField clave = new JPasswordField(20);
        JComboBox<Rol> rol = new JComboBox<>(Rol.values());
        JCheckBox activo = new JCheckBox("Cuenta activa", usuario == null || usuario.activo());
        if (usuario != null) {
            rol.setSelectedItem(usuario.rol());
        }
        JPanel form = new JPanel(new GridLayout(0, 1, 6, 6));
        form.setBorder(javax.swing.BorderFactory.createEmptyBorder(16, 16, 16, 16));
        form.add(new JLabel("Nombre"));
        form.add(nombre);
        form.add(new JLabel("Correo"));
        form.add(email);
        form.add(new JLabel(usuario == null ? "Contraseña" : "Contraseña nueva (vacío = conservar)"));
        form.add(clave);
        form.add(new JLabel("Rol"));
        form.add(rol);
        form.add(activo);
        var guardar = Estilo.primario("Guardar");
        guardar.addActionListener(event -> {
            try {
                controlador.guardarUsuario(
                        usuario == null ? 0 : usuario.id(),
                        nombre.getText(),
                        email.getText(),
                        new String(clave.getPassword()),
                        (Rol) rol.getSelectedItem(),
                        activo.isSelected()
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
