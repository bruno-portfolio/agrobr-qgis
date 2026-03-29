# Fontes BCB

Dados do Banco Central do Brasil — taxas de cambio, expectativas de mercado e series temporais.

---

## PTAX (BCB)

Taxa de cambio PTAX do Banco Central.

### Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **PTAX**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| data | Data | Nao | Data especifica |
| data_inicial | Data | Nao | Inicio do periodo |
| data_final | Data | Nao | Fim do periodo |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [x] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

### Notas

- Use `data` para consultar um dia especifico ou `data_inicial`/`data_final` para um periodo.

---

## Focus (BCB)

Relatorio Focus — expectativas de mercado coletadas pelo Banco Central.

### Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **Focus**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| indicador | Texto | Nao | Indicador economico (default: PIB Agropecuario) |
| top | Inteiro | Nao | Top N instituicoes |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## SGS (BCB)

Series temporais do Sistema Gerenciador de Series do Banco Central.

### Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **SGS**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| codigo | Inteiro | Sim | Codigo da serie SGS |
| data_inicial | Data | Nao | Inicio do periodo |
| data_final | Data | Nao | Fim do periodo |
| ultimos | Inteiro | Nao | Retorna os N ultimos valores |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [x] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## Notas

- Consulte o catalogo SGS no site do BCB para encontrar o codigo da serie desejada.
