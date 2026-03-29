# Indicadores (CEPEA)

Indicadores de precos agropecuarios CEPEA/ESALQ.

## Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **Indicadores**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

## Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| produto | Produto | Sim | Ex: Soja, Boi Gordo, Milho, Cafe, Acucar |
| praca | Texto | Nao | Praca de referencia |
| inicio | Data | Nao | Data inicio |
| fim | Data | Nao | Data fim |

## Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [x] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

## Notas

Fonte tabular (sem geometria). Use o filtro temporal para series historicas de preco.
