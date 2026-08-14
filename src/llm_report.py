import os
from google import genai

def generate_ai_report(parceiro, metrics_df, winner, p_value):
    """Usa a API do Gemini para gerar a análise qualitativa."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    contexto = f"""
    Você é um Analista de Growth na Méliuz.
    Acabamos de rodar um Teste A/B de cashback para o Parceiro {parceiro}.

    DADOS AGREGADOS:
    {metrics_df.to_string()}

    ANÁLISE ESTATÍSTICA:
    - Vencedor pela Margem Líquida por Comprador: {winner}
    - P-Value (Bootstrap vs 2º lugar): {p_value:.4f}

    REGRAS DE DECISÃO (Significância):
    - p_value < 0.05: Alta Confiança
    - 0.05 <= p_value < 0.10: Confiança Moderada
    - p_value >= 0.10: Baixa Confiança (Inconclusivo)

    Crie um relatório executivo curto em Markdown contendo:
    1. Resumo dos Dados
    2. Interpretação da Margem vs Volume
    3. Recomendação Acionável de qual grupo escalar para 100% do tráfego.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contexto,
    )

    return response.text
