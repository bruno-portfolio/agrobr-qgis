# Alertas (MapBiomas)

Alertas de desmatamento validados pelo MapBiomas.

## Como usar

1. No dock agrobr, expanda a categoria **Ambiental**
2. Selecione **Alertas**
3. Preencha os parâmetros abaixo
4. Clique em **Buscar Dados**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|:-----------:|-----------|
| start_date | Data | Não | Data início |
| end_date | Data | Não | Data fim |
| bbox | Bounding Box | Não | Área de interesse |
| limit | Inteiro | Não | Limite de registros por página (default: 100) |

## Capacidades

- [x] Saída geoespacial — marque "Saída geoespacial" para obter geometrias
- [x] Filtro temporal
- [x] Filtro por bounding box
- [x] Paginação — aumente o limite para mais resultados
- [ ] Join municipal

## Autenticação

Esta fonte requer um token de acesso do MapBiomas (`MAPBIOMAS_TOKEN`).

Para obter e configurar o token:

1. Acesse a plataforma [MapBiomas Alerta](https://alerta.mapbiomas.org/) e crie uma conta
2. Gere um token de API nas configurações da sua conta
3. No QGIS, vá em **agrobr > Settings > Tokens**
4. Insira o token no campo **MAPBIOMAS_TOKEN**
5. Clique em **Salvar**

O token será armazenado de forma segura via `QgsAuthManager`.

## Notas

Fonte paginada. Aumente o limite para obter mais resultados.
