# Prepara base de estabelecimentos CNES restrita a uma UF (Ciclo 2).

normalizar_nome_coluna <- function(x) {
  x <- iconv(x, from = "UTF-8", to = "ASCII//TRANSLIT")
  x <- tolower(x)
  x <- gsub("[^a-z0-9]+", "_", x)
  x <- gsub("^_+|_+$", "", x)
  x
}

ler_csv_cnes <- function(caminho_base_sem_ext) {
  candidatos <- c(
    paste0(caminho_base_sem_ext, ".csv"),
    paste0(caminho_base_sem_ext, ".csv.gz"),
    paste0(caminho_base_sem_ext, ".zip")
  )
  arquivo <- candidatos[file.exists(candidatos)][1]
  if (is.na(arquivo)) stop("Arquivo não encontrado para base: ", basename(caminho_base_sem_ext))

  detectar_sep <- function(con) {
    cab <- readLines(con, n = 1, warn = FALSE, encoding = "Latin1")
    if (length(cab) == 0) return(";")
    if (grepl("version https://git-lfs.github.com/spec/v1", cab[1], fixed = TRUE)) return("LFS")
    if (length(gregexpr(";", cab[1], fixed = TRUE)[[1]]) >= length(gregexpr(",", cab[1], fixed = TRUE)[[1]])) ";" else ","
  }

  ler_arquivo <- function(path, unzip_member = NULL) {
    if (!is.null(unzip_member)) {
      linhas <- readLines(unz(path, unzip_member), n = 1, warn = FALSE, encoding = "Latin1")
      sep <- if (length(linhas) > 0 && grepl(";", linhas[1], fixed = TRUE)) ";" else ","
      return(utils::read.csv(unz(path, unzip_member), sep = sep, stringsAsFactors = FALSE, check.names = FALSE, colClasses = "character", fileEncoding = "Latin1"))
    }
    con <- if (grepl("\\.gz$", path)) gzfile(path, open = "rt") else file(path, open = "rt")
    on.exit(close(con), add = TRUE)
    sep <- detectar_sep(con)
    close(con)
    if (sep == "LFS") stop("Arquivo ", basename(path), " é ponteiro Git LFS sem conteúdo tabular real.")
    utils::read.csv(path, sep = sep, stringsAsFactors = FALSE, check.names = FALSE, colClasses = "character", fileEncoding = "Latin1")
  }

  if (grepl("\\.zip$", arquivo)) {
    membros <- utils::unzip(arquivo, list = TRUE)$Name
    membro_csv <- membros[grepl("\\.csv$", membros, ignore.case = TRUE)][1]
    if (is.na(membro_csv)) stop("ZIP sem CSV interno: ", basename(arquivo))
    dados <- ler_arquivo(arquivo, unzip_member = membro_csv)
  } else {
    dados <- ler_arquivo(arquivo)
  }

  names(dados) <- normalizar_nome_coluna(names(dados))
  dados
}

primeira_coluna_existente <- function(df, candidatos) {
  col <- intersect(candidatos, names(df))
  if (length(col) == 0) return(NA_character_)
  col[1]
}

agregar_unicos <- function(x) {
  vals <- unique(trimws(x[!is.na(x) & trimws(x) != ""]))
  if (length(vals) == 0) return(NA_character_)
  paste(vals, collapse = " | ")
}

preparar_estabelecimentos_cnes <- function(dir_raw, competencia = "202601", uf_interesse = "ES") {
  base <- file.path(dir_raw, competencia)

  tb_municipio <- ler_csv_cnes(file.path(base, paste0("tbMunicipio", competencia)))
  col_uf <- primeira_coluna_existente(tb_municipio, c("co_sigla_estado", "uf", "sg_uf"))
  col_coduf <- primeira_coluna_existente(tb_municipio, c("co_estado", "co_uf", "codigo_uf"))
  col_codmun <- primeira_coluna_existente(tb_municipio, c("co_municipio", "cod_municipio", "codigo_municipio"))
  col_nome_mun <- primeira_coluna_existente(tb_municipio, c("no_municipio", "municipio", "nome_municipio"))
  if (is.na(col_codmun)) stop("tbMunicipio sem coluna de código de município.")

  filtro_es <- rep(FALSE, nrow(tb_municipio))
  if (!is.na(col_uf)) filtro_es <- filtro_es | toupper(trimws(tb_municipio[[col_uf]])) == toupper(uf_interesse)
  if (!is.na(col_coduf)) filtro_es <- filtro_es | trimws(tb_municipio[[col_coduf]]) == "32"
  municipios_es <- unique(trimws(tb_municipio[[col_codmun]][filtro_es]))
  municipios_es <- municipios_es[municipios_es != ""]
  if (length(municipios_es) == 0) stop("Não foi possível identificar municípios da UF de interesse em tbMunicipio.")

  tb_estab <- ler_csv_cnes(file.path(base, paste0("tbEstabelecimento", competencia)))
  col_cnes <- primeira_coluna_existente(tb_estab, c("co_unidade", "cnes"))
  col_mun_est <- primeira_coluna_existente(tb_estab, c("co_municipio_gestor", "co_municipio", "cod_municipio"))
  if (is.na(col_cnes) || is.na(col_mun_est)) stop("tbEstabelecimento sem colunas mínimas de CNES/município.")

  tb_estab <- tb_estab[trimws(tb_estab[[col_mun_est]]) %in% municipios_es, , drop = FALSE]
  if (nrow(tb_estab) == 0) stop("Nenhum estabelecimento encontrado para a UF de interesse.")

  tb_tipo <- ler_csv_cnes(file.path(base, paste0("tbTipoEstabelecimento", competencia)))
  tb_nat <- ler_csv_cnes(file.path(base, paste0("tbNaturezaJuridica", competencia)))
  tb_gest <- ler_csv_cnes(file.path(base, paste0("tbGestao", competencia)))
  rl_sub <- ler_csv_cnes(file.path(base, paste0("rlEstabSubTipo", competencia)))
  tb_sub <- ler_csv_cnes(file.path(base, paste0("tbSubTipo", competencia)))
  rl_at <- ler_csv_cnes(file.path(base, paste0("rlEstabAtendPrestConv", competencia)))
  tb_at <- ler_csv_cnes(file.path(base, paste0("tbAtendimentoPrestado", competencia)))
  tb_conv <- ler_csv_cnes(file.path(base, paste0("tbConvenio", competencia)))

  # joins auxiliares agregados por cnes
  col_sub_cnes <- primeira_coluna_existente(rl_sub, c("co_unidade", "cnes"))
  col_sub_tipo <- primeira_coluna_existente(rl_sub, c("co_tipo_unidade"))
  col_sub_sub <- primeira_coluna_existente(rl_sub, c("co_sub_tipo_unidade", "co_sub_tipo"))
  col_tbsub_tipo <- primeira_coluna_existente(tb_sub, c("co_tipo_unidade"))
  col_tbsub_sub <- primeira_coluna_existente(tb_sub, c("co_sub_tipo"))
  col_tbsub_ds <- primeira_coluna_existente(tb_sub, c("ds_sub_tipo"))

  subagg <- data.frame(cnes = character(0), subtipo_estabelecimento = character(0), stringsAsFactors = FALSE)
  if (!any(is.na(c(col_sub_cnes, col_sub_tipo, col_sub_sub, col_tbsub_tipo, col_tbsub_sub, col_tbsub_ds)))) {
    chave_rl <- paste(rl_sub[[col_sub_tipo]], rl_sub[[col_sub_sub]], sep = "__")
    chave_tb <- paste(tb_sub[[col_tbsub_tipo]], tb_sub[[col_tbsub_sub]], sep = "__")
    rl_sub$ds_sub_tipo <- tb_sub[[col_tbsub_ds]][match(chave_rl, chave_tb)]
    subagg <- aggregate(rl_sub$ds_sub_tipo, by = list(cnes = rl_sub[[col_sub_cnes]]), FUN = agregar_unicos)
    names(subagg)[2] <- "subtipo_estabelecimento"
  }

  col_rlat_cnes <- primeira_coluna_existente(rl_at, c("co_unidade", "cnes"))
  col_rlat_at <- primeira_coluna_existente(rl_at, c("co_atendimento_prestado"))
  col_rlat_conv <- primeira_coluna_existente(rl_at, c("co_convenio"))
  col_tbat_cod <- primeira_coluna_existente(tb_at, c("co_atendimento_prestado"))
  col_tbat_ds <- primeira_coluna_existente(tb_at, c("ds_atendimento_prestado"))
  col_tbco_cod <- primeira_coluna_existente(tb_conv, c("co_convenio"))
  col_tbco_ds <- primeira_coluna_existente(tb_conv, c("ds_convenio"))

  atagg <- data.frame(cnes = character(0), atendimento_prestado = character(0), convenio = character(0), stringsAsFactors = FALSE)
  if (!any(is.na(c(col_rlat_cnes, col_rlat_at, col_rlat_conv, col_tbat_cod, col_tbat_ds, col_tbco_cod, col_tbco_ds)))) {
    rl_at$ds_atendimento <- tb_at[[col_tbat_ds]][match(rl_at[[col_rlat_at]], tb_at[[col_tbat_cod]])]
    rl_at$ds_convenio <- tb_conv[[col_tbco_ds]][match(rl_at[[col_rlat_conv]], tb_conv[[col_tbco_cod]])]
    atagg <- aggregate(cbind(ds_atendimento, ds_convenio) ~ cnes, data = data.frame(cnes = rl_at[[col_rlat_cnes]], ds_atendimento = rl_at$ds_atendimento, ds_convenio = rl_at$ds_convenio, stringsAsFactors = FALSE), FUN = agregar_unicos)
    names(atagg)[2:3] <- c("atendimento_prestado", "convenio")
  }

  getcol <- function(df, cand) primeira_coluna_existente(df, cand)
  out <- data.frame(
    competencia = competencia,
    cnes = tb_estab[[col_cnes]],
    nome_estabelecimento = tb_estab[[getcol(tb_estab, c("no_fantasia", "nome_fantasia", "nome_estabelecimento"))]],
    razao_social = tb_estab[[getcol(tb_estab, c("no_razao_social", "razao_social"))]],
    cod_municipio = tb_estab[[col_mun_est]],
    stringsAsFactors = FALSE
  )

  out$municipio <- tb_municipio[[col_nome_mun]][match(out$cod_municipio, tb_municipio[[col_codmun]])]
  out$uf <- uf_interesse

  col_tipo_est <- getcol(tb_estab, c("co_tipo_unidade", "co_tipo_estabelecimento"))
  col_tb_tipo_cod <- getcol(tb_tipo, c("co_tipo_estabelecimento", "co_tipo_unidade"))
  col_tb_tipo_ds <- getcol(tb_tipo, c("ds_tipo_estabelecimento"))
  out$tipo_estabelecimento <- if (!any(is.na(c(col_tipo_est, col_tb_tipo_cod, col_tb_tipo_ds)))) tb_tipo[[col_tb_tipo_ds]][match(tb_estab[[col_tipo_est]], tb_tipo[[col_tb_tipo_cod]])] else NA_character_

  col_nat_est <- getcol(tb_estab, c("co_natureza_jur", "co_natureza_juridica"))
  col_nat_cod <- getcol(tb_nat, c("co_natureza_jur"))
  col_nat_ds <- getcol(tb_nat, c("ds_natureza_jur"))
  out$natureza_juridica <- if (!any(is.na(c(col_nat_est, col_nat_cod, col_nat_ds)))) tb_nat[[col_nat_ds]][match(tb_estab[[col_nat_est]], tb_nat[[col_nat_cod]])] else NA_character_

  col_ges_est <- getcol(tb_estab, c("co_gestao"))
  col_ges_cod <- getcol(tb_gest, c("co_gestao"))
  col_ges_ds <- getcol(tb_gest, c("ds_gestao"))
  out$gestao <- if (!any(is.na(c(col_ges_est, col_ges_cod, col_ges_ds)))) tb_gest[[col_ges_ds]][match(tb_estab[[col_ges_est]], tb_gest[[col_ges_cod]])] else NA_character_

  out <- merge(out, subagg, by = "cnes", all.x = TRUE, sort = FALSE)
  out <- merge(out, atagg, by = "cnes", all.x = TRUE, sort = FALSE)

  out$atende_sus <- ifelse(grepl("SUS", toupper(paste(out$atendimento_prestado, out$convenio))), "Sim", ifelse(is.na(out$atendimento_prestado) & is.na(out$convenio), NA_character_, "Revisar"))
  out$atende_sus[is.na(out$atende_sus)] <- "Revisar"

  out$fonte <- "CNES"
  out$arquivo_origem <- "tbEstabelecimento202601"
  out$data_processamento <- as.character(Sys.Date())

  out <- out[!duplicated(out$cnes) & !is.na(out$cnes) & trimws(out$cnes) != "", ]

  dir_saida <- file.path("data_interim", "cnes", "estabelecimentos")
  if (!dir.exists(dir_saida)) dir.create(dir_saida, recursive = TRUE)
  caminho_saida <- file.path(dir_saida, paste0("cnes_estabelecimentos_", tolower(uf_interesse), "_", competencia, ".csv"))
  utils::write.csv(out, caminho_saida, row.names = FALSE, fileEncoding = "UTF-8")
  out
}
