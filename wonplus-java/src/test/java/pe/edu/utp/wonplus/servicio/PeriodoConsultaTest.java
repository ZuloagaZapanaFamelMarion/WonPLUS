package pe.edu.utp.wonplus.servicio;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import org.junit.jupiter.api.Test;
import pe.edu.utp.wonplus.model.Periodo;

class PeriodoConsultaTest {
    @Test
    void elDiaCubreSoloLaFechaActual() {
        Clock reloj = Clock.fixed(Instant.parse("2026-10-26T15:00:00Z"), ZoneId.of("America/Lima"));
        PeriodoConsulta consulta = new PeriodoConsulta(reloj);

        var rango = consulta.rango(Periodo.HOY);

        assertEquals("2026-10-26T00:00", rango.desde().toString());
        assertEquals("2026-10-27T00:00", rango.hasta().toString());
    }
}
