import numpy as np
import pandas as pd

def compute_metrics(df):
    """Calcula as métricas totais e a margem líquida por grupo."""
    grp = df.groupby("grupo").agg(
        dias=("data", "nunique"),
        compradores_total=("compradores", "sum"),
        comissao_total=("comissao", "sum"),
        cashback_total=("cashback", "sum"),
        vendas_total=("vendas_totais", "sum"),
    ).reset_index()

    grp["margem_liquida"] = grp["comissao_total"] - grp["cashback_total"]
    grp["margem_por_comprador"] = grp["margem_liquida"] / grp["compradores_total"]
    return grp

def daily_margin_per_buyer(df, grupo):
    """Retorna o array da margem diária por comprador para o bootstrap."""
    d = df[df["grupo"] == grupo].copy()
    d["margem_dia"] = d["comissao"] - d["cashback"]
    d["margem_por_comprador_dia"] = d["margem_dia"] / d["compradores"].replace(0, np.nan)
    return d["margem_por_comprador_dia"].dropna().values

def bootstrap_diff(a, b, n_boot=10000, seed=42):
    """Teste de significância por re-amostragem (Bootstrap)."""
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(n_boot):
        sa = rng.choice(a, size=len(a), replace=True)
        sb = rng.choice(b, size=len(b), replace=True)
        diffs.append(sa.mean() - sb.mean())

    diffs = np.array(diffs)
    p_value = min((diffs <= 0).mean(), (diffs >= 0).mean()) * 2
    return p_value

def get_statistical_result(df, metrics_df):
    """Compara o melhor e o segundo melhor grupo."""
    ranked = metrics_df.sort_values("margem_por_comprador", ascending=False)
    winner = ranked.iloc[0]["grupo"]

    if len(ranked) < 2:
        return winner, 1.0

    runner_up = ranked.iloc[1]["grupo"]

    va = daily_margin_per_buyer(df, winner)
    vb = daily_margin_per_buyer(df, runner_up)

    p_value = bootstrap_diff(va, vb)
    return winner, p_value
