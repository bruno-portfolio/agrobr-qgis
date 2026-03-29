# DETER (INPE)

Alertas de desmatamento em tempo real (INPE/DETER).

## Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **DETER**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

## Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| bioma | Escolha | Nao | Amazonia, Cerrado, Mata Atlantica, Caatinga, Pampa, Pantanal |
| uf | UF | Nao | Filtrar por estado |
| data_inicio | Data | Nao | Data inicial do periodo |
| data_fim | Data | Nao | Data final do periodo |

## Capacidades

- [x] Saida geoespacial — marque "Saida geoespacial" para obter geometrias
- [x] Filtro temporal
- [x] Filtro por bounding box
- [ ] Join municipal

## Notas

- Dados de desmatamento em tempo quase-real.
- Use o filtro de bioma para refinar a busca.

---

# PRODES (INPE)

Desmatamento anual por corte raso (INPE/PRODES).

## Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **PRODES**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

## Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| bioma | Escolha | Nao | Amazonia, Cerrado, Mata Atlantica, Caatinga, Pampa, Pantanal |
| uf | UF | Nao | Filtrar por estado |
| data_inicio | Data | Nao | Data inicial do periodo |
| data_fim | Data | Nao | Data final do periodo |

## Capacidades

- [x] Saida geoespacial — marque "Saida geoespacial" para obter geometrias
- [ ] Filtro temporal
- [x] Filtro por bounding box
- [ ] Join municipal

## Notas

- Dados anuais consolidados.
- Use DETER para monitoramento em tempo real e PRODES para analise historica.
