# Operação local e recuperação — ciclo 2026–2027

Destinado às funções P1 (definição/interpretação), P2 (reprodução/engenharia) e P3 (curadoria/comunicação supervisionada), sem designar pessoas. Scripts e formatos abertos permitem operação sem conta pessoal de IA. Custódia definitiva, retenção e política de pequenas células continuam por deliberar.

## Ambiente e comandos de conferência

Executar na raiz do repositório, na branch de implementação. O ambiente observado já existe: CPython 3.12.14, R 4.5.0, PyArrow 19.0.1, DuckDB 1.5.6, pytest 9.1.1. Pins mínimos em `requirements-implementacao.txt`; dependências PySUS anteriores permanecem separadas e não foram atualizadas. Os logs de integração registram versões e comandos completos. Não são lock de sistema operacional nem promessa de reprodutibilidade binária de toda a pilha.

```sh
git status --short
git log -5 --oneline
PYTHONPATH=python .venv/bin/python -m pytest tests/python/test_custodia.py tests/python/test_qualidade_partes_csv.py tests/python/test_inventario_sih_rd.py -q
OBS_RSCRIPT=/workspace/.setup-observatorio/bin/Rscript PYTHONPATH=python .venv/bin/python -m pytest tests/python/test_contraprova_sih_sql.py -q
/workspace/.setup-observatorio/bin/Rscript tests/test_proveniencia_temporal_cnes.R
/workspace/.setup-observatorio/bin/Rscript tests/test_percurso_sih.R
```

Em instalação nova autorizada, usar Python 3.12, criar venv com `python3.12 -m venv .venv` e instalar `requirements-implementacao.txt` de wheelhouse institucional ou índice permitido: `.venv/bin/python -m pip install -r requirements-implementacao.txt`. Isso **não foi necessário nem executado** nesta rodada; não confundir instrução com ensaio. O roteiro de recuperação abaixo usa apenas stdlib e venv, sem pip ou rede durante o comando. R, PyArrow e OS completos não são reconstruídos por esse roteiro mínimo.

## Backup e ensaio realizado

Snapshot local autorizado da sentinela RUE: `.cache/implementacao/backup_rue/versoes/65d88261463327222dc01870c4c21e2ea74c5f981ac32f466745fd01889e3a59/`. Contém manifesto, código sentinela e entradas históricas com hashes; permanece fora de Git. Cópia operacional restaurada: `.cache/implementacao/restaurado_rue_v1/`. O ensaio do agente criou diretório vazio, restaurou arquivos, recriou venv sem pacotes externos, executou código em subprocesso isolado e confirmou 78/78 células contra a contraprova R. Tempo observado e comando estão em `evidencias/restauracao_operacional_rue.json`. Não foi execução por segundo operador humano e não demonstrou atualização da fonte.

Para restaurar **o backup existente**, sem buscar os insumos novamente:

```sh
PYTHONPATH=python python3 scripts/restaurar_snapshot.py \
  --fonte .cache/implementacao/backup_rue/versoes/65d88261463327222dc01870c4c21e2ea74c5f981ac32f466745fd01889e3a59 \
  --conteudo-id 65d88261463327222dc01870c4c21e2ea74c5f981ac32f466745fd01889e3a59 \
  --destino-vazio .cache/implementacao/restaurado_por_operador \
  --sentinela-rue
```

O destino deve estar ausente ou vazio; o programa recusa sobrescrita. Se houver corrupção, restaurar de outra cópia autorizada cujo manifesto confira, preservando os arquivos corrompidos para diagnóstico. O programa não conserta bytes por adivinhação. Atualização real é outra operação: exige novo inventário oficial, recorte aprovado e aquisição completa. Cópias de backup e raiz de custódia devem ficar sob acesso institucional autorizado; os caminhos locais deste ensaio não constituem decisão de custódia definitiva. Não se autoriza envio a terceiros.

## Falhas e retorno

Não remover `versoes/` para liberar espaço sem política de retenção. Em falha de parte, consultar `recibos/*.falha.json`; o ponteiro anterior e suas versões permanecem disponíveis. Em erro após selar versão e antes do ponteiro, pode existir versão íntegra sem promoção, o que é recuperável. `retornar_versao(raiz, id)` confere integridade e troca apenas o ponteiro, sob lock; não altera dados históricos.

Lock remanescente: ler `escritor.lock/owner.json`, verificar host/PID e confirmar ausência de escritor ativo. Não inferir abandono apenas pela idade ou por PID inexistente em outro host. Só depois de comprovar abandono, mover o diretório do lock para quarentena local com nome novo e registrar a ação. Staging de crash permanece fora do dataset corrente; validar ou quarentenar sem misturar com nova versão. Os testes cobrem crash abrupto antes da promoção e exclusão entre processos; não falta de energia.

## Aquisição SIH quando houver acesso legítimo

O acesso atual a notas SIH/PDR/catálogo foi negado pelo proxy com CONNECT 403. Não repetir nem alterar TLS/proxy/allowlist. Um operador com acesso institucional pode preservar o catálogo oficial, layout/DEF/CNV e atos com URI efetiva, UTC e hash. Não usar uma URI HTTPS presumida como prova da rota FTP. PySUS só será integrado como transporte quando sua origem efetiva atender ao contrato.

Converter listagem oficial efetivamente observada para JSON com `nome`, `uri_oficial`, `revisao` e `bytes` e executar:

```sh
PYTHONPATH=python .venv/bin/python scripts/inventariar_sih_rd.py --competencia 202401 --catalogo catalogo_observado.json --saida inventario_novo.json
```

Esse comando organiza a listagem; não comprova que ela é oficial nem adquire dados. Conferir todas as 27 UFs/partes, conflitos e tamanho observado antes de estimar volume. Adquirir um DBC mínimo, validar dois caminhos de leitura e fechar coorte/layout antes do lote nacional. `calcular_percurso_sih.R` recusa modo empírico sem gates documentais e operacionais; S04 exige ainda território validado. S03 não depende de população/SIGTAP/PDR quando sua própria coorte/cobertura estiver fechada. Somente depois do primeiro resultado real aprovado avançar a 202402. Nenhum dado sintético autoriza preencher gates reais.

## Aceite por segundo operador

Entregar código/commit, snapshot autorizado, manifesto e este guia por meio institucional. O segundo operador deve registrar identidade funcional, data, ambiente, tempo observado, erros, hash do resultado sentinela e comparação; distinguir ajuda recebida e acesso à rede. Nenhuma pessoa foi designada nem aceite humano foi inventado. REV-A03 permanece parcial até essa evidência. Para registrar resultado real, atualizar o plano canônico e gerar a mesma fila por `registrar_checkpoint_implementacao.py`.
