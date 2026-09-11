"""
analise.py

Análise exploratória de dados de vendas de um e-commerce fictício.

Etapas:
1. Carregar os dados
2. Limpar (duplicatas, valores nulos)
3. Calcular métricas de negócio
4. Gerar gráficos que respondem perguntas de negócio
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Estilo visual dos gráficos (deixa tudo mais legível e consistente)
sns.set_theme(style="whitegrid")
PALETA = "viridis"


def carregar_e_limpar(caminho_csv: str) -> pd.DataFrame:
    """Carrega o CSV e aplica limpeza básica de dados."""
    df = pd.read_csv(caminho_csv, parse_dates=["data"])

    linhas_antes = len(df)

    # Remove pedidos duplicados (mesmo id_pedido aparecendo mais de uma vez)
    df = df.drop_duplicates(subset="id_pedido")

    # Preenche forma_pagamento ausente com "Não informado" em vez de
    # descartar a linha inteira — perder o pedido todo por causa de uma
    # coluna faltando jogaria fora dados de vendas válidos.
    df["forma_pagamento"] = df["forma_pagamento"].fillna("Não informado")

    linhas_depois = len(df)
    print(f"Limpeza: {linhas_antes} linhas -> {linhas_depois} linhas "
          f"({linhas_antes - linhas_depois} duplicadas removidas)")

    # Colunas auxiliares de tempo, úteis para agrupar por mês/dia da semana
    df["ano_mes"] = df["data"].dt.to_period("M").astype(str)
    df["dia_semana"] = df["data"].dt.day_name()

    return df


def metricas_gerais(df: pd.DataFrame) -> None:
    """Imprime um resumo das principais métricas de negócio."""
    receita_total = df["valor_total"].sum()
    ticket_medio = df["valor_total"].mean()
    total_pedidos = df["id_pedido"].nunique()

    print("\n=== Resumo geral ===")
    print(f"Receita total:      R$ {receita_total:,.2f}")
    print(f"Total de pedidos:   {total_pedidos}")
    print(f"Ticket médio:       R$ {ticket_medio:,.2f}")

    print("\n=== Receita por categoria ===")
    print(
        df.groupby("categoria")["valor_total"]
        .sum()
        .sort_values(ascending=False)
        .apply(lambda x: f"R$ {x:,.2f}")
    )


def grafico_receita_mensal(df: pd.DataFrame, caminho_saida: str) -> None:
    """Evolução da receita mês a mês (mostra sazonalidade)."""
    receita_mensal = df.groupby("ano_mes")["valor_total"].sum()

    plt.figure(figsize=(11, 5))
    receita_mensal.plot(kind="line", marker="o", color="#2b6cb0")
    plt.title("Receita mensal (2024–2025)")
    plt.xlabel("Mês")
    plt.ylabel("Receita (R$)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=120)
    plt.close()


def grafico_receita_por_categoria(df: pd.DataFrame, caminho_saida: str) -> None:
    """Ranking de categorias por receita total."""
    receita_categoria = (
        df.groupby("categoria")["valor_total"].sum().sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))
    sns.barplot(
        x=receita_categoria.values,
        y=receita_categoria.index,
        hue=receita_categoria.index,
        palette=PALETA,
        legend=False,
    )
    plt.title("Receita total por categoria de produto")
    plt.xlabel("Receita (R$)")
    plt.ylabel("Categoria")
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=120)
    plt.close()


def grafico_vendas_por_regiao(df: pd.DataFrame, caminho_saida: str) -> None:
    """Distribuição de pedidos por região do país."""
    pedidos_regiao = df["regiao"].value_counts()

    plt.figure(figsize=(7, 7))
    plt.pie(
        pedidos_regiao.values,
        labels=pedidos_regiao.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette(PALETA, len(pedidos_regiao)),
    )
    plt.title("Distribuição de pedidos por região")
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=120)
    plt.close()


def grafico_ticket_medio_pagamento(df: pd.DataFrame, caminho_saida: str) -> None:
    """Ticket médio por forma de pagamento."""
    ticket_pagamento = (
        df.groupby("forma_pagamento")["valor_total"].mean().sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    sns.barplot(
        x=ticket_pagamento.index,
        y=ticket_pagamento.values,
        hue=ticket_pagamento.index,
        palette=PALETA,
        legend=False,
    )
    plt.title("Ticket médio por forma de pagamento")
    plt.xlabel("Forma de pagamento")
    plt.ylabel("Ticket médio (R$)")
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=120)
    plt.close()


def main():
    df = carregar_e_limpar("data/vendas.csv")
    metricas_gerais(df)

    grafico_receita_mensal(df, "images/receita_mensal.png")
    grafico_receita_por_categoria(df, "images/receita_por_categoria.png")
    grafico_vendas_por_regiao(df, "images/vendas_por_regiao.png")
    grafico_ticket_medio_pagamento(df, "images/ticket_medio_pagamento.png")

    print("\nGráficos salvos na pasta images/")


if __name__ == "__main__":
    main()
