CREATE TABLE IF NOT EXISTS usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('ADMIN', 'VENDEDOR')),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS categoria (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(160) NOT NULL,
    precio NUMERIC(12, 2) NOT NULL CHECK (precio >= 0),
    costo NUMERIC(12, 2) NOT NULL CHECK (costo >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    stock_minimo INTEGER NOT NULL CHECK (stock_minimo >= 0),
    id_categoria INTEGER NOT NULL REFERENCES categoria (id_categoria)
);

CREATE TABLE IF NOT EXISTS venta (
    id_venta SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT NOW(),
    total NUMERIC(12, 2) NOT NULL CHECK (total >= 0),
    id_usuario INTEGER NOT NULL REFERENCES usuario (id_usuario)
);

CREATE TABLE IF NOT EXISTS detalle_venta (
    id_detalle SERIAL PRIMARY KEY,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(12, 2) NOT NULL CHECK (precio_unitario >= 0),
    costo_unitario NUMERIC(12, 2) NOT NULL CHECK (costo_unitario >= 0),
    id_venta INTEGER NOT NULL REFERENCES venta (id_venta),
    id_producto INTEGER NOT NULL REFERENCES producto (id_producto)
);
