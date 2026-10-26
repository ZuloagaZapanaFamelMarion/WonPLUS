package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridLayout;
import javax.swing.JLabel;
import javax.swing.JPanel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.ResumenDia;

public final class PanelVista extends Vista {
    private final ControladorPrincipal controlador;
    private final JLabel ventas = dato();
    private final JLabel stock = dato();
    private final JLabel ganancia = dato();

    public PanelVista(ControladorPrincipal controlador, Navegacion navegacion) {
        this.controlador = controlador;
        add(encabezado("Panel principal", "Cifras del día calculadas con las ventas registradas"), BorderLayout.NORTH);

        JPanel grilla = new JPanel(new GridLayout(1, 3, 16, 16));
        grilla.setOpaque(false);
        grilla.add(tarjetaIndicador("Ventas de hoy", ventas, "Operaciones registradas hoy"));
        grilla.add(tarjetaIndicador("Stock bajo", stock, "Productos en o bajo el mínimo"));
        grilla.add(tarjetaIndicador("Ganancia del día", ganancia, "Precio de venta menos costo"));
        add(grilla, BorderLayout.CENTER);

        JPanel acciones = new JPanel();
        acciones.setOpaque(false);
        var vender = Estilo.primario("Registrar venta");
        vender.addActionListener(event -> navegacion.ir("venta"));
        var alertas = Estilo.primario("Ver alertas de stock");
        alertas.addActionListener(event -> navegacion.ir("stock"));
        acciones.add(vender);
        acciones.add(alertas);
        add(acciones, BorderLayout.SOUTH);
    }

    @Override
    public void alMostrar() {
        ResumenDia resumen = controlador.resumen();
        ventas.setText(resumen.operaciones() + "  ·  " + Formatos.dinero(resumen.totalVentas()));
        stock.setText(String.valueOf(resumen.productosStockBajo()));
        ganancia.setText(Formatos.dinero(resumen.ganancia()));
    }

    private JPanel tarjetaIndicador(String titulo, JLabel valor, String detalle) {
        JPanel texto = new JPanel(new GridLayout(3, 1, 0, 6));
        texto.setOpaque(false);
        JLabel tituloLabel = new JLabel(titulo);
        tituloLabel.setForeground(Estilo.SUAVE);
        valor.setFont(Estilo.TITULO);
        JLabel detalleLabel = new JLabel(detalle);
        detalleLabel.setForeground(Estilo.SUAVE);
        texto.add(tituloLabel);
        texto.add(valor);
        texto.add(detalleLabel);
        JPanel tarjeta = tarjeta(texto);
        tarjeta.setPreferredSize(new Dimension(220, 140));
        return tarjeta;
    }

    private JLabel dato() {
        JLabel etiqueta = new JLabel("—");
        etiqueta.setForeground(Estilo.TEXTO);
        return etiqueta;
    }
}
