package pe.edu.utp.wonplus.ui;

import java.awt.Color;
import java.awt.Cursor;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import javax.swing.BorderFactory;
import javax.swing.JButton;

public final class Estilo {
    public static final Color FONDO = new Color(0xFAFAFA);
    public static final Color BARRA = new Color(0x5C4580);
    public static final Color BARRA_ACTIVA = new Color(0x7B5EA7);
    public static final Color ACENTO = new Color(0x7B5EA7);
    public static final Color ACENTO_OSCURO = new Color(0x5C4580);
    public static final Color ACENTO_SUAVE = new Color(0x6B5B8A);
    public static final Color TARJETA_CLARA = new Color(0xF3EEF9);
    public static final Color PELIGRO = new Color(0xFDECEA);
    public static final Color TEXTO = new Color(0x222222);
    public static final Color SUAVE = new Color(0x6B5B8A);
    public static final Font TITULO = new Font("SansSerif", Font.BOLD, 26);
    public static final Font SUBTITULO = new Font("SansSerif", Font.PLAIN, 14);
    public static final Font TEXTO_NORMAL = new Font("SansSerif", Font.PLAIN, 14);
    public static final Font BOTON = new Font("SansSerif", Font.BOLD, 14);

    private Estilo() {
    }

    public static JButton primario(String texto) {
        JButton boton = new JButton(texto) {
            @Override
            protected void paintComponent(Graphics graphics) {
                Graphics2D g = (Graphics2D) graphics.create();
                g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g.setColor(ACENTO);
                g.fillRoundRect(0, 0, getWidth(), getHeight(), 12, 12);
                g.dispose();
                super.paintComponent(graphics);
            }
        };
        prepararBoton(boton);
        boton.setBorder(BorderFactory.createEmptyBorder(10, 16, 10, 16));
        return boton;
    }

    public static void prepararBoton(JButton boton) {
        boton.setFont(BOTON);
        boton.setForeground(Color.WHITE);
        boton.setContentAreaFilled(false);
        boton.setBorderPainted(false);
        boton.setFocusPainted(false);
        boton.setOpaque(false);
        boton.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
    }
}
