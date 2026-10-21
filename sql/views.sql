CREATE OR REPLACE VIEW vw_resumen_cx AS
SELECT 
    c.cliente_id,
    c.ciudad,
    c.segmento,
    t.canal_atencion,
    SUM(v.monto) AS total_gastado,
    COUNT(DISTINCT v.venta_id) AS total_compras,
    t.ticket_id,
    t.tiempo_respuesta_min,
    t.resuelto,
    t.comentario_cliente
FROM clientes c
LEFT JOIN ventas v ON c.cliente_id = v.cliente_id
LEFT JOIN tickets_cx t ON c.cliente_id = t.cliente_id
GROUP BY c.cliente_id, c.ciudad, c.segmento, t.canal_atencion, t.ticket_id, t.tiempo_respuesta_min, t.resuelto, t.comentario_cliente;
