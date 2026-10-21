SELECT 
    id_cliente,
    segmento,
    ciudad
FROM {{ source('public', 'dim_cliente') }}
