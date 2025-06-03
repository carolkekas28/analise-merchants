import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('Lojas.csv', parse_dates=['month'])

# Filtrar lojas com status "churn"
churn_df = df[df['status'] == 'churn']

# Agrupar por mês e segmento e contar número de lojas
churn_counts = churn_df.groupby(['month', 'segment']).size().unstack(fill_value=0)

# Plotar
plt.figure(figsize=(12, 6))
for segment in churn_counts.columns:
    plt.plot(churn_counts.index, churn_counts[segment], label=segment)

plt.title('Número de Lojas com Status "Churn" por Segmento (jan/2023 - dez/2024)')
plt.xlabel('Mês')
plt.ylabel('Quantidade de Lojas Churn')
plt.legend(title='Segmento')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
