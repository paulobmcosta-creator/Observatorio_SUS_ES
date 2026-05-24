# Prova de conceito PySUS/CNES e estrutura Python mínima

## 1. Objetivo da Etapa 3
Esta etapa prepara uma estrutura Python mínima, experimental e não substitutiva para avaliar de forma controlada a viabilidade técnica do uso de PySUS na extração e engenharia de dados CNES.

Confirmações de escopo:
- não houve migração plena;
- não houve substituição de scripts R;
- não houve alteração de dados reais;
- não houve alteração de metadados;
- não houve alteração de workflows;
- R permanece como oráculo metodológico.

## 2. Insumos considerados
Insumos avaliados:
- docs/migracao_python/00_baseline_r_pre_migracao.md
- docs/migracao_python/01_classificacao_legado_r.md
- docs/migracao_python/02_governanca_arquitetura_hibrida.md
- README.md
- docs/convensoes_metodologicas.md
- docs/governanca_codigo.md
- docs/cnes/
- metadata/cnes/
- src/
- tests/

Estado do repositório no início desta etapa:
- branch atual: `work`
- commit HEAD: `0ea160e075e2700680fbf58c93d3c1fad3a5787f`
- último commit: `0ea160e Merge pull request #47 from paulobmcosta-creator/codex/execute-etapa-2-do-plano-de-migracao-8wj4c6`
- status inicial (`git status --short`): sem alterações rastreadas.

## 3. Pré-checagem documental
| Documento | Checagem | Resultado | Observação |
|---|---|---|---|
| README.md | Diretriz de linguagem híbrida R–Python | Compatível | README já registra Python/PySUS como preferencial para extração/engenharia e R como oráculo. |
| docs/convensoes_metodologicas.md | Contradições com arquitetura híbrida | Compatível com pendência textual | Há menção em seção de funções a “Python (quando estritamente necessário)”, que reflete redação antiga e pode gerar ambiguidade interpretativa. |
| docs/governanca_codigo.md | Regras para PRs e paridade R/Python | Compatível | Documento já exige migração por componente/paridade. |
| docs/migracao_python/02_governanca_arquitetura_hibrida.md | Coerência com objetivo da POC | Compatível | Etapa 2 determina POC controlada sem migração plena. |

Pendência documental registrada: revisar, em etapa futura, a redação legada de `docs/convensoes_metodologicas.md` que ainda contém formulação histórica de Python como exceção em trecho específico.

## 4. Estrutura Python criada
Arquivos criados:
- `python/observatorio_sus/__init__.py`
- `python/observatorio_sus/extract/__init__.py`
- `python/observatorio_sus/extract/avaliar_pysus_cnes.py`
- `python/observatorio_sus/io/__init__.py`
- `python/observatorio_sus/io/manifestos.py`
- `python/observatorio_sus/utils/__init__.py`
- `python/observatorio_sus/utils/normalizacao.py`
- `tests/python/test_estrutura_python_minima.py`
- `requirements-python-poc.txt`

A estrutura é deliberadamente mínima e experimental, focada em diagnóstico técnico sem alterar pipeline R existente.

## 5. Dependências avaliadas
Conteúdo de `requirements-python-poc.txt`:
- pysus
- pandas
- pyarrow
- pytest
- duckdb

Execução e ambiente:
- versão do Python: `Python 3.14.4`
- versão do pip (antes): `pip 26.1`
- versão do pip (após upgrade no venv): `pip 26.1.1`
- ambiente virtual criado: sim (`.venv-pysus-poc`)
- instalação das dependências: funcionou
- versão de PySUS detectada: `0.11.0`
- erro relevante observado: import indireto de `pysus.tests.test_cnes` falhou por símbolo ausente em `_cffi_backend` na inspeção de submódulos de teste, sem impedir import do pacote principal.

## 6. Script de avaliação PySUS/CNES
Script criado: `python/observatorio_sus/extract/avaliar_pysus_cnes.py`.

Características implementadas:
- argumentos CLI: `--uf`, `--competencia`, `--modo`;
- modo padrão: `diagnostico`;
- sem gravação de dados reais no repositório;
- uso de `tempfile.TemporaryDirectory` para escopo temporário;
- tentativa de import de PySUS e registro de versão;
- inspeção de submódulos relacionados a CNES;
- varredura de objetos com palavras-chave de UF/competência/CNES;
- proteção com try/except em pontos de risco;
- sem download massivo nacional;
- saída diagnóstica em stdout (JSON textual);
- retorno `0` para diagnóstico executado, inclusive quando cobertura CNES não confirmada;
- retorno não zero apenas para erro inesperado do script.

Perguntas técnicas respondidas no próprio diagnóstico quando possível; quando não confirmadas, marcador explícito: “não confirmado nesta POC”.

## 7. Funções auxiliares mínimas
### `python/observatorio_sus/utils/normalizacao.py`
Funções:
- `normalizar_nome_coluna(nome: str) -> str`
  - minúsculas
  - sem acentos
  - não alfanuméricos para `_`
  - remoção de `_` nas bordas
- `normalizar_competencia(competencia: str) -> str`
  - aceita `202601` e `2026-01`
  - retorna `2026-01`
  - lança `ValueError` para formato inválido.

### `python/observatorio_sus/io/manifestos.py`
Função:
- `criar_manifesto_execucao(...)`
  - retorna dicionário com `timestamp_utc`, `ferramenta`, `parametros`, `observacoes`.

Nenhum manifesto real foi persistido no repositório.

## 8. Testes Python mínimos
Arquivo criado: `tests/python/test_estrutura_python_minima.py`.

Cobertura aplicada (sem dependência de rede):
- importação dos módulos locais criados;
- `normalizar_nome_coluna`;
- `normalizar_competencia`;
- `criar_manifesto_execucao`;
- existência de `avaliar_pysus_cnes.py`.

Comando executado:
- `python -m pytest tests/python`

Resultado:
- `6 passed`.

## 9. Resultado da prova de conceito PySUS/CNES
Comando executado:
- `python python/observatorio_sus/extract/avaliar_pysus_cnes.py --uf ES --competencia 202601 --modo diagnostico`

Resultado:
- execução concluída com sucesso (exit code 0);
- PySUS importado com sucesso;
- versão identificada: `0.11.0`;
- módulo relacionado encontrado na inspeção: `pysus.tests.test_cnes`;
- import desse submódulo falhou por erro de símbolo `_cffi_backend`;
- não foi possível confirmar interface operacional CNES com recorte UF/competência sem risco de download inadequado;
- não foi possível confirmar CO_UNIDADE, CO_CNES, tabelas relacionais e retorno DataFrame em consulta real controlada.

Classificação da POC: **INSUFICIENTE_NESTA_POC**.

Justificativa: embora PySUS instale e importe, a POC não confirmou interface CNES operacional controlada (UF/competência/chaves/tabelas) no escopo restrito e sem download massivo.

## 10. Perguntas obrigatórias respondidas
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. PySUS instala no ambiente efêmero? | Sim | `pip install -r requirements-python-poc.txt` concluído com sucesso. | Viabilidade inicial de ambiente Python. |
| 2. PySUS importa corretamente? | Sim (pacote principal) | Diagnóstico registra `pysus_importado: true`. | Biblioteca é utilizável ao menos para inspeção. |
| 3. PySUS fornece interface CNES? | Não confirmado nesta POC | Apenas `pysus.tests.test_cnes` detectado na varredura. | Requer investigação adicional focada em API real. |
| 4. PySUS permite recorte por UF? | Não confirmado nesta POC | Diagnóstico não encontrou evidência robusta sem consulta remota. | Necessário teste dirigido com endpoint controlado. |
| 5. PySUS permite recorte por competência mensal? | Não confirmado nesta POC | Sem API operacional confirmada nesta etapa. | Requer nova validação em Etapa 4. |
| 6. PySUS retorna pandas DataFrame ou objeto conversível? | Não confirmado nesta POC | Não houve extração CNES efetiva nesta etapa. | Conversão/parquet depende de confirmação posterior. |
| 7. PySUS preserva ou permite preservar códigos como texto? | Parcialmente inferido | Risco de coerção numérica foi marcado como possível por inferência de dtype. | Exigirá contrato explícito de tipos no desenho da extração. |
| 8. PySUS fornece CO_UNIDADE? | Não confirmado nesta POC | Sem dataset CNES carregado no diagnóstico controlado. | Chave operacional ainda não validada em Python. |
| 9. PySUS fornece CO_CNES? | Não confirmado nesta POC | Sem dataset CNES carregado no diagnóstico controlado. | Código público ainda não validado em Python. |
| 10. PySUS permite acessar tabelas relacionais CNES necessárias? | Não confirmado nesta POC | Sem API relacional confirmada via inspeção segura. | Fallback pode ser necessário. |
| 11. PySUS reduz dependência de Git LFS? | Parcialmente sim (potencial) | Instalação e abordagem Python independem do materializado local para exploração. | Redução só se extração CNES operacional for comprovada. |
| 12. PySUS parece adequado como camada principal de extração CNES? | Não confirmado nesta POC | Ausência de prova operacional de cobertura CNES. | Não autoriza adoção plena nesta etapa. |
| 13. Será necessário fallback complementar fora do PySUS? | Provavelmente sim | Lacunas de cobertura/confirmabilidade nesta POC. | Planejar fallback técnico na Etapa 4. |

## 11. Implicações para a migração
- A extração Python/PySUS pode avançar apenas para desenho técnico e novos testes controlados.
- Será necessário prever fallback complementar fora do PySUS até comprovação de cobertura CNES.
- Scripts R preservados como oráculo nesta etapa (sem substituição):
  - `src/transform/preparar_estabelecimentos_cnes.R`
  - `src/transform/preparar_habilitacoes_cnes.R`
  - demais componentes sensíveis de transformação/classificação/validação.
- Partes que não devem migrar ainda: classificação metodológica de habilitações, regras de validação sensíveis e contratos implícitos ainda não formalizados.
- Contratos a formalizar antes da Etapa 4:
  - tipos e chaves (CO_UNIDADE, CO_CNES/cnes);
  - recorte por UF/competência;
  - evidência de tabelas relacionais necessárias;
  - contrato de serialização (DataFrame/Parquet) com preservação de códigos textuais.

Restrições mantidas:
- não autorizar substituição de `preparar_estabelecimentos_cnes.R` nesta etapa;
- não autorizar substituição de `preparar_habilitacoes_cnes.R` nesta etapa;
- não autorizar depreciação de scripts R;
- não autorizar mudança em `data_interim`.

## 12. Riscos identificados na Etapa 3
- PySUS não fornecer todas as tabelas CNES necessárias.
- PySUS mudar API entre versões.
- PySUS converter códigos para número sem controle explícito de dtype.
- Dependência de rede para validação operacional real.
- Download massivo involuntário em rotinas não controladas.
- Duplicação de lógica entre R e Python.
- Estrutura Python nascer sem contrato de dados formal.
- Divergência futura entre POC e pipeline real.

## 13. Critérios de aceite da Etapa 3
- [x] Documento 03_poc_pysus_cnes.md criado.
- [x] Estrutura Python mínima criada.
- [x] requirements-python-poc.txt criado.
- [x] Script de diagnóstico PySUS/CNES criado.
- [x] Funções auxiliares mínimas criadas.
- [x] Testes Python mínimos criados.
- [x] Testes Python executados ou limitação registrada.
- [x] PySUS instalado/testado ou limitação registrada.
- [x] Diagnóstico CNES executado ou limitação registrada.
- [x] Nenhum script R alterado.
- [x] Nenhum dado alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum workflow alterado.
- [x] Nenhuma substituição de pipeline executada.

## 14. Conclusão
Resultado geral da POC: a estrutura Python mínima foi criada e validada com testes locais, e PySUS foi instalado/importado. Contudo, a cobertura operacional CNES exigida (UF, competência, CO_UNIDADE, CO_CNES e tabelas relacionais) não foi comprovada de forma suficiente nesta etapa controlada.

Classificação final: **INSUFICIENTE_NESTA_POC**.

A Etapa 4 pode avançar somente para:
- desenho explícito de contratos de dados/chaves/tipos;
- investigação técnica adicional de interfaces CNES com salvaguardas de download;
- definição de fallback complementar.

Foco da Etapa 4: validação dirigida de extração controlada CNES (com recortes estritos), sem substituir pipeline R sensível.

Reforços finais:
- esta etapa não migrou pipeline;
- PySUS foi apenas avaliado;
- R permanece como oráculo;
- a próxima etapa só deve avançar para desenho de contratos/extração quando houver pelo menos suficiência parcial comprovada.

## 15. Auditoria posterior de ambiente e resolução de versão PySUS

Esta auditoria curta foi executada após a Etapa 3 para esclarecer a divergência entre a versão instalada na POC (`0.11.0`) e a linha atual esperada do PySUS (`2.0.4`).

### 15.1 Python/pip efetivamente usados na Etapa 3
Comandos de auditoria no ambiente padrão (fora de venv):
- `python --version` -> `Python 3.14.4`
- `which python` -> `/root/.pyenv/shims/python`
- `python -c "import sys; print(sys.executable); print(sys.version)"` -> executável `/root/.pyenv/versions/3.14.4/bin/python`
- `python -m pip --version` -> `pip 26.1 (python 3.14)`

Implicação: a Etapa 3 foi executada com Python 3.14 e, nesse contexto, o resolvedor do pip selecionou a versão mais nova compatível com esse interpretador (PySUS `0.11.0`).

### 15.2 Versões disponíveis de PySUS observadas na auditoria
Comando:
- `python -m pip index versions pysus`

Resultado resumido:
- índice exibiu `0.11.0` como versão instalada/listada no contexto ativo;
- versões `2.0.0`–`2.1.0` aparecem como **ignoradas** por requisito de Python (`>=3.10,<3.14`) quando consultadas a partir do Python 3.14.

### 15.3 Tentativa de instalar PySUS 2.x no Python da Etapa 3 (3.14)
Comando:
- `python -m pip install --dry-run --no-cache-dir "pysus>=2.0.4,<2.1"`

Resultado:
- falha com `No matching distribution found` para a faixa `>=2.0.4,<2.1` no Python 3.14;
- causa explícita informada pelo pip: versões 2.x exigem `Requires-Python >=3.10,<3.14`.

Conclusão parcial: em Python 3.14, a instalação de PySUS 2.x é bloqueada por restrição declarada de compatibilidade.

### 15.4 Auditoria em ambiente efêmero Python 3.12
Comandos executados:
- `python3.12 --version` -> `Python 3.12.3`
- `which python3.12` -> `/root/.pyenv/shims/python3.12`
- `python3.12 -m venv .venv-pysus-2x`
- `. .venv-pysus-2x/bin/activate`
- `python --version` -> `Python 3.12.3`
- `python -m pip --version` -> `pip 24.0` (atualizado para `26.1.1`)
- `python -m pip install --no-cache-dir "pysus>=2.0.4,<2.1" pandas pyarrow pytest duckdb`
- `python -c "import pysus, sys; print(sys.version); print(getattr(pysus, '__version__', 'sem __version__'))"`
- `python -m pip show pysus`

Resultado:
- instalação bem-sucedida de `pysus-2.0.4` em Python `3.12.3`;
- import bem-sucedido e versão confirmada como `2.0.4`.

### 15.5 Implicação para a classificação da Etapa 3
A classificação original da Etapa 3 (`INSUFICIENTE_NESTA_POC`) permanece válida para o **recorte executado** (Python 3.14 + PySUS 0.11.0), mas a auditoria demonstra que a POC **não avaliou a linha atual do PySUS** em um Python compatível.

Portanto, para decisão sobre adoção do PySUS atual, a evidência da Etapa 3 deve ser tratada como **inconclusiva quanto ao PySUS 2.x**.

### 15.6 Recomendação para próxima etapa
Recomenda-se repetir a POC controlada com:
- ambiente fixado em Python 3.12 ou 3.13 (sempre `<3.14`);
- instalação explícita de `pysus>=2.0.4,<2.1`;
- mesmas salvaguardas contra download massivo;
- revalidação objetiva de recorte por UF/competência e presença de `CO_UNIDADE`/`CO_CNES`.

Somente após essa repetição será possível concluir adequadamente sobre suficiência do PySUS **atual** como camada principal/parcial de extração CNES.
