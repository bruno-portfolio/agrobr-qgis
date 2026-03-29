# ZARC (MAPA)

Zoneamento Agrícola de Risco Climático — define períodos de plantio com menor risco climático por município.

## Como usar

1. No dock agrobr, expanda a categoria **Regulatório**
2. Selecione **ZARC**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| cultura | Texto | Não | Nome da cultura |
| uf | UF | Não | Filtrar por estado |
| municipio | Texto | Não | Nome do município |
| safra | Texto | Não | Safra de referência |

## Capacidades

- [x] Saída tabular
- [ ] Saída geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [x] Join municipal

## Join Municipal

Marque "Join municipal" para gerar uma camada geoespacial a partir do geocódigo IBGE. O plugin realiza um inner join entre a coluna `geocodigo` e a malha municipal do IBGE, gerando uma camada com geometria de cada município.

## Notas

- O ZARC define períodos de plantio com menor risco climático por município.
- Fonte do MAPA (Ministério da Agricultura, Pecuária e Abastecimento).
