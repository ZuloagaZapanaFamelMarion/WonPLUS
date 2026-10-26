package pe.edu.utp.wonplus.servicio;

import java.nio.file.Path;
import java.util.List;
import pe.edu.utp.wonplus.model.Periodo;
import pe.edu.utp.wonplus.model.Usuario;
import pe.edu.utp.wonplus.model.Venta;
import pe.edu.utp.wonplus.reporte.ExportadorExcel;

public final class ReporteService {
    private final VentaService ventas;
    private final ExportadorExcel excel;

    public ReporteService(VentaService ventas, ExportadorExcel excel) {
        this.ventas = ventas;
        this.excel = excel;
    }

    public List<Venta> consultar(Usuario sesion, Periodo periodo) {
        return ventas.historial(sesion, periodo);
    }

    public Path exportar(Usuario sesion, Periodo periodo, Path destino) {
        return excel.exportar(consultar(sesion, periodo), destino);
    }
}
