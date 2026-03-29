# ZARC (MAPA)

Zoneamento Agricola de Risco Climatico — define periodos de plantio com menor risco climatico por municipio.

## Como usar

1. No dock agrobr, expanda a categoria **Regulatorio**
2. Selecione **ZARC**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

## Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| cultura | Texto | Nao | Nome da cultura |
| uf | UF | Nao | Filtrar por estado |
| municipio | Texto | Nao | Nome do municipio |
| safra | Texto | Nao | Safra de referencia |

## Capacidades

- [x] Saida tabular
- [ ] Saida geoespacial
- [ ] Filtro temporal
- [ ] Filtro por bounding box
- [x] Join municipal

## Join Municipal

Marque "Join municipal" para gerar uma camada geoespacial a partir do geocodigo IBGE. O plugin realiza um inner join entre a coluna `geocodigo` e a malha municipal do IBGE, gerando uma camada com geometria de cada municipio.

## Notas

- O ZARC define periodos de plantio com menor risco climatico por municipio.
- Fonte do MAPA (Ministerio da Agricultura, Pecuaria e Abastecimento).
