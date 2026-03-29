# Solucao de Problemas

## Erros de Instalacao

### "A biblioteca agrobr nao esta instalada"

**Causa:** O Python do QGIS nao encontra o pacote `agrobr`.

**Solucao:**
1. Abra o terminal do QGIS (ou OSGeo4W Shell no Windows)
2. Execute: `pip install agrobr[geo]`
3. Reinicie o QGIS

**Verificacao:** No Python Console do QGIS (`Ctrl+Alt+P`): `import agrobr`

### "pip nao encontrado"

**Causa:** O `pip` nao esta disponível no ambiente Python do QGIS.

**Solucao:**
- **Windows:** Use o OSGeo4W Shell (instalado com o QGIS)
- **Linux:** `python3 -m ensurepip` ou instale via gerenciador de pacotes
- **macOS:** `python3 -m ensurepip`

### "Falha na instalacao (codigo N)"

**Causa:** O `pip install` falhou (permissoes, conflito de dependencias, rede).

**Solucao:**
1. Tente manualmente: `pip install agrobr[geo] --user`
2. Se houver conflito: `pip install agrobr[geo] --force-reinstall`
3. Verifique se o Python do QGIS e o mesmo do terminal: `python -c "import sys; print(sys.executable)"`

### "Timeout na instalacao"

**Causa:** A instalacao excedeu o tempo limite de 120 segundos (rede lenta ou instavel).

**Solucao:**
1. Verifique a conexao com a internet
2. Instale manualmente sem timeout: `pip install agrobr[geo]`
3. Se estiver atras de proxy, configure antes: veja [Proxy](#proxy-corporativo)

---

## Erros de Execucao

### Erro ao buscar dados (FetchError)

**Causa:** Falha na comunicacao com a fonte de dados (API fora do ar, timeout, rede).

**Solucao:**
1. Verifique a conexao com a internet
2. Tente novamente em alguns minutos (a fonte pode estar temporariamente indisponivel)
3. Verifique os logs: **View > Log Messages > agrobr**

### Token nao configurado (AuthError)

**Causa:** A fonte requer autenticacao e o token nao foi configurado.

**Fontes que requerem token:**
- **MapBiomas Alertas** — variavel: `MAPBIOMAS_TOKEN`
- **USDA PSD** — variavel: `USDA_API_KEY`

**Solucao:**
1. No dock agrobr, clique em **Configuracoes**
2. Va na aba **Tokens**
3. Insira o token da fonte e clique **Salvar**

Os tokens sao armazenados de forma cifrada pelo QgsAuthManager do QGIS.

### Malha corrompida (ChecksumError)

**Causa:** O arquivo da malha municipal IBGE foi corrompido durante o download.

**Acao automatica:** O plugin deleta o arquivo corrompido e retenta o download na proxima operacao.

**Solucao manual (se persistir):**
1. Apague o diretorio de cache: `~/.agrobr/meshes/`
2. Tente a operacao novamente (o plugin faz o download automaticamente)

### Join vazio (JoinError)

**Causa:** Nenhum municipio do resultado bateu com a malha IBGE.

**Solucao:**
1. Verifique se os parametros estao corretos (UF, produto, ano)
2. Verifique se o nivel esta como "municipio" (fontes IBGE)
3. Consulte os logs para ver amostras dos codigos de municipio

### Formato inesperado (ContractError)

**Causa:** Os dados retornados pela fonte estao em formato diferente do esperado.

**Solucao:**
1. Verifique se a biblioteca agrobr esta atualizada: `pip install --upgrade agrobr[geo]`
2. Se persistir, reporte como bug (veja [Como reportar](#como-reportar-um-bug))

---

## Problemas Comuns

### Plugin nao aparece no QGIS

1. Verifique se a pasta `agrobr_qgis/` esta no diretorio correto de plugins
2. Verifique se o plugin esta ativado: **Plugins > Manage and Install Plugins > Installed**
3. Verifique se e QGIS 4 — o plugin nao funciona no QGIS 3.x
4. Consulte os logs: **View > Log Messages > aba "General"** para erros de carregamento

### Dados nao carregam / resultado vazio

1. Verifique os parametros — alguns sao obrigatorios (marcados com *)
2. Para fontes com filtro por UF, verifique se a UF esta correta
3. Para fontes temporais, verifique se o periodo tem dados disponíveis
4. Consulte os logs: **View > Log Messages > aba "agrobr"**

### Proxy corporativo

O plugin propaga automaticamente as configuracoes de proxy do QGIS.

Se nao funcionar:
1. Verifique a configuracao: **QGIS > Settings > Options > Network > Proxy**
2. Confirme que o tipo de proxy esta correto (HTTP, SOCKS5, etc.)
3. Se o proxy exigir autenticacao, preencha usuario e senha
4. Reinicie o QGIS apos alterar configuracoes de proxy

### Operacao muito lenta

1. Fontes geoespaciais com muitos poligonos podem demorar (DETER, PRODES)
2. O plugin usa camadas em memoria para datasets pequenos e GPKG temporario para datasets grandes (>50.000 linhas ou >2.000.000 vertices)
3. Reduza o escopo da busca: filtre por UF, bbox, ou periodo menor

### Botao "Buscar Dados" desabilitado

O botao fica desabilitado enquanto uma busca esta em andamento. Aguarde a conclusao ou cancele a operacao atual.

---

## Diagnostico

### Onde encontrar logs

**QGIS > View > Log Messages > aba "agrobr"**

| Nivel | Significado |
|-------|-------------|
| Info | Operacoes normais (fetch realizado, linhas retornadas, tempo) |
| Warning | Informacoes de debug (stack traces, decisoes internas) |
| Critical | Erros (falhas de fetch, autenticacao, checksum) |

### Como reportar um bug

Inclua as seguintes informacoes:

1. **Versao do QGIS:** Help > About QGIS
2. **Versao do agrobr:** Python Console > `import agrobr; print(agrobr.__version__)`
3. **Sistema operacional** e versao
4. **Log completo** da aba "agrobr" (copie todo o conteudo)
5. **Passos para reproduzir** o problema
6. **Parametros utilizados** (fonte, UF, datas, etc.)

Abra uma issue em: https://github.com/bruno-portfolio/agrobr-qgis/issues
