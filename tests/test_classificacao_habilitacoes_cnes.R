# Teste estrutural da classificação refinada de habilitações e referências CNES.
# Usa apenas R base para evitar dependências externas.

arquivo_classificacao <- file.path("metadata", "cnes", "classificacao_habilitacoes_cnes.csv")
arquivo_documentacao <- file.path("docs", "cnes", "classificacao_habilitacoes_cnes.md")

if (!file.exists(arquivo_classificacao)) {
  stop("Arquivo de classificação de habilitações e referências CNES não encontrado.")
}

if (!file.exists(arquivo_documentacao)) {
  stop("Documentação da classificação de habilitações e referências CNES não encontrada.")
}

classificacao <- read.csv(
  arquivo_classificacao,
  stringsAsFactors = FALSE,
  na.strings = c("", "NA"),
  check.names = FALSE,
  fileEncoding = "UTF-8"
)

colunas_obrigatorias <- c(
  "id_classificacao",
  "tipo_referencia_cnes",
  "codigo_referencia",
  "status_codigo",
  "descricao_referencia",
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
    "Colunas da classificação refinada não correspondem exatamente ao contrato esperado.\n",
    "Esperado: ", paste(colunas_obrigatorias, collapse = ", "), "\n",
    "Encontrado: ", paste(names(classificacao), collapse = ", ")
  )
}

if (any(is.na(classificacao$id_classificacao) | trimws(classificacao$id_classificacao) == "")) {
  stop("Existem linhas com id_classificacao vazio.")
}

ids_duplicados <- classificacao$id_classificacao[duplicated(classificacao$id_classificacao)]
if (length(ids_duplicados) > 0) {
  stop("Existem id_classificacao duplicados: ", paste(unique(ids_duplicados), collapse = ", "))
}

if (any(is.na(classificacao$descricao_referencia) | trimws(classificacao$descricao_referencia) == "")) {
  stop("Existem linhas com descricao_referencia vazia.")
}

if (any(is.na(classificacao$linha_cuidado) | trimws(classificacao$linha_cuidado) == "")) {
  stop("Existem linhas com linha_cuidado vazia.")
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

tipos_validos <- c(
  "habilitacao",
  "servico_especializado",
  "equipamento",
  "leito",
  "tipo_estabelecimento",
  "componente_rede",
  "procedimento_sigtap",
  "ocupacao_cbo",
  "conceito_metodologico",
  "outro_a_confirmar"
)

tipos_invalidos <- setdiff(unique(classificacao$tipo_referencia_cnes), tipos_validos)
if (length(tipos_invalidos) > 0) {
  stop("Valores inválidos em tipo_referencia_cnes: ", paste(tipos_invalidos, collapse = ", "))
}

status_validos <- c("confirmado", "a_confirmar", "nao_aplicavel", "conceitual")
status_invalidos <- setdiff(unique(classificacao$status_codigo), status_validos)
if (length(status_invalidos) > 0) {
  stop("Valores inválidos em status_codigo: ", paste(status_invalidos, collapse = ", "))
}

prioridades_validas <- c("alta", "media", "baixa")
prioridades_invalidas <- setdiff(unique(classificacao$prioridade_observatorio), prioridades_validas)
if (length(prioridades_invalidas) > 0) {
  stop("Valores inválidos em prioridade_observatorio: ", paste(prioridades_invalidas, collapse = ", "))
}

if (!any(classificacao$codigo_referencia == "codigo_a_confirmar")) {
  stop("A classificação deve conter pelo menos uma linha com codigo_referencia igual a codigo_a_confirmar.")
}

for (tipo_obrigatorio in c("habilitacao", "equipamento", "leito", "componente_rede")) {
  if (!any(classificacao$tipo_referencia_cnes == tipo_obrigatorio)) {
    stop("A classificação deve conter pelo menos uma linha com tipo_referencia_cnes = ", tipo_obrigatorio, ".")
  }
}

documentacao <- paste(readLines(arquivo_documentacao, warn = FALSE, encoding = "UTF-8"), collapse = "\n")
termos_documentacao <- c("codigo_a_confirmar", "tipo_referencia_cnes", "status_codigo")
termos_ausentes <- termos_documentacao[!vapply(termos_documentacao, grepl, logical(1), x = documentacao, fixed = TRUE)]
if (length(termos_ausentes) > 0) {
  stop("A documentação não menciona explicitamente: ", paste(termos_ausentes, collapse = ", "))
}

message("Teste da classificação refinada de habilitações e referências CNES executado com sucesso.")
