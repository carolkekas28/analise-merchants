import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Carregar o CSV e converter a coluna 'month' para datetime
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Agrupar (somar) o GMV por mês e por segmento
df_agrupado = (
    df
    .groupby(['month', 'segment'], as_index=False)['gmv']
    .sum()
    .rename(columns={'gmv': 'gmv_total'})
)

# Pivotar para obter um DataFrame com índice 'month' e colunas para cada segmento
tabela_pivot = df_agrupado.pivot(
    index='month',
    columns='segment',
    values='gmv_total'
).fillna(0)

# Garantir que as datas estejam em ordem crescente
tabela_pivot = tabela_pivot.sort_index()

# Definir um estilo de fundo discreto
plt.style.use('seaborn-v0_8-whitegrid')

# Cores mais suaves (pastel) para cada segmento
colors = {
    'Escala':      '#aec7e8',  # azul pastel
    'Freemium':    '#ffbb78',  # laranja pastel
    'Mid Market':  '#98df8a',  # verde pastel
    'SMB':         '#ff9896'   # vermelho pastel
}

# Plotar o gráfico de linhas do GMV total por segmento
plt.figure(figsize=(12, 6))

for segmento in tabela_pivot.columns:
    plt.plot(
        tabela_pivot.index,
        tabela_pivot[segmento],
        label=segmento,
        color=colors.get(segmento, '#cccccc'),
        linewidth=2.5
    )

# Formatação do eixo Y para exibir separador de milhares com ponto
formatter = FuncFormatter(lambda x, pos: f'{int(x):,}'.replace(',', '.'))
plt.gca().yaxis.set_major_formatter(formatter)

# Títulos e rótulos
plt.title(
    'Evolução do GMV Total por Segmento\n(Jan/2023 – Dez/2024)',
    fontsize=16,
    pad=12,
    weight='bold'
)
plt.xlabel('Mês', fontsize=13)
plt.ylabel('GMV Total (R$)', fontsize=13)

# Legenda posicionada fora do eixo, à direita
plt.legend(
    title='Segmento',
    loc='center left',
    bbox_to_anchor=(1, 0.5),
    frameon=False
)

# Ajuste dos rótulos do eixo X (rotacionar para melhor legibilidade)
plt.xticks(fontsize=11)

# Grade apenas no eixo Y
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()