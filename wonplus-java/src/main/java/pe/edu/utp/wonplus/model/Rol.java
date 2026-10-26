package pe.edu.utp.wonplus.model;

public enum Rol {
    ADMIN,
    VENDEDOR;

    public String etiqueta() {
        return this == ADMIN ? "Administrador" : "Vendedor";
    }

    public static Rol desde(String valor) {
        return Rol.valueOf(valor);
    }
}
