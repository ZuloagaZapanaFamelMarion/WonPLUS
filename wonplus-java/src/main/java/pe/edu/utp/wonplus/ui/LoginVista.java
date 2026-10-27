package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;

public final class LoginVista extends Vista {
    private final ControladorPrincipal controlador;
    private final Navegacion navegacion;
    private final JTextField email = new JTextField(22);
    private final JPasswordField clave = new JPasswordField(22);
    private final JLabel aviso = new JLabel(" ");

    public LoginVista(ControladorPrincipal controlador, Navegacion navegacion) {
        this.controlador = controlador;
        this.navegacion = navegacion;

        JPanel centro = new JPanel(new GridBagLayout());
        centro.setOpaque(false);
        JPanel formulario = new JPanel(new GridBagLayout());
        formulario.setBackground(Estilo.TARJETA_CLARA);
        formulario.setBorder(javax.swing.BorderFactory.createEmptyBorder(28, 28, 28, 28));
        formulario.setPreferredSize(new Dimension(420, 360));

        GridBagConstraints gc = new GridBagConstraints();
        gc.gridx = 0;
        gc.gridy = 0;
        gc.anchor = GridBagConstraints.WEST;
        gc.insets = new Insets(4, 0, 4, 0);
        gc.fill = GridBagConstraints.HORIZONTAL;
        gc.weightx = 1;

        JLabel marca = new JLabel("WonPLUS");
        marca.setFont(Estilo.TITULO);
        marca.setForeground(Estilo.ACENTO);
        formulario.add(marca, gc);

        gc.gridy++;
        formulario.add(new JLabel("Correo"), gc);
        gc.gridy++;
        formulario.add(email, gc);
        gc.gridy++;
        formulario.add(new JLabel("Contraseña"), gc);
        gc.gridy++;
        formulario.add(clave, gc);
        gc.gridy++;
        aviso.setForeground(Estilo.SUAVE);
        formulario.add(aviso, gc);
        gc.gridy++;
        var entrar = Estilo.primario("Ingresar");
        entrar.addActionListener(event -> ingresar());
        formulario.add(entrar, gc);
        gc.gridy++;
        JLabel ayuda = new JLabel("<html>Admin: admin@wonplus.pe / Admin123<br>Vendedor: vendedor@wonplus.pe / Venta123</html>");
        ayuda.setForeground(Estilo.SUAVE);
        formulario.add(ayuda, gc);

        clave.addActionListener(event -> ingresar());
        centro.add(formulario);
        add(centro, BorderLayout.CENTER);
    }

    private void ingresar() {
        aviso.setText(" ");
        try {
            controlador.ingresar(email.getText(), new String(clave.getPassword()));
            clave.setText("");
            navegacion.ir("panel");
        } catch (RuntimeException e) {
            aviso.setText(e.getMessage());
        }
    }
}
