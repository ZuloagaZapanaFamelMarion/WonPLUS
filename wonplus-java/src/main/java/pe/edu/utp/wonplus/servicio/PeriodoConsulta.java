package pe.edu.utp.wonplus.servicio;

import java.time.Clock;
import java.time.LocalDate;
import java.time.ZoneId;
import pe.edu.utp.wonplus.model.Periodo;
import pe.edu.utp.wonplus.model.RangoFechas;

public final class PeriodoConsulta {
    public static final ZoneId ZONA = ZoneId.of("America/Lima");

    private final Clock reloj;

    public PeriodoConsulta(Clock reloj) {
        this.reloj = reloj;
    }

    public static PeriodoConsulta lima() {
        return new PeriodoConsulta(Clock.system(ZONA));
    }

    public RangoFechas rango(Periodo periodo) {
        LocalDate hoy = LocalDate.now(reloj);
        LocalDate desde = switch (periodo) {
            case HOY -> hoy;
            case SEMANA -> hoy.minusDays(6);
            case MES -> hoy.minusDays(29);
        };
        return new RangoFechas(desde.atStartOfDay(), hoy.plusDays(1).atStartOfDay());
    }
}
