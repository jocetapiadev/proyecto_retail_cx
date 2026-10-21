CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    ciudad VARCHAR(50),
    segmento VARCHAR(20)
);

CREATE TABLE ventas (
    venta_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id),
    monto DECIMAL(10,2),
    fecha DATE
);

CREATE TABLE tickets_cx (
    ticket_id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES clientes(cliente_id),
    canal_atencion VARCHAR(30),
    tiempo_respuesta_min INT,
    resuelto INT,
    comentario_cliente TEXT
);
