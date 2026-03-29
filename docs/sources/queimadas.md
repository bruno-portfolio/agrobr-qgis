# Queimadas (INPE)

Focos de incêndio detectados por satélite (INPE/Programa Queimadas).

## Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Queimadas**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| ano | Inteiro | Sim | Ano dos focos (default: 2026) |
| mes | Inteiro | Sim | Mês dos focos (default: 1) |
| dia | Inteiro | Não | Dia específico. Deixe 0 para o mês inteiro |
| uf | UF | Não | Filtrar por estado |

## Capacidades

- [x] Saída geoespacial — marque "Saída geoespacial" para obter geometrias
- [x] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

## Notas

- Suporta saída tabular e geoespacial.
- Dados atualizados diariamente pelo INPE.
