# DETER (INPE)

Alertas de desmatamento em tempo real (INPE/DETER).

## Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **DETER**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| bioma | Escolha | Não | Amazônia, Cerrado, Mata Atlântica, Caatinga, Pampa, Pantanal |
| uf | UF | Não | Filtrar por estado |
| data_inicio | Data | Não | Data inicial do período |
| data_fim | Data | Não | Data final do período |

## Capacidades

- [x] Saída geoespacial — marque "Saída geoespacial" para obter geometrias
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
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| bioma | Escolha | Não | Amazônia, Cerrado, Mata Atlântica, Caatinga, Pampa, Pantanal |
| uf | UF | Não | Filtrar por estado |
| data_inicio | Data | Não | Data inicial do período |
| data_fim | Data | Não | Data final do período |

## Capacidades

- [x] Saída geoespacial — marque "Saída geoespacial" para obter geometrias
- [ ] Filtro temporal
- [x] Filtro por bounding box
- [ ] Join municipal

## Notas

- Dados anuais consolidados.
- Use DETER para monitoramento em tempo real e PRODES para análise histórica.
