# Auditoria metodológica das habilitações classificadas como "Fora do escopo inicial" (Ciclo 3).

auditar_fora_escopo_habilitacoes_cnes <- function(
  dir_interim = "data_interim/cnes",
  dir_metadata = "metadata/cnes",
  competencia = "202601"
) {
  caminho_hab <- file.path(dir_interim, "habilitacoes", paste0("cnes_habilitacoes_es_", competencia, ".csv"))
  if (!file.exists(caminho_hab)) stop("Base de habilitações não encontrada: ", caminho_hab)

  hab <- utils::read.csv(caminho_hab, stringsAsFactors = FALSE, colClasses = "character", fileEncoding = "UTF-8")
  fora <- hab[trimws(hab$linha_cuidado) == "Fora do escopo inicial", , drop = FALSE]
  if (nrow(fora) == 0) stop("Não há registros com linha_cuidado == 'Fora do escopo inicial'.")

  chave <- c(
    "codigo_habilitacao", "tipo_habilitacao", "descricao_habilitacao", "origem_habilitacao",
    "linha_cuidado", "sublinha_cuidado", "componente_rede", "usar_observatorio", "prioridade", "status_validacao"
  )
  missing <- setdiff(chave, names(fora))
  if (length(missing) > 0) stop("Campos ausentes na base de habilitações: ", paste(missing, collapse = ", "))

  fora$id_grupo <- do.call(paste, c(fora[chave], sep = "||"))
  grupos <- split(fora, fora$id_grupo)

  classificar_categoria <- function(codigo, tipo, descricao) {
    txt <- toupper(trimws(ifelse(is.na(descricao), "", descricao)))
    ch <- paste0(trimws(codigo), "-", trimws(tipo))

    if (ch %in% c("1901-H", "1902-H")) return("Saúde sexual e reprodutiva / tema futuro")
    if (ch %in% c("0403-H", "0405-H")) return("Saúde bucal especializada / tema futuro")
    if (ch %in% c("8231-I", "8232-I")) return("Reabilitação/deficiência")

    if (grepl("INCENTIVO|INTEGRASUS|PMAE|PROJETO|PROGRAMA|ADESAO|ADESÃO|SEM GERACAO DE CREDITO|CREDITO", txt)) return("Programático/incentivo")
    if (grepl("TRANSPLANT|RETIRADA DE ORGAOS|SNT", txt)) return("Transplantes")
    if (grepl("DEFICIEN|REABILIT|ORTOP", txt)) return("Reabilitação/deficiência")
    if (grepl("AUDITIV|VISUAL|GLAUCOMA|OFTAL", txt)) return("Saúde auditiva/visual")
    if (grepl("HOSPITAL|ENFERMARIA|LEITO|PORTA DE ENTRADA", txt)) return("Componente hospitalar genérico")

    # Falso negativo restrito a linhas já priorizadas no observatório
    if (grepl("UNACON|CACON|RADIOTERAP|CITOPAT|PEHU|AVC|RETAGUARDA|TAVI|DRC|QUEIMAD|UCIN", txt)) return("Falso negativo do escopo atual")

    if (txt == "" || grepl("A DEFINIR|NAO APLICAVEL|NÃO APLICÁVEL", txt)) return("Ambíguo/revisar")
    "Outro tema futuro"
  }

  recomendar <- function(categoria) {
    if (categoria == "Falso negativo do escopo atual") return("Revisar classificação no Ciclo 1")
    if (categoria %in% c("Saúde sexual e reprodutiva / tema futuro", "Saúde bucal especializada / tema futuro", "Outro tema futuro", "Reabilitação/deficiência")) return("Considerar como futura linha temática")
    if (categoria %in% c("Programático/incentivo", "Componente hospitalar genérico", "Transplantes", "Saúde auditiva/visual")) return("Manter fora do escopo atual")
    if (categoria == "Ambíguo/revisar") return("Verificar documentação normativa")
    "Manter como revisar"
  }

  out_list <- lapply(grupos, function(df) {
    desc <- df$descricao_habilitacao[1]
    categoria <- classificar_categoria(df$codigo_habilitacao[1], df$tipo_habilitacao[1], desc)
    recomendacao <- recomendar(categoria)
    data.frame(
      codigo_habilitacao = df$codigo_habilitacao[1],
      tipo_habilitacao = df$tipo_habilitacao[1],
      descricao_habilitacao = desc,
      origem_habilitacao = df$origem_habilitacao[1],
      linha_cuidado = df$linha_cuidado[1],
      sublinha_cuidado = df$sublinha_cuidado[1],
      componente_rede = df$componente_rede[1],
      usar_observatorio = df$usar_observatorio[1],
      prioridade = df$prioridade[1],
      status_validacao = df$status_validacao[1],
      n_registros = nrow(df),
      n_estabelecimentos = length(unique(df$cnes)),
      n_municipios = length(unique(df$cod_municipio)),
      exemplos_cnes = paste(head(unique(df$cnes), 5), collapse = " | "),
      exemplos_municipios = paste(head(unique(df$municipio), 5), collapse = " | "),
      categoria_auditoria_escopo = categoria,
      recomendacao_auditoria = recomendacao,
      stringsAsFactors = FALSE
    )
  })

  auditoria <- do.call(rbind, out_list)
  auditoria <- auditoria[order(-auditoria$n_registros, auditoria$codigo_habilitacao, auditoria$tipo_habilitacao), , drop = FALSE]

  caminho_saida <- file.path(dir_metadata, paste0("auditoria_fora_escopo_habilitacoes_cnes_", competencia, ".csv"))
  utils::write.csv(auditoria, caminho_saida, row.names = FALSE, fileEncoding = "UTF-8")

  attr(auditoria, "total_registros_fora_escopo") <- nrow(fora)
  attr(auditoria, "total_habilitacoes_distintas") <- nrow(auditoria)
  attr(auditoria, "caminho_saida") <- caminho_saida
  auditoria
}
