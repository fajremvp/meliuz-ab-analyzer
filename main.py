import argparse
import os
from dotenv import load_dotenv

from src.load import load_dataset
from src.analyze import compute_metrics, get_statistical_result
from src.sheets import log_result
from src.llm_report import generate_ai_report

load_dotenv()

def main():
    p = argparse.ArgumentParser(description="Méliuz AI-Native A/B Test Analyzer")
    p.add_argument("--file", required=True, help="Caminho para o CSV do parceiro")
    args = p.parse_args()

    print(f"Buscando dados em: {args.file}...")
    df = load_dataset(args.file)
    parceiro = df["parceiro"].iloc[0]

    # Criar descrição dinâmica baseada nos dados do teste
    num_variantes = df['grupo'].nunique()
    dias_teste = df['data'].nunique()
    descricao = f"Teste de cashback com {num_variantes} variantes durante {dias_teste} dias."

    print("Calculando métricas e executando Bootstrap...")
    metrics = compute_metrics(df)
    winner, p_value, recomendacao, confianca = get_statistical_result(df, metrics)

    print("Invocando Agente de IA para redação do relatório...")
    report_md = generate_ai_report(parceiro, metrics, winner, p_value, recomendacao)

    # Salvar o relatório Markdown
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/analise_{parceiro.replace(' ', '_')}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"\n[!] Relatório executivo gerado: {report_path}")

    # Gravar na planilha/CSV
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    log_result(
        nome_teste=f"Cashback A/B - {parceiro}",
        descricao=descricao,
        resultado=winner,
        decisao=recomendacao,
        confianca=confianca,
        p_value=p_value,
        sheet_id=sheet_id
    )

if __name__ == "__main__":
    main()
