# Teste estrutural da classificação temática de habilitações CNES.
# Usa apenas R base para evitar dependências externas.

arquivo_classificacao <- file.path("metadata", "cnes", "classificacao_habilitacoes_cnes.csv")
arquivo_documentacao <- file.path("docs", "cnes", "classificacao_habilitacoes_cnes.md")

if (!file.exists(arquivo_classificacao)) {
  stop("Arquivo de classificação de habilitações CNES não encontrado.")
}

if (!file.exists(arquivo_documentacao)) {
  stop("Documentação da classificação de habilitações CNES não encontrada.")
}

classificacao <- read.csv(
  arquivo_classificacao,
  stringsAsFactors = FALSE,
  na.strings = c("", "NA"),
  check.names = FALSE,
  fileEncoding = "UTF-8"
)

colunas_obrigatorias <- c(
  "codigo_habilitacao",
  "descricao_habilitacao",
  "linha_cuidado",
  "grupo_tematico",
  "subgrupo",
  "tipo_componente",
  "prioridade_observatorio",
  "fonte_referencia",
  "observacao_metodologica"
)

if (!identical(names(classificacao), colunas_obrigatorias)) {
  stop(
    "Colunas da classificação não correspondem exatamente ao contrato esperado.\n",
    "Esperado: ", paste(colunas_obrigatorias, collapse = ", "), "\n",
    "Encontrado: ", paste(names(classificacao), collapse = ", ")
  )
}

linhas_cuidado_minimas <- c(
  "oncologia",
  "cardiologia",
  "rede_urgencia_emergencia",
  "uti_cuidado_critico",
  "diagnostico_apoio_terapeutico",
  "terapia_renal_substitutiva",
  "reabilitacao"
)

linhas_ausentes <- setdiff(linhas_cuidado_minimas, unique(classificacao$linha_cuidado))
if (length(linhas_ausentes) > 0) {
  stop("Linhas de cuidado mínimas ausentes: ", paste(linhas_ausentes, collapse = ", "))
}

if (any(is.na(classificacao$descricao_habilitacao) | trimws(classificacao$descricao_habilitacao) == "")) {
  stop("Existem linhas com descricao_habilitacao vazia.")
}

if (any(is.na(classificacao$linha_cuidado) | trimws(classificacao$linha_cuidado) == "")) {
  stop("Existem linhas com linha_cuidado vazia.")
}

prioridades_validas <- c("alta", "media", "baixa")
prioridades_invalidas <- setdiff(unique(classificacao$prioridade_observatorio), prioridades_validas)
if (length(prioridades_invalidas) > 0) {
  stop("Valores inválidos em prioridade_observatorio: ", paste(prioridades_invalidas, collapse = ", "))
}

if (!any(classificacao$prioridade_observatorio == "alta")) {
  stop("A classificação deve conter pelo menos uma linha com prioridade alta.")
}

if (!any(classificacao$codigo_habilitacao == "codigo_a_confirmar")) {
  stop("A classificação deve conter pelo menos uma linha com codigo_habilitacao igual a codigo_a_confirmar.")
}

documentacao <- paste(readLines(arquivo_documentacao, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
if (!grepl("codigo_a_confirmar", documentacao, fixed = TRUE)) {
  stop("A documentação deve mencionar explicitamente codigo_a_confirmar.")
}

message("Teste da classificação de habilitações CNES executado com sucesso.")
