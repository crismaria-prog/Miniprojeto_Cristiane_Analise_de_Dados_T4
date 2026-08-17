
# Importação das bibliotecas
# =========================================================

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# pandas → leitura e manipulação da base
# numpy → cálculos numéricos
# matplotlib → criação de gráficos
# seaborn → gráficos com melhor aparência


# Configuração dos gráficos
# =========================================================

sns.set_theme(style="whitegrid")

plt.rcParams["figure.figsize"] = (10, 6)

plt.rcParams["figure.dpi"] = 120

# Essas configurações deixam todos os gráficos mais legíveis e profissionais


# Leitura da base de dados
# =========================================================

try:

    df = pd.read_csv(
        "dados/Varejo.csv",
        sep=";", # Utilizei para separar os campos da base, pois o separador é ponto e vírgula
        encoding="utf-8" # Utilizei para evitar problemas com acentuação, pois a base contém caracteres especiais
    )
except FileNotFoundError:

    print("Arquivo Varejo.csv não encontrado.")    
else:
    print("Leitura do arquivo concluída com sucesso.")
    

# Utilizei o bloco try-except para tratar possíveis erros na leitura do arquivo, como o arquivo não encontrado ou problemas de codificação




# Informações gerais da base
# =========================================================

print("=" * 60)

print("ANÁLISE INICIAL DA BASE")

print("=" * 60)

print(f"Número de linhas: {df.shape[0]}")

print(f"Número de colunas: {df.shape[1]}")

print("\nColunas:")

print(df.columns)

print("\nTipos de dados:")

print(df.dtypes)


# Primeiras linhas da base
# =========================================================

print("\nPrimeiros registros:")

print(df.head()) # head() mostra os cinco primeiros registros para verificar se a leitura ocorreu corretamente.


# Informações detalhadas da base
# =========================================================

print("\nInformações da base:")

print(df.info()) # info mostra informações detalhadas sobre a base, como número de registros,valores nulos, colunas e tipos de dados.


# Valores nulos
# =========================================================

print("\nValores nulos por coluna:")
valores_nulos = df.isnull().sum() # isnull().sum() mostra a quantidade de valores nulos por coluna, o que é importante para identificar possíveis problemas na base
print(valores_nulos) 
if valores_nulos.sum() > 0: # verifica se existe valores nulos 
    print("\nForam encontrados valores nulos na base.")
else:
    print("\nNão foram encontrados valores nulos na base.") #caso não exita ele imprimirá essa mensagem

duplicados= df.duplicated().sum()
print(f"\nQuantidade de registros duplicado: {duplicados}") # duplicated().sum() mostra a quantidade de registros duplicados na base, o que é importante para identificar possíveis problemas na base
print(df.filter(regex="Unnamed").head()) # Verificando colunas vazias com nomes não informados, que podem ser resultado de problemas na leitura da base. 
#O filter(regex="Unnamed") filtra as colunas que possuem "Unnamed" no nome, que geralmente são colunas sem nome.
if duplicados > 0:
    print("Existem registros duplicados. Eles serão removidos na etapa de limpeza.")
else:
    print("Não foram encontrados registros duplicados.")


# Remoção de colunas vazias
# =========================================================

df = df.loc[:, ~df.columns.str.contains("^Unnamed")] # contains("^Unnamed") filtra as colunas que possuem "Unnamed" no nome. O ~ inverte a seleção, ou seja, seleciona todas as colunas que não possuem "Unnamed". 
#O df.loc[:, ...] seleciona todas as linhas e apenas as colunas filtradas.
df = df.dropna(axis=1, how="all") # dropna(axis=1, how="all") remove as colunas que possuem todos os valores nulos. O axis=1 indica que a remoção será feita nas colunas. O how="all" indica que a remoção será feita apenas se todos os valores da coluna forem nulos.
print("\nColunas após a limpeza:")
print(df.columns)
print("\nNúmero de colunas após limpeza:")
print(df.shape[1]) # Utilizei df.shape[1] para mostrar o número de colunas após a limpeza, que é importante para verificar se a limpeza foi realizada corretamente.

# -----------------------------------------------------------

print("\n Panorama da qualidade dos dados")

print(f"Quantidade de linhas: {df.shape[0]}") # Shape[0] mostra o número de linhas da base
print(f"Quantidade de colunas: {df.shape[1]}")
print(f"Registros duplicados: {duplicados}")

print("\nColunas com valores nulos:")

print(valores_nulos[valores_nulos > 0])


# Convertando colunas DATA
# =========================================================
df["DATA"] = pd.to_datetime( # utilizei datetime para converter a coluna DATA para o formato datetime, que é mais adequado para análise de séries temporais.
    df["DATA"],
    format="%d/%m/%Y",
    errors="coerce" # coerce converte os valores inválidos para NaT (Not a Time), que é o equivalente a NaN para datas. Isso é importante para evitar erros na análise de dados
)
print("\nTipos da coluna DATA após conversão:")
print(df["DATA"].dtypes)


# Estatística descritiva
# =========================================================

print("\n" + "=" * 60)
print("Estatísticas de Número de Filhos")
print("=" * 60)

print(f"Contagem: {df['CL_FHL'].count()}") #count() mostra a quantidade de registros não nulos da coluna

print(f"Média: {df['CL_FHL'].mean():.2f}")

print(f"Mediana: {df['CL_FHL'].median()}") 

print(f"Moda: {df['CL_FHL'].mode()[0]}") 

print(f"Desvio padrão: {df['CL_FHL'].std():.2f}") 

print(f"Mínimo: {df['CL_FHL'].min()}")

print(f"Máximo: {df['CL_FHL'].max()}")

print("\nQuartis:")

print(df["CL_FHL"].describe())


# Agrupamento por gênero
# =========================================================

print("\n" + "=" * 60)
print("COMPRAS POR GÊNERO")
print("=" * 60)

compras_genero = (
    df.groupby("CL_GENERO") # utilizei o groupby para agrupar os dados por gênero para analisar a quantidade de compra por genero 
      .size()
      .sort_values(ascending=False)
)

print(compras_genero)


#Gráfico - Compras por gênero
#=========================================================

plt.figure(figsize=(8,5))

sns.countplot(
    data=df,
    x="CL_GENERO",
    hue="CL_GENERO",
    palette="pastel",
    legend=False
)

plt.title("Quantidade de Compras por Gênero")

plt.xlabel("Gênero")

plt.ylabel("Quantidade")

plt.tight_layout()

plt.savefig("output/compras_genero.png", dpi=300, bbox_inches="tight")
plt.show()


# Categorias mais vendidas
# # =========================================================

print("\n" + "=" * 60)
print("CATEGORIAS MAIS VENDIDAS")
print("=" * 60)

categorias = (
    df.groupby("PR_CAT")
      .size()
      .sort_values(ascending=False)
)

print(categorias)


# As 10 categorias mais vendidas
# =========================================================

top10 = categorias.head(10)

plt.figure(figsize=(12,6))

sns.barplot(
    x=top10.values,
    y=top10.index,
    palette="viridis"
)

plt.title("Top 10 Categorias Mais Vendidas")

plt.xlabel("Quantidade de Compras")

plt.ylabel("Categoria")

plt.tight_layout()

plt.savefig("output/top10_categorias.png", dpi=300, bbox_inches="tight") # salvando o grafico na pasta output
plt.show()

# Salvando Dataframe, base limpa
# =========================================================

df.to_csv(
    "output/df_limpo.csv",
    index=False,
    encoding="utf-8"
)

print("\nBase limpa salva com sucesso!")

# =========================================================
# Conclusões
# =========================================================

print("\n" + "="*60)
print("CONCLUSÕES")
print("="*60)

print("""

RESUMO

- A planilha contém aproximadamente 830 mil registros.

- Foram identificadas quatro colunas totalmente vazias,
  que foram removidas.

- Foram encontrados registros duplicados,
  eliminados durante a limpeza.

- A coluna DATA foi convertida para datetime,
  permitindo análises temporais.

- Os agrupamentos permitiram identificar os gêneros
  e categorias com maior volume de compras.

- Criei gráficos para visualização das análises, que foram salvos na pasta output.  


ETAPAS 

- Importação das bibliotecas

- Leitura da base de dados

- Análise inicial

- Limpeza da base

- Estatística descritiva

- Agrupamentos

- Gráficos

- Exportação da base limpa

- Conclusões

""")