import pandas as pd
from sqlalchemy import create_engine

# 1. Leer dataset con NLP
df = pd.read_csv('data/dataset_retail_cx_nlp.csv')

# Conexión a PostgreSQL en Docker
engine = create_engine('postgresql://admin:adminpassword@localhost:5432/retail_cx_dw')

# 2. Convertir columna resuelto a Boolean (1 -> True, 0 -> False)
df['resuelto'] = df['resuelto'].astype(bool)

# 3. Poblar dim_cliente (insertar solo clientes no existentes)
dim_cliente = df[['cliente_id', 'segmento', 'ciudad']].drop_duplicates(subset=['cliente_id'])
dim_cliente = dim_cliente.rename(columns={'cliente_id': 'id_cliente'})

clientes_existentes = pd.read_sql('SELECT id_cliente FROM dim_cliente;', engine)
dim_cliente_nuevos = dim_cliente[~dim_cliente['id_cliente'].isin(clientes_existentes['id_cliente'])]

if not dim_cliente_nuevos.empty:
    dim_cliente_nuevos.to_sql('dim_cliente', engine, if_exists='append', index=False)

# 4. Mapear id_canal para la tabla de hechos
canales = pd.read_sql('SELECT id_canal, nombre_canal FROM dim_canal;', engine)
df = df.merge(canales, left_on='canal_atencion', right_on='nombre_canal', how='left')

# 5. Poblar fact_atencion_cx
fact = df[[
    'ticket_id', 
    'cliente_id', 
    'id_canal', 
    'total_gastado', 
    'tiempo_respuesta_min', 
    'resuelto', 
    'comentario_cliente'
]].copy()

fact = fact.rename(columns={
    'ticket_id': 'id_ticket',
    'cliente_id': 'id_cliente',
    'total_gastado': 'monto_gastado'
})

tickets_existentes = pd.read_sql('SELECT id_ticket FROM fact_atencion_cx;', engine)
fact_nuevos = fact[~fact['id_ticket'].isin(tickets_existentes['id_ticket'])]

if not fact_nuevos.empty:
    fact_nuevos.to_sql('fact_atencion_cx', engine, if_exists='append', index=False)

print("✅ Datos cargados exitosamente en dim_cliente y fact_atencion_cx")
