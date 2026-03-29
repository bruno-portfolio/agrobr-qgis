# Fontes IBGE

Dados de producao agricola e pecuaria do Instituto Brasileiro de Geografia e Estatistica.

---

## PAM (IBGE)

Producao Agricola Municipal — dados anuais de producao, area plantada, rendimento e valor da producao por municipio.

### Como usar

1. No dock agrobr, expanda a categoria **Producao**
2. Selecione **PAM**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| produto | Produto | Sim | Produto agricola |
| ano | Inteiro | Nao | Ano de referencia |
| uf | UF | Nao | Filtrar por estado |
| nivel | Escolha | Nao | Nivel de agregacao: brasil, uf ou municipio (default: uf) |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [x] Join municipal

### Join Municipal

Quando `nivel="municipio"`, marque "Join municipal" para transformar os dados tabulares em uma camada geoespacial. O plugin realiza um inner join entre a coluna `codigo_municipio` e a malha municipal do IBGE, gerando uma camada com geometria de cada municipio.

---

## LSPA (IBGE)

Levantamento Sistematico da Producao Agricola — estimativas mensais de safra.

### Como usar

1. No dock agrobr, expanda a categoria **Producao**
2. Selecione **LSPA**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| produto | Produto | Sim | Produto agricola |
| ano | Inteiro | Nao | Ano de referencia |
| mes | Inteiro | Nao | Mes de referencia |
| uf | UF | Nao | Filtrar por estado |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [x] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

---

## PPM (IBGE)

Pesquisa da Pecuaria Municipal — dados anuais de rebanho, producao e valor por municipio.

### Como usar

1. No dock agrobr, expanda a categoria **Producao**
2. Selecione **PPM**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

### Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| especie | Texto | Sim | Especie pecuaria (ex: Bovino, Suino, Aves) |
| ano | Inteiro | Nao | Ano de referencia |
| uf | UF | Nao | Filtrar por estado |
| nivel | Escolha | Nao | Nivel de agregacao: brasil, uf ou municipio (default: uf) |

### Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [x] Join municipal

### Join Municipal

Quando `nivel="municipio"`, marque "Join municipal" para transformar os dados tabulares em uma camada geoespacial. O plugin realiza um inner join entre a coluna `codigo_municipio` e a malha municipal do IBGE, gerando uma camada com geometria de cada municipio.

---

## Notas

- Para PAM e PPM com join municipal, use `nivel="municipio"`.
- A LSPA e mensal e nao suporta join municipal.
