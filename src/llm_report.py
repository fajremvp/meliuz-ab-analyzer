import os
from google import genai

def generate_ai_report(parceiro, metrics_df, winner, p_value, recomendacao):
    """Usa a API do Gemini para gerar a análise qualitativa baseada na decisão determinística."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    contexto = f"""
    Você é um Analista de Growth na Méliuz.
    Acabamos de rodar um Teste A/B de cashback para o Parceiro {parceiro}.

    DADOS AGREGADOS:
    {metrics_df.to_string()}

    ANÁLISE ESTATÍSTICA:
    - Vencedor pela Margem Líquida por Comprador: {winner}
    - P-Value (Bootstrap vs 2º lugar): {p_value:.4f}

    RECOMENDAÇÃO OFICIAL (Já decidida pelo sistema, APENAS JUSTIFIQUE):
    - Ação a ser tomada: {recomendacao}

    Crie um relatório executivo curto em Markdown contendo:
    1. Resumo dos Dados
    2. Interpretação da Margem vs Volume
    3. Recomendação Acionável (Use a recomendação oficial acima e explique o porquê com base nos dados).
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contexto,
    )

    return response.text
