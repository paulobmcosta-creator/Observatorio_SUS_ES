# Indicadores CNES de Oferta — Piloto Técnico

## 1. Finalidade

Este documento descreve os primeiros indicadores técnicos de oferta derivados da camada interim do pipeline piloto CNES do Observatório SUS-ES.

Os indicadores têm finalidade arquitetural e metodológica inicial: testar uma camada analítica simples, reprodutível, documentada e validada por testes automatizados a partir de dados CNES já padronizados pelo pipeline piloto.

## 2. Escopo

Os indicadores aqui descritos são métricas descritivas básicas sobre registros, estabelecimentos, municípios gestores e competências observadas na saída intermediária do CNES.

Eles não são indicadores epidemiológicos finais, não avaliam suficiência da rede assistencial, não estimam cobertura populacional e não substituem análise sanitária especializada. Qualquer interpretação substantiva deve considerar a qualidade da base de entrada, o recorte temporal, a completude dos identificadores administrativos e validações metodológicas adicionais.

## 3. Fonte de dados

A fonte de dados é a saída intermediária do pipeline piloto CNES, gerada após leitura e padronização técnica dos arquivos de entrada. A função espera um `data.frame` já padronizado contendo, no mínimo, as colunas:

- `competencia_aaaamm`;
- `co_municipio_gestor`;
- `co_cnes`.

## 4. Indicadores implementados

### 4.1 `total_registros`

- **Definição:** quantidade total de linhas no `data.frame` interim recebido pela função.
- **Fórmula ou regra de cálculo:** `nrow(dados_cnes_interim)`.
- **Unidade:** registros.
- **Interpretação:** indica o volume total de registros disponíveis para a camada analítica inicial.
- **Limitações:** não mede estabelecimentos únicos, qualidade dos registros ou completude dos campos.

### 4.2 `total_estabelecimentos_distintos`

- **Definição:** quantidade de códigos CNES distintos observados na coluna `co_cnes`.
- **Fórmula ou regra de cálculo:** contagem de valores únicos de `co_cnes`, desconsiderando `NA`.
- **Unidade:** estabelecimentos.
- **Interpretação:** aproxima o número de estabelecimentos distintos presentes na camada interim.
- **Limitações:** depende da completude e consistência de `co_cnes`; não classifica estabelecimentos por tipo, natureza jurídica ou situação cadastral.

### 4.3 `total_municipios_gestores_distintos`

- **Definição:** quantidade de códigos de municípios gestores distintos observados na coluna `co_municipio_gestor`.
- **Fórmula ou regra de cálculo:** contagem de valores únicos de `co_municipio_gestor`, desconsiderando `NA`.
- **Unidade:** municípios.
- **Interpretação:** indica quantos municípios gestores aparecem na camada interim analisada.
- **Limitações:** não valida se o código municipal é oficial, vigente ou compatível com recortes territoriais externos.

### 4.4 `total_competencias_distintas`

- **Definição:** quantidade de competências distintas observadas na coluna `competencia_aaaamm`.
- **Fórmula ou regra de cálculo:** contagem de valores únicos de `competencia_aaaamm`, desconsiderando `NA`.
- **Unidade:** competências.
- **Interpretação:** indica a amplitude temporal mínima do conjunto processado em número de competências observadas.
- **Limitações:** não avalia continuidade temporal, ausência de meses intermediários ou qualidade da competência original.

### 4.5 `registros_por_competencia`

- **Definição:** quantidade de registros por competência válida.
- **Fórmula ou regra de cálculo:** contagem de linhas agrupadas por `competencia_aaaamm`, ignorando registros com competência `NA`.
- **Unidade:** registros.
- **Interpretação:** permite observar a distribuição inicial do volume de registros entre competências processadas.
- **Limitações:** não diferencia variações reais de oferta de variações de carga, extração, completude ou duplicidade.

### 4.6 `estabelecimentos_distintos_por_municipio_gestor`

- **Definição:** quantidade de estabelecimentos distintos por município gestor válido.
- **Fórmula ou regra de cálculo:** para cada `co_municipio_gestor` não ausente, contagem de valores únicos de `co_cnes`, desconsiderando `NA`.
- **Unidade:** estabelecimentos.
- **Interpretação:** fornece uma primeira visão técnica da distribuição de estabelecimentos distintos por município gestor.
- **Limitações:** não mede cobertura, capacidade instalada, tipos de serviço, leitos, profissionais, especialidades ou suficiência regional.

## 5. Formato de saída

A função `calcular_indicadores_cnes_oferta()` retorna um `data.frame` em formato longo com as seguintes colunas:

- `indicador`: nome técnico do indicador calculado;
- `valor`: valor numérico do indicador;
- `unidade`: unidade de medida do valor;
- `recorte`: nível de agregação ou recorte usado no cálculo;
- `categoria`: categoria específica do recorte ou grupo geral;
- `observacao`: nota técnica curta sobre a regra aplicada.

## 6. Limitações

Esta etapa ainda não implementa:

- cálculo de cobertura populacional;
- comparação regional;
- classificação de estabelecimentos;
- análise de leitos;
- análise de especialidades;
- dashboards.

## 7. Próximos passos

Evoluções recomendadas para ciclos posteriores incluem:

- indicadores por tipo de estabelecimento;
- indicadores por natureza jurídica;
- indicadores de leitos;
- integração com IBGE para taxas por população;
- futura camada `data_processed`.
