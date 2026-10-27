package pe.edu.utp.wonplus.ui;

import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.util.LinkedHashMap;
import java.util.Map;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import pe.edu.utp.wonplus.controlador.ControladorPrincipal;
import pe.edu.utp.wonplus.model.Usuario;

public final class MarcoPrincipal extends JFrame implements Navegacion {
    private final ControladorPrincipal controlador;
    private final CardLayout cards = new CardLayout();
    private final JPanel contenido = new JPanel(cards);
    private final JPanel menu = new JPanel();
    private final Map<String, Vista> vistas = new LinkedHashMap<>();
    private final JLabel sesion = new JLabel(" ");

    public MarcoPrincipal(ControladorPrincipal controlador) {
        super("WonPLUS");
        this.controlador = controlador;
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1100, 700);
        setLocationRelativeTo(null);

        menu.setLayout(new BoxLayout(menu, BoxLayout.Y_AXIS));
        menu.setBackground(Estilo.BARRA);
        menu.setPreferredSize(new Dimension(230, 0));
        contenido.setBackground(Estilo.FONDO);

        registrar("login", new LoginVista(controlador, this));
        registrar("panel", new PanelVista(controlador, this));
        registrar("usuarios", new UsuariosVista(controlador));
        registrar("productos", new ProductosVista(controlador));
        registrar("categorias", new CategoriasVista(controlador));
        registrar("venta", new VentaVista(controlador, this));
        registrar("ticket", new TicketVista(controlador, this));
        registrar("historial", new HistorialVista(controlador, this));
        registrar("detalle", new DetalleVista(controlador, this));
        registrar("stock", new StockVista(controlador));
        registrar("reportes", new ReportesVista(controlador));

        add(menu, BorderLayout.WEST);
        add(contenido, BorderLayout.CENTER);
        ir("login");
    }

    @Override
    public void ir(String destino) {
        if (!"login".equals(destino)) {
            armarMenu();
        }
        menu.setVisible(!"login".equals(destino));
        Vista vista = vistas.get(destino);
        vista.alMostrar();
        cards.show(contenido, destino);
        revalidate();
    }

    @Override
    public void salir() {
        controlador.cerrarSesion();
        ir("login");
    }

    private void registrar(String nombre, Vista vista) {
        vistas.put(nombre, vista);
        contenido.add(vista, nombre);
    }

    private void armarMenu() {
        menu.removeAll();
        menu.add(Box.createVerticalStrut(18));
        JLabel marca = new JLabel("  WonPLUS");
        marca.setForeground(Color.WHITE);
        marca.setFont(Estilo.BOTON);
        marca.setAlignmentX(LEFT_ALIGNMENT);
        menu.add(marca);
        Usuario usuario = controlador.sesion();
        sesion.setText(usuario == null ? " " : "  " + usuario.nombre());
        sesion.setForeground(Estilo.TARJETA_CLARA);
        sesion.setAlignmentX(LEFT_ALIGNMENT);
        menu.add(sesion);
        menu.add(Box.createVerticalStrut(16));
        item("Panel", "panel");
        item("Registrar venta", "venta");
        item("Historial", "historial");
        item("Alertas de stock", "stock");
        item("Reportes", "reportes");
        if (controlador.esAdmin()) {
            menu.add(Box.createVerticalStrut(8));
            item("Productos", "productos");
            item("Categorías", "categorias");
            item("Usuarios", "usuarios");
        }
        menu.add(Box.createVerticalGlue());
        BotonMenu salir = new BotonMenu("Cerrar sesión");
        salir.addActionListener(event -> salir());
        menu.add(salir);
        menu.add(Box.createVerticalStrut(12));
        menu.revalidate();
        menu.repaint();
    }

    private void item(String texto, String destino) {
        BotonMenu boton = new BotonMenu(texto);
        boton.addActionListener(event -> ir(destino));
        menu.add(boton);
    }
}
