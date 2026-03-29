# PSD (USDA)

Production, Supply & Distribution — dados de produção, oferta e distribuição de commodities do USDA.

## Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **PSD**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| commodity | Texto | Sim | Nome da commodity em inglês (ex: Soybeans, Corn, Cotton) |
| country | Texto | Não | Código do país (default: BR) |
| market_year | Inteiro | Não | Ano-safra |

## Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal
- [x] Requer autenticação

## Autenticação

Esta fonte requer uma chave de API do USDA (`USDA_API_KEY`).

1. Obtenha a chave em https://apps.fas.usda.gov/PSDOnline
2. No plugin, acesse **Settings > Tokens**
3. Informe a chave no campo USDA_API_KEY

## Notas

- Fonte tabular. Nomes de commodities devem ser informados em inglês.
