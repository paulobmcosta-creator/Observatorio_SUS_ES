# Base de habilitações CNES por estabelecimento (Ciclo 3)

## 1) Objetivo do Ciclo 3
Construir base intermediária tabular de habilitações CNES classificadas por estabelecimento do ES.

## 2) Competência CNES usada
202601.

## 3) Arquivos usados
- `data_raw/cnes/202601/rlEstabSipac202601.csv`
- `data_raw/cnes/202601/tbSubGruposHabilitacao202601.csv`
- `metadata/cnes/classificacao_habilitacoes_cnes.csv`
- `data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv`

## 4) Relação com o Ciclo 1
Reutiliza a classificação analítica de habilitações sem alterar o conteúdo do ciclo 1.

## 5) Relação com o Ciclo 2
Utiliza a base-mãe de estabelecimentos do ES para filtro territorial e enriquecimento cadastral.

## 6) Justificativa da chave composta
A habilitação deve ser relacionada por `codigo_habilitacao + tipo_habilitacao`, evitando ambiguidades de join por código isolado.

## 7) Regra de filtro territorial
Manter apenas registros de habilitação cujo `cnes` exista na base de estabelecimentos do ES.

## 8) Regras de relacionamento
1. `rlEstabSipac` -> padronização de campos operacionais da habilitação.
2. Join com `tbSubGruposHabilitacao` por `codigo_habilitacao + tipo_habilitacao`.
3. Join com `classificacao_habilitacoes_cnes` por `codigo_habilitacao + tipo_habilitacao`.
4. Join com base de estabelecimentos por `cnes`.

## 9) Granularidade
Registro de habilitação por estabelecimento, preservando multiplicidade por competência/início/fim/portaria/leitos quando aplicável.

## 10) Habilitações não classificadas
Não são descartadas. Recebem fallback:
- `linha_cuidado = "Não classificada"`
- `usar_observatorio = "Não"`
- `status_validacao = "revisar"`

Essa regra funciona como mecanismo de segurança para impedir descarte silencioso de registros. Na execução final da competência 202601, após correções do Ciclo 3C, não restaram registros com `linha_cuidado = "Não classificada"`.

## 11) Limitações metodológicas
- Dependência de consistência entre base de estabelecimentos e `rlEstabSipac` para interseção de CNES.
- Campos textuais podem sofrer variação de encoding entre fontes.
- Se o filtro territorial resultar em 0 linhas, o script interrompe com erro e não grava produto vazio.

## 12) Próximos passos
No Ciclo 4, esta base poderá ser utilizada como insumo para construção de indicadores tabulares por município, região, linha de cuidado e estabelecimento. A geração desses indicadores deve preservar a distinção entre base intermediária, classificação metodológica e produto analítico agregado.

## 13) Histórico de bloqueio inicial
Diagnóstico da execução real em 2026-05-21:
- linhas em `rlEstabSipac202601`: **115.103**
- CNES únicos em `rlEstabSipac202601`: **69.446**
- CNES únicos na base ES disponível: **1**
- CNES de `rlEstabSipac` com match na base ES: **0**
- registros após filtro ES: **0**
- chaves únicas (`codigo_habilitacao + tipo_habilitacao`) em `rlEstabSipac`: **371**
- chaves com match no domínio `tbSubGruposHabilitacao`: **371**
- chaves com match na classificação do Ciclo 1: **371**

Interpretação histórica: em execução anterior, o Ciclo 3 ficou bloqueado porque a base de estabelecimentos ES disponível estava em formato de fixture/placeholder (1 CNES) e não representava o produto real do Ciclo 2. Esse bloqueio foi superado após restauração/regeneração da base real do Ciclo 2B.


## 14) Primeira execução real após restauração do Ciclo 2B (2026-05-21)
- Registros na base final de habilitações ES: **1.963**.
- Estabelecimentos com pelo menos uma habilitação: **1.283**.
- Municípios representados: **78**.
- Registros sem classificação analítica: **0**.
- CNES da base de habilitações não encontrados na base de estabelecimentos ES: **0**.
- Duplicidades exatas removidas: **0**.
- Tamanho aproximado do arquivo final: **888.187 bytes** (~0,89 MB).

Distribuição por `linha_cuidado`:
- Fora do escopo inicial: **1.562**
- RUE: **168**
- UTI / cuidado crítico: **54**
- Outras habilitações estratégicas: **49**
- Nefrologia: **41**
- Saúde mental: **41**
- Cardiovascular: **32**
- Oncologia: **16**

Distribuição por `usar_observatorio`:
- Não: **1.562**
- Sim: **401**

Confirmação histórica: estes resultados representam a primeira execução real após a restauração do Ciclo 2B e foram posteriormente superados por correções metodológicas do Ciclo 3C.

## 15) Resultado final validado após Ciclo 3C e reclassificação 1708-H
- Registros na base final de habilitações ES: **1.963**.
- Estabelecimentos com pelo menos uma habilitação: **1.283**.
- Municípios representados: **78**.
- Registros sem classificação analítica: **0**.
- CNES da base de habilitações não encontrados na base de estabelecimentos ES: **0**.
- Duplicidades exatas removidas: **0**.
- Tamanho aproximado do arquivo final: **899.389 bytes** (~0,90 MB).

Distribuição final por `linha_cuidado`:
- Fora do escopo inicial: **1.462**
- RUE: **220**
- UTI / cuidado crítico: **68**
- Nefrologia: **49**
- Outras habilitações estratégicas: **49**
- Saúde mental: **41**
- Oncologia: **41**
- Cardiovascular: **33**

Distribuição final por `usar_observatorio`:
- Sim: **501**
- Não: **1.462**

Auditoria fora do escopo conciliada com a base final:
- auditoria fora do escopo: soma `n_registros = 1.462`.

Confirmação metodológica: o produto permanece uma **base intermediária tabular** de habilitações por estabelecimento, sem agregações analíticas finais e sem criação de indicadores.

## Critérios de validação
- base final com mais de zero registros;
- apenas CNES pertencentes à base de estabelecimentos ES;
- ausência de `cnes` vazio;
- ausência de `codigo_habilitacao` vazio;
- ausência de `tipo_habilitacao` vazio;
- ausência de registros “Não classificada” na execução final;
- chave composta `codigo_habilitacao + tipo_habilitacao` preservada como texto;
- uso de join por chave composta, nunca apenas por código;
- auditoria fora do escopo conciliada com a base final;
- testes automatizados executados e aprovados.

## Execução do pipeline
```r
source("src/transform/preparar_habilitacoes_cnes.R")

preparar_habilitacoes_cnes(
  dir_raw = "data_raw/cnes",
  dir_interim = "data_interim/cnes",
  dir_metadata = "metadata/cnes",
  competencia = "202601"
)
```

```bash
Rscript tests/test_base_habilitacoes_cnes.R
```
