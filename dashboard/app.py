import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

st.set_page_config(page_title="Retail CX - Analytics Dashboard", layout="wide")
st.title("📊 Retail CX - Executive Dashboard")

# Intentar conectar a PostgreSQL local; si falla o no existe, leer datos locales/CSV
@st.cache_data
def load_data():
    try:
        engine = create_engine('postgresql://admin:adminpassword@localhost:5432/retail_cx_dw', connect_args={'connect_timeout': 3})
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
        return pd.read_sql(query, engine)
    except Exception:
        # Fallback a CSV para despliegue en la nube
        csv_path = "data/dataset_retail_cx_nlp.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Normalizar columnas para el dashboard
            if 'canal' in df.columns:
                df = df.rename(columns={'canal': 'nombre_canal'})
            return df
        else:
            # Datos de respaldo mínimos en memoria
            return pd.DataFrame({
                "id_ticket": [1, 2, 3],
                "segmento": ["VIP", "Regular", "Corporativo"],
                "ciudad": ["Santiago", "Valparaíso", "Concepción"],
                "nombre_canal": ["Web", "WhatsApp", "Telefónico"],
                "monto_gastado": [120.50, 45.00, 300.00],
                "tiempo_respuesta_min": [12, 5, 45],
                "resuelto": [True, True, False],
                "comentario_cliente": ["Excelente", "Rápido", "Demasiada espera"]
            })

df = load_data()

# Métricas Principales (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", len(df))
col2.metric("Tiempo Resp. Promedio", f"{df['tiempo_respuesta_min'].mean():.1f} min")
resuelto_pct = (df['resuelto'].astype(bool).sum() / len(df) * 100) if len(df) > 0 else 0
col3.metric("Tasa de Resolución", f"{resuelto_pct:.1f}%")
col4.metric("Monto Total Atendido", f"${df['monto_gastado'].sum():,.2f}")

st.markdown("---")

# Gráficos
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Tiempo de Respuesta por Canal")
    fig_canal = px.bar(
        df, 
        x="nombre_canal", 
        y="tiempo_respuesta_min", 
        color="resuelto",
        labels={"nombre_canal": "Canal", "tiempo_respuesta_min": "Tiempo Resp. (min)"},
        title="Atenciones por Canal"
    )
    st.plotly_chart(fig_canal, use_container_width=True)

with col_right:
    st.subheader("Proporción de Casos Resueltos")
    fig_pie = px.pie(
        df, 
        names="resuelto", 
        title="Casos Resueltos vs Pendientes",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Detalle de Atenciones Registradas")
st.dataframe(df)
