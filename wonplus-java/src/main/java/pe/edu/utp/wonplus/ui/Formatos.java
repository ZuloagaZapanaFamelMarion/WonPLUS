package pe.edu.utp.wonplus.ui;

import java.math.BigDecimal;
import java.text.NumberFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

public final class Formatos {
    private static final DateTimeFormatter FECHA = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

    private Formatos() {
    }

    public static String dinero(BigDecimal valor) {
        NumberFormat formato = NumberFormat.getCurrencyInstance(Locale.forLanguageTag("es-PE"));
        return formato.format(valor == null ? BigDecimal.ZERO : valor);
    }

    public static String fecha(LocalDateTime valor) {
        return valor == null ? "" : valor.format(FECHA);
    }
}
