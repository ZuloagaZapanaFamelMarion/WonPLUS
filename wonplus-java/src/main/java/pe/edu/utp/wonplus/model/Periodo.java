package pe.edu.utp.wonplus.model;

public enum Periodo {
    HOY("Hoy"),
    SEMANA("Últimos 7 días"),
    MES("Últimos 30 días");

    private final String etiqueta;

    Periodo(String etiqueta) {
        this.etiqueta = etiqueta;
    }

    public String etiqueta() {
        return etiqueta;
    }

    @Override
    public String toString() {
        return etiqueta;
    }
}
