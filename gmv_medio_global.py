import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Carregar dados
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Calcular GMV agregado por segmento e mês
gmv_segmento_mes = (
    df
    .groupby(['month', 'segment'])['gmv']
    .sum()
    .reset_index()
)

# Contar número de lojas ativas por segmento e mês
ativos_segmento_mes = (
    df[df['status'] == 'ativo']
    .groupby(['month', 'segment'])['store_id']
    .nunique()
    .reset_index(name='ativos')
)

# Mesclar para obter GMV médio por loja
gmv_medios = pd.merge(
    gmv_segmento_mes,
    ativos_segmento_mes,
    on=['month', 'segment'],
    how='left'
)
gmv_medios['gmv_medio_loja'] = gmv_medios['gmv'] / gmv_medios['ativos']

# Gerar índice completo de meses (jan/2023 a dez/2024)
todos_os_meses = pd.date_range(start='2023-01-01', end='2024-12-01', freq='MS')
segmentos = gmv_medios['segment'].unique()

# Reindexar cada segmento para garantir todos os meses apareçam
lista_completa = []
for seg in segmentos:
    temp = gmv_medios[gmv_medios['segment'] == seg].set_index('month')
    temp = temp.reindex(todos_os_meses, fill_value=0).reset_index()
    temp['segment'] = seg
    lista_completa.append(temp)

gmv_medios_completo = (
    pd.concat(lista_completa)
    .rename(columns={'index': 'month'})
)

# Calcular GMV total por mês (todos os segmentos juntos)
gmv_total_mes = (
    df
    .groupby('month')['gmv']
    .sum()
    .reindex(todos_os_meses, fill_value=0)
    .reset_index(name='gmv_total')
)
gmv_total_mes = gmv_total_mes.rename(columns={'index': 'month'})

# Calcular número total de lojas ativas por mês (todos os segmentos juntos)
ativos_global_mes = (
    df[df['status'] == 'ativo']
    .groupby('month')['store_id']
    .nunique()
    .reindex(todos_os_meses, fill_value=0)
    .reset_index(name='ativos_total')
)
ativos_global_mes = ativos_global_mes.rename(columns={'index': 'month'})

# Mesclar GMV total e ativos para obter GMV médio global
global_merge = pd.merge(
    gmv_total_mes,
    ativos_global_mes,
    on='month',
    how='left'
)
global_merge['gmv_medio_global'] = global_merge['gmv_total'] / global_merge['ativos_total']

plt.style.use('ggplot')  # estilo mais suave (linhas de grade claras, fundo levemente cinza)

cores_pastel = {
    'Escala':     '#A6CEE3',   # Azul claro
    'Freemium':   '#FDBF6F',   # Laranja pastel
    'Mid Market': '#B2DF8A',   # Verde claro
    'SMB':        '#FB9A99'    # Rosa claro
}

# Plotar o gráfico
fig, ax = plt.subplots(figsize=(12, 6))

# Linhas de cada segmento
for seg in sorted(segmentos): 
    dados = gmv_medios_completo[gmv_medios_completo['segment'] == seg]
    ax.plot(
        dados['month'],
        dados['gmv_medio_loja'],
        marker='o',
        markersize=5,
        linestyle='-',
        linewidth=2,
        label=seg,
        color=cores_pastel.get(seg, '#CCCCCC'),
        alpha=0.8
    )

# Linha global (todos os segmentos juntos) 
ax.plot(
    global_merge['month'],
    global_merge['gmv_medio_global'],
    color='black',
    linestyle='-',
    linewidth=2.5,
    marker='D',
    markersize=6,
    label='Todos Segmentos (Global)'
)

# Ajustes visuais finais
ax.set_title(
    'Evolução do GMV Médio por Loja Ativa Para Cada Segmento\n(Jan/2023 – Dez/2024)',
    fontsize=16,
    pad=15,
    weight='bold'
)
ax.set_xlabel('Mês', fontsize=12, labelpad=10)
ax.set_ylabel('GMV Médio por Loja (R$)', fontsize=12, labelpad=10)

ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.setp(ax.get_xticklabels(), fontsize=10)
plt.setp(ax.get_yticklabels(), fontsize=10)

ax.legend(
    title='Segmento',
    fontsize=10,
    title_fontsize=11,
    frameon=True,
    loc='upper left',
    bbox_to_anchor=(1.02, 1)
)

# Linhas de grid leves no eixo y
ax.grid(axis='y', color='white', linestyle='-', linewidth=1, alpha=0.7)

# Fundo do gráfico e figura mais claros
fig.patch.set_facecolor('#F9F9F9')
ax.set_facecolor('#FBFBFB')

plt.tight_layout()
plt.show()
