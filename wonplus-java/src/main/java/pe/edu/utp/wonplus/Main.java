package pe.edu.utp.wonplus;

import java.nio.file.Files;
import java.nio.file.Path;
import javax.swing.JOptionPane;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.ui.MarcoPrincipal;

public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        try {
            Files.createDirectories(Path.of("logs"));
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            Aplicacion aplicacion = Aplicacion.iniciar();
            SwingUtilities.invokeLater(() -> new MarcoPrincipal(new ControladorPrincipal(aplicacion)).setVisible(true));
        } catch (Exception e) {
            JOptionPane.showMessageDialog(
                    null,
                    e.getMessage(),
                    "WonPLUS no pudo iniciar",
                    JOptionPane.ERROR_MESSAGE
            );
        }
    }
}
