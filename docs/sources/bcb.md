# Fontes BCB

Dados do Banco Central do Brasil — taxas de câmbio, expectativas de mercado e séries temporais.

---

## PTAX (BCB)

Taxa de câmbio PTAX do Banco Central.

### Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **PTAX**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| data | Data | Não | Data específica |
| data_inicial | Data | Não | Início do período |
| data_final | Data | Não | Fim do período |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [x] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

### Notas

- Use `data` para consultar um dia específico ou `data_inicial`/`data_final` para um período.

---

## Focus (BCB)

Relatório Focus — expectativas de mercado coletadas pelo Banco Central.

### Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **Focus**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| indicador | Texto | Não | Indicador econômico (default: PIB Agropecuário) |
| top | Inteiro | Não | Top N instituições |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## SGS (BCB)

Séries temporais do Sistema Gerenciador de Séries do Banco Central.

### Como usar

1. No dock agrobr, expanda a categoria **Mercado**
2. Selecione **SGS**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| codigo | Inteiro | Sim | Código da série SGS |
| data_inicial | Data | Não | Início do período |
| data_final | Data | Não | Fim do período |
| ultimos | Inteiro | Não | Retorna os N últimos valores |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [x] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## Notas

- Consulte o catálogo SGS no site do BCB para encontrar o código da série desejada.
