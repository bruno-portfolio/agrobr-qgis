# Fontes CONAB

Dados de safras, producao agricola e precos praticados nas CEASAs.

---

## Safras (CONAB)

Levantamento de safras CONAB.

### Como usar

1. No dock agrobr, expanda a categoria **Producao**
2. Selecione **Safras**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| produto | Texto | Nao | Produto agricola |
| safra | Texto | Nao | Safra (ex: 2023/24) |
| uf | UF | Nao | Unidade da Federacao |

### Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Serie Historica (CONAB)

Serie historica de producao agricola.

### Como usar

1. No dock agrobr, expanda a categoria **Producao**
2. Selecione **Serie Historica**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| produto | Texto | Sim | Produto agricola |
| inicio | Inteiro | Nao | Ano inicial |
| fim | Inteiro | Nao | Ano final |
| uf | UF | Nao | Unidade da Federacao |

### Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [x] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## CEASA Precos (CONAB)

Precos praticados nas CEASAs.

### Como usar

1. No dock agrobr, expanda a categoria **Producao**
2. Selecione **CEASA Precos**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| produto | Texto | Nao | Produto agricola |
| ceasa | Texto | Nao | Central de abastecimento |

### Capacidades

- [ ] GEO
- [x] TABULAR
- [ ] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Notas

Todas as fontes CONAB sao tabulares (sem geometria).
