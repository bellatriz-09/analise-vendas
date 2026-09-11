[README.md](https://github.com/user-attachments/files/32107523/README.md)
# 📊 Análise de Vendas de E-commerce

Projeto de análise exploratória de dados (EDA) de vendas de uma loja virtual fictícia, usando **Python, pandas, matplotlib e seaborn**.

## 🎯 Objetivo

Simular o trabalho de um analista de dados: partir de um conjunto de dados "sujo" (com duplicatas e valores ausentes), limpá-lo, calcular métricas de negócio e responder perguntas como:

- Qual foi a receita ao longo do tempo? Existe sazonalidade?
- Quais categorias de produto mais vendem?
- Como as vendas se distribuem entre as regiões do Brasil?
- Qual forma de pagamento gera o maior ticket médio?

## 🗂️ Estrutura do projeto

```
analise-vendas-ecommerce/
├── data/
│   └── vendas.csv              # dataset (gerado por src/gerar_dados.py)
├── images/                     # gráficos gerados pela análise
├── src/
│   ├── gerar_dados.py          # gera o dataset sintético
│   └── analise.py              # limpeza de dados + análise + gráficos
├── requirements.txt
└── README.md
```

## 📦 Sobre os dados

O dataset é **sintético** (gerado por código, não são dados reais de nenhuma empresa), com 5.000 pedidos simulados entre 2024 e 2025, incluindo:

- Categoria do produto, preço, quantidade e valor total
- Região do Brasil e forma de pagamento
- Sazonalidade proposital em datas comemorativas (Dia das Mães, Namorados, Black Friday, Natal)
- Sujeira proposital nos dados (linhas duplicadas e valores nulos em `forma_pagamento`), para exercitar a etapa de limpeza

## 🚀 Como rodar

```bash
pip install -r requirements.txt
python src/gerar_dados.py   # gera data/vendas.csv
python src/analise.py       # roda a análise e salva os gráficos em images/
```

## 📈 Principais insights

- **Sazonalidade forte**: a receita mensal mostra picos claros em maio, junho, novembro e dezembro, associados a datas comemorativas.
- **Eletrônicos domina a receita**: mesmo não sendo a categoria com mais pedidos, é a que tem maior receita total, por ter o ticket médio mais alto.
- **Concentração regional**: Sudeste e Nordeste respondem pela maior parte dos pedidos.
- **Cartão de crédito** é a forma de pagamento predominante e também a de maior ticket médio.

### Gráficos gerados

| Receita mensal | Receita por categoria |
|---|---|
| ![Receita mensal](images/receita_mensal.png) | ![Receita por categoria](images/receita_por_categoria.png) |

| Vendas por região | Ticket médio por pagamento |
|---|---|
| ![Vendas por região](images/vendas_por_regiao.png) | ![Ticket médio](images/ticket_medio_pagamento.png) |

## 🛠️ Tecnologias

- Python 3
- pandas
- matplotlib
- seaborn

## 💡 Possíveis próximos passos

- Adicionar um dashboard interativo (Streamlit ou Plotly Dash)
- Segmentação de clientes (RFM)
- Previsão de vendas futuras com um modelo simples de série temporal
