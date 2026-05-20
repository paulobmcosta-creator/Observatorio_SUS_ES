script <- file.path("src", "transform", "preparar_estabelecimentos_cnes.R")
if (!file.exists(script)) stop("Script preparar_estabelecimentos_cnes.R não encontrado.")
source(script)
if (!exists("preparar_estabelecimentos_cnes")) stop("Função preparar_estabelecimentos_cnes não encontrada.")

raw_hash_before <- tools::md5sum(list.files(file.path("data_raw", "cnes", "202601"), full.names = TRUE))

resultado <- preparar_estabelecimentos_cnes(dir_raw = file.path("tests", "fixtures", "cnes"), competencia = "202601", uf_interesse = "ES")
if (!is.data.frame(resultado)) stop("Resultado da função não é data.frame.")
if (nrow(resultado) <= 0) stop("Resultado sem linhas.")

cols_min <- c("competencia", "cnes", "nome_estabelecimento", "cod_municipio", "municipio", "uf", "tipo_estabelecimento", "subtipo_estabelecimento", "natureza_juridica", "gestao", "atende_sus", "fonte", "arquivo_origem", "data_processamento")
miss <- setdiff(cols_min, names(resultado))
if (length(miss) > 0) stop("Colunas mínimas ausentes: ", paste(miss, collapse = ", "))

if (any(is.na(resultado$cnes) | trimws(resultado$cnes) == "")) stop("cnes vazio encontrado.")
if (any(is.na(resultado$cod_municipio) | trimws(resultado$cod_municipio) == "")) stop("cod_municipio vazio encontrado.")
if (!all(resultado$cod_municipio %in% c("3200102"))) stop("Base contém município fora do ES na fixture.")
if ("uf" %in% names(resultado) && !all(resultado$uf == "ES")) stop("Campo uf contém valor diferente de ES.")
if (any(duplicated(resultado$cnes))) stop("Duplicidade de cnes encontrada.")
if (length(setdiff(unique(na.omit(resultado$atende_sus)), c("Sim", "Não", "Revisar"))) > 0) stop("atende_sus fora do conjunto permitido.")

schema <- file.path("metadata", "cnes", "schema_estabelecimentos_cnes.csv")
dicionario <- file.path("metadata", "cnes", "dicionario_estabelecimentos_cnes.csv")
doc <- file.path("docs", "cnes", "base_estabelecimentos_cnes.md")
if (!file.exists(schema)) stop("Schema não encontrado.")
if (!file.exists(dicionario)) stop("Dicionário não encontrado.")
if (!file.exists(doc)) stop("Documentação não encontrada.")

schema_df <- read.csv(schema, stringsAsFactors = FALSE)
dic_df <- read.csv(dicionario, stringsAsFactors = FALSE)
if (length(setdiff(names(resultado), schema_df$nome_campo)) > 0) stop("Nem todos os campos da base constam no schema.")
if (length(setdiff(names(resultado), dic_df$nome_campo)) > 0) stop("Nem todos os campos da base constam no dicionário.")

raw_hash_after <- tools::md5sum(list.files(file.path("data_raw", "cnes", "202601"), full.names = TRUE))
if (!identical(raw_hash_before, raw_hash_after)) stop("Arquivos brutos foram alterados indevidamente.")

nacional <- list.files(file.path("data_interim", "cnes"), pattern = "nacional|brasil", recursive = TRUE, ignore.case = TRUE)
if (length(nacional) > 0) stop("Detectado indício de base nacional em data_interim.")

message("OK: testes base estabelecimentos CNES passaram.")
