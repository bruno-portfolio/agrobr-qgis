# Queimadas (INPE)

Focos de incendio detectados por satelite (INPE/Programa Queimadas).

## Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Queimadas**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

## Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| ano | Inteiro | Sim | Ano dos focos (default: 2026) |
| mes | Inteiro | Sim | Mes dos focos (default: 1) |
| dia | Inteiro | Nao | Dia especifico. Deixe 0 para o mes inteiro |
| uf | UF | Nao | Filtrar por estado |

## Capacidades

- [x] Saida geoespacial — marque "Saida geoespacial" para obter geometrias
- [x] Filtro temporal
- [ ] Filtro por bounding box
- [ ] Join municipal

## Notas

- Suporta saida tabular e geoespacial.
- Dados atualizados diariamente pelo INPE.
