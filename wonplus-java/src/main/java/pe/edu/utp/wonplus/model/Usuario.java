package pe.edu.utp.wonplus.model;

public record Usuario(
        int id,
        String nombre,
        String email,
        String passwordHash,
        Rol rol,
        boolean activo
) {
}
