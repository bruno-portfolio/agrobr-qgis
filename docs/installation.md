# Instalação

## Requisitos

| Componente | Versão |
|------------|--------|
| QGIS | 4.0+ |
| Python | 3.12+ |
| agrobr | >=1.0.0,<2.0.0 |

> **QGIS 3.x não é suportado.** O plugin targeta exclusivamente QGIS 4 / Qt6.

## Via Plugin Manager (recomendado)

1. Abra o QGIS 4
2. Menu **Plugins > Manage and Install Plugins**
3. Busque por **agrobr**
4. Clique **Install Plugin**

O plugin tenta instalar a dependência `agrobr[geo]` automaticamente na primeira execução. Se a instalação automática falhar, instale manualmente (veja abaixo).

## Instalação Manual

### 1. Instalar a biblioteca agrobr

No terminal do Python do QGIS ou no terminal do sistema:

```bash
pip install agrobr[geo]
```

No Windows com OSGeo4W, use o **OSGeo4W Shell**:

```bash
python -m pip install agrobr[geo]
```

### 2. Copiar o plugin

Copie a pasta `agrobr_qgis/` para o diretório de plugins do QGIS:

- **Linux:** `~/.local/share/QGIS/QGIS4/profiles/default/python/plugins/`
- **Windows:** `%APPDATA%\QGIS\QGIS4\profiles\default\python\plugins\`
- **macOS:** `~/Library/Application Support/QGIS/QGIS4/profiles/default/python/plugins/`

### 3. Ativar o plugin

1. Reinicie o QGIS
2. Menu **Plugins > Manage and Install Plugins**
3. Na aba **Installed**, marque **agrobr**

## Ambientes Corporativos

### Proxy

O plugin propaga automaticamente as configurações de proxy do QGIS para a biblioteca agrobr. Configure o proxy em:

**QGIS > Settings > Options > Network > Proxy**

Se o proxy exigir autenticação, preencha usuário e senha — o plugin codifica as credenciais corretamente na URL.

### Firewall

O plugin acessa os seguintes domínios (lista parcial dos principais):

| Domínio | Uso |
|---------|-----|
| `geoftp.ibge.gov.br` | Malha municipal para join espacial |
| `agroapi.cnptia.embrapa.br` | Dados ZARC |
| `queimadas.dgi.inpe.br` | Focos de queimadas INPE |
| `terrabrasilis.dpi.inpe.br` | DETER/PRODES |
| `plataforma.alerta.mapbiomas.org` | Alertas MapBiomas |
| `apps.fas.usda.gov` | Dados USDA PSD |
| `olinda.bcb.gov.br` | Dados BCB (PTAX, Focus, SGS) |
| `www.cepea.esalq.usp.br` | Indicadores CEPEA |
| `pypi.org` | Auto-instalação da biblioteca agrobr |

### Uso Offline

A biblioteca agrobr possui cache local. Após o primeiro acesso a uma fonte, os dados ficam disponíveis offline (dependendo da configuração de cache).

Para verificar se o cache está ativo: **Dock agrobr > Configurações > Cache habilitado**.

## Verificação

### Plugin carregou corretamente?

1. O dock **agrobr** aparece na lateral direita do QGIS
2. A árvore de fontes mostra as categorias (Ambiental, Produção, Mercado, etc.)

### Onde ver logs

**QGIS > View > Log Messages > aba "agrobr"**

Os logs mostram:
- **Info**: operações normais (fetch, timing, rows retornados)
- **Warning**: avisos de debug (stack traces, decisões internas)
- **Critical**: erros (falhas de fetch, problemas de autenticação)

### Verificar versão do agrobr

No Python Console do QGIS (`Ctrl+Alt+P`):

```python
import agrobr
print(agrobr.__version__)
```

## Desinstalação

### Via Plugin Manager

1. Menu **Plugins > Manage and Install Plugins**
2. Na aba **Installed**, selecione **agrobr**
3. Clique **Uninstall Plugin**

### Manual

1. Remova a pasta `agrobr_qgis/` do diretório de plugins
2. (Opcional) Remova a biblioteca: `pip uninstall agrobr`
3. (Opcional) Remova o cache de malhas: apague `~/.agrobr/meshes/`
