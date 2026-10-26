package pe.edu.utp.wonplus.reporte;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;
import pe.edu.utp.wonplus.model.Venta;

class ExportadorExcelTest {
    @Test
    void generaUnArchivoXlsx() throws Exception {
        Path destino = Files.createTempFile("wonplus-ventas", ".xlsx");
        Venta venta = new Venta(1, LocalDateTime.of(2026, 10, 26, 9, 20), new BigDecimal("17.00"),
                new BigDecimal("9.00"), 1, "Administrador", List.of());

        Path generado = new ExportadorExcel().exportar(List.of(venta), destino);

        assertTrue(Files.size(generado) > 100);
        Files.deleteIfExists(generado);
    }
}
