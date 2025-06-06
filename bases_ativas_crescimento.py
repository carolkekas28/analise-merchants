import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Leitura dos arquivos
df = pd.read_csv('Lojas.csv', parse_dates=['month'])
df_ativos = df[df['status'] == 'ativo']

contagem_mensal = (
    df_ativos
    .groupby(['month', 'segment'])['store_id']
    .nunique()
    .reset_index(name='ativos')
)

pivot_ativos = (
    contagem_mensal
    .pivot(index='month', columns='segment', values='ativos')
    .fillna(0)
)

todos_os_meses = pd.date_range('2023-01-01', '2024-12-01', freq='MS')
pivot_ativos = pivot_ativos.reindex(todos_os_meses, fill_value=0)
pivot_ativos.index.name = 'month'

# Estilização do gráfico
plt.style.use('seaborn-v0_8-whitegrid')
cores = ['#AEC6CF', '#FFB347', '#77DD77', '#FF6961']   # Escala, Freemium, Mid Market, SMB
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cores)

fig, ax = plt.subplots(figsize=(11, 6))
ax.set_facecolor('white')

# Plot + rótulo de deslocamento
for cor, segment in zip(cores, pivot_ativos.columns):
    ax.plot(
        pivot_ativos.index,
        pivot_ativos[segment],
        marker='o',
        linewidth=2.2,
        label=segment
    )

    y_last = pivot_ativos[segment].iloc[-1]
    ax.annotate(f'{y_last:.0f}',
                xy=(pivot_ativos.index[-1], y_last),
                xytext=(5, 2),
                textcoords='offset points',
                fontsize=9,
                va='bottom',
    )

ax.set_xlim(pivot_ativos.index[0],
            pivot_ativos.index[-1] + pd.DateOffset(months=1))

# Formatar eixos
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
plt.setp(ax.get_xticklabels(), ha='right')

ax.set_xlabel('Mês')
ax.set_ylabel('Número de lojas ativas')

ax.set_title('Evolução Mensal da Base Ativa por Segmento\n(Jan/2023 – Dez/2024)',
             fontsize=14, weight='bold')

ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.grid(axis='x', visible=False)
ax.legend(title='Segmento', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.show()
