package pe.edu.utp.wonplus.reporte;

import java.io.IOException;
import java.io.OutputStream;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.format.DateTimeFormatter;
import java.util.List;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;
import pe.edu.utp.wonplus.model.Venta;

public final class ExportadorExcel {
    private static final Logger LOG = LoggerFactory.getLogger(ExportadorExcel.class);
    private static final DateTimeFormatter FECHA = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

    public Path exportar(List<Venta> ventas, Path destino) {
        if (ventas == null) {
            throw new ReglaNegocioException("No hay ventas para exportar");
        }
        Path archivo = asegurarExtension(destino);
        try (XSSFWorkbook libro = new XSSFWorkbook()) {
            XSSFSheet hoja = libro.createSheet("Ventas");
            escribirEncabezado(hoja);
            int fila = 1;
            for (Venta venta : ventas) {
                Row row = hoja.createRow(fila++);
                row.createCell(0).setCellValue(venta.id());
                row.createCell(1).setCellValue(venta.fecha().format(FECHA));
                row.createCell(2).setCellValue(venta.vendedor());
                row.createCell(3).setCellValue(numero(venta.total()));
                row.createCell(4).setCellValue(numero(venta.ganancia()));
            }
            for (int columna = 0; columna < 5; columna++) {
                hoja.autoSizeColumn(columna);
            }
            Path carpeta = archivo.getParent();
            if (carpeta != null) {
                Files.createDirectories(carpeta);
            }
            try (OutputStream salida = Files.newOutputStream(archivo)) {
                libro.write(salida);
            }
        } catch (IOException e) {
            LOG.error("No se pudo escribir el Excel en {}", archivo, e);
            throw new ReglaNegocioException("No se pudo crear el archivo Excel");
        }
        LOG.info("Reporte Excel generado en {}", archivo.toAbsolutePath());
        return archivo;
    }

    private Path asegurarExtension(Path destino) {
        String nombre = FilenameUtils.getName(destino.toString());
        if (StringUtils.isBlank(nombre)) {
            throw new ReglaNegocioException("Indica un nombre para el archivo");
        }
        if (!StringUtils.endsWithIgnoreCase(nombre, ".xlsx")) {
            return destino.resolveSibling(nombre + ".xlsx");
        }
        return destino;
    }

    private void escribirEncabezado(XSSFSheet hoja) {
        Row encabezado = hoja.createRow(0);
        encabezado.createCell(0).setCellValue("Id");
        encabezado.createCell(1).setCellValue("Fecha");
        encabezado.createCell(2).setCellValue("Vendedor");
        encabezado.createCell(3).setCellValue("Total");
        encabezado.createCell(4).setCellValue("Ganancia");
    }

    private double numero(BigDecimal valor) {
        return valor == null ? 0 : valor.doubleValue();
    }
}
