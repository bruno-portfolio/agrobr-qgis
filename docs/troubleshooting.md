# Solução de Problemas

## Erros de Instalação

### "A biblioteca agrobr não está instalada"

**Causa:** O Python do QGIS não encontra o pacote `agrobr`.

**Solução:**
1. Abra o terminal do QGIS (ou OSGeo4W Shell no Windows)
2. Execute: `pip install agrobr[geo]`
3. Reinicie o QGIS

**Verificação:** No Python Console do QGIS (`Ctrl+Alt+P`): `import agrobr`

### "pip não encontrado"

**Causa:** O `pip` não está disponível no ambiente Python do QGIS.

**Solução:**
- **Windows:** Use o OSGeo4W Shell (instalado com o QGIS)
- **Linux:** `python3 -m ensurepip` ou instale via gerenciador de pacotes
- **macOS:** `python3 -m ensurepip`

### "Falha na instalação (código N)"

**Causa:** O `pip install` falhou (permissões, conflito de dependências, rede).

**Solução:**
1. Tente manualmente: `pip install agrobr[geo] --user`
2. Se houver conflito: `pip install agrobr[geo] --force-reinstall`
3. Verifique se o Python do QGIS é o mesmo do terminal: `python -c "import sys; print(sys.executable)"`

### "Timeout na instalação"

**Causa:** A instalação excedeu o tempo limite de 120 segundos (rede lenta ou instável).

**Solução:**
1. Verifique a conexão com a internet
2. Instale manualmente sem timeout: `pip install agrobr[geo]`
3. Se estiver atrás de proxy, configure antes: veja [Proxy](#proxy-corporativo)

---

## Erros de Execução

### Erro ao buscar dados (FetchError)

**Causa:** Falha na comunicação com a fonte de dados (API fora do ar, timeout, rede).

**Solução:**
1. Verifique a conexão com a internet
2. Tente novamente em alguns minutos (a fonte pode estar temporariamente indisponível)
3. Verifique os logs: **View > Log Messages > agrobr**

### Token não configurado (AuthError)

**Causa:** A fonte requer autenticação e o token não foi configurado.

**Fontes que requerem token:**
- **MapBiomas Alertas** — variável: `MAPBIOMAS_TOKEN`
- **USDA PSD** — variável: `USDA_API_KEY`

**Solução:**
1. No dock agrobr, clique em **Configurações**
2. Vá na aba **Tokens**
3. Insira o token da fonte e clique **Salvar**

Os tokens são armazenados de forma cifrada pelo QgsAuthManager do QGIS.

### Malha corrompida (ChecksumError)

**Causa:** O arquivo da malha municipal IBGE foi corrompido durante o download.

**Ação automática:** O plugin deleta o arquivo corrompido e retenta o download na próxima operação.

**Solução manual (se persistir):**
1. Apague o diretório de cache: `~/.agrobr/meshes/`
2. Tente a operação novamente (o plugin faz o download automaticamente)

### Join vazio (JoinError)

**Causa:** Nenhum município do resultado bateu com a malha IBGE.

**Solução:**
1. Verifique se os parâmetros estão corretos (UF, produto, ano)
2. Verifique se o nível está como "município" (fontes IBGE)
3. Consulte os logs para ver amostras dos códigos de município

### Formato inesperado (ContractError)

**Causa:** Os dados retornados pela fonte estão em formato diferente do esperado.

**Solução:**
1. Verifique se a biblioteca agrobr está atualizada: `pip install --upgrade agrobr[geo]`
2. Se persistir, reporte como bug (veja [Como reportar](#como-reportar-um-bug))

---

## Problemas Comuns

### Plugin não aparece no QGIS

1. Verifique se a pasta `agrobr_qgis/` está no diretório correto de plugins
2. Verifique se o plugin está ativado: **Plugins > Manage and Install Plugins > Installed**
3. Verifique se é QGIS 4 — o plugin não funciona no QGIS 3.x
4. Consulte os logs: **View > Log Messages > aba "General"** para erros de carregamento

### Dados não carregam / resultado vazio

1. Verifique os parâmetros — alguns são obrigatórios (marcados com *)
2. Para fontes com filtro por UF, verifique se a UF está correta
3. Para fontes temporais, verifique se o período tem dados disponíveis
4. Consulte os logs: **View > Log Messages > aba "agrobr"**

### Proxy corporativo

O plugin propaga automaticamente as configurações de proxy do QGIS.

Se não funcionar:
1. Verifique a configuração: **QGIS > Settings > Options > Network > Proxy**
2. Confirme que o tipo de proxy está correto (HTTP, SOCKS5, etc.)
3. Se o proxy exigir autenticação, preencha usuário e senha
4. Reinicie o QGIS após alterar configurações de proxy

### Operação muito lenta

1. Fontes geoespaciais com muitos polígonos podem demorar (DETER, PRODES)
2. O plugin usa camadas em memória para datasets pequenos e GPKG temporário para datasets grandes (>50.000 linhas ou >2.000.000 vértices)
3. Reduza o escopo da busca: filtre por UF, bbox, ou período menor

### Botão "Buscar Dados" desabilitado

O botão fica desabilitado enquanto uma busca está em andamento. Aguarde a conclusão ou cancele a operação atual.

---

## Diagnóstico

### Onde encontrar logs

**QGIS > View > Log Messages > aba "agrobr"**

| Nível | Significado |
|-------|-------------|
| Info | Operações normais (fetch realizado, linhas retornadas, tempo) |
| Warning | Informações de debug (stack traces, decisões internas) |
| Critical | Erros (falhas de fetch, autenticação, checksum) |

### Como reportar um bug

Inclua as seguintes informações:

1. **Versão do QGIS:** Help > About QGIS
2. **Versão do agrobr:** Python Console > `import agrobr; print(agrobr.__version__)`
3. **Sistema operacional** e versão
4. **Log completo** da aba "agrobr" (copie todo o conteúdo)
5. **Passos para reproduzir** o problema
6. **Parâmetros utilizados** (fonte, UF, datas, etc.)

Abra uma issue em: https://github.com/bruno-portfolio/agrobr-qgis/issues
