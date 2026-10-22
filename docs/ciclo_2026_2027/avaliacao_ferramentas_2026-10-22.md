# Aquisição e processamento: avaliação reconciliada de ferramentas

Avaliação de 22/10/2026, incorporada a **R08/R19 do plano existente**. Autor da execução: Codex, sob solicitação do pesquisador. Nenhuma revisão humana, execução discente ou homologação metodológica foi presumida. D1 §§4.2–4.3 e o pedido atual orientam Python/PySUS para engenharia quando comprovado por família; os preparadores R permanecem como referência. O relatório 2025–2026 não foi alterado.

## Decisão e alcance

Integrar o percurso **CSV verificado → PyArrow/Parquet → leitura de auditoria DuckDB**, aprovado nesta rodada para o snapshot CNES 202601. Manter PySUS como candidato preferencial de aquisição por família, com requisitos explícitos de origem, integridade e paridade. Manter microdatasus como alternativa de aquisição/leitura e referência de recodificações a examinar. Não trocar os preparadores R por funções `process_*`, nem equiparar ST/DBC ao pacote CSV relacional com `CO_UNIDADE`.

A [matriz completa de decisão](matriz_decisao_ferramentas.csv) registra **13 candidatos/versões**, endereço, pin, licença, manutenção observada, cobertura, chaves, limitações, ambiente e condição de integração. A [matriz por família](cobertura_ferramentas_por_familia.csv) tem **14 linhas** e separa capacidade implementada, evidência histórica, download, conversão, equivalência e alternativa oficial. Cobertura declarada em um diretório ou registry não significa que todos os meses, famílias e campos existam.

| Componente | Decisão nesta rodada |
|---|---|
| PySUS 2.0.4 | Reutilizar cliente/conversor; aquisição condicionada por família; extra DBC testado separadamente; leitura sem recodificação antes do contrato |
| PySUS HEAD 2.11.7 | Manter como opção de atualização em ambiente separado; mudança de dependências/API/leitor não homologada |
| microdatasus 3.0.0 | Alternativa de aquisição/leitura local; não aplicar `process_*` à camada RAW |
| DataHub Brasil — rafa-trindade/kaggle-datahub | Identificado pelo usuário e examinado; alternativa condicionada, sem adoção integral; [seis casos locais e limites](avaliacao_datahub_2026-10-22.md) |
| PyArrow 19.0.1 / DuckDB 1.5.6 | Integrar serialização e reutilizar auditoria no escopo comprovado |
| pandas 2.3.3 / dbfread 2.0.7 | Reutilizar dependências existentes com política explícita de tipos, ausentes e registros excluídos |
| pyreaddbc 2.0.4 | Reutilizar como extra de conversão; fixture aprovada, arquivo oficial ainda necessário |
| read.dbc 1.2.0 | Alternativa para segundo leitor; descartar inclusão redundante como dependência obrigatória agora |
| healthbR 0.4.0.9000 | Alternativa nova, encontrada na origem do leitor microdatasus; não introduzir terceiro pipeline sem lacuna comprovada |
| GeoPandas 1.1.1 / QGIS 3.44.0 | Preservar como opções geográficas posteriores às referências territoriais; nenhuma instalação nesta rodada |

Não se está descartando PySUS por uma falha de rede, nem adotando qualquer biblioteca por presença no GitHub. A preferência tecnológica continua subordinada ao contrato de dados.

## Identificação, acervo e fontes examinadas

A busca cobriu os textos dos dossiês, o PDF da proposta, o prompt inicial/complementar, documentação, código, dependências e **227 commits acessíveis por `git rev-list --all`**. Foram recuperados os dois repositórios explicitamente citados em D1: [AlertaDengue/PySUS](https://github.com/AlertaDengue/PySUS) e [rfsaldanha/microdatasus](https://github.com/rfsaldanha/microdatasus). pandas, PyArrow e DuckDB já constavam das dependências e decisões; GeoPandas/QGIS constam de D1/README. dbfread/pyreaddbc e read.dbc/healthbR foram identificados nas dependências e origens dos projetos examinados, **não apresentados como decisões prévias do Observatório**.

**DataHub — identificação resolvida nesta complementação:** a busca inicial encontrou somente a menção em D2 §26, sem URL, e nenhuma ocorrência nos 227 commits ou no PDF. O [registro histórico da busca](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/busca_datahub_historico.json) permanece intacto. O usuário forneceu depois o endereço [rafa-trindade/kaggle-datahub](https://github.com/rafa-trindade/kaggle-datahub), identificado como **DataHub Brasil**, de Rafael Trindade. O commit `60aa9cbd82509e0595d5c99ec74794e6be1588bd` foi examinado e seis casos locais foram executados. A [avaliação complementar](avaliacao_datahub_2026-10-22.md) registra cobertura, licença, ambiente, resultados e decisão: alternativa condicionada; sem adoção integral, sem substituir RAW oficial, histórico CNES ou preparadores R. Os outros projetos homônimos não foram associados a essa identidade.

Foram consultados código, README, licenças, descritores de dependências e testes dos projetos originais. [Fontes originais com URLs permanentes e SHA-256](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/fontes_originais.csv) e [pins dos repositórios](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/pins_repositorios.json). Os pins separam PySUS instalado/tag `363029b550eaf5ae56a64f46641ab25dd47a0f12` do HEAD `47e8371ab85cd00a1373af5965216852c0b11cad`; microdatasus foi examinado em `7109ec2c42cf674ba453e0d7a20d2f464890b543`. O código de pyreaddbc foi obtido do sdist original PyPI 2.0.4, SHA-256 `e3ce8f12b0feec3d6bf2b3722309346f015a22e8279f9789e9eeda869d8b33d1`; não foi inventado um repositório próprio ausente nos metadados.

“Manutenção observada” significa a data/revisão, changelog e testes encontrados no recorte examinado. Não houve auditoria de issues, governança ou garantia de suporte futuro; para versões pinadas de bibliotecas gerais, não foi alegado que fossem a release mais recente. A matriz registra GPL/AGPL/MIT/BSD/Apache conforme os arquivos examinados, inclusive a diferença entre a licença AGPL declarada de pyreaddbc e o cabeçalho GPL do módulo Python. Código de terceiros não foi incorporado ao pipeline; a fixture sintética microdatasus inclui atribuição e licença MIT.

## Confronto com o trabalho anterior

1. **Permanece válido:** cache gzip com SHA-256; separação `CO_UNIDADE`/CNES público; recorte por município gestor explicitado; preparadores sem descarte silencioso; contratos e perfis D1/D2; fila normativa e territorialização com pins ainda pendentes. Nenhuma conclusão normativa ou regional foi promovida por esta PoC.
2. **Precisão necessária no histórico PySUS:** 5N.5 registra ST/LT/SR em ES 202401, 202406 e 202412, com estruturas estáveis; 5N.7–8F registra timeout de ST, e 5N.7–8G registra sucesso em quatro caminhos, com ST 8.867 × 208 e chamada de 106,378 s. A conclusão é acesso observado com intermitência e contrato incompleto, não incapacidade geral do PySUS. Esses resultados antigos são documentais; não equivalem a arquivos/hash de origem revalidados agora.
3. **Origem do transporte:** no PySUS 2.0.4, `_fetch_data` abre `PySUS()`, que carrega o catálogo DuckLake em `https://nbg1.your-objectstorage.com/pysus/public/catalog.db` e lê Parquet. O pacote também possui cliente FTP; a função de conveniência usada no histórico não prova aquisição direta do DBC oficial. Um espelho pode ser útil, mas requer pareamento com o arquivo oficial e proveniência própria. O nome DuckLake não identifica DataHub.
4. **Chaves e recodificação:** o contrato local já sinaliza `CO_UNIDADE` ausente no ST observado e `CODUFMUN` com semântica potencial. Nada nesta rodada resolve essas pendências. `Parquet.load(parse=True)` do PySUS converte `CODMUNRES`/`IDADE` para números; `add_dv=True` é padrão e pode modificar geocódigos. A PoC confirma perda de zero inicial mesmo com `add_dv=False`. Usar `parse=False` conserva o que está no Parquet, mas não recupera informação perdida na geração do espelho.
5. **microdatasus:** `fetch_datasus` usa `read_dbc(as_character=TRUE)`; a conversão para texto ocorre depois da interpretação DBF. `process_cnes` transforma `CNPJ_MAN` em número; `process_sim` recodifica categorias e trunca códigos municipais. Essas rotinas não devem substituir a correspondência central ou o RAW. Download com `stop_on_error=TRUE`, `track_source=TRUE` e `vars=NULL` melhora controle, mas ainda exige manifesto de cobertura: períodos indisponíveis geram aviso, e arquivos temporários são apagados. É preciso preservar o arquivo recebido antes do leitor e verificar esperado versus obtido.
6. **SIGTAP:** `fetch_sigtab()` baixa `TAB_SIA.zip/TB_SIGTAW.dbf` corrente, com código/descrição. Isso não entrega o pacote SIGTAP mensal histórico com relações e vigências. Os 77 candidatos TCC permanecem preliminares; nenhuma whitelist foi autorizada por essa função.
7. **Ambiente:** `PYSUS_CACHEPATH` existe em 2.0.4 e foi usado na nova sondagem, sem redefinir `HOME`. Os scripts históricos de isolamento foram preservados como diagnósticos, não escolhidos para o novo executor. Não houve atualização geral: HEAD 2.11.7 requer NumPy ≥2.4, enquanto o ambiente validado contém 1.26.4 e PySUS 2.0.4 requer NumPy <2. O extra pyreaddbc foi instalado isoladamente, sem alterar a instalação base.

## Prova de conceito e resultados de referência

Evidências canônicas: [execução](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/poc_20261022_v2/execucao.json), [manifestos](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/poc_20261022_v2/manifestos_conversao.json), [paridade R](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/poc_20261022_v2/paridade_r.csv) e [115 verificações](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/poc_20261022_v2/contrato_r.csv). A execução durou cerca de cinco minutos, incluindo a reexecução R; isso não é benchmark comparativo de ferramentas.

| Etapa | Experimento | Resultado e limite |
|---|---|---|
| Aquisição | Uma chamada PySUS LT/ES/202401, subprocesso limitado a 25 s; uma sondagem HEAD HTTPS do caminho oficial | Catálogo e sondagem oficial recusados com `403 Forbidden` pelo proxy. Nenhum download oficial validado. FTP direto não tentado: não há concessão TCP. Não comprova ausência do arquivo ou defeito da biblioteca |
| Conversão DBC | Fixture sintética original microdatasus, dois registros, via PySUS 2.0.4 + pyreaddbc 2.0.4 | Campos e zeros `001`/`010` preservados; léxico numérico/data preservado. R de referência espera `1.5/NA` e `2020-01-02/NA`; PySUS entrega texto e os marcadores `*******************`/`00000000`. Não há igualdade automática de tipos/ausentes |
| Conversão CSV | Fonte nacional CNES 202601, 602.160 linhas × 56 campos, Latin-1; dois derivados R ES | Digest independente `csv` versus Parquet inclui todas as células, cabeçalho, ordem e duplicatas. Sem seleção, deduplicação ou coerção; fonte com SHA conhecido preservada |
| Consulta | DuckDB em memória sobre derivados R serializados | Oito medidas iguais à referência: 12.548 estabelecimentos/chaves, 1.297 códigos com zero inicial, 78 municípios gestores, 1.963 habilitações, 501 selecionadas = 304 status interno validado + 197 revisar |
| Paridade do percurso | Parquet nacional restituído em CSV → mesmos preparadores R → comparação integral com execução de reconciliação | Dois produtos com campos, ordem e valores idênticos; 115 verificações aprovadas. Prova o percurso de serialização, não uma reimplementação analítica Python, nem paridade ST/CSV, nem indicadores TCC |
| Contraexemplo | Parquet sintético `CODMUNRES="012345"`, `IDADE="001"` | Leitura padrão com `add_dv=False`: `12345` e `1`; `parse=False`: textos originais. Caso explícito que impede adoção da leitura recodificada como RAW |

O CSV nacional de 284.224.999 bytes gerou Parquet de 80.037.744 bytes. Este resultado de tamanho não autoriza retirar RAW ou histórico LFS. O gzip já verificado (85.482.494 bytes) continua como alternativa de cache e recuperação, sem migração destrutiva. Os novos arquivos grandes estão somente em `.cache/avaliacao_ferramentas/`, ignorada pelo Git; evidências publicáveis contêm hashes e agregados, não registros pessoais.

A primeira execução `poc_20261022` parou na expectativa incorreta de vazios da fixture DBC. O diagnóstico foi preservado, a expectativa foi corrigida para distinguir léxico DBF de interpretação R e a execução inteira repetida em `poc_20261022_v2`. Nenhum dado foi alterado para fazer o teste passar. A referência DBC provém das asserções do projeto microdatasus; o pacote microdatasus não foi instalado/executado nesta rodada. A comparação R efetivamente executada foi a dos preparadores validados do Observatório.

Há limites adicionais a conferir em DBC real: `dbfread` separa registros marcados como excluídos e a iteração normal usada pelo wrapper não os inclui; o wrapper PySUS remove padding/NUL e usa CP1252 com substituição de erro. A fixture não contém todos esses casos. A etapa seguinte precisa confrontar contagem do cabeçalho, ativos/excluídos, campos, valores e encoding, sem descartar linhas por conveniência.

## Incremento implementado e reprodução

- [Adaptador de serialização](../../python/observatorio_sus/transform/converter_csv_parquet.py): APIs PyArrow existentes, campos textuais explícitos, hash de entrada, destino novo, conferência integral independente, manifesto com origem e limites. Não implementa aquisição, decoder DBC ou regras sanitárias.
- [Executor da PoC](../../scripts/executar_poc_ferramentas.py) e [comparador R](../../scripts/conferir_paridade_parquet_r.R): reaproveitam preparadores e contratos atuais. A comparação R é estrita, inclusive metadados; em outra data, `data_processamento` pode diferir e deve ser auditado explicitamente antes de aprovar a repetição.
- [Sondagem limitada de aquisição](../../scripts/avaliar_aquisicao_pysus.py): proxy/CA herdados, sem alteração de política e sem repetição automática após recusa. Não repetir enquanto o acesso continuar negado.
- [Testes de serialização](../../tests/python/test_converter_csv_parquet.py): zeros/chave de 31 dígitos, Latin-1/acentos, separador/newline dentro do campo, duplicatas, `NA`/vazio/espaços distintos, hash divergente, cabeçalho duplicado e linha incompleta. [Log Python](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/testes_python.txt): **55 testes aprovados** (51 preexistentes + 4 novos). O [workflow da serialização](../../.github/workflows/validar_serializacao_python.yml) executa os quatro testes novos com dependências pinadas, sem aquisição DATASUS. CI remoto não executado nesta rodada.

O [ambiente Python observado](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/ambiente_python.txt) fixa as dependências base para reprodução; pyreaddbc 2.0.4 é extra isolado. No ambiente preparado, a execução foi:

```bash
UV_CACHE_DIR=/workspace/.setup-observatorio/uv-cache UV_SYSTEM_CERTS=true \
  uv pip install --python .venv/bin/python \
  --target .cache/avaliacao_ferramentas/dependencias_dbc --no-deps pyreaddbc==2.0.4

PATH=/workspace/.setup-observatorio/bin:$PATH \
PYTHONPATH=python:.cache/avaliacao_ferramentas/dependencias_dbc \
  .venv/bin/python scripts/executar_poc_ferramentas.py \
  /workspace/.cache/observatorio-cnes-lfs/objects/a6/dd/a6dd87e847e2905949dd160f1d88ddd5e7f088fdf61b1124404cf566297d36d6 \
  .cache/avaliacao_ferramentas/poc_20261022_v2 \
  metadata/ciclo_2026_2027/avaliacao_ferramentas/poc_20261022_v2

PYTHONPATH=python .venv/bin/python -m pytest tests/python -q
```

Os diretórios registrados já existem e são preservados: uma repetição deve usar identificadores novos. A fonte pode estar em outro caminho, mas o executor exige o SHA-256 original. O sdist e seu hash estão registrados; o extra não exige reconstrução do ambiente produtivo.

## Proveniência, alternativas e continuidade

A fonte permanece **o sistema oficial**, e a biblioteca/espelho são transportes ou conversores. Um manifesto novo de aquisição deve separar URL oficial, URL efetivamente usada, arquivo original, sistema/família/UF/competência/parte, estado final/preliminar, instante de obtenção, bytes, SHA-256, versão do cliente e do layout, cobertura esperada/observada e perdas. Preservar DBC/ZIP/CSV exato antes de converter. Comparar espelho com RAW oficial; sem esse vínculo, não promover o Parquet espelhado como fonte bruta verificada. Nos arquivos recebidos do Observatório, URL/data da coleta primária permanecem **não documentadas**; o hash comprova identidade da recuperação Git, não inventa uma coleta oficial retrospectiva.

R08/R19 seguem com ensaio de **um arquivo por família**, começando por LT/ES/202401 para retomar a evidência histórica e, separadamente, ST para o contrato que não fornece `CO_UNIDADE`. Exigir arquivo oficial com hash, dois leitores, contagens/campos/chaves/ausentes e comparação metodológica no mesmo período. Só depois ampliar para extremos 2014/2024 e mudanças de layout; um arquivo aprovado não certifica a década. Não abrir download nacional amplo ou novas subetapas intermináveis de timeout.

Quando a biblioteca não cobrir arquivo/período/chave, manter arquivo oficial obtido por meio autorizado e reutilizar conversor existente; microdatasus/read.dbc são alternativas de leitura. Pacote CNES CSV relacional completo continua necessário quando o contrato demanda `CO_UNIDADE`; não concatenar município e CNES para fabricá-lo. SIGTAP histórico, denominadores e regionalização continuam com suas próprias fontes e contratos. SIH/SIA para fluxos de residentes ES exigem conferir cobertura de prestadores externos; UF do arquivo não é automaticamente residência. Saúde cardiovascular não se reduz a um filtro genérico da biblioteca.

Retomar também **R06/T01/R18** (território/população oficiais) e **R17** (um pacote SIGTAP histórico), conforme as dependências já registradas. Os hosts da rodada 3 seguem pendentes; esta sondagem acrescenta `ftp.datasus.gov.br` e o transporte `nbg1.your-objectstorage.com` à avaliação de acesso. A URL HTTPS sondada não comprova que FTP esteja disponível por HTTPS. Não foi alterada a política de rede nem tentado contorná-la.

O plano único, a matriz de impacto e a lista de recálculos foram atualizados. **Não há recálculo substantivo novo exigido pela serialização aprovada**; os dois produtos existentes foram reexecutados para comparação e permaneceram iguais. As séries TCC ainda não calculadas continuam dependentes de fontes/layouts/regras, sem resultados fabricados. A documentação anterior está preservada em `referencias/estado_pre_avaliacao_ferramentas.zip`; arquivos e evidências anteriores não foram reescritos, exceto os documentos de estado atual explicitamente relacionados no manifesto de preservação.

Conferência de preservação: [268 arquivos anteriores auditados](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/preservacao_sha256.csv), 261 idênticos e sete documentos atuais com backup byte a byte. Os quatro testes do novo workflow passaram também em ambiente isolado apenas com suas dependências ([log](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/testes_dependencias_ci.txt)); a execução remota do CI permanece não realizada.


Complementação após o link do usuário: a coluna DataHub foi acrescentada às 14 linhas de cobertura e sua decisão foi atualizada na matriz de 13 candidatos/versões. Evidências adicionais em [avaliacao_datahub](../../metadata/ciclo_2026_2027/avaliacao_datahub/README.md); os manifestos acima continuam descrevendo a avaliação anterior. As dez versões documentais anteriores à identificação estão preservadas em `referencias/estado_pre_identificacao_datahub.zip`. Não foi alterado qualquer resultado anterior para justificar a decisão.
