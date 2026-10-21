import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Configuración de página
st.set_page_config(page_title="Retail CX - Analytics Dashboard", layout="wide")
st.title("📊 Retail CX - Executive Dashboard")

# Conexión a PostgreSQL en Docker
engine = create_engine('postgresql://admin:adminpassword@localhost:5432/retail_cx_dw')

# Cargar datos desde la tabla de hechos y dimensiones
query = """
SELECT 
    f.id_ticket,
    c.segmento,
    c.ciudad,
    can.nombre_canal,
    f.monto_gastado,
    f.tiempo_respuesta_min,
    f.resuelto,
    f.comentario_cliente
FROM fact_atencion_cx f
JOIN dim_cliente c ON f.id_cliente = c.id_cliente
JOIN dim_canal can ON f.id_canal = can.id_canal;
"""

df = pd.read_sql(query, engine)

# KPIs Principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", len(df))
col2.metric("Tiempo Resp. Promedio", f"{df['tiempo_respuesta_min'].mean():.1f} min")
col3.metric("Tasa de Resolución", f"{(df['resuelto'].sum() / len(df) * 100):.1f}%")
col4.metric("Monto Total Atendido", f"${df['monto_gastado'].sum():,.2f}")

st.markdown("---")

# Gráficos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Tickets por Canal de Atención")
    fig_canal = px.bar(
        df, 
        x="nombre_canal", 
        y="tiempo_respuesta_min", 
        color="resuelto",
        labels={"nombre_canal": "Canal", "tiempo_respuesta_min": "Tiempo Resp. (min)"},
        title="Tiempo de Respuesta por Canal"
    )
    st.plotly_chart(fig_canal, use_container_width=True)

with col_right:
    st.subheader("Estado de Resolución")
    fig_pie = px.pie(
        df, 
        names="resuelto", 
        title="Proporción de Casos Resueltos",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Tabla de Datos
st.subheader("Detalle de Atenciones")
st.dataframe(df)
