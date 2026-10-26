package pe.edu.utp.wonplus.seguridad;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;
import java.util.HexFormat;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public final class CifradorClave {
    private static final int ITERACIONES = 65536;
    private static final int BYTES_SAL = 16;
    private static final int BITS_HASH = 256;
    private static final SecureRandom ALEATORIO = new SecureRandom();

    private CifradorClave() {
    }

    public static String cifrar(String clave) {
        byte[] sal = new byte[BYTES_SAL];
        ALEATORIO.nextBytes(sal);
        byte[] hash = derivar(clave, sal, ITERACIONES);
        return ITERACIONES + "$" + HexFormat.of().formatHex(sal) + "$" + HexFormat.of().formatHex(hash);
    }

    public static boolean coincide(String clave, String almacenado) {
        if (clave == null || almacenado == null) {
            return false;
        }
        String[] partes = almacenado.split("\\$");
        if (partes.length != 3) {
            return false;
        }
        try {
            int iteraciones = Integer.parseInt(partes[0]);
            byte[] sal = HexFormat.of().parseHex(partes[1]);
            byte[] esperado = HexFormat.of().parseHex(partes[2]);
            byte[] actual = derivar(clave, sal, iteraciones);
            return MessageDigest.isEqual(esperado, actual);
        } catch (IllegalArgumentException e) {
            return false;
        }
    }

    private static byte[] derivar(String clave, byte[] sal, int iteraciones) {
        try {
            PBEKeySpec spec = new PBEKeySpec(clave.toCharArray(), sal, iteraciones, BITS_HASH);
            return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            throw new IllegalStateException("No se pudo cifrar la contraseña", e);
        }
    }
}
