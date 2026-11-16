# Instalação e operação local com espaço limitado

Preparado/testado na nuvem em Linux; nenhuma ação foi executada no computador pessoal. Windows foi contemplado nos caminhos/diagnóstico e comandos abaixo, mas **não ensaiado em Windows real**. Não se exige compra de unidade, exclusão de dados, administrador ou alteração global do sistema.

## Diagnóstico de leitura

Na raiz do clone, usando Python 3.12:

```sh
PYTHONPATH=python python3 scripts/diagnosticar_ambiente_local.py --saida /caminho/autorizado/diagnostico.json
```

O programa lê SO, RAM/CPU, espaço dos caminhos configurados, versões de runtimes, dependências do intérprete e nomes/PIDs de processos do projeto. Não coleta argumentos de processos, credenciais, arquivos pessoais ou listagem recursiva de diretórios. Só escreve o relatório explicitamente indicado, recusando sobrescrita. O diagnóstico cloud observado está em `evidencias/diagnostico_cloud.json`; não constitui requisito mínimo do computador local.

## Configuração fora do checkout

Copiar `config/operacao_local_linux.exemplo.json` ou `operacao_local_windows.exemplo.json` para arquivo **fora do repositório** e substituir os caminhos por locais escolhidos. O programa recusa configuração, RAW, cache, temporários, saída ou backup dentro do checkout. Caminhos com espaços são suportados. É possível usar volumes diferentes, inclusive unidade externa escolhida posteriormente; não se presume sua existência.

`margem_livre_bytes` é reserva configurável (o exemplo usa 1 GiB), não mínimo científico medido. `concorrencia_max` é um limite; a aquisição atual permanece serial, uma conexão, mesmo se o teto configurado for maior. Não se altera HOME, proxy, TLS ou configuração global.

## Preflight sem adivinhar volumes

Um plano de lote contém `objetos` do contrato de custódia (ID, caminho, sistema, família, competência, UF, parte, revisão, layout, URI, bytes/hash observados quando existentes e `limite_bytes`) e limites explícitos para `limite_derivados_bytes`, `limite_temporarios_bytes` e eventual `backup_novo_bytes`. Declare `transporte=ftp` ou `snapshot`, conforme evidência. A fila nominal RD recebida não contém tamanhos observados e **não é** esse catálogo. Sem tamanho/limite ou expansão delimitada o preflight bloqueia; não se atribui tamanho fictício.

```sh
PYTHONPATH=python python3 scripts/diagnosticar_ambiente_local.py --config /caminho/config.json --plano-lote /caminho/lote.json --saida /caminho/preflight.json
PYTHONPATH=python python3 scripts/adquirir_lote_controlado.py --config /caminho/config.json --plano-lote /caminho/lote.json --resultado /caminho/somente_preflight.json
```

O segundo comando também faz somente preflight. Somar destinos que compartilham filesystem evita contabilizar o mesmo espaço livre várias vezes. RAW em staging é contado pelo limite integral; derivados, temporários e backup novo pelos limites declarados. Versões anteriores já estão no uso de disco observado; não se excluem automaticamente. Cache validado por identidade/revisão/hash pode ser lido sem reconsulta, mesmo quando não há espaço para nova versão. Durante aquisição nova, o preflight é refeito antes de cada arquivo, considerando os restantes. Se outro processo consumir espaço, o comando interrompe antes da próxima parte; falha de escrita não autoriza promoção parcial.

Aquisição real somente com catálogo observado e condição legítima de acesso:

```sh
PYTHONPATH=python python3 scripts/adquirir_lote_controlado.py --config /caminho/config.json --plano-lote /caminho/lote.json --adquirir --resultado /caminho/aquisicao_nova.json
```

Não repetir fontes já negadas nesta nuvem nem presumir HTTPS equivalente a FTP. Nenhum servidor oficial foi novamente consultado neste incremento. A interface FTP stdlib foi ensaiada com fake; transporte oficial continua pendente. Não se sincroniza cache inteiro com Git/nuvem, nem se promove snapshot de espelho como RAW oficial.

## Ambientes isolados e componentes opcionais

Custódia, diagnóstico, inventário e checkpoints usam apenas stdlib Python 3.12. Pode-se criar ambiente isolado em caminho escolhido, sem apagar `.venv` existente:

```sh
python3.12 -m venv "/caminho escolhido/ambiente observatorio"
"/caminho escolhido/ambiente observatorio/bin/python" -m pip install -r requirements-implementacao.txt
```

A instalação via pip é necessária somente para testes/Arrow/DuckDB escolhidos; não foi repetida nesta nuvem. Para operação stdlib não é necessária. Não instalar PySUS/DBC ou uma terceira pilha só por novidade. Node 24 e o MVP usam `npm ci` com cache explícito e dependências pinadas; o módulo tem README próprio. R permanece nos preparadores e cálculos. O verificador SHA R legado requer `sha256sum`; esse requisito deve ser conferido no Windows antes de executá-lo, sem presumir que esteja instalado. O diagnóstico informa runtimes faltantes; não tenta instalar globalmente.

PowerShell, com Python/R/Node já disponíveis:

```powershell
py -3.12 -m venv "C:\caminho escolhido\ambiente observatorio"
$env:PYTHONPATH = (Resolve-Path .\python).Path
& "C:\caminho escolhido\ambiente observatorio\Scripts\python.exe" scripts\diagnosticar_ambiente_local.py --config "C:\caminho escolhido\config.json" --saida "C:\caminho escolhido\diagnostico.json"
```

A variável é da sessão; não altera configuração global. Ajustar caminhos escolhidos e não reutilizar um nome de relatório existente. Não houve ensaio em outro SO ou segundo operador humano.

## Receber DBC e documentos do Work/operador

Preservar bytes, URI oficial/efetiva, UTC, revisão, tamanho, hash e eventuais checksums oficiais separadamente. O novo executor técnico não adquire dados e não homologa fonte/layout:

```sh
PYTHONPATH=python:/caminho/extra_validado .venv/bin/python scripts/perfilar_dbc_recebido.py --dbc /caminho/arquivo.dbc --sha256 HASH_MEDIDO --saida /caminho/saida_nova --encoding ENCODING_DOCUMENTADO --natureza empirico_recebido_nao_homologado
```

Reutiliza pyreaddbc 2.0.4 externo já existente e dbfread, sem copiar código AGPL para MIT. Mantém DBC original, DBF, estados ativos/excluídos e células lexicais com padding/marcadores. Uma fixture de dois registros reconciliou cabeçalho/ativos/excluídos. A primeira chamada de desenvolvimento forneceu hash incorreto e foi recusada; o hash efetivamente medido foi usado na execução válida. Não houve DBC oficial novo. Pyreaddbc e wrappers PySUS podem compartilhar descendência blast; dois wrappers não demonstram independência. O segundo mecanismo/decodificador real permanece pendente.

O plano de provas SIH referencia snapshot por identidade, inventário observado, aquisição, conversão, paridade por partes/decodificadores, perfil IDENT efetivo, layout, coorte e catálogo municipal, cada um com caminho/hash/competência/dataset. Layout/coorte/catalogo incluem documentos integrais e revisão funcional. `preparar_aceite_sih.py --plano provas.json --saida diretorio_novo` valida os vínculos e gera `aceite.csv`/`parametros.csv`; `--aceite` revalida sem escrever. Em R, carregar `validar_vinculos_sih.R`, fornecer aceite/hash/Python e ler o CSV com `colClasses="character", na.strings=character()`. A função compara os mesmos bytes e parâmetros. Flags APROVADO isoladas, fixture e apenas ES são recusadas. Hash/vínculo não autenticam por si só a revisão humana; sem provas reais completas não há aceite empírico.

O candidato territorial foi preparado em schema v2 no cache, mantendo códigos CNES, IDs oficiais, vigências e hashes de atos vazios quando não comprovados. O hash do candidato é rotulado como derivado, nunca fonte normativa. Não aplicá-lo a S04 até receber atos/eficácia/catálogo. S03 estadual continua independente do PDR quando seu próprio contrato/cobertura estiver fechado.

## Checkpoints, recuperação e retenção

Antes de continuar: `python scripts/registrar_checkpoint_implementacao.py --verificar`. Uma geração interrompida fica no journal `.cache/checkpoints/`; após comprovar que não existe escritor ativo, recuperar o lock conforme guia e executar `--recuperar`. Alterações externas conflitantes são preservadas e bloqueiam recuperação automática. Não apagar versões, dados pessoais ou snapshots para obter espaço. `CHECKPOINT_INTEGRIDADE.json` vincula hashes ao checkpoint; não há promessa de transação global para leitores que ignorem o preflight.

A01 distingue falha antes/depois de replace: versão íntegra nova pode estar ativa com durabilidade indeterminada; não há rollback automático. Fsync de diretório não é portátil em Windows, onde o código registra durabilidade não comprovada. A10 corrige a afirmação anterior de ausência de rede: não há chamadas explícitas no código sentinela, mas isolamento não foi demonstrado. A tentativa `unshare --net` retornou Operation not permitted; não se solicitaram privilégios nem alterou o sistema. `--exigir-isolamento-rede` falha se a exigência não puder ser cumprida. Segundo operador e custódia/retenção institucional continuam pendentes.

## Executor SIH condicionado às provas

Depois de receber e conferir todos os insumos, na raiz do clone:

```sh
PYTHONPATH=python .venv/bin/python scripts/preparar_aceite_sih.py --plano /dados/provas.json --saida /dados/aceite_novo
Rscript scripts/executar_percurso_sih_validado.R /dados/aceite_novo/aceite.csv SHA_MEDIDO_ACEITE /caminho/venv/bin/python /dados/resultado_sih_novo
```

Sem mapa, somente S03 estadual e categorias não regionalizadas ficam disponíveis. Para S04 acrescentar os quatro argumentos `MAPA.csv VERSAO SHA_MAPA PROVAS_ATOS.csv`. O executor relê os mesmos bytes e parâmetros, bloqueia saída dentro do checkout ou sobrescrita, escreve staging e promove somente ao final. Não há execução empírica aprovada nesta rodada; apenas sintaxe e rejeição sem provas foram verificadas. Falhas preservam staging para diagnóstico e não publicam resultados.

Medição deste build Linux: node_modules 73.332.279 bytes e dist aproximadamente 510 KB; são medições do componente, sem RAW, temporários npm, ambiente Python/R ou histórico. Não são requisito mínimo de RAM/disco para o Observatório completo.
