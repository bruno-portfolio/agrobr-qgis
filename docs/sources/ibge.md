# Fontes IBGE

Dados de produção agrícola e pecuária do Instituto Brasileiro de Geografia e Estatística.

---

## PAM (IBGE)

Produção Agrícola Municipal — dados anuais de produção, área plantada, rendimento e valor da produção por município.

### Como usar

1. No dock agrobr, expanda a categoria **Produção**
2. Selecione **PAM**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| produto | Produto | Sim | Produto agrícola |
| ano | Inteiro | Não | Ano de referência |
| uf | UF | Não | Filtrar por estado |
| nivel | Escolha | Não | Nível de agregação: brasil, uf ou municipio (default: uf) |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [x] Join municipal

### Join Municipal

Quando `nivel="municipio"`, marque "Join municipal" para transformar os dados tabulares em uma camada geoespacial. O plugin realiza um inner join entre a coluna `codigo_municipio` e a malha municipal do IBGE, gerando uma camada com geometria de cada município.

---

## LSPA (IBGE)

Levantamento Sistemático da Produção Agrícola — estimativas mensais de safra.

### Como usar

1. No dock agrobr, expanda a categoria **Produção**
2. Selecione **LSPA**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| produto | Produto | Sim | Produto agrícola |
| ano | Inteiro | Não | Ano de referência |
| mes | Inteiro | Não | Mês de referência |
| uf | UF | Não | Filtrar por estado |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [x] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## PPM (IBGE)

Pesquisa da Pecuária Municipal — dados anuais de rebanho, produção e valor por município.

### Como usar

1. No dock agrobr, expanda a categoria **Produção**
2. Selecione **PPM**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| especie | Texto | Sim | Espécie pecuária (ex: Bovino, Suíno, Aves) |
| ano | Inteiro | Não | Ano de referência |
| uf | UF | Não | Filtrar por estado |
| nivel | Escolha | Não | Nível de agregação: brasil, uf ou municipio (default: uf) |

### Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [x] Join municipal

### Join Municipal

Quando `nivel="municipio"`, marque "Join municipal" para transformar os dados tabulares em uma camada geoespacial. O plugin realiza um inner join entre a coluna `codigo_municipio` e a malha municipal do IBGE, gerando uma camada com geometria de cada município.

---

## Notas

- Para PAM e PPM com join municipal, use `nivel="municipio"`.
- A LSPA é mensal e não suporta join municipal.
