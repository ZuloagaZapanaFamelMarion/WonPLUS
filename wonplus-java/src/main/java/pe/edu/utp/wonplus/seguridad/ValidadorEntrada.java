package pe.edu.utp.wonplus.seguridad;

import com.google.common.base.CharMatcher;
import com.google.common.base.Strings;
import java.math.BigDecimal;
import java.math.RoundingMode;
import org.apache.commons.lang3.StringUtils;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;

public final class ValidadorEntrada {
    private ValidadorEntrada() {
    }

    public static String nombre(String valor, String campo) {
        String limpio = CharMatcher.whitespace().trimFrom(Strings.nullToEmpty(valor));
        if (StringUtils.isBlank(limpio)) {
            throw new ReglaNegocioException("Ingresa " + campo);
        }
        if (limpio.length() > 120) {
            throw new ReglaNegocioException(campo + " es demasiado largo");
        }
        return limpio;
    }

    public static String correo(String valor) {
        String limpio = CharMatcher.whitespace().trimFrom(Strings.nullToEmpty(valor)).toLowerCase();
        if (Strings.isNullOrEmpty(limpio)) {
            throw new ReglaNegocioException("El correo es obligatorio");
        }
        if (!limpio.matches("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$")) {
            throw new ReglaNegocioException("Ingresa un correo válido");
        }
        return limpio;
    }

    public static void clave(String valor) {
        if (StringUtils.length(StringUtils.trimToEmpty(valor)) < 6) {
            throw new ReglaNegocioException("La contraseña debe tener al menos 6 caracteres");
        }
    }

    public static BigDecimal dinero(String valor, String campo) {
        String limpio = StringUtils.trimToEmpty(valor).replace(',', '.');
        if (StringUtils.isBlank(limpio)) {
            throw new ReglaNegocioException("Ingresa " + campo);
        }
        try {
            BigDecimal numero = new BigDecimal(limpio).setScale(2, RoundingMode.HALF_UP);
            if (numero.signum() < 0) {
                throw new ReglaNegocioException(campo + " no puede ser negativo");
            }
            return numero;
        } catch (NumberFormatException e) {
            throw new ReglaNegocioException(campo + " no es un número válido");
        }
    }

    public static int enteroNoNegativo(String valor, String campo) {
        String limpio = StringUtils.trimToEmpty(valor);
        if (!StringUtils.isNumeric(limpio)) {
            throw new ReglaNegocioException(campo + " debe ser un número entero igual o mayor que cero");
        }
        return Integer.parseInt(limpio);
    }
}
