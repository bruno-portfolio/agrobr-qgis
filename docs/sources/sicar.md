# Fontes SICAR

Dados do Sistema Nacional de Cadastro Ambiental Rural.

---

## Imóveis Rurais (SICAR)

Imóveis rurais do Cadastro Ambiental Rural.

### Como usar

1. No dock agrobr, expanda a categoria **Fundiário**
2. Selecione **Imóveis Rurais**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| uf | UF | Sim | Unidade da Federação |
| municipio | Texto | Não | Nome do município |
| status | Texto | Não | Status do imóvel no CAR |
| tipo | Texto | Não | Tipo do imóvel |

### Capacidades

- [x] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Resumo CAR (SICAR)

Resumo estatístico do CAR por município/UF.

### Como usar

1. No dock agrobr, expanda a categoria **Fundiário**
2. Selecione **Resumo CAR**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| uf | UF | Sim | Unidade da Federação |
| municipio | Texto | Não | Nome do município |

### Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Notas

Dados do SICAR são acessados via `agrobr.alt` (módulo alternativo). A UF é obrigatória para ambas as fontes.
