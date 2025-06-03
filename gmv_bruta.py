import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Ordenar por loja e mês
df = df.sort_values(['store_id', 'month'])

# Calcular variação bruta de GMV mês a mês por loja
df['gmv_diff'] = df.groupby('store_id')['gmv'].diff()

# Remover NaN resultantes (primeiro mês de cada loja não tem diff)
df_diff = df.dropna(subset=['gmv_diff'])

# Obter segmento de cada loja no último registro
ultimo_segmento = df.groupby('store_id')['segment'].last().reset_index()

# Calcular média de variação bruta por loja
media_diff_loja = df_diff.groupby('store_id')['gmv_diff'].mean().reset_index(name='avg_gmv_diff')

# Associar segmento a cada loja
media_diff_loja = media_diff_loja.merge(ultimo_segmento, on='store_id')

# Calcular média da variação bruta por segmento
crescimento_bruto_por_segmento = media_diff_loja.groupby('segment')['avg_gmv_diff'].mean().reset_index()

# Plotar gráfico de barras
plt.figure(figsize=(8, 5))
plt.bar(crescimento_bruto_por_segmento['segment'], crescimento_bruto_por_segmento['avg_gmv_diff'], color='green')
plt.xlabel('Segmento')
plt.ylabel('Média de Variação Bruta Mensal de GMV (R$)')
plt.title('Média da Variação Bruta de GMV por Segmento (Jan/23 → Dez/24)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()