# Convenções Metodológicas e Nomenclatura

Este documento estabelece padrões para nomenclatura de arquivos, funções e variáveis, bem como convenções metodológicas que assegurem consistência e reprodutibilidade das análises em saúde coletiva.

## Estrutura de Diretórios

* **`data_raw/`**: contém dados brutos exatamente como obtidos de fontes externas. Não modificar manualmente os arquivos neste diretório; qualquer transformação deve ocorrer em `data_interim/` ou `data_processed/`.
* **`data_interim/`**: dados parcialmente tratados; podem incluir correções preliminares de formatos ou integrações múltiplas.
* **`data_processed/`**: dados finais prontos para análise e visualização.
* **`src/`**: código-fonte organizado em subpastas (`extract`, `transform`, `indicators`, `validation`).
* **`dashboards/`** e **`maps/`**: objetos de visualização interativa.

## Nomenclatura de Arquivos

* Use nomes descritivos e minúsculos separados por underlines (`_`), ex.: `mortalidade_infantil_2023.csv`.
* Scripts devem ter extensão de acordo com a linguagem (`.py` para Python, `.R` para R) e iniciar com verbo no infinitivo indicando ação: `extrair_dados_sinan.py`.
* Arquivos de relatórios em Markdown ou HTML devem incluir a data de geração: `relatorio_incidentes_2024-03-15.md`.

## Convenções de Funções e Variáveis

* Nome de funções em Python: `extrair_casos_notificados()`; em R, use `extrair_casos_notificados <- function(...)`.
* Variáveis devem ser explícitas: `numero_obitos`, `taxa_cobertura_vacinal`.
* Evite siglas não padronizadas; quando necessário, defina a sigla no início do script ou documento.

## Docstrings e Comentários

* Toda função deve incluir docstring com:
  * **Descrição breve** do objetivo.
  * **Parâmetros** com tipos esperados.
  * **Retorno** e estrutura de dados gerada.
  * **Referências metodológicas** (ex.: artigos, portarias do Ministério da Saúde).
* Utilize comentários (`#`) para explicar trechos complexos ou decisões não triviais.

Exemplo em Python:

```python
def calcular_incidence_rate(casos: int, populacao: int) -> float:
    """
    Calcula a taxa de incidência por 100.000 habitantes.

    Parâmetros:
        casos (int): número de casos observados no período.
        populacao (int): população em risco no mesmo período.

    Retorno:
        float: taxa de incidência por 100.000 habitantes.

    Referência:
        Ministério da Saúde. Guia de Vigilância Epidemiológica.
    """
    return (casos / populacao) * 100000
```

## Tratamento de Dados e Metodologia

* **Anonimização**: removam ou codifiquem dados pessoais sensíveis antes de qualquer compartilhamento público.
* **Validação Cruzada**: sempre que possível, compare dados provenientes de diferentes fontes (ex.: bases do SUS vs. IBGE) para verificar consistência.
* **Análises Estatísticas**: documente premissas (ex.: normalidade, independência), métodos utilizados (ex.: regressão Poisson, séries temporais) e critérios de qualidade.
* **Reprodutibilidade**: use scripts para todas as etapas; evite manipulação manual de planilhas. Informe a versão de bibliotecas e sistemas operacionais quando relevante.

## Idioma

Adote o português para nomes, comentários e documentação. Termos técnicos em inglês podem ser utilizados quando não houver tradução consagrada ou quando se referirem a nomenclatura de funções de bibliotecas.
