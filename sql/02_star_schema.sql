-- Creación de Tablas de Dimensión
DROP TABLE IF EXISTS dim_canal CASCADE;
CREATE TABLE dim_canal (
    id_canal SERIAL PRIMARY KEY,
    nombre_canal VARCHAR(50) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS dim_cliente CASCADE;
CREATE TABLE dim_cliente (
    id_cliente INT PRIMARY KEY,
    segmento VARCHAR(50),
    ciudad VARCHAR(100)
);

-- Tabla de Hechos (Fact Table)
DROP TABLE IF EXISTS fact_atencion_cx CASCADE;
CREATE TABLE fact_atencion_cx (
    id_ticket INT PRIMARY KEY,
    id_cliente INT REFERENCES dim_cliente(id_cliente),
    id_canal INT REFERENCES dim_canal(id_canal),
    monto_gastado NUMERIC(10,2),
    tiempo_respuesta_min NUMERIC(5,2),
    resuelto BOOLEAN,
    comentario_cliente TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos Semilla para Dimensiones
INSERT INTO dim_canal (nombre_canal) VALUES ('Llamada'), ('Web'), ('WhatsApp');
