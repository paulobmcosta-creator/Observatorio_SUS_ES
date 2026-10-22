# Revisão geral do repositório Observatório SUS-ES (pré-novos ciclos)

> Referência técnica histórica: o estado e a ordem de ciclos abaixo não representam o planejamento vigente de 2026–2027. Consultar o [plano integral](../ciclo_2026_2027/plano_operacional.md) e o [inventário atualizado](../ciclo_2026_2027/inventario_transicao.csv). Afirmações de disponibilidade e validação devem ser lidas no escopo do registro original.


## 1. Objetivo da revisão
Realizar revisão transversal técnica, metodológica, documental, operacional e linguística do repositório antes de novos ciclos CNES.

## 2. Escopo da revisão
Foram revisados: `README.md`, `docs/`, `src/`, `tests/`, `metadata/`, `data_interim/`, `data_raw/` (presença/estrutura), `tests/fixtures/`, `.gitignore`, `.gitattributes`, `config/` e `scripts/`.

## 3. Estado atual do repositório
- Estrutura geral coerente com separação por camadas (`extract`, `transform`, `validation`, `tests`, `metadata`, `docs`).
- Existem artefatos CNES dos ciclos 1, 2, 3 e 3C documentados e versionados.
- Ambiente R habilitado nesta complementação (`R`/`Rscript` versão 4.3.3) e testes obrigatórios executados com sucesso.

## 4. Síntese dos Ciclos 1, 2, 3 e 3C
- Ciclo 1: construção e refinamento da classificação analítica das habilitações CNES por linha de cuidado.
- Ciclo 2: consolidação da base de estabelecimentos CNES do Espírito Santo.
- Ciclo 3: construção da base intermediária de habilitações por estabelecimento, com vínculo à base de estabelecimentos e à classificação analítica.
- Ciclo 3C: revisão de falsos negativos, reclassificações pontuais e auditoria das habilitações fora do escopo inicial.

## 5. Principais produtos gerados
- Base intermediária de estabelecimentos (`12.548` linhas; `78` municípios; UF `ES`).
- Base intermediária de habilitações (`1.963` linhas; `1.283` CNES únicos).
- Auditoria de fora do escopo (`81` linhas; soma `n_registros = 1.462`).
- Schemas e dicionários de estabelecimentos e habilitações.

## 6. Produtos de uso imediato
- `data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv`
- `data_interim/cnes/habilitacoes/cnes_habilitacoes_es_202601.csv`
- `metadata/cnes/classificacao_habilitacoes_cnes.csv`
- `metadata/cnes/schema_*` e `metadata/cnes/dicionario_*`
- Scripts de transformação e testes CNES.

## 7. Produtos de uso futuro
- Auditorias metodológicas, documentação de famílias de indicadores e roadmap.
- Fixtures e testes de integração para regressão.

## 8. Subprodutos metodológicos relevantes
- Auditoria de fora do escopo (recorte metodológico explícito).
- Documentos de contrato de dados, metadados e visão analítica.

## 9. Produtos OK para uso analítico
- Base de estabelecimentos (coerente com cardinalidades esperadas).
- Base de habilitações sem registros “Não classificada”.
- Integridade referencial habilitações→estabelecimentos sem faltantes.

## 10. Produtos OK apenas com ressalva
- Auditoria linguística: gerada por triagem automática e requer validação humana final.
- Validação automatizada em R: executada com sucesso nesta revisão, mas recomenda-se repetição em CI.

## 11. Produtos que exigem revisão automática
- Verificação contínua de duplicidade, domínios, vazios e cobertura schema/dicionário.
- Verificação de LFS e política de versionamento de `data_raw`.

## 12. Produtos que exigem revisão por IA
- Documentos longos com possíveis trechos em inglês e padronização narrativa.

## 13. Produtos que exigem revisão humana
- Casos limítrofes de classificação metodológica de habilitações.

## 14. Produtos que exigem revisão técnica
- `.gitattributes`: apenas um arquivo grande está em LFS (risco para novos arquivos grandes).
- Garantia de execução reprodutível em ambientes sem R pré-instalado.

## 15. Produtos que não devem ser usados para análise
- Fixtures de `tests/fixtures/` (apenas para teste/validação).
- Arquivos brutos (`data_raw/`) devem ser preservados sem uso analítico direto.

## 16. Riscos técnicos identificados
- Dependência de ambiente R/Rscript para reprodutibilidade dos testes; recomenda-se documentar instalação mínima de R ou incorporar validação em CI.
- Cobertura de LFS possivelmente insuficiente para outros arquivos grandes futuros.

## 17. Riscos metodológicos identificados
- Interpretação de “Fora do escopo inicial” pode ser confundida com irrelevância sanitária se não houver ressalva explícita.

## 18. Riscos documentais identificados
- Alguns textos possuem termos/trechos em inglês fora do núcleo estritamente técnico e demandam padronização.

## 19. Auditoria linguística: textos em inglês e padronização
- Ocorrências identificadas na triagem: `186`.
- Arquivos com mais ocorrências: `docs/cnes/README.md`, `docs/convensoes_metodologicas.md`, `docs/fluxo_trabalho.md`.
- Tipos encontrados: texto de documentação e termos técnicos.
- Recomendação: fluxo em duas etapas (triagem IA + validação humana por mantenedor metodológico).

## 20. Pendências antes do Ciclo 4
1. Pendência técnica recomendada antes do Ciclo 4: confirmar em CI a repetibilidade dos 3 testes obrigatórios já aprovados localmente.
2. Pendência documental/linguística não bloqueante para desenvolvimento técnico do Ciclo 4: validar manualmente ocorrências de inglês marcadas como “Avaliar”, priorizando documentos críticos.

## 21. Pendências antes de ciclos futuros
- Fortalecer política de LFS para novos brutos/intermediários volumosos.
- Expandir testes para bloqueios metodológicos adicionais e regressão documental.

## 22. Recomendações de ordem de revisão
1. Revisões automáticas de consistência de dados.
2. Revisão técnica de versionamento/LFS/CI.
3. Revisão metodológica de classificações sensíveis.
4. Revisão linguística final humana.

## 23. Checklist final antes de iniciar o Ciclo 4
- [x] Testes R executados e aprovados nesta complementação.
- [x] Integridade referencial confirmada.
- [x] Sem “Não classificada”.
- [x] Auditoria fora do escopo conciliada com total real.
- [ ] Revisão linguística mínima concluída em docs críticos.

## 24. Checklist geral antes de uso público
- [ ] Metadados completos e consistentes com bases.
- [ ] Documentação metodológica sem contradições com código.
- [ ] Trilhas de auditoria e rastreabilidade atualizadas.
- [ ] Avisos de escopo e limitações explícitos.

## Resumo das validações executadas nesta revisão
- Base estabelecimentos: 12.548 linhas, 78 municípios, UF somente ES.
- Base habilitações: 1.963 linhas; 1.283 CNES únicos; 0 duplicidades de chave (`cnes`,`codigo_habilitacao`).
- Integridade referencial habilitações→estabelecimentos: 0 faltantes.
- `usar_observatorio`: Sim=501; Não=1.462.
- `linha_cuidado`: “Fora do escopo inicial”=1.462; sem “Não classificada”.
- Auditoria fora do escopo: soma `n_registros` = 1.462 (conciliada).
- Cobertura schema/dicionário: sem lacunas para estabelecimentos e habilitações.

- Hashes e tamanhos pré/pós-testes permaneceram idênticos para bases e metadados centrais, sem indício de sobrescrita por fixtures.
