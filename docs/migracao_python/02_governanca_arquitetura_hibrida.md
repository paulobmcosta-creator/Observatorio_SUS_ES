# Governança da arquitetura híbrida R–Python/PySUS

## 1. Objetivo da Etapa 2
Esta etapa formaliza a mudança de diretriz do projeto: de uma base operacional prioritariamente em R para uma arquitetura híbrida R–Python/PySUS, em que Python/PySUS passa a ser a camada preferencial futura para extração e engenharia de dados, enquanto R permanece preservado como oráculo metodológico, validação comparativa, análise e indicadores.

Esta etapa:
- não cria código Python;
- não instala PySUS;
- não remove scripts R;
- não altera pipeline;
- não substitui testes;
- apenas atualiza a governança documental.

## 2. Insumos considerados
Foram considerados os seguintes insumos:
- `docs/migracao_python/00_baseline_r_pre_migracao.md`
- `docs/migracao_python/01_classificacao_legado_r.md`
- `README.md`
- `docs/convensoes_metodologicas.md`
- `docs/governanca_codigo.md`
- `docs/cnes/`
- `metadata/cnes/`
- `src/`
- `tests/`

Snapshot de versionamento e contexto da execução desta etapa:
- branch atual: `work`;
- commit HEAD: `becba1292521f5f40a873a7e93385c7f066be5f0`;
- último commit: `becba12 Merge pull request #45 from paulobmcosta-creator/codex/execute-etapa-1-de-migracao-r-python`;
- status inicial do repositório: sem alterações rastreadas em `git status --short`.

## 3. Diretriz geral da arquitetura híbrida
Diretriz formal da arquitetura híbrida:

### Python/PySUS
- extração;
- obtenção de dados SUS;
- cache;
- conversão para Parquet;
- organização longitudinal por competência;
- manifestos;
- logs;
- automação operacional;
- preparação de bases regeneráveis.

### R
- oráculo metodológico temporário;
- validação comparativa;
- análise estatística;
- indicadores;
- exploração analítica;
- produtos acadêmicos;
- apoio à geração de tabelas e relatórios;
- manutenção de scripts sensíveis até paridade Python validada.

### Metadados e documentação
- contratos de dados;
- schemas;
- dicionários;
- classificação de habilitações;
- decisões metodológicas;
- regras de chave e join;
- limitações e critérios de validação.

### Testes
- ponte de paridade R versus Python;
- proteção contra regressão metodológica;
- base para substituição controlada;
- não devem ser descartados até existirem equivalentes Python.

## 4. Divisão de responsabilidades por camada
| Camada | Responsável preferencial | Responsável secundário | Papel | Observação de transição |
|---|---|---|---|---|
| Extração de dados SUS | Python/PySUS | R (referência legada) | Ingestão de dados de fontes SUS | Priorizar substituição operacional por Python/PySUS |
| Cache e armazenamento bruto | Python/PySUS | R (suporte temporário) | Estratégia de cache e persistência regenerável | Reduzir acoplamento a insumos locais não regeneráveis |
| Conversão para Parquet | Python/PySUS | R (comparação de saída) | Conversão e padronização técnica de formatos | CSV permanece auxiliar durante transição |
| Padronização inicial | Python (com contrato formal) | R (oráculo) | Normalização de colunas, tipos e competência | Exigir equivalência de contrato antes de substituição |
| Transformações sensíveis CNES | R (oráculo metodológico) | Python (paridade progressiva) | Regras de negócio críticas, chaves e joins | Dupla cautela até validação de paridade |
| Classificação de habilitações | R + metadados (patrimônio metodológico) | Python (consumo do mesmo contrato) | Aplicação da taxonomia classificatória | Independente de linguagem, sem descarte de regra |
| Indicadores | R (curto prazo) | Python (médio prazo) | Cálculo analítico e séries de indicadores | Pode permanecer híbrido conforme maturidade |
| Validação metodológica | R (curto prazo) | Python (expansão gradual) | Validação comparativa e consistência metodológica | Mantida como ponte de paridade |
| Testes de regressão | R (oráculo existente) | Python (equivalentes progressivos) | Proteção contra regressão metodológica | Testes R permanecem até equivalência Python |
| Documentação e contratos | Independente de linguagem | R + Python | Regras, schemas, dicionários e decisões | Fonte normativa transversal |
| Produtos para painéis/dashboards futuros | Híbrido (dados em Python; análise em R quando necessário) | R/Python | Entrega de datasets e produtos analíticos | Evolução por componente, sem reescrita total |

## 5. Princípios de transição
1. Nenhum script R será removido apenas por existir alternativa Python.
2. Nenhum script R sensível será deprecado sem paridade funcional validada.
3. Python/PySUS deve substituir primeiro a extração e a engenharia de dados, não as regras metodológicas.
4. `co_unidade` continua sendo a chave operacional do CNES.
5. `cnes` continua sendo o código público.
6. CSVs `data_interim` históricos sem `co_unidade` não são contrato estrutural vigente.
7. `metadata/cnes/classificacao_habilitacoes_cnes.csv` é patrimônio metodológico.
8. Git LFS é risco operacional a ser reduzido por extração reprodutível, cache e manifestos.
9. A migração deve ser feita por função, não por linguagem.
10. Todo componente Python que substituir R deve ter teste de paridade.

## 6. Critérios para substituição de um componente R por Python/PySUS
Um componente R só poderá ser substituído quando:
- houver implementação Python equivalente;
- houver contrato de entrada/saída definido;
- houver teste Python equivalente ou superior;
- houver comparação R versus Python documentada;
- houver preservação das regras metodológicas;
- houver aprovação explícita em documento de migração;
- não houver perda de cardinalidade, chave, domínio ou integridade referencial sem justificativa documentada.

## 7. Critérios para manter componente em R
Um componente deve permanecer em R quando:
- contém regra metodológica ainda não portada;
- contém classificação sanitária sensível;
- é usado como oráculo temporário;
- não há paridade Python validada;
- a implementação R é mais adequada para análise, indicadores ou produto acadêmico;
- a migração geraria risco maior que benefício imediato.

## 8. Critérios para uso de PySUS
PySUS deve ser avaliado como base preferencial, mas não assumido sem validação.

Perguntas obrigatórias para futuras etapas:
- PySUS fornece `CO_UNIDADE`?
- PySUS fornece `CO_CNES`?
- PySUS permite acessar ou reconstruir as tabelas relacionais CNES necessárias?
- PySUS permite recuperar competências mensais?
- PySUS permite recorte por UF?
- PySUS preserva códigos como texto?
- PySUS permite saída compatível com Parquet/pandas?
- PySUS elimina ou reduz dependência de Git LFS?
- PySUS cobre SIH, SIM, SIA e demais bases previstas no Observatório?
- PySUS é estável o suficiente para ser usado como camada principal de extração?

## 9. Implicações para versionamento de dados
Diretrizes preliminares:
- `data_raw` deve ser regenerável sempre que possível;
- `data_interim` deve ser produto gerável, não fonte primária de verdade;
- CSV pode existir como formato auxiliar, mas Parquet deve ser avaliado como formato preferencial para bases intermediárias;
- manifestos devem registrar competência, origem, versão da biblioteca, data de extração e parâmetros;
- Git LFS não deve ser a única forma de reprodutibilidade da base bruta;
- metadados, schemas, dicionários e contratos devem ser sempre versionados.

Nesta etapa não foram alterados `.gitignore` nem `.gitattributes`.

## 10. Implicações para a documentação existente
A documentação de governança deve refletir a arquitetura híbrida em `README.md`, `docs/convensoes_metodologicas.md` e `docs/governanca_codigo.md`.

Arquivos editados e mudanças:
- `README.md` — seção “Linguagem principal e ecossistema”: atualização de diretriz, de R exclusivo para arquitetura híbrida com Python/PySUS preferencial em extração/engenharia e R como oráculo/metodologia.
- `docs/convensoes_metodologicas.md` — nova subseção “Arquitetura híbrida R–Python/PySUS”: inclusão de separação de camadas, regras de chave (`co_unidade`, `cnes`), caráter gerável de `data_interim`, contratos transversais e requisito de paridade.
- `docs/governanca_codigo.md` — nova seção “Governança de código na arquitetura híbrida R–Python/PySUS”: critérios para PRs de migração, preservação de oráculos R e exigência de testes/documentação em Python.

## 11. Atualizações realizadas nesta etapa
- Novo documento criado:
  - `docs/migracao_python/02_governanca_arquitetura_hibrida.md`

- Arquivos editados:
  - `README.md` — revisão da diretriz de linguagem para modelo híbrido com responsabilidades por camada.
  - `docs/convensoes_metodologicas.md` — adição de seção específica de arquitetura híbrida e contratos independentes de linguagem.
  - `docs/governanca_codigo.md` — adição de diretrizes formais para mudanças em R e Python durante migração por componente/paridade.

## 12. Recomendações para a próxima etapa
Próxima etapa recomendada:

**Etapa 3 — Preparação da estrutura Python mínima e prova de conceito controlada com PySUS para CNES.**

A próxima etapa deverá:
- criar ambiente Python mínimo;
- definir dependências;
- testar importação/uso de PySUS;
- verificar cobertura PySUS para CNES;
- não substituir ainda transformações sensíveis;
- produzir relatório de viabilidade PySUS/CNES;
- preservar R como oráculo.

## 13. Riscos remanescentes
- PySUS não cobrir todas as tabelas CNES necessárias;
- divergência entre PySUS e arquivos brutos CNES utilizados anteriormente;
- perda de `co_unidade` ou conversão indevida de códigos;
- duplicação de lógica entre R e Python;
- manutenção simultânea de dois pipelines sem contratos;
- Git LFS continuar como dependência residual;
- documentação ficar à frente do código se a governança híbrida não for implementada gradualmente.

## 14. Critérios de aceite da Etapa 2
- [x] Documento `02_governanca_arquitetura_hibrida.md` criado.
- [x] Etapas 0 e 1 consideradas.
- [x] Arquitetura híbrida formalizada.
- [x] Papel de Python/PySUS definido.
- [x] Papel de R definido.
- [x] Papel de metadados e contratos definido.
- [x] Critérios para substituição de R por Python definidos.
- [x] Critérios para manter R definidos.
- [x] Critérios preliminares de uso de PySUS definidos.
- [x] README e/ou documentos de governança revisados quando aplicável.
- [x] Nenhum código alterado.
- [x] Nenhum dado alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum teste alterado.
- [x] Nenhum workflow alterado.
- [x] Nenhuma migração executada.

## 15. Conclusão
A Etapa 2 formaliza a arquitetura híbrida, mas não inicia implementação Python.

Com isso:
- Python/PySUS passa a ser direção preferencial para extração e engenharia de dados;
- R permanece como oráculo, análise e camada metodológica enquanto necessário;
- metadados e contratos passam a ter papel central;
- a próxima etapa será uma prova de conceito controlada, não uma migração plena.
