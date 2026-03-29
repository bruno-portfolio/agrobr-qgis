# Indicadores (CEPEA)

Indicadores de preços agropecuários CEPEA/ESALQ.

## Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **Indicadores**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| produto | Produto | Sim | Ex: Soja, Boi Gordo, Milho, Café, Açúcar |
| praca | Texto | Não | Praça de referência |
| inicio | Data | Não | Data início |
| fim | Data | Não | Data fim |

## Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [x] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

## Notas

Fonte tabular (sem geometria). Use o filtro temporal para séries históricas de preço.
