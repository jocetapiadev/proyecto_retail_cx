SELECT 
    id_ticket,
    id_cliente,
    id_canal,
    monto_gastado,
    tiempo_respuesta_min,
    resuelto,
    comentario_cliente,
    fecha_registro
FROM {{ source('public', 'fact_atencion_cx') }}
