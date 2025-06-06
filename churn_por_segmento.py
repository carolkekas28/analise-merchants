import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Carregar dados
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Filtrar apenas os meses em que status == 'churn'
df_churn = df[df['status'] == 'churn']

# Agrupar por mês e segmento para contar lojas únicas em churn
churn_grouped = (
    df_churn
    .groupby(['month', 'segment'])['store_id']
    .nunique()               # conta quantas lojas distintas ficaram em churn naquele mês/segmento
    .reset_index(name='churn_count')
)

# Pivotar em formato “wide” para ter colunas por segmento
pivot_churn = churn_grouped.pivot(
    index='month',
    columns='segment',
    values='churn_count'
)

# Criar um índice completo de meses (jan/2023 a dez/2024)
todos_os_meses = pd.date_range(start='2023-01-01', end='2024-12-01', freq='MS')

# Reindexar o DataFrame para incluir todos os meses no índice, meses sem dados terão valor zero
pivot_churn = pivot_churn.reindex(todos_os_meses, fill_value=0)

# Definir estilo mais suave
plt.style.use('ggplot')

# Escolher cores suaves para cada segmento (paleta pastel)
cores_pastel = {
    'Escala':     '#A6CEE3',   # Azul claro
    'Freemium':   '#FDBF6F',   # Laranja pastel
    'Mid Market': '#B2DF8A',   # Verde claro
    'SMB':        '#FB9A99'    # Rosa claro
}

# Configurar o plot
fig, ax = plt.subplots(figsize=(14, 6))

for segmento in pivot_churn.columns:
    ax.plot(
        pivot_churn.index,
        pivot_churn[segmento],
        marker='o',
        label=segmento,
        color=cores_pastel.get(segmento, '#CCCCCC'),
        linewidth=2,
        alpha=0.8
    )

ax.set_title('Número de Lojas com Status "Churn" por Segmento\n(Jan/2023 – Dez/2024)', fontsize=16, pad=15, weight='bold')
ax.set_xlabel('Mês', fontsize=12)
ax.set_ylabel('Quantidade de Lojas Churn', fontsize=12)
ax.legend(title='Segmento', fontsize=10, title_fontsize=11, frameon=True, loc='upper right')

# Mostrar apenas cada início de trimestre
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Melhorar aparência dos ticks
plt.setp(ax.get_xticklabels(), fontsize=10)
plt.setp(ax.get_yticklabels(), fontsize=10)

# Linhas de grade leves e fundo mais claro
ax.grid(color='white', linestyle='-', linewidth=1, alpha=0.7)
fig.patch.set_facecolor('#F9F9F9')
ax.set_facecolor('#FBFBFB')

plt.tight_layout()
plt.show()
