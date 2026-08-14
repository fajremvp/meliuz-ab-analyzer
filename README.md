# Méliuz A/B Analyzer

Ferramenta em Python para analisar testes A/B de cashback por parceiro e apoiar a decisão de qual variante deve ser escalada. Feita para o teste técnico de Estágio de Operações Integradas - Méliuz.

## O que ela faz

Dado um CSV de teste A/B (schema: `Data`, `Grupos de usuários`, `Parceiro`, `compradores`, `comissão`, `cashback`, `vendas totais`), a ferramenta:

1. Lê e limpa os dados (parsing de moeda em formato BR, remoção de duplicatas e linhas inválidas).
2. Calcula, por grupo/variante: compradores totais, comissão, cashback, vendas (GMV) e **margem líquida por comprador** (comissão − cashback, normalizada por comprador) — a métrica usada para decidir, em vez de volume bruto.
3. Roda um teste de significância por **bootstrap** (10.000 reamostragens), comparando o grupo com maior margem contra o segundo colocado, usando o **dia** como unidade estatística.
4. Aplica uma regra de decisão determinística (calculada em Python, não pelo LLM):
   - `p < 0.05` **e** volume de compradores do vencedor não abaixo da mediana → confiança **Alta**, recomenda escalar.
   - `p < 0.10` → confiança **Moderada**, escalar com monitoramento.
   - Caso contrário → **Baixa** confiança / inconclusivo.
5. Usa a API do Gemini **só para redigir** o relatório executivo em Markdown a partir da decisão já tomada - o LLM nunca decide o vencedor, apenas explica.
6. Registra o resultado (teste, vencedor, confiança, p-value) no Google Sheets, com fallback automático para um CSV local se as credenciais não estiverem configuradas.

## Arquitetura

```text
main.py                # CLI orquestrador
src/load.py            # leitura e limpeza do CSV
src/analyze.py         # métricas, bootstrap e regra de decisão (determinístico)
src/llm_report.py      # chamada ao Gemini para redigir o relatório
src/sheets.py          # grava no Google Sheets, com fallback para CSV
data/                  # datasets de entrada
reports/               # relatórios .md gerados (um por parceiro)
tracking/tests_log.csv # planilha de acompanhamento (fallback local)
```

O cálculo (métricas, teste estatístico, decisão) é 100% determinístico em Python - rodar o mesmo dataset duas vezes sempre dá o mesmo vencedor e o mesmo p-value. O Gemini entra só na etapa final, para transformar os números já decididos em relatório em Markdown. Isso mantém a solução auditável e reproduzível mesmo usando IA no pipeline.

## Como rodar

### 1. Pré-requisitos

- Python 3.11+
- Uma chave de API do Gemini ([Google AI Studio](https://aistudio.google.com/apikey))
- (Opcional) uma Service Account do Google Cloud com acesso de edição à planilha, para gravar direto no Sheets

### 2. Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuração

Copie `.env.example` para `.env` e preencha com sua própria chave:

```bash
cp .env.example .env
```

```env
GEMINI_API_KEY=sua_chave_aqui
GOOGLE_SHEET_ID=id_da_planilha_aqui   # opcional
```

Se quiser gravar direto no Google Sheets (em vez do fallback CSV), coloque o arquivo de credenciais da Service Account em `config/service_account.json` (compartilhe a planilha com o e-mail da service account). Sem isso, os resultados são salvos automaticamente em `tracking/tests_log.csv`.

### 4. Rodando uma análise

```bash
python main.py --file data/dataset_01_parceiroA.csv
```

O mesmo comando funciona para qualquer um dos três datasets fornecidos (ou um novo, desde que siga o mesmo schema) - não é necessário alterar código:

```bash
python main.py --file data/dataset_02_parceiroB.csv
python main.py --file data/dataset_03_parceiroC.csv
```

Cada execução gera:
- Um relatório em `reports/analise_<Parceiro>.md`
- Uma nova linha em `tracking/tests_log.csv` (ou na planilha do Google Sheets)

## Planilha de acompanhamento

📊 [Link da planilha (leitura pública)](https://docs.google.com/spreadsheets/d/1eKAPaw7eyRXPApi5KXRQacrniLZyiKXNNxFDQ7rSUbA/edit?usp=sharing)

Fallback local (sempre disponível, mesmo sem acesso ao Sheets):
[`tracking/tests_log.csv`](tracking/tests_log.csv)

## Relatórios gerados

- [`reports/analise_Parceiro_A.md`](reports/analise_Parceiro_A.md)
- [`reports/analise_Parceiro_B.md`](reports/analise_Parceiro_B.md)
- [`reports/analise_Parceiro_C.md`](reports/analise_Parceiro_C.md)

## Limitações conhecidas

- Os dados de entrada são agregados por dia, não por usuário - o teste de significância usa o dia como unidade amostral, o que limita o tamanho da amostra em testes muito curtos.
- A decisão de "inconclusivo" (p ≥ 0.10) não bloqueia a leitura do relatório, mas indica que mais dias de teste são recomendados antes de escalar com confiança total.
