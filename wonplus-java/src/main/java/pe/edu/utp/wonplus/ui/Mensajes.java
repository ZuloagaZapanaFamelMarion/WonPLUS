package pe.edu.utp.wonplus.ui;

import java.awt.Component;
import javax.swing.JOptionPane;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;

public final class Mensajes {
    private Mensajes() {
    }

    public static void error(Component padre, Exception error) {
        String texto = error instanceof ReglaNegocioException
                ? error.getMessage()
                : "Ocurrió un problema. El detalle quedó en logs/wonplus.log";
        JOptionPane.showMessageDialog(padre, texto, "WonPLUS", JOptionPane.WARNING_MESSAGE);
    }

    public static void info(Component padre, String texto) {
        JOptionPane.showMessageDialog(padre, texto, "WonPLUS", JOptionPane.INFORMATION_MESSAGE);
    }
}
