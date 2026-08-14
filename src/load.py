import pandas as pd
import re

def parse_currency_brl(val):
    """Converte 'R$ 1.234,56' -> 1234.56 de forma segura."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    s = re.sub(r"[R$\s]", "", s)
    if s == "":
        return None

    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def load_dataset(path: str) -> pd.DataFrame:
    """Lê o CSV, padroniza as colunas e limpa os dados sujos."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    rename_map = {
        "data": "data", "grupos de usuários": "grupo", "grupos de usuarios": "grupo",
        "parceiro": "parceiro", "compradores": "compradores",
        "comissão": "comissao", "cashback": "cashback", "vendas totais": "vendas_totais",
    }
    df = df.rename(columns=rename_map)

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["comissao"] = df["comissao"].apply(parse_currency_brl)
    df["cashback"] = df["cashback"].apply(parse_currency_brl)
    df["vendas_totais"] = df["vendas_totais"].apply(parse_currency_brl)
    df["compradores"] = pd.to_numeric(df["compradores"], errors="coerce")

    df = df.dropna(subset=["data", "grupo", "comissao", "cashback", "vendas_totais", "compradores"])
    df = df.drop_duplicates(subset=["data", "grupo", "parceiro"])
    df = df[(df["compradores"] >= 0) & (df["vendas_totais"] >= 0) & (df["cashback"] >= 0)]

    return df.reset_index(drop=True)
