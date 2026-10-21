import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración visual para los gráficos
sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# 1. CARGA DE DATOS
# ---------------------------------------------------------
archivo_csv = "vw_resumen_cx.csv"

# Definición explícita de las columnas de la vista
columnas = [
    'cliente_id', 
    'ciudad', 
    'segmento', 
    'canal_atencion', 
    'total_gastado', 
    'total_compras', 
    'ticket_id', 
    'tiempo_respuesta_min', 
    'resuelto', 
    'comentario_cliente'
]

try:
    df = pd.read_csv(archivo_csv, header=None, names=columnas)
    print("✓ Datos cargados correctamente desde el CSV.\n")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo '{archivo_csv}' en el directorio actual.")
    exit()

# ---------------------------------------------------------
# 2. MÉTRICAS GENERALES DE CX Y VENTAS
# ---------------------------------------------------------
print("="*45)
print("       RESUMEN EJECUTIVO DE METRICAS CX")
print("="*45)
total_clientes = df['cliente_id'].nunique()
monto_total = df['total_gastado'].sum()
tiempo_promedio = df['tiempo_respuesta_min'].mean()
tasa_resolucion = df['resuelto'].mean() * 100

print(f"Total Clientes Únicos : {total_clientes}")
print(f"Monto Total Ventas    : ${monto_total:,.2f}")
print(f"Tiempo Resp. Promedio : {tiempo_promedio:.1f} minutos")
print(f"Tasa de Resolución    : {tasa_resolucion:.1f}%\n")

# ---------------------------------------------------------
# 3. ANÁLISIS DE SENTIMIENTO EN COMENTARIOS
# ---------------------------------------------------------
def clasificar_sentimiento(comentario):
    if pd.isna(comentario):
        return 'Sin Comentario'
    comentario_lower = str(comentario).lower()
    palabras_positivas = ['excelente', 'rápido', 'rapido', 'bien', 'bueno', 'satisfecho']
    palabras_negativas = ['demoraron', 'falló', 'fallo', 'no resolvieron', 'malo', 'tarde', 'error']
    
    if any(p in comentario_lower for p in palabras_positivas):
        return 'Positivo'
    elif any(p in comentario_lower for p in palabras_negativas):
        return 'Negativo'
    return 'Neutral'

df['sentimiento'] = df['comentario_cliente'].apply(clasificar_sentimiento)

print("="*45)
print("      DETALLE DE SENTIMIENTO POR CLIENTE")
print("="*45)
for _, row in df.iterrows():
    print(f"Cliente ID : {row['cliente_id']} | Ciudad: {row['ciudad']}")
    print(f"Canal      : {row['canal_atencion']} | Sentimiento: [{row['sentimiento']}]")
    print(f"Comentario : \"{row['comentario_cliente']}\"")
    print("-" * 45)

# ---------------------------------------------------------
# 4. GENERACIÓN DE GRÁFICO RESUMEN
# ---------------------------------------------------------
plt.figure(figsize=(10, 5))

sns.barplot(
    data=df, 
    x='canal_atencion', 
    y='tiempo_respuesta_min', 
    hue='sentimiento',
    palette={'Positivo': 'green', 'Negativo': 'red', 'Neutral': 'gray'}
)

plt.title('Tiempo de Respuesta por Canal y Sentimiento del Cliente', fontsize=12)
plt.xlabel('Canal de Atención', fontsize=10)
plt.ylabel('Tiempo de Respuesta (Minutos)', fontsize=10)
plt.tight_layout()

plt.savefig('reporte_cx_canales.png')
print("\n✓ Gráfico guardado exitosamente como 'reporte_cx_canales.png'")
