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

    DIRETRIZ DE ESCRITA IMPORTANTE:
    - Nunca use linguagem de certeza absoluta em estatística (ex: "100% de certeza" ou "irrefutável"). Prefira "alta confiança estatística" ou "altamente improvável ser ao acaso".
    - NUNCA invente ou adicione datas no cabeçalho (como "Outubro de 2023"). Mantenha apenas o nome do Parceiro e o período de dias.
    """

    chat = client.chats.create(model="gemini-3.5-flash-lite")
    response = chat.send_message(contexto)

    return response.text
