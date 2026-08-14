# Relatório Executivo: Teste A/B de Cashback - Parceiro A

Como Analista de Growth na Méliuz, analisei os resultados do Teste A/B de cashback rodado ao longo de 92 dias para o **Parceiro A**. Abaixo, apresento o resumo dos dados, a análise de trade-off entre margem e volume, e a recomendação oficial baseada na significância estatística.

---

## 1. Resumo dos Dados

O teste comparou três grupos com diferentes estruturas de cashback ao longo de um período de 3 meses:

| Grupo | Compradores | Vendas Totais (GMV) | Comissão Total | Cashback Total | Margem Líquida | Margem por Comprador |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Grupo 1** | 9.633 | R$ 5.605.173,00 | R$ 638.135,00 | R$ 233.424,00 | **R$ 404.711,00** | **R$ 42,01** |
| **Grupo 2** | 10.814 | R$ 6.423.096,00 | R$ 728.178,00 | R$ 370.659,00 | R$ 357.519,00 | R$ 33,06 |
| **Grupo 3** | 11.410 | R$ 6.785.856,00 | R$ 767.887,00 | R$ 503.600,00 | R$ 264.287,00 | R$ 23,16 |

---

## 2. Interpretação da Margem vs. Volume

Os dados evidenciam um claro trade-off entre **volume de vendas** e **eficiência de margem**:
* **Efeito Volume:** À medida que o cashback aumentou (do Grupo 1 para o Grupo 3), houve um crescimento natural no número de compradores e no volume de vendas (GMV).
* **Efeito Margem (Canibalização):** No entanto, o aumento na comissão gerada não acompanhou o salto nos custos de cashback. O **Grupo 3** obteve o maior GMV (R$ 6,78M), mas apresentou a menor margem líquida (R$ 264,28k) devido à alta distribuição de cashback (R$ 503,60k).
* **Eficiência:** O **Grupo 1**, com uma oferta de cashback mais enxuta, gerou o menor volume bruto, mas foi altamente eficiente, entregando a maior **Margem Líquida Total (R$ 404.711,00)** e a maior **Margem por Comprador (R$ 42,01)**.

O teste estatístico (Bootstrap) comparando o 1º e o 2º lugar apresentou um **P-Value de 0.0000**, confirmando com 100% de confiabilidade estatística que a superioridade do Grupo 1 na margem por comprador não é fruto do acaso.

---

## 3. Recomendação Acionável

> **Ação Tomada:** Escalar Grupo 1 (com monitoramento).

### Por que esta é a melhor decisão?
O objetivo de negócio da Méliuz é maximizar a rentabilidade sustentável. Embora os Grupos 2 e 3 movimentem mais volume bruto para o parceiro, eles sacrificam a rentabilidade da Méliuz ao subsidiar um cashback excessivo que não se paga através das comissões recebidas. 

O **Grupo 1** provou ser o único modelo financeiramente saudável a longo prazo, maximizando o lucro bruto retido por usuário ativo. 

**Próximos passos:**
1. **Escalar o Grupo 1** como a regra padrão de cashback para o Parceiro A.
2. **Monitorar** a retenção dos compradores e o comportamento do parceiro nas próximas semanas para garantir que a menor agressividade de oferta não impacte negativamente o share of wallet a médio prazo.