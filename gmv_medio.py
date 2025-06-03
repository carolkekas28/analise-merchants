import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Calcular GMV agregado por segmento e mês
gmv_segmento_mes = df.groupby(['month', 'segment'])['gmv'].sum().reset_index()

# Contar número de lojas ativas por segmento e mês
ativos_segmento_mes = df[df['status'] == 'ativo'] \
    .groupby(['month', 'segment'])['store_id'] \
    .nunique().reset_index(name='ativos')

# Mesclar GMV agregado e ativos para obter GMV médio por loja
gmv_medios = pd.merge(
    gmv_segmento_mes, ativos_segmento_mes,
    on=['month', 'segment'], how='left'
)
gmv_medios['gmv_medio_loja'] = gmv_medios['gmv'] / gmv_medios['ativos']

# Garantir que todos os meses entre jan/23 e dez/24 apareçam para cada segmento
todos_os_meses = pd.date_range(start='2023-01-01', end='2024-12-01', freq='MS')
segmentos = gmv_medios['segment'].unique()

completa = []
for seg in segmentos:
    temp = gmv_medios[gmv_medios['segment'] == seg].set_index('month')
    temp = temp.reindex(todos_os_meses, fill_value=0).reset_index()
    temp['segment'] = seg
    completa.append(temp)

gmv_medios_completo = pd.concat(completa).rename(columns={'index': 'month'})

# Plotar série temporal de GMV médio por loja para cada segmento
plt.figure(figsize=(10, 6))
for seg in segmentos:
    dados = gmv_medios_completo[gmv_medios_completo['segment'] == seg]
    plt.plot(dados['month'], dados['gmv_medio_loja'], marker='o', label=seg)

plt.xlabel('Mês')
plt.ylabel('GMV Médio por Loja (R$)')
plt.title('Evolução do GMV Médio por Loja por Segmento (Jan/23 → Dez/24)')
plt.legend(title='Segmento')
plt.xticks(todos_os_meses[::3])
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()