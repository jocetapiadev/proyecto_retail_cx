import pandas as pd
from textblob import TextBlob

# 1. Cargar el dataset limpio desde Excel
df = pd.read_excel('data/vw_resumen_cx_limpio.xlsx')

# 2. Función de Análisis de Sentimiento (NLP)
def evaluar_sentimiento(texto):
    if pd.isna(texto) or texto == '':
        return 'Neutro', 0.0
    polaridad = TextBlob(str(texto)).sentiment.polarity
    if polaridad > 0.1:
        return 'Positivo', round(polaridad, 2)
    elif polaridad < -0.1:
        return 'Negativo', round(polaridad, 2)
    return 'Neutro', round(polaridad, 2)

# 3. Aplicar clasificación
df[['sentimiento_categoria', 'sentimiento_score']] = df['comentario_cliente'].apply(
    lambda x: pd.Series(evaluar_sentimiento(x))
)

# 4. Exportar el dataset enriquecido
df.to_csv('data/dataset_retail_cx_nlp.csv', index=False)
print("✅ Procesamiento NLP completado exitosamente: data/dataset_retail_cx_nlp.csv")
