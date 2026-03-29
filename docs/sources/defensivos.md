# Fontes Defensivos (MAPA)

Dados de defensivos agricolas registrados no Ministerio da Agricultura.

---

## Defensivos Formulados (MAPA)

Produtos formulados de defensivos registrados no MAPA.

### Como usar

1. No dock agrobr, expanda a categoria **Regulatorio**
2. Selecione **Defensivos Formulados**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| ingrediente_ativo | Texto | Nao | Filtrar por ingrediente ativo |
| classe | Texto | Nao | Classe do produto |
| titular | Texto | Nao | Empresa titular do registro |
| marca | Texto | Nao | Nome comercial do produto |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## Autorizacoes de Defensivos (MAPA)

Autorizacoes de uso de defensivos por cultura.

### Como usar

1. No dock agrobr, expanda a categoria **Regulatorio**
2. Selecione **Autorizacoes de Defensivos**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| cultura | Texto | Nao | Cultura autorizada |
| ingrediente_ativo | Texto | Nao | Filtrar por ingrediente ativo |
| nr_registro | Texto | Nao | Numero de registro |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## Defensivos Tecnicos (MAPA)

Produtos tecnicos de defensivos registrados no MAPA.

### Como usar

1. No dock agrobr, expanda a categoria **Regulatorio**
2. Selecione **Defensivos Tecnicos**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| ingrediente_ativo | Texto | Nao | Filtrar por ingrediente ativo |
| titular | Texto | Nao | Empresa titular do registro |
| classe | Texto | Nao | Classe do produto |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## Notas

- Todas as fontes de defensivos sao tabulares.
- Use o filtro por ingrediente ativo para refinar a busca.
