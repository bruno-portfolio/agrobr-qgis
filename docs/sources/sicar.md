# Fontes SICAR

Dados do Sistema Nacional de Cadastro Ambiental Rural.

---

## Imoveis Rurais (SICAR)

Imoveis rurais do Cadastro Ambiental Rural.

### Como usar

1. No dock agrobr, expanda a categoria **Fundiario**
2. Selecione **Imoveis Rurais**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| uf | UF | Sim | Unidade da Federacao |
| municipio | Texto | Nao | Nome do municipio |
| status | Texto | Nao | Status do imovel no CAR |
| tipo | Texto | Nao | Tipo do imovel |

### Capacidades

- [x] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Resumo CAR (SICAR)

Resumo estatistico do CAR por municipio/UF.

### Como usar

1. No dock agrobr, expanda a categoria **Fundiario**
2. Selecione **Resumo CAR**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| uf | UF | Sim | Unidade da Federacao |
| municipio | Texto | Nao | Nome do municipio |

### Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Notas

Dados do SICAR sao acessados via `agrobr.alt` (modulo alternativo). A UF e obrigatoria para ambas as fontes.
