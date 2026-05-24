# Classificação formal do legado R para migração/hibridização Python/PySUS

## 1. Objetivo da Etapa 1
Esta Etapa 1 classifica formalmente o legado R para orientar a migração/hibridização futura com Python/PySUS, sem executar migração e sem alterar ativos existentes do repositório.

A classificação foi conduzida em dois eixos:
1. **valor metodológico** (quanto o componente preserva regras científicas, de chave, join, escopo e integridade);
2. **valor operacional futuro** (quanto o componente deve seguir executando em R, ser portado, substituído ou apenas mantido como referência temporária).

## 2. Insumos considerados
Principal insumo utilizado:
- `docs/migracao_python/00_baseline_r_pre_migracao.md`

Também foram considerados:
- `src/`
- `tests/`
- `metadata/cnes/`
- `docs/cnes/`
- `config/`
- `scripts/`
- `.github/workflows/`
- `.gitignore`
- `.gitattributes`

Snapshot de versionamento no início desta Etapa 1:
- **Branch:** `work`
- **HEAD atual (`git rev-parse HEAD`):** `32f031400666025038fcc6abb1fcc82ae77b6932`
- **Último commit (`git log -1 --oneline`):** `32f0314 Merge pull request #44 from paulobmcosta-creator/codex/create-baseline-document-for-r-project`
- **Status inicial (`git status --short`):** sem alterações rastreadas.

## 3. Critérios de classificação

### 3.1 Valor metodológico
Cada componente foi classificado como **Alto**, **Médio** ou **Baixo**.

Critérios de valor metodológico alto:
- contém regra de chave;
- contém regra de join;
- contém classificação sanitária/metodológica;
- contém decisão sobre escopo do Observatório;
- contém regra de integridade referencial;
- contém regra de validação crítica;
- contém lógica de indicador ou semântica analítica relevante.

### 3.2 Valor operacional futuro
Cada componente foi classificado em uma das opções:
- **Manter no curto prazo**;
- **Substituir por Python/PySUS**;
- **Portar para Python**;
- **Preservar como oráculo temporário**;
- **Avaliar caso a caso**;
- **Deprecar futuramente**.

### 3.3 Status final sugerido
Rótulos finais adotados:
- `PRESERVAR_COMO_PATRIMONIO_METODOLOGICO`
- `PRESERVAR_COMO_ORACULO_TEMPORARIO`
- `SUBSTITUIR_POR_PYTHON_PYSUS`
- `PORTAR_PARA_PYTHON_COM_PARIDADE`
- `AVALIAR_CASO_A_CASO`
- `DEPRECAR_APOS_PARIDADE`
- `MANTER_NO_CURTO_PRAZO`

**Importante:** nenhum status implica remoção imediata de arquivos.

## 4. Princípios herdados da baseline
A classificação desta etapa incorpora obrigatoriamente os princípios da Etapa 0:
- não classificar componente como descartável apenas por estar em R;
- diferenciar código operacional substituível de regra metodológica preservável;
- tratar CSVs `data_interim` sem `co_unidade` como produtos históricos, não contrato estrutural vigente;
- usar `co_unidade` como eixo decisório central;
- preservar `metadata/cnes/classificacao_habilitacoes_cnes.csv` como patrimônio metodológico;
- tratar falha Git LFS como risco operacional, não como falha lógica demonstrada do código R;
- considerar scripts de transformação/classificação como fonte de regra até existir paridade Python.

## 5. Inventário classificado dos scripts R

| Caminho | Camada | Função principal | Valor metodológico | Valor operacional futuro | Status final sugerido | Regras a preservar | Justificativa | Observações para futura migração Python/PySUS |
|---|---|---|---|---|---|---|---|---|
| `src/extract/ler_arquivos_cnes.R` | Extract | Leitura robusta de arquivos CNES com preservação textual e rastreabilidade | Médio | Substituir por Python/PySUS | `SUBSTITUIR_POR_PYTHON_PYSUS` | preservação de códigos como texto; validação de arquivos; rastreio de origem | Camada tipicamente operacional de ingestão, alvo natural para PySUS/IO Python | Implementar leitor Python com paridade de tipos e validações |
| `src/transform/padronizar_cnes_interim.R` | Transform | Padronização estrutural (colunas, competência, referência) | Alto | Portar para Python | `PORTAR_PARA_PYTHON_COM_PARIDADE` | normalização de colunas; derivação de competência; regras de IDs | Define semântica estrutural do produto interim | Converter em contrato de transformação independente de linguagem |
| `src/transform/executar_pipeline_piloto_cnes.R` | Transform/Orquestração | Orquestra pipeline piloto E2E | Médio | Substituir por Python/PySUS | `SUBSTITUIR_POR_PYTHON_PYSUS` | sequência de etapas; pontos de validação; logs | Script de execução piloto, com forte caráter operacional | Reimplementar orquestração em Python mantendo checkpoints e logs |
| `src/transform/preparar_estabelecimentos_cnes.R` | Transform | Preparação de estabelecimentos CNES ES | Alto | Portar para Python | `PORTAR_PARA_PYTHON_COM_PARIDADE` | chave operacional `co_unidade`; uso de `cnes` como código público; filtros territoriais; classificação `atende_sus` | Contém regra de negócio crítica e decisão metodológica de chave | Portar após formalização explícita de contratos de join/chaves |
| `src/transform/preparar_habilitacoes_cnes.R` | Transform | Integração e preparação de habilitações CNES | Alto | Portar para Python | `PORTAR_PARA_PYTHON_COM_PARIDADE` | join por `co_unidade`; chave composta `codigo_habilitacao+tipo_habilitacao`; defaults de classificação | Núcleo metodológico da integração de habilitações | Priorizar testes de paridade por join/classificação |
| `src/transform/classificar_habilitacoes_cnes.R` | Transform/Classificação | Classificação metodológica de habilitações | Alto | Preservar como oráculo temporário | `PRESERVAR_COMO_PATRIMONIO_METODOLOGICO` | chave composta obrigatória; consistência classificatória; escopo Observatório | É patrimônio metodológico explícito (regra sanitária) | Python deve consumir a mesma taxonomia/classificação |
| `src/transform/auditar_fora_escopo_habilitacoes_cnes.R` | Transform/Auditoria | Auditoria de itens fora do escopo | Médio | Avaliar caso a caso | `AVALIAR_CASO_A_CASO` | critérios de fora de escopo; rastreabilidade de revisão | Útil para governança de qualidade, menos central ao pipeline mínimo | Pode virar rotina Python de QA ou permanecer em R |
| `src/transform/corrigir_falsos_negativos_habilitacoes_cnes.R` | Transform/Correção | Ajustes metodológicos de classificação (falsos negativos) | Alto | Preservar como oráculo temporário | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | regras de correção classificatória; critérios de exceção | Regra sensível de qualidade semântica; exige paridade cuidadosa | Manter como referência até validação estatística no Python |
| `src/indicators/calcular_indicadores_cnes_oferta.R` | Indicators | Cálculo de indicadores de oferta CNES | Alto | Avaliar caso a caso | `AVALIAR_CASO_A_CASO` | semântica de indicadores; contratos de entrada; agregações | Indicadores podem ser implementados em R ou Python, mantendo semântica | Definir contrato de indicador antes de decidir linguagem final |
| `src/validation/validar_pipeline_cnes.R` | Validation | Validação estrutural e de consistência do pipeline | Alto | Preservar como oráculo temporário | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | validações críticas; falha explícita por ausência de colunas/saídas | Referência objetiva para checks de paridade | Reescrever em Python apenas após espelhamento 1:1 das regras |
| `scripts/instalar_dependencias_r.R` | Scripts/Infra | Instalação de dependências R locais | Baixo | Manter no curto prazo | `MANTER_NO_CURTO_PRAZO` | lista de dependências R | Suporte operacional ao legado enquanto houver execução R | Reclassificar para deprecação após ambiente Python consolidado |

## 6. Classificação dos testes R

| Caminho do teste | Tipo de teste | Dependência principal | Resultado na Etapa 0 | Valor como oráculo R versus Python | Status sugerido | Observação |
|---|---|---|---|---|---|---|
| `tests/test_estrutura_repositorio.R` | Estrutural | Árvore do repositório | Passou | Alto | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Garante pré-condições de organização |
| `tests/test_metadata_cnes.R` | Metadados | `metadata/cnes/` | Passou | Alto | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Valida consistência de metadados |
| `tests/test_classificacao_habilitacoes_cnes.R` | Regra metodológica | função classificadora + metadata | Passou | Muito alto | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Crítico para paridade de classificação |
| `tests/test_ler_arquivos_cnes.R` | Unitário de extração | fixtures CNES | Passou | Alto | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Referência para novo leitor Python |
| `tests/test_padronizar_cnes_interim.R` | Unitário de transformação | fixtures + função de padronização | Passou | Alto | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Define comportamento esperado de padronização |
| `tests/test_validar_pipeline_cnes.R` | Validação contratual | fixtures + validação | Passou | Alto | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Essencial para checks de integridade |
| `tests/test_executar_pipeline_piloto_cnes.R` | Integração/orquestração | fixtures + temporários | Passou | Médio/alto | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Útil para comportamento E2E do piloto |
| `tests/teste_pipeline_piloto_cnes.R` | Integração mínima | fixture piloto | Passou | Médio | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Complementar ao teste E2E |
| `tests/test_indicadores_cnes_oferta.R` | Indicadores | dados sintéticos | Passou | Alto | `PRESERVAR_COMO_ORACULO_TEMPORARIO` | Determinístico para semântica de indicadores |
| `tests/test_base_estabelecimentos_cnes.R` | Integração com dado real | `data_raw/cnes/202601` (LFS) | Falhou por LFS | Alto (potencial) | `MANTER_NO_CURTO_PRAZO` | Oráculo funcional potencial, dependente de materialização LFS |
| `tests/test_base_habilitacoes_cnes.R` | Integração com dado real | `data_raw/cnes/202601` + metadata | Falhou por LFS | Alto (potencial) | `MANTER_NO_CURTO_PRAZO` | Falha operacional de dado indisponível, não falha lógica demonstrada |

Classificação consolidada dos testes:
- Os 9 testes que passaram permanecem **oráculos úteis** para comparação R vs Python.
- Os 2 testes bloqueados por LFS permanecem **oráculos funcionais potenciais**, condicionados à materialização do dado real.

## 7. Classificação dos metadados CNES

| Caminho | Tipo de artefato | Função | Valor metodológico | Uso na migração | Status sugerido | Observação |
|---|---|---|---|---|---|---|
| `metadata/cnes/classificacao_habilitacoes_cnes.csv` | Tabela classificatória | Matriz de classificação de habilitações | Alto | Regra central de paridade | `PRESERVAR_COMO_PATRIMONIO_METODOLOGICO` | Patrimônio metodológico obrigatório |
| `metadata/cnes/dicionario_estabelecimentos_cnes.csv` | Dicionário | Semântica de campos de estabelecimentos | Alto | Contrato/pré-contrato de dados | `PORTAR_PARA_PYTHON_COM_PARIDADE` | Preservar e adaptar nomenclatura |
| `metadata/cnes/dicionario_habilitacoes_cnes.csv` | Dicionário | Semântica de campos de habilitações | Alto | Contrato/pré-contrato de dados | `PORTAR_PARA_PYTHON_COM_PARIDADE` | Base para mapeamento de schema Python |
| `metadata/cnes/schema_estabelecimentos_cnes.csv` | Schema tabular | Estrutura esperada de estabelecimentos | Alto | Contrato técnico a espelhar | `PORTAR_PARA_PYTHON_COM_PARIDADE` | Revisar aderência com `co_unidade` |
| `metadata/cnes/schema_habilitacoes_cnes.csv` | Schema tabular | Estrutura esperada de habilitações | Alto | Contrato técnico a espelhar | `PORTAR_PARA_PYTHON_COM_PARIDADE` | Validar chaves compostas no Python |
| `metadata/cnes/schema_cnes_piloto.yml` | Schema YAML | Contrato do piloto | Alto | Fonte para validações Python | `PORTAR_PARA_PYTHON_COM_PARIDADE` | Converter para validação automatizada multi-linguagem |
| `metadata/cnes/dicionario_cnes_piloto.csv` | Dicionário piloto | Descrição de campos do piloto | Médio | Apoio ao desenho da camada Python | `MANTER_NO_CURTO_PRAZO` | Referência de transição |
| `metadata/cnes/matriz_revisao_produtos_cnes_observatorio.csv` | Matriz de revisão | Governança/revisão de produtos | Médio | Apoio gerencial de migração | `AVALIAR_CASO_A_CASO` | Documentação auxiliar, não regra operacional |
| `metadata/cnes/auditoria_linguistica_textos_ingles.csv` | Auditoria linguística | Padronização textual | Baixo/Médio | Apoio documental | `AVALIAR_CASO_A_CASO` | Não é regra de transformação principal |

Artefatos adicionais relevantes:
- `metadata/cnes/dicionario_indicadores_cnes_oferta.csv` -> `AVALIAR_CASO_A_CASO` (alto valor semântico para indicadores).
- `metadata/cnes/auditoria_fora_escopo_habilitacoes_cnes_202601.csv` -> `MANTER_NO_CURTO_PRAZO` como registro de auditoria histórica.

## 8. Classificação da documentação CNES

| Caminho | Função | Valor metodológico | Uso para Etapa 2/3 | Status sugerido | Observação |
|---|---|---|---|---|---|
| `docs/cnes/README.md` | Porta de entrada documental do módulo CNES | Médio | Contexto geral | `MANTER_NO_CURTO_PRAZO` | Atualizar na Etapa 2 (não nesta etapa) |
| `docs/cnes/decisoes_metodologicas_cnes.md` | Decisões de chave/join/classificação | Alto | Base para contratos independentes de linguagem | `PRESERVAR_COMO_PATRIMONIO_METODOLOGICO` | Documento central de método |
| `docs/cnes/base_estabelecimentos_cnes.md` | Especificação da base de estabelecimentos | Alto | Paridade estrutural Etapa 2/3 | `PRESERVAR_COMO_PATRIMONIO_METODOLOGICO` | Alto valor para regra de chave e escopo |
| `docs/cnes/base_habilitacoes_cnes.md` | Especificação da base de habilitações | Alto | Paridade estrutural Etapa 2/3 | `PRESERVAR_COMO_PATRIMONIO_METODOLOGICO` | Alto valor para classificação/joins |
| `docs/cnes/contrato_dados_cnes_piloto.md` | Contrato técnico do piloto | Alto | Tradução para contrato híbrido R/Python | `PORTAR_PARA_PYTHON_COM_PARIDADE` | Não substituir por roadmap |
| `docs/cnes/produtos_tabulares_cnes.md` | Catálogo de produtos tabulares | Médio/Alto | Mapear outputs na migração | `MANTER_NO_CURTO_PRAZO` | Diferenciar histórico x contrato |
| `docs/cnes/familias_indicadores_cnes.md` | Organização de famílias de indicadores | Alto | Planejamento de paridade analítica | `AVALIAR_CASO_A_CASO` | Semântica deve ser preservada |
| `docs/cnes/roadmap_tecnico_cnes.md` | Planejamento técnico evolutivo | Médio | Orientar execução Etapa 2/3 | `MANTER_NO_CURTO_PRAZO` | Roadmap orienta, mas não substitui contrato |
| `docs/cnes/setup_execucao_local_r.md` | Setup operacional do ambiente R | Médio | Suporte ao legado até paridade | `MANTER_NO_CURTO_PRAZO` | Pode ser reclassificado após consolidação Python |
| `docs/cnes/auditoria_fora_escopo_habilitacoes_cnes.md` | Registro de auditoria metodológica | Médio | Apoio de QA durante migração | `AVALIAR_CASO_A_CASO` | Auxiliar, não contrato principal |
| `docs/cnes/classificacao_habilitacoes_cnes.md` | Regra/explicação de classificação | Alto | Base direta para equivalência Python | `PRESERVAR_COMO_PATRIMONIO_METODOLOGICO` | Alinhado ao CSV de classificação |

## 9. Classificação dos produtos data_interim e data_raw

### 9.1 `data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv`
- **Situação observada na baseline:** produto histórico com cardinalidade registrada; sem `co_unidade` no export observado.
- **Utilidade:** referência histórica de volume/cobertura e comparação preliminar.
- **Limitação:** não representa contrato estrutural vigente por desalinhamento com regra metodológica de chave operacional.
- **Status sugerido:** `MANTER_NO_CURTO_PRAZO` (como referência histórica, não contrato).

### 9.2 `data_interim/cnes/habilitacoes/cnes_habilitacoes_es_202601.csv`
- **Situação observada na baseline:** produto histórico com cardinalidade registrada; ausência/não aferição de `co_unidade` no export observado.
- **Utilidade:** referência histórica de cardinalidade e domínios de classificação.
- **Limitação:** não pode ser usado como contrato estrutural vigente.
- **Status sugerido:** `MANTER_NO_CURTO_PRAZO` (como referência histórica, não contrato).

### 9.3 `data_raw/cnes/202601/tbEstabelecimento202601.csv`
- **Situação observada na baseline:** arquivo está como ponteiro Git LFS na sessão baseline, sem conteúdo tabular real materializado.
- **Utilidade:** insumo bruto essencial para testes de base real.
- **Limitação:** risco operacional de reprodutibilidade enquanto LFS não materializa consistentemente.
- **Status sugerido:** `AVALIAR_CASO_A_CASO` (manter e mitigar via estratégia de extração reprodutível).

Conclusão desta seção:
- os CSVs `data_interim` atuais são **referência histórica de cardinalidade**, não contrato estrutural vigente;
- `tbEstabelecimento202601.csv` em LFS representa **risco operacional de reprodutibilidade**;
- nenhum dado foi apagado, movido ou editado nesta etapa.

## 10. Matriz sintética de decisão

| Categoria | Artefatos principais |
|---|---|
| 1. Preservar como patrimônio metodológico | `src/transform/classificar_habilitacoes_cnes.R`; `docs/cnes/decisoes_metodologicas_cnes.md`; `docs/cnes/base_estabelecimentos_cnes.md`; `docs/cnes/base_habilitacoes_cnes.md`; `docs/cnes/classificacao_habilitacoes_cnes.md`; `metadata/cnes/classificacao_habilitacoes_cnes.csv` |
| 2. Preservar como oráculo temporário | `src/validation/validar_pipeline_cnes.R`; `src/transform/corrigir_falsos_negativos_habilitacoes_cnes.R`; 9 testes R aprovados na Etapa 0 |
| 3. Substituir por Python/PySUS | `src/extract/ler_arquivos_cnes.R`; `src/transform/executar_pipeline_piloto_cnes.R` |
| 4. Portar para Python com paridade | `src/transform/padronizar_cnes_interim.R`; `src/transform/preparar_estabelecimentos_cnes.R`; `src/transform/preparar_habilitacoes_cnes.R`; schemas e dicionários CNES principais |
| 5. Avaliar caso a caso | `src/indicators/calcular_indicadores_cnes_oferta.R`; `src/transform/auditar_fora_escopo_habilitacoes_cnes.R`; matriz/auditorias auxiliares de metadata |
| 6. Deprecar após paridade | scripts transitórios estritamente operacionais de pilotagem R (quando houver equivalência Python validada) |
| 7. Manter no curto prazo | `scripts/instalar_dependencias_r.R`; testes bloqueados por LFS; setup local R e documentação operacional enquanto coexistirem duas camadas |

## 11. Recomendações para a próxima etapa
Próxima etapa recomendada:

**Etapa 2 — Atualização da governança de linguagem e arquitetura híbrida**

Recomendações objetivas:
- atualizar README e documentação de governança para admitir oficialmente Python/PySUS na camada de extração;
- manter R como oráculo e eventual camada analítica;
- definir estrutura de diretórios para Python;
- estabelecer que nenhum script R sensível será removido antes de paridade validada;
- transformar regras metodológicas em contratos independentes de linguagem.

**Não executar a Etapa 2 nesta tarefa.**

## 12. Riscos para a classificação
- risco de descartar regra metodológica junto com código operacional;
- risco de usar CSV histórico sem `co_unidade` como contrato estrutural;
- risco de PySUS não cobrir todas as tabelas CNES necessárias;
- risco de perda de rastreabilidade se scripts R forem movidos cedo demais;
- risco de duplicação de lógica entre R e Python se a migração não tiver contratos;
- risco de Git LFS continuar impedindo reprodução dos testes com dado real.

## 13. Critérios de aceite da Etapa 1
- [x] Documento `01_classificacao_legado_r.md` criado.
- [x] Baseline da Etapa 0 lida e incorporada.
- [x] Scripts R classificados.
- [x] Testes R classificados.
- [x] Metadados CNES classificados.
- [x] Documentação CNES classificada.
- [x] Produtos `data_interim/data_raw` classificados com ressalvas.
- [x] Matriz sintética de decisão criada.
- [x] Recomendações para a próxima etapa registradas.
- [x] Nenhum código alterado.
- [x] Nenhum dado alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum teste alterado.
- [x] Nenhum workflow alterado.

## 14. Conclusão
A Etapa 1 **não autoriza** descarte, remoção ou migração imediata; ela apenas organiza a decisão para etapas posteriores.

Síntese final:
- extração e orquestração piloto são candidatas fortes à substituição por Python/PySUS;
- transformação/classificação com regras de chave, joins e classificação devem ser preservadas como fonte metodológica;
- testes R devem permanecer como oráculos até haver testes Python equivalentes;
- `data_interim` atual é referência histórica, não contrato estrutural vigente;
- a próxima etapa deve formalizar a arquitetura híbrida.
