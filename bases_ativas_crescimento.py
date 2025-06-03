import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do arquivo CSV
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Filtrar as linhas onde o status da loja é ativo
df_ativos = df[df['status'] == 'ativo']

# Contar número de lojas ativas por segmento em cada mês
contagem_mensal = (
    df_ativos
    .groupby(['month', 'segment'])['store_id']
    .nunique()
    .reset_index(name='ativos')
)

# Pivotar para ter segmentos como colunas
pivot_ativos = contagem_mensal.pivot(index='month', columns='segment', values='ativos').fillna(0)

# Garantir que todos os meses estejam presentes no índice (de jan/2023 a dez/2024)
todos_os_meses = pd.date_range(start='2023-01-01', end='2024-12-01', freq='MS')
pivot_ativos = pivot_ativos.reindex(todos_os_meses, fill_value=0)
pivot_ativos.index.name = 'month'

# Plotar gráfico de linhas
plt.figure(figsize=(10, 6))
for segment in pivot_ativos.columns:
    plt.plot(pivot_ativos.index, pivot_ativos[segment], marker='o', label=segment)

plt.xlabel('Mês')
plt.ylabel('Número de Lojas Ativas')
plt.title('Evolução da Base Ativa por Segmento de Jan/2023 a Dez/2024')
plt.legend(title='Segmento')
plt.xticks(todos_os_meses[::3])  # Marca a cada 3 meses para legibilidade
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()