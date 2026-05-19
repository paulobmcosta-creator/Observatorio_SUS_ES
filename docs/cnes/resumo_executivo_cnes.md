# Resumo executivo CNES (one-pager)

## Objetivo

Oferecer uma visão rápida para onboarding do módulo CNES do Observatório SUS-ES: o que já existe, como validar localmente, quais indicadores iniciais estão disponíveis e quais limites metodológicos devem ser respeitados.

## Fontes e papel analítico

- Fonte principal desta camada: CNES (estrutura de oferta instalada).
- Papel analítico: descrever capacidade cadastrada da rede (estabelecimentos, habilitações, leitos, equipamentos e profissionais), sem confundir oferta registrada com produção assistencial ou desfechos.
- Integrações com SIH/SUS, SIA/SUS, SIM, IBGE e ANS estão planejadas em ciclos futuros.

Referência metodológica detalhada: `docs/cnes/visao_analitica_cnes_observatorio.md`.

## Pipeline atual (piloto técnico em R)

1. **Extração**: `src/extract/ler_arquivos_cnes.R`
2. **Transformação**: `src/transform/padronizar_cnes_interim.R`
3. **Validação**: `src/validation/validar_pipeline_cnes.R`
4. **Orquestração**: `src/transform/executar_pipeline_piloto_cnes.R`

Metadados e rastreabilidade:
- `metadata/cnes/schema_cnes_piloto.yml`
- `metadata/cnes/dicionario_cnes_piloto.csv`
- `docs/cnes/metadados_cnes_piloto.md`

## Indicadores principais já implementados

Camada inicial de **indicadores de oferta CNES**:
- Função: `src/indicators/calcular_indicadores_cnes_oferta.R`
- Documentação: `docs/cnes/indicadores_cnes_oferta.md`
- Dicionário: `metadata/cnes/dicionario_indicadores_cnes_oferta.csv`
- Teste: `tests/test_indicadores_cnes_oferta.R`

## Limites metodológicos (importante)

- O módulo atual é piloto técnico e não representa análise epidemiológica final.
- Não há ainda integração completa com produção (SIH/SUS, SIA/SUS), mortalidade (SIM) e denominadores populacionais (IBGE/ANS).
- Não gera dashboards/mapas como produto final nesta etapa.
- A interpretação deve explicitar diferença entre cadastro de oferta e uso/resultado em saúde.

## Como validar rapidamente

- Setup e sequência oficial de validação local: `docs/cnes/setup_execucao_local_r.md`.
- Testes de metadados e estrutura devem ser executados antes de mudanças de pipeline.

## Para aprofundamento

- Roadmap técnico completo: `docs/cnes/roadmap_tecnico_cnes.md`
- Arquitetura de produtos tabulares: `docs/cnes/produtos_tabulares_cnes.md`
- Famílias de indicadores: `docs/cnes/familias_indicadores_cnes.md`
