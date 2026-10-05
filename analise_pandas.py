"""Versão alternativa da análise usando pandas (Requisito Opcional RO1).

Lê o transacoes.csv com pd.read_csv, aplica as mesmas regras de validação
da solução nativa, agrupa por mês com groupby e compara o resultado com o
relatorio.json gerado pelo notebook (os valores devem ser iguais).

Execução:  python analise_pandas.py
"""

import json

import numpy as np
import pandas as pd

CAMINHO_CSV = "transacoes.csv"
CAMINHO_JSON = "relatorio.json"
TIPOS_VALIDOS = ["credito", "debito"]
METRICAS = ["quantidade", "total_credito", "total_debito", "saldo",
            "media", "maior_valor", "menor_valor"]


def carregar_dados(caminho=CAMINHO_CSV):
    """Lê o CSV como texto puro (igual ao csv nativo) e remove espaços extras."""
    df = pd.read_csv(caminho, dtype=str, keep_default_na=False)
    return df.apply(lambda coluna: coluna.str.strip())


def limpar_dados(df):
    """Aplica as regras de validação e remove ids duplicados."""
    ids = pd.to_numeric(df["id"], errors="coerce")
    datas = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    valores = pd.to_numeric(df["valor"], errors="coerce")
    tipos = df["tipo"].str.lower()

    linha_valida = (
        ids.notna() & (ids % 1 == 0)
        & (df["cliente_id"] != "")
        & datas.notna() & df["data"].str.fullmatch(r"\d{4}-\d{2}-\d{2}")
        & tipos.isin(TIPOS_VALIDOS)
        & np.isfinite(valores) & (valores > 0)
    )
    limpo = df.assign(id=ids, data=datas, tipo=tipos, valor=valores)[linha_valida]
    limpo = limpo.drop_duplicates(subset="id", keep="first")
    return limpo.astype({"id": int})


def gerar_resumo_mensal(df):
    """Agrupa por mês (AAAA-MM) e calcula as mesmas métricas da versão nativa."""
    df = df.assign(
        mes=df["data"].dt.strftime("%Y-%m"),
        credito=df["valor"].where(df["tipo"] == "credito", 0.0),
        debito=df["valor"].where(df["tipo"] == "debito", 0.0),
    )
    resumo = df.groupby("mes").agg(
        quantidade=("id", "count"),
        total_credito=("credito", "sum"),
        total_debito=("debito", "sum"),
        media=("valor", "mean"),
        maior_valor=("valor", "max"),
        menor_valor=("valor", "min"),
    )
    resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]
    return resumo[METRICAS].round(2)


def carregar_resumo_nativo(caminho=CAMINHO_JSON):
    """Lê o resumo mensal da solução nativa a partir do relatorio.json."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return json.load(arquivo)["resumo_mensal"]
    except FileNotFoundError:
        print(f"'{caminho}' não encontrado: execute o notebook antes da comparação.")
        return None


def comparar_resultados(resumo_pandas, resumo_nativo):
    """Retorna True se pandas e solução nativa chegaram aos mesmos números."""
    nativo = pd.DataFrame(resumo_nativo).T[METRICAS].astype(float)
    mesmos_meses = list(nativo.index) == list(resumo_pandas.index)
    return mesmos_meses and np.allclose(nativo.values, resumo_pandas.values, atol=0.01)


def main(caminho_csv=CAMINHO_CSV, resumo_nativo=None):
    df = carregar_dados(caminho_csv)
    limpo = limpar_dados(df)
    print("===== ANÁLISE COM PANDAS =====")
    print(f"Linhas lidas: {len(df)} | Válidas: {len(limpo)} | Inválidas: {len(df) - len(limpo)}\n")

    resumo = gerar_resumo_mensal(limpo)
    print(resumo.to_string())

    if resumo_nativo is None:
        resumo_nativo = carregar_resumo_nativo()
    if resumo_nativo is not None:
        iguais = comparar_resultados(resumo, resumo_nativo)
        status = "IGUAIS ✅" if iguais else "DIFERENTES ❌"
        print(f"\nComparação com a solução nativa: valores {status}")
    return resumo


if __name__ == "__main__":
    main()
