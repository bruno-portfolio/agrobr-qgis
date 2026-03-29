# PSD (USDA)

Production, Supply & Distribution — dados de producao, oferta e distribuicao de commodities do USDA.

## Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **PSD**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

## Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| commodity | Texto | Sim | Nome da commodity em ingles (ex: Soybeans, Corn, Cotton) |
| country | Texto | Nao | Codigo do pais (default: BR) |
| market_year | Inteiro | Nao | Ano-safra |

## Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal
- [x] Requer autenticacao

## Autenticacao

Esta fonte requer uma chave de API do USDA (`USDA_API_KEY`).

1. Obtenha a chave em https://apps.fas.usda.gov/PSDOnline
2. No plugin, acesse **Settings > Tokens**
3. Informe a chave no campo USDA_API_KEY

## Notas

- Fonte tabular. Nomes de commodities devem ser informados em ingles.
