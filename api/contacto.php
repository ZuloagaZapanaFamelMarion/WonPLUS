<?php
require_once __DIR__ . '/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método no permitido']);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

$nombre = isset($data['nombre']) ? trim($data['nombre']) : '';
$email = isset($data['email']) ? trim($data['email']) : '';
$mensaje = isset($data['mensaje']) ? trim($data['mensaje']) : '';

$errors = [];

if (empty($nombre)) {
    $errors[] = 'El nombre es obligatorio';
}

if (empty($email)) {
    $errors[] = 'El correo es obligatorio';
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'El correo no es válido';
}

if (empty($mensaje)) {
    $errors[] = 'El mensaje es obligatorio';
}

if (!empty($errors)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'errors' => $errors]);
    exit;
}

$nombre = htmlspecialchars($nombre, ENT_QUOTES, 'UTF-8');
$mensaje = htmlspecialchars($mensaje, ENT_QUOTES, 'UTF-8');

try {
    $stmt = $pdo->prepare('INSERT INTO contactos (nombre, email, mensaje) VALUES (:nombre, :email, :mensaje)');
    $stmt->execute([
        ':nombre' => $nombre,
        ':email' => $email,
        ':mensaje' => $mensaje,
    ]);

    echo json_encode(['success' => true, 'message' => 'Mensaje enviado correctamente']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Error al guardar el mensaje']);
}
