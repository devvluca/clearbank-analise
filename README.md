# ClearBank — Análise Financeira com Python

Projeto do desafio final do módulo de Python para análise de dados. O notebook lê o histórico mensal de transações dos clientes da fintech ClearBank (`transacoes.csv`), **valida e limpa** os registros problemáticos (campos vazios, valores inválidos, datas mal formatadas e ids duplicados), calcula **métricas financeiras por mês**, sinaliza **transações suspeitas** (acima de R$ 10.000,00) e exporta o resultado em JSON.

A solução principal usa só a biblioteca padrão (`csv`, `json`, `datetime`, `math`, `os`).

## Estrutura

```
clearbank-analise/
├── desafio-final.ipynb   # notebook principal, com as saídas salvas
├── transacoes.csv        # dados de entrada (20 válidos, 10 inválidos, 4 meses)
├── relatorio.json        # saída gerada pelo notebook
├── analise_pandas.py     # (opcional RO1) mesma análise com pandas + comparação
├── grafico.png           # (opcional RO2) saldo mensal com matplotlib
└── README.md
```

## Como executar

**Google Colab**
1. Abra o `desafio-final.ipynb` no Colab (File → Upload notebook).
2. (Opcional) Faça upload do `transacoes.csv` e do `analise_pandas.py` para a pasta do Colab. Se o CSV não existir, a célula 0 cria o arquivo automaticamente.
3. Rode tudo em ordem: Runtime → Run all.

**Jupyter local** (Python 3.10+)

```bash
pip install pandas matplotlib notebook
```

```bash
jupyter notebook desafio-final.ipynb
```

Depois, Kernel → Restart & Run All. A versão com pandas também roda sozinha com `python analise_pandas.py` (depois que o `relatorio.json` já foi gerado).

## O que o notebook gera

- **Relatório no terminal**: resumo da limpeza (linhas lidas, válidas e inválidas, com o motivo de cada descarte), período analisado, métricas de cada mês (quantidade, total de crédito, total de débito, saldo, média, maior e menor valor) e a lista de transações suspeitas.
- **`relatorio.json`**: o mesmo conteúdo em formato estruturado (`gerado_em`, totais, `periodo`, `resumo_mensal` e `transacoes_suspeitas`).
- **`grafico.png`**: gráfico de barras com o saldo mensal (crédito − débito).
- **Comparação pandas × nativo**: confirma que as duas abordagens chegam aos mesmos valores.

## Organização do código

| Etapa | Funções |
|---|---|
| Leitura | `ler_transacoes()` |
| Validação | `validar_id()`, `validar_data()`, `validar_valor()`, `validar_transacao()`, `limpar_transacoes()` |
| Datas | `extrair_mes()`, `calcular_periodo()` |
| Métricas | `agrupar_por_mes()`, `calcular_metricas_mes()`, `identificar_suspeitas()`, `gerar_relatorio()` |
| Saída | `salvar_json()`, `formatar_moeda()`, `exibir_relatorio()` |
| Execução | `executar_analise()` |

`try/except` aparece na abertura do CSV (`FileNotFoundError`), na conversão do `id` e do `valor` (`ValueError`), na conversão da data com `strptime` (`ValueError`) e na gravação do JSON (`OSError`).
