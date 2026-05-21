script <- file.path("src", "transform", "preparar_habilitacoes_cnes.R")
if (!file.exists(script)) stop("Script preparar_habilitacoes_cnes.R não encontrado.")
source(script)
if (!exists("preparar_habilitacoes_cnes")) stop("Função preparar_habilitacoes_cnes não encontrada.")

raw_hash_before <- tools::md5sum(list.files(file.path("data_raw", "cnes", "202601"), full.names = TRUE))

res <- preparar_habilitacoes_cnes(dir_raw = "data_raw/cnes", dir_interim = "data_interim/cnes", dir_metadata = "metadata/cnes", competencia = "202601")

out_path <- file.path("data_interim", "cnes", "habilitacoes", "cnes_habilitacoes_es_202601.csv")
if (!file.exists(out_path)) stop("Base final não foi gerada.")
out <- tryCatch(read.csv(out_path, stringsAsFactors = FALSE, fileEncoding = "UTF-8"), error = function(e) stop("Falha de leitura/encoding da base final."))

cols_min <- c("competencia","cnes","nome_estabelecimento","cod_municipio","municipio","uf","tipo_estabelecimento","subtipo_estabelecimento","natureza_juridica","gestao","atende_sus","codigo_habilitacao","tipo_habilitacao","descricao_habilitacao","origem_habilitacao","linha_cuidado","sublinha_cuidado","componente_rede","nivel_complexidade","usar_observatorio","prioridade","criterio_classificacao","status_validacao","competencia_inicio","competencia_fim","numero_leitos","portaria","fonte","arquivo_origem","data_processamento")
if (length(setdiff(cols_min, names(out))) > 0) stop("Colunas mínimas ausentes.")
if (nrow(out) <= 0) stop("Base final sem linhas.")
if (any(is.na(out$cnes) | trimws(out$cnes) == "")) stop("cnes vazio encontrado.")
if (any(is.na(out$codigo_habilitacao) | trimws(out$codigo_habilitacao) == "")) stop("codigo_habilitacao vazio encontrado.")
if (any(is.na(out$tipo_habilitacao) | trimws(out$tipo_habilitacao) == "")) stop("tipo_habilitacao vazio encontrado.")
if (!all(out$uf == "ES")) stop("UF diferente de ES encontrada.")

estab <- read.csv(file.path("data_interim", "cnes", "estabelecimentos", "cnes_estabelecimentos_es_202601.csv"), stringsAsFactors = FALSE)
if (!all(out$cnes %in% estab$cnes)) stop("CNES fora da base de estabelecimentos ES.")

if (any(out$usar_observatorio == "Sim" & (is.na(out$linha_cuidado) | trimws(out$linha_cuidado) == ""))) stop("linha_cuidado vazia com usar_observatorio=Sim.")
classif <- read.csv(file.path("metadata", "cnes", "classificacao_habilitacoes_cnes.csv"), stringsAsFactors = FALSE, sep = ";")
if (length(setdiff(unique(na.omit(out$usar_observatorio)), unique(na.omit(classif$usar_observatorio)))) > 0) stop("usar_observatorio fora do domínio da classificação.")
if (length(setdiff(unique(na.omit(out$status_validacao)), unique(na.omit(classif$status_validacao)))) > 0) stop("status_validacao fora do domínio da classificação.")

schema <- file.path("metadata", "cnes", "schema_habilitacoes_cnes.csv")
dic <- file.path("metadata", "cnes", "dicionario_habilitacoes_cnes.csv")
if (!file.exists(schema)) stop("Schema não encontrado.")
if (!file.exists(dic)) stop("Dicionário não encontrado.")
schema_df <- read.csv(schema, stringsAsFactors = FALSE)
dic_df <- read.csv(dic, stringsAsFactors = FALSE)
if (length(setdiff(names(out), schema_df$nome_campo)) > 0) stop("Campos da base não cobertos no schema.")
if (length(setdiff(names(out), dic_df$nome_campo)) > 0) stop("Campos da base não cobertos no dicionário.")

raw_hash_after <- tools::md5sum(list.files(file.path("data_raw", "cnes", "202601"), full.names = TRUE))
if (!identical(raw_hash_before, raw_hash_after)) stop("Arquivos brutos foram alterados.")

if (length(list.files(file.path("data_interim", "cnes"), pattern = "nacional|brasil", recursive = TRUE, ignore.case = TRUE)) > 0) stop("Indício de base nacional em data_interim.")
if (length(list.files(file.path("data_interim", "cnes"), pattern = "indicador", recursive = TRUE, ignore.case = TRUE)) > 0) stop("Indício de indicador criado neste ciclo.")

message("OK: testes base habilitações CNES passaram.")
