# Fontes ANA (Agência Nacional de Águas)

Dados hidrológicos e de irrigação disponibilizados pela ANA via WFS.

---

## Demanda de Irrigação (ANA)

Dados de demanda de irrigação por bacia hidrográfica.

### Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Demanda de Irrigação**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| bbox | Bounding Box | Sim | Área de interesse |
| max_features | Inteiro | Não | Limite de feições retornadas |

### Capacidades

- [x] GEO
- [x] TABULAR
- [x] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Disponibilidade Hídrica (ANA)

Dados de disponibilidade hídrica superficial e subterrânea.

### Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Disponibilidade Hídrica**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| bbox | Bounding Box | Não | Área de interesse |
| max_features | Inteiro | Não | Limite de feições retornadas |

### Capacidades

- [x] GEO
- [x] TABULAR
- [x] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Hidrografia (ANA)

Rede hidrográfica brasileira (rios, reservatórios, massas d'água).

### Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Hidrografia**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| bbox | Bounding Box | Sim | Área de interesse |
| max_features | Inteiro | Não | Limite de feições retornadas |

### Capacidades

- [x] GEO
- [x] TABULAR
- [x] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Pivôs de Irrigação (ANA)

Mapeamento de pivôs centrais de irrigação identificados por sensoriamento remoto.

### Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Pivôs de Irrigação**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| uf | UF | Não | Unidade da Federação |
| bbox | Bounding Box | Não | Área de interesse |
| max_features | Inteiro | Não | Limite de feições retornadas |

### Capacidades

- [x] GEO
- [x] TABULAR
- [x] BBOX_FILTER
- [ ] TEMPORAL
- [ ] AUTH
- [ ] PAGINATION

---

## Notas

Fontes da ANA disponibilizadas via WFS. Para Demanda de Irrigação e Hidrografia, o bounding box é obrigatório.
