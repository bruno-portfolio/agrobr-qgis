# Fontes Defensivos (MAPA)

Dados de defensivos agrícolas registrados no Ministério da Agricultura.

---

## Defensivos Formulados (MAPA)

Produtos formulados de defensivos registrados no MAPA.

### Como usar

1. No dock agrobr, expanda a categoria **Regulatório**
2. Selecione **Defensivos Formulados**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| ingrediente_ativo | Texto | Não | Filtrar por ingrediente ativo |
| classe | Texto | Não | Classe do produto |
| titular | Texto | Não | Empresa titular do registro |
| marca | Texto | Não | Nome comercial do produto |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## Autorizações de Defensivos (MAPA)

Autorizações de uso de defensivos por cultura.

### Como usar

1. No dock agrobr, expanda a categoria **Regulatório**
2. Selecione **Autorizações de Defensivos**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| cultura | Texto | Não | Cultura autorizada |
| ingrediente_ativo | Texto | Não | Filtrar por ingrediente ativo |
| nr_registro | Texto | Não | Número de registro |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## Defensivos Técnicos (MAPA)

Produtos técnicos de defensivos registrados no MAPA.

### Como usar

1. No dock agrobr, expanda a categoria **Regulatório**
2. Selecione **Defensivos Técnicos**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| ingrediente_ativo | Texto | Não | Filtrar por ingrediente ativo |
| titular | Texto | Não | Empresa titular do registro |
| classe | Texto | Não | Classe do produto |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## Notas

- Todas as fontes de defensivos são tabulares.
- Use o filtro por ingrediente ativo para refinar a busca.
