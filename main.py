import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import seaborn as sns


# Carregar a base de dados
file_path = "PR.csv"  # ajuste o caminho se necessário
df = pd.read_csv(file_path, sep=";")

# Converter coluna de data para datetime
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

# Criar colunas auxiliares
df["Ano"] = df["Data"].dt.year
df["Mes"] = df["Data"].dt.month

# grafico de temperatura media total da base
data_temp_total =df.groupby(df['Data'].dt.date).agg({
    'TEMPERATURA_MEDIA': 'mean'
})
print("Temperatura média total da base:")
print(data_temp_total.head())

plt.figure(figsize=(12,6))
plt.plot(data_temp_total.index, data_temp_total['TEMPERATURA_MEDIA'], color='orange')
plt.title("Temperatura média total da base (°C)")
plt.xlabel("Data")
plt.show()

# ==============================
# 1) Temperatura mínima, média e máxima por ano
# ==============================
temp_ano = df.groupby("Ano")["TEMPERATURA_MEDIA"].agg(["mean", "min", "max"])
print("Temperatura média, mínima e máxima por ano:")
print(temp_ano)

plt.figure(figsize=(10,5))
plt.plot(temp_ano.index, temp_ano["mean"], marker='o', label='Média', color='orange')
plt.plot(temp_ano.index, temp_ano["min"], marker='o', label='Mínima', color='blue')
plt.plot(temp_ano.index, temp_ano["max"], marker='o', label='Máxima', color='red')

# Adiciona os valores nos pontos e colunas dos graficos
for col, color in zip(["mean", "min", "max"], ["orange", "blue", "red"]):
    for x, y in zip(temp_ano.index, temp_ano[col]):
        plt.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0,5), ha="center", color=color)

plt.title("Temperatura média, mínima e máxima por ano (°C)")
plt.xlabel("Ano")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.grid()
plt.show()

# ==============================
# 2) Temperatura média por mês (média considerando todos os anos)
# ==============================
temp_mes = df.groupby("Mes")["TEMPERATURA_MEDIA"].mean()
print("\nTemperatura média por mês:")
print(temp_mes)

plt.figure(figsize=(8,5))
plt.plot(temp_mes.index, temp_mes.values, marker='o', color='orange')

# Adicionar rótulos nos pontos
for x, y in zip(temp_mes.index, temp_mes.values):
    plt.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0,5), ha="center", color="black")

plt.title("Temperatura média por mês (°C)")
plt.xlabel("Mês")
plt.ylabel("Temperatura (°C)")
plt.xticks(range(1,13))
plt.grid()
plt.show()

# ==============================
# 3) Volume de chuva por mês (média considerando todos os anos)
# ==============================
chuva_mes = df.groupby("Mes")["PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)"].mean()

print("\nVolume médio de chuva por mês (mm):")
print(chuva_mes)

plt.figure(figsize=(8,5))
plt.bar(range(1,13), chuva_mes)

for x, y in zip(chuva_mes.index, chuva_mes.values):
    plt.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0,5), ha="center", color="black")

plt.title("Volume médio de chuva por mês (mm)")
plt.xlabel("Mês")
plt.ylabel("Chuva (mm)")
plt.xticks(range(1,13))
plt.grid(axis='y')
plt.show()



# ==============================
# 4) Análise da correlação entre precipitação e umidade relativa do ar
# ==============================

# Agrupar por ano e calcular médias anuais
df_analise_precip_umid = df.groupby('Ano').agg({
    "PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)": "mean",
    "UMIDADE_MEDIA": "mean"
})

print(df_analise_precip_umid.corr()) # correlação entre as colunas


# Plot com duplo eixo Y
fig, ax1 = plt.subplots(figsize=(14, 7)) # mexe no tamaho da figura
ax1.grid(True, linestyle='--', alpha=0.6) # so adiciona grade no fundo

# Linha 1: Precipitação (verde, eixo da esquerda)
color1 = 'green'
ax1.set_xlabel("Ano", fontsize=14)
ax1.set_ylabel("Precipitação Média Anual (mm)", color=color1, fontsize=12)
# Plota os dados anuais originais
ax1.plot(
    df_analise_precip_umid.index,
    df_analise_precip_umid["PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)"],
    color=color1,
    marker="o", linestyle='-',
    label="Precipitação Média Anual")
ax1.tick_params(axis="y", labelcolor=color1) # mexe na cor dos numeros do eixo y da esquerda

# --- INTRODUZIDO: Zona de Confiança para Precipitação ---
sns.regplot(x=df_analise_precip_umid.index, y=df_analise_precip_umid["PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)"], ax=ax1, scatter=False, color=color1,
            line_kws={'linestyle':'', 'label':'Tendência Precipitação'})


# Rótulos nos pontinhos
for ano, valor in df_analise_precip_umid["PRECIPITAÇÃO_TOTAL__HORÁRIO_(mm)"].items():
    ax1.annotate(f"{valor:.2f}", (ano, valor), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

# Linha 2: Umidade (azul, eixo da direita)
ax2 = ax1.twinx() # faz ele usar o mesmo eixo x porem fica na direita
color2 = 'blue'
ax2.set_ylabel("Umidade Média Anual (%)", color=color2, fontsize=12)
# Plota os dados anuais originais
ax2.plot(
    df_analise_precip_umid.index,
    df_analise_precip_umid["UMIDADE_MEDIA"],
    color=color2,
    marker="o",
    linestyle='-',
    label="Umidade Média Anual")
ax2.tick_params(axis="y", labelcolor=color2) # mexe na cor dos numeros do eixo y da direita

# --- INTRODUZIDO: Zona de Confiança para Umidade ---
sns.regplot(x=df_analise_precip_umid.index, y=df_analise_precip_umid["UMIDADE_MEDIA"], ax=ax2, scatter=False, color=color2,
            line_kws={'linestyle':'', 'label':'Tendência Umidade'})


# Rótulos nos pontos de Umidade
for ano, valor in df_analise_precip_umid["UMIDADE_MEDIA"].items():
    ax2.annotate(f"{valor:.1f}", (ano, valor), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8, color=color2)

# Título e layout
plt.title("Evolução Anual da Precipitação Média vs. Umidade Média com Tendência", fontsize=18, pad=20)
fig.tight_layout()

# Força a exibição de todos os anos no eixo X
plt.xticks(ticks=df_analise_precip_umid.index, rotation=45)

# Une as legendas dos dois eixos em uma só caixa
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')
plt.show()





