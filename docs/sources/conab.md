# Fontes CONAB

Dados de safras, produção agrícola e preços praticados nas CEASAs.

---

## Safras (CONAB)

Levantamento de safras CONAB.

### Como usar

1. No dock agrobr, expanda a categoria **Produção**
2. Selecione **Safras**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| produto | Texto | Não | Produto agrícola |
| safra | Texto | Não | Safra (ex: 2023/24) |
| uf | UF | Não | Unidade da Federação |

### Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Série Histórica (CONAB)

Série histórica de produção agrícola.

### Como usar

1. No dock agrobr, expanda a categoria **Produção**
2. Selecione **Série Histórica**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| produto | Texto | Sim | Produto agrícola |
| inicio | Inteiro | Não | Ano inicial |
| fim | Inteiro | Não | Ano final |
| uf | UF | Não | Unidade da Federação |

### Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [x] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## CEASA Preços (CONAB)

Preços praticados nas CEASAs.

### Como usar

1. No dock agrobr, expanda a categoria **Produção**
2. Selecione **CEASA Preços**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| produto | Texto | Não | Produto agrícola |
| ceasa | Texto | Não | Central de abastecimento |

### Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Notas

Todas as fontes CONAB são tabulares (sem geometria).
