import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Determinar o segmento de cada loja (assumimos que esse segmento não é alterado)
store_segments = df.groupby('store_id')['segment'].first().reset_index()

# Contar quantas lojas existem em cada segmento (valor bruto)
counts = store_segments['segment'].value_counts()

# Função para exibir, dentro de cada fatia 
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{val} ({pct:.1f}%)'
    return my_autopct

colors = [
    "#AEC6CF",  # Azul pastel
    "#FFB347",  # Laranja suave
    "#77DD77",  # Verde claro
    "#FF6961"   # Vermelho claro
]

# Plotar o gráfico de pizza
plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    counts.values,
    labels=counts.index,
    colors=colors,
    autopct=make_autopct(counts.values),
    startangle=90,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1}
)

for txt in texts:
    txt.set_fontsize(12)
    txt.set_color('#333333') 
for atxt in autotexts:
    atxt.set_color('#333333')
    atxt.set_fontsize(11)
    atxt.set_weight('semibold')

plt.title('Distribuição de Lojas por Segmento')
plt.axis('equal')  # Para garantir que o gráfico seja um círculo
plt.show()