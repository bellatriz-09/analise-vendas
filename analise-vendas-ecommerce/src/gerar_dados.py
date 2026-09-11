"""
gerar_dados.py

Gera um dataset SINTÉTICO (fictício, mas realista) de vendas de e-commerce,
simulando 2 anos de pedidos, com sazonalidade (picos em datas comemorativas),
várias categorias de produto, regiões do Brasil e formas de pagamento.

Por que dados sintéticos?
Como este projeto roda em um ambiente sem acesso à internet para baixar
datasets públicos (ex: Olist), geramos os dados aqui mesmo com regras que
imitam um comportamento real de vendas. Isso não muda o objetivo do projeto:
o que importa é o processo de análise (limpeza, agregação, visualização),
que é o mesmo independentemente da origem dos dados.
"""

import numpy as np
import pandas as pd

# Semente fixa: garante que, toda vez que rodarmos o script, os "números
# aleatórios" gerados sejam sempre os mesmos. Isso torna o projeto reprodutível.
np.random.seed(42)

# --- 1. Configuração básica -------------------------------------------------

N_PEDIDOS = 5000

categorias = {
    "Eletrônicos": (150, 3500),
    "Moda": (40, 400),
    "Casa e Decoração": (30, 900),
    "Livros": (20, 120),
    "Beleza": (15, 250),
    "Esporte e Lazer": (25, 600),
}

regioes = ["Sudeste", "Nordeste", "Sul", "Centro-Oeste", "Norte"]
# Pesos: Sudeste e Nordeste concentram mais pedidos (mais parecido com a
# distribuição populacional/e-commerce real no Brasil)
pesos_regioes = [0.42, 0.25, 0.18, 0.09, 0.06]

pagamentos = ["Cartão de Crédito", "Pix", "Boleto", "Cartão de Débito"]
pesos_pagamentos = [0.55, 0.30, 0.08, 0.07]

# --- 2. Datas com sazonalidade ----------------------------------------------

data_inicio = pd.Timestamp("2024-01-01")
data_fim = pd.Timestamp("2025-12-31")
dias_totais = (data_fim - data_inicio).days

# Sorteamos um "dia base" para cada pedido, mas damos peso maior a datas
# comemorativas (Dia das Mães, Black Friday, Natal) para simular picos de venda.
dias_normais = np.random.randint(0, dias_totais, size=int(N_PEDIDOS * 0.75))

datas_especiais = []
for ano in [2024, 2025]:
    picos = [
        pd.Timestamp(f"{ano}-05-10"),  # Dia das Mães
        pd.Timestamp(f"{ano}-06-12"),  # Dia dos Namorados
        pd.Timestamp(f"{ano}-11-28"),  # Black Friday
        pd.Timestamp(f"{ano}-12-20"),  # Natal
    ]
    for pico in picos:
        # gera pedidos concentrados em uma janela de +-4 dias ao redor do pico
        offsets = np.random.normal(loc=0, scale=1.5, size=int(N_PEDIDOS * 0.25 / 8))
        for off in offsets:
            dia = pico + pd.Timedelta(days=round(off))
            if data_inicio <= dia <= data_fim:
                datas_especiais.append((dia - data_inicio).days)

dias_pedidos = np.concatenate([dias_normais, np.array(datas_especiais, dtype=int)])
np.random.shuffle(dias_pedidos)

# Garante exatamente N_PEDIDOS datas: se sobrar, corta; se faltar (caso raro),
# completa sorteando dias aleatórios extras.
if len(dias_pedidos) >= N_PEDIDOS:
    dias_pedidos = dias_pedidos[:N_PEDIDOS]
else:
    faltam = N_PEDIDOS - len(dias_pedidos)
    extra = np.random.randint(0, dias_totais, size=faltam)
    dias_pedidos = np.concatenate([dias_pedidos, extra])

datas = [data_inicio + pd.Timedelta(days=int(d)) for d in dias_pedidos]

# --- 3. Monta o restante das colunas -----------------------------------------

lista_categorias = list(categorias.keys())
cat_sorteadas = np.random.choice(lista_categorias, size=N_PEDIDOS)

precos = []
for cat in cat_sorteadas:
    preco_min, preco_max = categorias[cat]
    # distribuição log-normal: a maioria dos preços fica mais perto do mínimo,
    # com alguns produtos mais caros puxando a média para cima (comum em e-commerce)
    preco = np.random.triangular(preco_min, preco_min * 1.3, preco_max)
    precos.append(round(preco, 2))

quantidades = np.random.choice([1, 1, 1, 2, 2, 3, 4], size=N_PEDIDOS)

df = pd.DataFrame({
    "id_pedido": range(1, N_PEDIDOS + 1),
    "data": datas,
    "categoria": cat_sorteadas,
    "preco_unitario": precos,
    "quantidade": quantidades,
    "regiao": np.random.choice(regioes, size=N_PEDIDOS, p=pesos_regioes),
    "forma_pagamento": np.random.choice(pagamentos, size=N_PEDIDOS, p=pesos_pagamentos),
})

df["valor_total"] = (df["preco_unitario"] * df["quantidade"]).round(2)

# Introduz de propósito alguns problemas comuns de dados reais, para o
# projeto também mostrar uma etapa de limpeza de dados (muito cobrado em
# entrevistas e em portfólios):
# - algumas linhas duplicadas
# - alguns valores nulos em forma_pagamento
idx_duplicar = np.random.choice(df.index, size=15, replace=False)
df = pd.concat([df, df.loc[idx_duplicar]], ignore_index=True)

idx_nulos = np.random.choice(df.index, size=25, replace=False)
df.loc[idx_nulos, "forma_pagamento"] = None

df = df.sort_values("data").reset_index(drop=True)

df.to_csv("data/vendas.csv", index=False)
print(f"Dataset gerado com {len(df)} linhas em data/vendas.csv")
