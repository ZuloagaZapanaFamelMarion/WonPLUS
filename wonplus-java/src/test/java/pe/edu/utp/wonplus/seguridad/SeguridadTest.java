package pe.edu.utp.wonplus.seguridad;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import pe.edu.utp.wonplus.excepcion.ReglaNegocioException;

class SeguridadTest {
    @Test
    void laClaveCifradaCoincideSoloConLaOriginal() {
        String hash = CifradorClave.cifrar("Admin123");

        assertTrue(CifradorClave.coincide("Admin123", hash));
        assertFalse(CifradorClave.coincide("otra-clave", hash));
        assertFalse(hash.contains("Admin123"));
    }

    @Test
    void rechazaCorreoVacioClaveCortaYPrecioNegativo() {
        assertThrows(ReglaNegocioException.class, () -> ValidadorEntrada.correo("  "));
        assertThrows(ReglaNegocioException.class, () -> ValidadorEntrada.clave("123"));
        assertThrows(ReglaNegocioException.class, () -> ValidadorEntrada.dinero("-1", "El precio"));
    }
}
