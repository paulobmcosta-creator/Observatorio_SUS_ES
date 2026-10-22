# Comparação isolada da competência 202601. Não promove resultados às camadas oficiais.
# Uso: Rscript scripts/comparar_reprocessamento_cnes.R FONTE_LOCAL ID_EXECUCAO RESPONSAVEL
source("src/extract/preparar_cache_cnes.R")
source("src/transform/preparar_estabelecimentos_cnes.R")
source("src/transform/preparar_habilitacoes_cnes.R")
source("src/validation/conferir_contrato_snapshot_cnes.R")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L || !grepl("^[a-zA-Z0-9_-]+$", args[2]) || !nzchar(trimws(args[3]))) {
  stop("Informe FONTE_LOCAL ID_EXECUCAO (letras/números/_/-) RESPONSAVEL.")
}
fonte <- normalizePath(args[1], mustWork = TRUE)
saida <- file.path(".cache/cnes/execucoes", args[2])
evidencia <- file.path("metadata/ciclo_2026_2027/execucoes", args[2])
if (file.exists(saida) || file.exists(evidencia)) stop("Execução já existente: use outro identificador.")
manifesto <- "metadata/cnes/fontes/tbEstabelecimento202601.csv"
legado_est <- "data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv"
legado_hab <- "data_interim/cnes/habilitacoes/cnes_habilitacoes_es_202601.csv"
insumos <- unique(c(fonte, manifesto, legado_est, legado_hab,
  list.files("data_raw/cnes/202601", full.names = TRUE),
  "metadata/cnes/classificacao_habilitacoes_cnes.csv",
  "metadata/cnes/schema_estabelecimentos_cnes.csv", "metadata/cnes/schema_habilitacoes_cnes.csv",
  "src/extract/preparar_cache_cnes.R", "src/transform/preparar_estabelecimentos_cnes.R",
  "src/transform/preparar_habilitacoes_cnes.R", "src/validation/conferir_contrato_snapshot_cnes.R",
  "scripts/comparar_reprocessamento_cnes.R"))
insumos <- insumos[!file.info(insumos)$isdir]
hashes <- vapply(insumos, sha256_fonte_cnes, character(1))
inicio <- format(Sys.time(), tz = "UTC", usetz = TRUE)
cache <- preparar_cache_cnes(fonte, manifesto)
est <- preparar_estabelecimentos_cnes("data_raw/cnes", dir_interim = saida, arquivo_estabelecimentos = cache)
hab <- preparar_habilitacoes_cnes(dir_interim = saida)
n_fonte <- c(attr(est, "n_registros_fonte"), attr(hab, "n_registros_fonte"))
n_recorte <- c(attr(est, "n_registros_recorte"), attr(hab, "n_registros_recorte"))
# Conferência da representação persistida (todos os identificadores como texto).
est <- ler_snapshot_cnes(file.path(saida, "estabelecimentos/cnes_estabelecimentos_es_202601.csv"))
hab <- ler_snapshot_cnes(file.path(saida, "habilitacoes/cnes_habilitacoes_es_202601.csv"))
classif <- ler_snapshot_cnes("metadata/cnes/classificacao_habilitacoes_cnes.csv", ";")
checks <- conferir_contrato_snapshot_cnes(est, hab, classif,
  ler_schema_snapshot_cnes("metadata/cnes/schema_estabelecimentos_cnes.csv"),
  ler_schema_snapshot_cnes("metadata/cnes/schema_habilitacoes_cnes.csv"))
ant_est <- ler_snapshot_cnes(legado_est)
ant_hab <- ler_snapshot_cnes(legado_hab)
# Comparação explícita de chaves observadas: nunca modifica os snapshots legados.
comparar <- function(antigo, novo, escopo, campos_chave) {
  chave_antiga <- antigo
  chave_antiga$co_unidade <- antigo$cnes
  chave <- function(d) do.call(paste, c(d[campos_chave], sep = "__"))
  ka <- chave(chave_antiga); kn <- chave(novo)
  if (anyDuplicated(ka) || anyDuplicated(kn)) stop("Chave de comparação não é única: ", escopo)
  idx <- match(ka, kn)
  comuns <- intersect(names(antigo), names(novo))
  diferentes <- vapply(comuns, function(campo) {
    a <- antigo[[campo]]; b <- novo[[campo]][idx]
    sum(is.na(idx) | xor(is.na(a), is.na(b)) | (!is.na(a) & !is.na(b) & a != b))
  }, integer(1))
  data.frame(escopo = escopo, medida = c("chaves_antigas_ausentes", "chaves_novas_sem_legado", paste0("diferencas:", comuns)),
    valor = c(sum(is.na(idx)), sum(!kn %in% ka), diferentes))
}
comparacao <- rbind(comparar(ant_est, est, "estabelecimentos", "co_unidade"),
  comparar(ant_hab, hab, "habilitacoes", c("co_unidade", "codigo_habilitacao", "tipo_habilitacao")))
resumo <- data.frame(medida = c("estabelecimentos", "municipios", "cnes_publicos_7_digitos", "cnes_publicos_com_zero_inicial",
  "habilitacoes", "habilitacoes_no_escopo", "no_escopo_validado_interno", "no_escopo_revisar", "fora_escopo",
  "checks_passou", "checks_falhou", "checks_nao_executado", "bytes_csv", "bytes_gzip"),
  valor = c(nrow(est), length(unique(est$cod_municipio)), sum(grepl("^[0-9]{7}$", est$cnes)), sum(grepl("^0", est$cnes)),
    nrow(hab), sum(hab$usar_observatorio == "Sim"), sum(hab$usar_observatorio == "Sim" & hab$status_validacao == "validado"),
    sum(hab$usar_observatorio == "Sim" & hab$status_validacao == "revisar"), sum(hab$usar_observatorio == "Não"),
    sum(checks$estado == "passou"), sum(checks$estado == "falhou"), sum(checks$estado == "nao_executado"),
    read.csv(manifesto)$bytes_csv, file.info(cache)$size))
stopifnot(identical(hashes, vapply(insumos, sha256_fonte_cnes, character(1))))
dir.create(evidencia, recursive = TRUE)
gravar <- function(d, nome) write.csv(d, file.path(evidencia, nome), row.names = FALSE, na = "", fileEncoding = "UTF-8")
gravar(data.frame(arquivo = insumos, sha256 = unname(hashes)), "insumos_sha256.csv")
gravar(checks, "verificacoes.csv")
gravar(comparacao, "comparacao_legado.csv")
gravar(resumo, "contagens_observadas.csv")
gravar(data.frame(inicio_utc = inicio, fim_utc = format(Sys.time(), tz = "UTC", usetz = TRUE), responsavel = args[3],
  competencia = "202601", finalidade = "comparacao_isolada_sem_promocao", versao_r = as.character(getRversion()),
  cache = cache, sha256_gzip = sha256_fonte_cnes(cache), saida_dados = saida), "execucao.csv")
arquivos_derivados <- c(file.path(saida, "estabelecimentos/cnes_estabelecimentos_es_202601.csv"),
  file.path(saida, "habilitacoes/cnes_habilitacoes_es_202601.csv"))
versao_base <- system2("git", c("rev-parse", "HEAD"), stdout = TRUE)
gravar(data.frame(sistema = "CNES", familia = c("tbEstabelecimento", "rlEstabSipac"),
  abrangencia_fonte = "Brasil", recorte_derivado = "ES por municipio gestor; competencia 202601",
  competencia = "2026-01", arquivo_original = c("tbEstabelecimento202601.csv", "rlEstabSipac202601.csv"),
  origem_primaria = "nao_documentada_no_acervo_recebido", data_hora_obtencao_primaria = "nao_documentada",
  origem_recuperacao = c("Git LFS; commit e SHA-256 no manifesto da fonte", "arquivo bruto versionado no checkout"),
  inicio_processamento_utc = inicio, fim_processamento_utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
  arquivo_derivado = arquivos_derivados, tamanho_bytes = file.info(arquivos_derivados)$size,
  sha256_derivado = vapply(arquivos_derivados, sha256_fonte_cnes, character(1)),
  n_registros_fonte = n_fonte, n_registros_recorte = n_recorte, n_registros_derivado = c(nrow(est), nrow(hab)),
  schema = c("metadata/cnes/schema_estabelecimentos_cnes.csv", "metadata/cnes/schema_habilitacoes_cnes.csv"),
  versao_pipeline_base = versao_base, versao_pipeline_efetiva = paste0("sha256_manifesto_insumos:", sha256_fonte_cnes(file.path(evidencia, "insumos_sha256.csv"))),
  responsavel = args[3], observacoes = "Nova execução local com diff não commitado; origem primária não reconstituída; não houve deduplicação nem promoção analítica."), "manifesto_derivados.csv")
produtos <- c(list.files(saida, recursive = TRUE, full.names = TRUE), list.files(evidencia, full.names = TRUE))
gravar(data.frame(arquivo = produtos, sha256 = vapply(produtos, sha256_fonte_cnes, character(1))), "produtos_sha256.csv")
print(resumo, row.names = FALSE)
cat("Evidências:", evidencia, "\n")
if (any(checks$estado != "passou")) quit(status = 1L)
