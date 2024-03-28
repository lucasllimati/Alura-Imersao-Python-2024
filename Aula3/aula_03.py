# -*- coding: utf-8 -*-
"""[Imersão Python] Aula 03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bZJGHP04eoNCnyQQ40hqmtn0EGqdRAaT
"""

import pandas as pd
import plotly.express as px

"""##### Verificar abas do arquivo"""

df_principal = pd.read_excel("/content/acoes_pura.xlsx", sheet_name="Principal")
df_principal

df_total_acoes = pd.read_excel("/content/acoes_pura.xlsx", sheet_name="Total_de_acoes")
df_total_acoes

df_ticker = pd.read_excel("/content/acoes_pura.xlsx", sheet_name="Ticker")
df_ticker

df_chatgpt = pd.read_excel("/content/acoes_pura.xlsx", sheet_name="Chatgpt")
df_chatgpt

"""##### Tratamentos Iniciais"""

# Selecionar as colunas desajadas para o dataframe
df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()
df_principal

"""".copy()" é utilizado para resetar o dataframe, meio que cria um novo a partir dos ajustes feitos."""

# Renomear os nomes das colunas (facilitar nas futuras análises)
df_principal = df_principal.rename(columns={'Último (R$)':'valor_final', 'Var. Dia (%)':'var_dia_pct'}).copy()
df_principal

# Criando novas informações (Variação percentual e Valor Iniciao da Ação no dia)
df_principal['Var_pct'] = df_principal['var_dia_pct'] / 100
df_principal['valor_inicial'] = df_principal['valor_final'] / (df_principal['Var_pct'] + 1)
df_principal

# União das informações (Semelhante ao JOIN do SQL e PROCV/VLOOKUP do Excel).
df_principal = df_principal.merge(df_total_acoes, left_on='Ativo', right_on='Código', how='left')
df_principal

# Deleta a coluna Código que seria a mesma informação que o Ativo
df_principal = df_principal.drop(columns=['Código'])
df_principal

# Cria a coluna variação monetária R$
df_principal['Variacao_rs'] = (df_principal['valor_final'] - df_principal['valor_inicial']) * df_principal['Qtde. Teórica']
df_principal

# Converter colunas para float (decimal)
pd.options.display.float_format = '{:.2f}'.format
df_principal.head()

# Converter colunas para int (inteiro)
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)
df_principal

# Renomear os nomes das colunas
df_principal = df_principal.rename(columns={'Qtde. Teórica':'Qtd_teorica'}).copy()
df_principal

# Coluna informando se a variação foi positica, negativa ou neutra.
df_principal['Resultado'] = df_principal['Variacao_rs'].apply(lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável'))
df_principal

# União das informações (Semelhante ao JOIN do SQL e PROCV/VLOOKUP do Excel) e deletar a coluna Ticker.
df_principal = df_principal.merge(df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.drop(columns=['Ticker'])
df_principal

# União das informações (Semelhante ao JOIN do SQL e PROCV/VLOOKUP do Excel) e deletar a coluna Nome da empresa.
df_principal = df_principal.merge(df_chatgpt, left_on='Nome', right_on='Nome da empresa', how='left')
df_principal = df_principal.drop(columns=['Nome da empresa'])
df_principal

# Renomear os nomes das colunas
df_principal = df_principal.rename(columns={'Idade (fundação ou início de operações)':'Idade'}).copy()
df_principal

# Renomear os nomes das colunas
df_principal = df_principal.rename(columns={'Idade (anos)':'Ano_de_fundacao'}).copy()
df_principal

df_principal['Cat_idade'] = df_principal['Ano_de_fundacao'].apply(lambda x: 'Mais de 100' if x > 100 else ('Menos de 50' if x < 50 else 'Entre 50 e 100'))
df_principal

"""##### **Dataset** df_principal"""

df_principal.head()

"""#### Iniciando as Análise no dataset que foi criado"""

# Calculando o maior valor
maior = df_principal['Variacao_rs'].max()

# Calculando o menor valor
menor = df_principal['Variacao_rs'].min()

# Calculando a média
media = df_principal['Variacao_rs'].mean()

# Calculando a média de quem subiu
media_subiu = df_principal[df_principal['Resultado'] == 'Subiu']['Variacao_rs'].mean()

# Calculando a média de quem desceu
media_desceu = df_principal[df_principal['Resultado'] == 'Desceu']['Variacao_rs'].mean()

# Imprimindo os resultados
print(f"Maior\tR$ {maior:,.2f}")
print(f"Menor\tR$ {menor:,.2f}")
print(f"Média\tR$ {media:,.2f}")
print(f"Média de quem subiu\tR$ {media_subiu:,.2f}")
print(f"Média de quem desceu\tR$ {media_desceu:,.2f}")

# Novo dataframe somente com os resultados que subiram
df_principal_subiu = df_principal[df_principal['Resultado'] == 'Subiu']
df_principal_subiu

# Agrupamento das variações por Segmentos
df_analise_segmento = df_principal_subiu.groupby('Segmento')['Variacao_rs'].sum().reset_index()
df_analise_segmento

# Agrupameto pelo resultado
df_analise_saldo = df_principal.groupby('Resultado')['Variacao_rs'].sum().reset_index()
df_analise_saldo

# Criando o primeiro gráfico com o resultado e as suas variações
fig = px.bar(df_analise_saldo, x='Resultado', y='Variacao_rs', text='Variacao_rs', title='Variação Reais por Resultado')
fig.show()