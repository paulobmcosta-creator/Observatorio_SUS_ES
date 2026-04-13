# Convenções Metodológicas e Nomenclatura

Este documento estabelece padrões para nomenclatura de arquivos, funções e variáveis, bem como convenções metodológicas que assegurem consistência e reprodutibilidade das análises em saúde coletiva.

## Estrutura de Diretórios

* **`data_raw/`**: contém dados brutos exatamente como obtidos de fontes externas. Não modificar manualmente os arquivos neste diretório; qualquer transformação deve ocorrer em `data_interim/` ou `data_processed/`.
* **`data_interim/`**: dados parcialmente tratados; podem incluir correções preliminares de formatos ou integrações múltiplas.
* **`data_processed/`**: dados finais prontos para análise e visualização.
* **`src/`**: código-fonte organizado em subpastas (`extract`, `transform`, `indicators`, `validation`), concebidas para scripts de coleta, transformação, cálculo de indicadores e validação.
* **`dashboards/`** e **`maps/`**: objetos de visualização interativa.

## Nomenclatura de Arquivos

* Use nomes descritivos e minúsculos separados por underlines (`_`), ex.: `mortalidade_infantil_2023.csv`.
* **Scripts de pipeline reprodutível** devem, sempre que possível, ser escritos em **R** (extensão `.R`) e iniciar com verbo no infinitivo indicando a ação, por exemplo: `extrair_dados_sinan.R`. O uso de scripts em Python (`.py`) só é admitido quando houver **justificativa técnica específica**.
* Arquivos de relatórios em Markdown ou HTML devem incluir a data de geração: `relatorio_incidentes_2026-04-13.md`.

## Convenções de Funções e Variáveis

* **Nome de funções em R**: `extrair_casos_notificados <- function(...)`; em **Python** (quando estritamente necessário), use `extrair_casos_notificados()`.
* Variáveis devem ser explícitas e autoexplicativas: `numero_obitos`, `taxa_cobertura_vacinal`.
* Evite siglas não padronizadas; quando necessário, defina a sigla no início do script ou documento.

## Docstrings e Comentários

* Toda função deve incluir documentação que aborde:
  * Descrição breve do objetivo.
  * Parâmetros com tipos esperados.
  * Retorno e estrutura de dados gerada.
  * Referências metodológicas (ex.: artigos, portarias do Ministério da Saúde).
* Utilize comentários (`#`) para explicar trechos complexos ou decisões não triviais.

Exemplo em R:

```R
#' Calcula a taxa de incidência por 100.000 habitantes.
#'
#' @param casos Número de casos observados no período.
#' @param populacao População em risco no mesmo período.
#' @return Taxa de incidência por 100.000 habitantes.
#' @examples
#' calcular_taxa_incidencia(50, 1000000)
calcular_taxa_incidencia <- function(casos, populacao) {
    (casos / populacao) * 100000
}
## Tratamento de Dados e Metodologia

* **Anonimização**: removam ou codifiquem dados pessoais sensíveis antes de qualquer compartilhamento público.
* **Validação Cruzada**: sempre que possível, compare dados provenientes de diferentes fontes (ex.: bases do SUS vs. IBGE) para verificar consistência.
* **Análises Estatísticas**: documente premissas (ex.: normalidade, independência), métodos utilizados (ex.: regressão de Poisson, séries temporais) e critérios de qualidade.
* **Reprodutibilidade**: use scripts para todas as etapas; evite manipulação manual de planilhas. Informe a versão de bibliotecas e sistemas operacionais quando relevante.

## Idioma

Adote o português para nomes, comentários e documentação. Termos técnicos em inglês podem ser utilizados quando não houver tradução consagrada ou quando se referirem à nomenclatura de funções de bibliotecas.
