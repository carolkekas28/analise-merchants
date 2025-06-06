import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Filtrar apenas os meses onde o status é 'churn'
df_churn = df[df['status'] == 'churn']

# Contar quantos meses cada loja ficou em churn
churn_por_loja = df_churn.groupby('store_id').size().reset_index(name='churn_months')

# Mostrar que lojas que nunca churnaram também apareçam com 0 meses
lojas_info = df[['store_id', 'segment']].drop_duplicates()

# Fazer merge para incluir lojas sem churn, preenchendo NaN com 0
lojas_churn_completo = lojas_info.merge(churn_por_loja, on='store_id', how='left')
lojas_churn_completo['churn_months'] = lojas_churn_completo['churn_months'].fillna(0).astype(int)

# Calcular o tempo médio de churn por segmento
tempo_medio_churn_segmento = (
    lojas_churn_completo
    .groupby('segment')['churn_months']
    .mean()
    .reset_index()
    .round(2)
)

plt.style.use('default')                 # ① volta ao tema padrão (fundo branco)

fig, ax = plt.subplots(figsize=(8, 5))   # ② nova figura/eixo
ax.set_facecolor('white')                # ③ fundo do eixo branco

cores_pastel = {
    'Mid Market': '#B2DF8A',
    'Escala':     '#A6CEE3',
    'SMB':        '#FB9A99',
    'Freemium':   '#FDBF6F'
}

bars = ax.bar(
    tempo_medio_churn_segmento['segment'],
    tempo_medio_churn_segmento['churn_months'],
    color=[cores_pastel.get(seg, '#CCCCCC') for seg in tempo_medio_churn_segmento['segment']],
    edgecolor='gray'
)

# Rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.2,
        f"{height:.2f}",
        ha='center',
        va='bottom',
        fontsize=10
    )

ax.set_title("Tempo Médio de Churn por Segmento", fontsize=14, fontweight='bold')
ax.set_xlabel("Segmento", fontsize=12)
ax.set_ylabel("Meses em Churn (média)", fontsize=12)
ax.set_ylim(0, tempo_medio_churn_segmento['churn_months'].max() + 2)

ax.grid(axis='y', linestyle='--', alpha=0.2)
ax.spines[['top', 'right']].set_visible(False)   # remove bordas sup./dir.

plt.tight_layout()
plt.show()