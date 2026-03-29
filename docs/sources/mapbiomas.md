# Alertas (MapBiomas)

Alertas de desmatamento validados pelo MapBiomas.

## Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Alertas**
3. Preencha os parametros abaixo
4. Clique em **Buscar Dados**

## Parametros

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|:-----------:|-----------|
| start_date | Data | Nao | Data inicio |
| end_date | Data | Nao | Data fim |
| bbox | Bounding Box | Nao | Area de interesse |
| limit | Inteiro | Nao | Limite de registros por pagina (default: 100) |

## Capacidades

- [x] Saida geoespacial — marque "Saida geoespacial" para obter geometrias
- [x] Filtro temporal
- [x] Filtro por bounding box
- [x] Paginacao — aumente o limite para mais resultados
- [ ] Join municipal

## Autenticacao

Esta fonte requer um token de acesso do MapBiomas (`MAPBIOMAS_TOKEN`).

Para obter e configurar o token:

1. Acesse a plataforma [MapBiomas Alerta](https://alerta.mapbiomas.org/) e crie uma conta
2. Gere um token de API nas configuracoes da sua conta
3. No QGIS, va em **agrobr > Settings > Tokens**
4. Insira o token no campo **MAPBIOMAS_TOKEN**
5. Clique em **Salvar**

O token sera armazenado de forma segura via `QgsAuthManager`.

## Notas

Fonte paginada. Aumente o limite para obter mais resultados.
