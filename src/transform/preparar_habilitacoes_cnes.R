# Prepara base intermediária de habilitações CNES classificadas por estabelecimento (Ciclo 3).

normalizar_nome_coluna <- function(x) {
  x <- iconv(x, from = "UTF-8", to = "ASCII//TRANSLIT")
  x <- tolower(x)
  x <- gsub("[^a-z0-9]+", "_", x)
  x <- gsub("^_+|_+$", "", x)
  x
}

ler_csv_generico <- function(caminho, sep = ";", encoding = "Latin1") {
  if (!file.exists(caminho)) stop("Arquivo não encontrado: ", caminho)
  df <- utils::read.csv(caminho, sep = sep, stringsAsFactors = FALSE, check.names = FALSE, colClasses = "character", fileEncoding = encoding)
  names(df) <- normalizar_nome_coluna(names(df))
  df
}

preparar_habilitacoes_cnes <- function(
  dir_raw = "data_raw/cnes",
  dir_interim = "data_interim/cnes",
  dir_metadata = "metadata/cnes",
  competencia = "202601"
) {
  caminho_estab <- file.path(dir_interim, "estabelecimentos", paste0("cnes_estabelecimentos_es_", competencia, ".csv"))
  caminho_rl <- file.path(dir_raw, competencia, paste0("rlEstabSipac", competencia, ".csv"))
  caminho_dom <- file.path(dir_raw, competencia, paste0("tbSubGruposHabilitacao", competencia, ".csv"))
  caminho_class <- file.path(dir_metadata, "classificacao_habilitacoes_cnes.csv")

  estab <- ler_csv_generico(caminho_estab, sep = ",", encoding = "UTF-8")
  rl <- ler_csv_generico(caminho_rl, sep = ";", encoding = "Latin1")
  dom <- ler_csv_generico(caminho_dom, sep = ";", encoding = "Latin1")
  classif <- ler_csv_generico(caminho_class, sep = ";", encoding = "UTF-8")

  map_rl <- c(
    co_unidade = "cnes",
    cod_sub_grupo_habilitacao = "codigo_habilitacao",
    tp_habilitacao = "tipo_habilitacao",
    cmtp_inicio = "competencia_inicio",
    cmtp_fim = "competencia_fim",
    nu_leitos = "numero_leitos",
    no_portaria = "portaria",
    to_char_dt_atualizacao_dd_mm_yyyy = "data_atualizacao"
  )
  for (k in names(map_rl)) if (k %in% names(rl)) names(rl)[names(rl) == k] <- map_rl[[k]]

  map_dom <- c(
    co_codigo_grupo = "codigo_habilitacao",
    no_descricao_grupo = "descricao_habilitacao",
    tp_origem = "origem_habilitacao",
    tp_habilitacao = "tipo_habilitacao"
  )
  for (k in names(map_dom)) if (k %in% names(dom)) names(dom)[names(dom) == k] <- map_dom[[k]]

  obrig_rl <- c("cnes", "codigo_habilitacao", "tipo_habilitacao")
  obrig_dom <- c("codigo_habilitacao", "tipo_habilitacao", "descricao_habilitacao", "origem_habilitacao")
  obrig_class <- c("codigo_habilitacao", "tipo_habilitacao", "linha_cuidado", "sublinha_cuidado", "componente_rede", "nivel_complexidade", "usar_observatorio", "prioridade", "criterio_classificacao", "status_validacao")
  obrig_estab <- c("cnes", "nome_estabelecimento", "cod_municipio", "municipio", "uf", "tipo_estabelecimento", "subtipo_estabelecimento", "natureza_juridica", "gestao", "atende_sus")

  if (length(setdiff(obrig_rl, names(rl))) > 0) stop("rlEstabSipac sem colunas obrigatórias.")
  if (length(setdiff(obrig_dom, names(dom))) > 0) stop("tbSubGruposHabilitacao sem colunas obrigatórias.")
  if (length(setdiff(obrig_class, names(classif))) > 0) stop("Classificação sem colunas obrigatórias.")
  if (length(setdiff(obrig_estab, names(estab))) > 0) stop("Base de estabelecimentos sem colunas obrigatórias.")

  txt_cols <- intersect(c("cnes", "codigo_habilitacao", "tipo_habilitacao", "cod_municipio"), names(estab))
  for (col in txt_cols) estab[[col]] <- trimws(as.character(estab[[col]]))
  for (col in c("cnes", "codigo_habilitacao", "tipo_habilitacao")) {
    if (col %in% names(rl)) rl[[col]] <- trimws(as.character(rl[[col]]))
    if (col %in% names(dom)) dom[[col]] <- trimws(as.character(dom[[col]]))
    if (col %in% names(classif)) classif[[col]] <- trimws(as.character(classif[[col]]))
  }

  cnes_es <- unique(estab$cnes)
  rl_filtrado <- rl[rl$cnes %in% cnes_es, , drop = FALSE]
  cnes_fora_base <- sum(!(unique(rl$cnes) %in% cnes_es))

  if (nrow(rl_filtrado) == 0) {
    stop(
      paste0(
        "Filtro territorial resultou em 0 registros. ",
        "Verifique se a base de estabelecimentos ES do Ciclo 2 foi gerada com dados reais ",
        "(não fixture/placeholder) e se os formatos de CNES são compatíveis."
      )
    )
  }

  base <- merge(rl_filtrado, dom[, obrig_dom], by = c("codigo_habilitacao", "tipo_habilitacao"), all.x = TRUE, sort = FALSE)
  base <- merge(base, classif[, c("codigo_habilitacao", "tipo_habilitacao", "linha_cuidado", "sublinha_cuidado", "componente_rede", "nivel_complexidade", "usar_observatorio", "prioridade", "criterio_classificacao", "status_validacao")], by = c("codigo_habilitacao", "tipo_habilitacao"), all.x = TRUE, sort = FALSE)
  base <- merge(base, estab[, obrig_estab], by = "cnes", all.x = TRUE, sort = FALSE)

  base$competencia <- competencia
  base$linha_cuidado[is.na(base$linha_cuidado) | trimws(base$linha_cuidado) == ""] <- "Não classificada"
  base$usar_observatorio[is.na(base$usar_observatorio) | trimws(base$usar_observatorio) == ""] <- "Não"
  base$status_validacao[is.na(base$status_validacao) | trimws(base$status_validacao) == ""] <- "revisar"
  base$fonte <- "CNES"
  base$arquivo_origem <- paste0("rlEstabSipac", competencia)
  base$data_processamento <- as.character(Sys.Date())

  campos_finais <- c(
    "competencia", "cnes", "nome_estabelecimento", "cod_municipio", "municipio", "uf",
    "tipo_estabelecimento", "subtipo_estabelecimento", "natureza_juridica", "gestao", "atende_sus",
    "codigo_habilitacao", "tipo_habilitacao", "descricao_habilitacao", "origem_habilitacao",
    "linha_cuidado", "sublinha_cuidado", "componente_rede", "nivel_complexidade", "usar_observatorio",
    "prioridade", "criterio_classificacao", "status_validacao", "competencia_inicio", "competencia_fim",
    "numero_leitos", "portaria", "data_atualizacao", "fonte", "arquivo_origem", "data_processamento"
  )
  for (c in setdiff(campos_finais, names(base))) base[[c]] <- NA_character_
  base <- base[, campos_finais, drop = FALSE]

  dup_antes <- nrow(base)
  base <- unique(base)
  attr(base, "duplicidades_exatas_removidas") <- dup_antes - nrow(base)
  attr(base, "cnes_fora_base_estabelecimentos") <- cnes_fora_base

  dir_saida <- file.path(dir_interim, "habilitacoes")
  if (!dir.exists(dir_saida)) dir.create(dir_saida, recursive = TRUE)
  caminho_saida <- file.path(dir_saida, paste0("cnes_habilitacoes_es_", competencia, ".csv"))
  utils::write.csv(base, caminho_saida, row.names = FALSE, fileEncoding = "UTF-8")

  base
}
