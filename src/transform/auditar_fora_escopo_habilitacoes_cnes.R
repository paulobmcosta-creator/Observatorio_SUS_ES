# Auditoria metodológica das habilitações classificadas como "Fora do escopo inicial" (Ciclo 3).

auditar_fora_escopo_habilitacoes_cnes <- function(
  dir_interim = "data_interim/cnes",
  dir_metadata = "metadata/cnes",
  dir_docs = "docs/cnes",
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

  classificar_categoria <- function(descricao) {
    txt <- toupper(trimws(ifelse(is.na(descricao), "", descricao)))
    if (grepl("TRANSPLANT|RETIRADA DE ORGAOS|SNT", txt)) return("Transplantes")
    if (grepl("INCENTIVO|INTEGRASUS|PMAE|PROJETO|PROGRAMA|ADESAO|ADESÃO|SEM GERACAO DE CREDITO|CREDITO", txt)) return("Programático/incentivo")
    if (grepl("ATENCAO BASICA|ATENÇÃO BASICA|APS|EMULTI|MAIS MEDICOS|MAIS MÉDICOS", txt)) return("Atenção básica/APS")
    if (grepl("DEFICIEN|REABILIT|ORTOP", txt)) return("Reabilitação/deficiência")
    if (grepl("AUDITIV|VISUAL|GLAUCOMA|OFTAL", txt)) return("Saúde auditiva/visual")
    if (grepl("HOSPITAL|ENFERMARIA|LEITO|PORTA DE ENTRADA", txt)) return("Componente hospitalar genérico")
    if (grepl("CEO|ODONTO|VASECTOMIA|LAQUEADURA|CITOPATOLOG", txt)) return("Potencial falso negativo")
    if (txt == "" || grepl("A DEFINIR|NAO APLICAVEL|NÃO APLICÁVEL", txt)) return("Ambíguo/revisar")
    "Outro tema futuro"
  }

  recomendar <- function(categoria) {
    if (categoria %in% c("Fora do escopo confirmado", "Programático/incentivo", "Componente hospitalar genérico")) return("Manter fora do escopo")
    if (categoria %in% c("Potencial falso negativo", "Transplantes", "Saúde auditiva/visual")) return("Revisar classificação no Ciclo 1")
    if (categoria %in% c("Atenção básica/APS", "Reabilitação/deficiência", "Outro tema futuro")) return("Considerar como futura linha temática")
    if (categoria == "Ambíguo/revisar") return("Verificar documentação normativa")
    "Manter como revisar"
  }

  out_list <- lapply(grupos, function(df) {
    desc <- df$descricao_habilitacao[1]
    categoria <- classificar_categoria(desc)
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

  dir_saida <- file.path(dir_metadata)
  if (!dir.exists(dir_saida)) dir.create(dir_saida, recursive = TRUE)
  caminho_saida <- file.path(dir_saida, paste0("auditoria_fora_escopo_habilitacoes_cnes_", competencia, ".csv"))
  utils::write.csv(auditoria, caminho_saida, row.names = FALSE, fileEncoding = "UTF-8")

  attr(auditoria, "total_registros_fora_escopo") <- nrow(fora)
  attr(auditoria, "total_habilitacoes_distintas") <- nrow(auditoria)
  attr(auditoria, "caminho_saida") <- caminho_saida
  auditoria
}
