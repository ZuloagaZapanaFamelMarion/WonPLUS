package pe.edu.utp.wonplus.ui;

import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JButton;
import javax.swing.SwingConstants;

public final class BotonMenu extends JButton {
    public BotonMenu(String texto) {
        super(texto);
        setFont(Estilo.TEXTO_NORMAL);
        setForeground(Color.WHITE);
        setHorizontalAlignment(SwingConstants.LEFT);
        setContentAreaFilled(false);
        setBorderPainted(false);
        setFocusPainted(false);
        setOpaque(false);
        setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        setMaximumSize(new Dimension(Integer.MAX_VALUE, 44));
        setAlignmentX(LEFT_ALIGNMENT);
    }

    @Override
    protected void paintComponent(Graphics graphics) {
        Graphics2D g = (Graphics2D) graphics.create();
        g.setColor(getModel().isRollover() ? Estilo.BARRA_ACTIVA : Estilo.BARRA);
        g.fillRect(0, 0, getWidth(), getHeight());
        g.dispose();
        super.paintComponent(graphics);
    }
}
