# Fontes ANA (Agencia Nacional de Aguas)

Dados hidrologicos e de irrigacao disponibilizados pela ANA via WFS.

---

## Demanda de Irrigacao (ANA)

Dados de demanda de irrigacao por bacia hidrografica.

### Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Demanda de Irrigacao**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| bbox | Bounding Box | Sim | Area de interesse |
| max_features | Inteiro | Nao | Limite de feicoes retornadas |

### Capacidades

- [x] GEO
- [x] TABULAR
- [x] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Disponibilidade Hidrica (ANA)

Dados de disponibilidade hidrica superficial e subterranea.

### Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Disponibilidade Hidrica**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| bbox | Bounding Box | Nao | Area de interesse |
| max_features | Inteiro | Nao | Limite de feicoes retornadas |

### Capacidades

- [x] GEO
- [x] TABULAR
- [x] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Hidrografia (ANA)

Rede hidrografica brasileira (rios, reservatorios, massas d'agua).

### Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Hidrografia**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| bbox | Bounding Box | Sim | Area de interesse |
| max_features | Inteiro | Nao | Limite de feicoes retornadas |

### Capacidades

- [x] GEO
- [x] TABULAR
- [x] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Pivos de Irrigacao (ANA)

Mapeamento de pivos centrais de irrigacao identificados por sensoriamento remoto.

### Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Pivos de Irrigacao**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| uf | UF | Nao | Unidade da Federacao |
| bbox | Bounding Box | Nao | Area de interesse |
| max_features | Inteiro | Nao | Limite de feicoes retornadas |

### Capacidades

- [x] GEO
- [x] TABULAR
- [x] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Notas

Fontes da ANA disponibilizadas via WFS. Para Demanda de Irrigacao e Hidrografia, o bounding box e obrigatorio.
