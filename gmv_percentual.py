import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar os dados do arquivo CSV
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Ordenar por loja e mês para cálculo de pct_change
df = df.sort_values(['store_id', 'month'])

# Calcular o crescimento percentual mês a mês do GMV por loja
df['growth_rate'] = df.groupby('store_id')['gmv'].pct_change()

# Remover valores inválidos (NaN ou infinitos) resultantes de divisão por zero
df_clean = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['growth_rate'])

# Para cada loja, obter o segmento (usando o segmento do último registro de cada loja)
ultimo_segmento = df.groupby('store_id')['segment'].last().reset_index()

# Calcular taxa média de crescimento (percentual) por loja
media_crescimento_loja = df_clean.groupby('store_id')['growth_rate'].mean().reset_index(name='avg_growth_rate')

# Associar o segmento de cada loja ao seu avg_growth_rate
media_crescimento_loja = media_crescimento_loja.merge(ultimo_segmento, on='store_id')

# Calcular a taxa média de crescimento por segmento (média das taxas médias das lojas de cada segmento)
crescimento_por_segmento = media_crescimento_loja.groupby('segment')['avg_growth_rate'].mean().reset_index()

# Converter para porcentagem para visualização
crescimento_por_segmento['avg_growth_rate_pct'] = crescimento_por_segmento['avg_growth_rate'] * 100

# Plotar gráfico de barras: média do crescimento percentual por segmento
plt.figure(figsize=(8, 5))
plt.bar(crescimento_por_segmento['segment'], crescimento_por_segmento['avg_growth_rate_pct'], color='orange')
plt.xlabel('Segmento')
plt.ylabel('Taxa Média de Crescimento Mensal (%)')
plt.title('Crescimento Médio Percentual do GMV por Segmento')
plt.tight_layout()
plt.show()