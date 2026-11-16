# Executor local: Rscript script ACEITE.csv SHA_ACEITE PYTHON SAIDA_NOVA [MAPA VERSAO SHA_MAPA PROVAS_ATOS.csv]
# Sem documento/DBC/cobertura válidos o verificador bloqueia; não aceita flags avulsas.
source("src/extract/preparar_cache_cnes.R")
source("src/validation/validar_vinculos_sih.R")
source("src/validation/validar_correspondencia_territorial.R")
source("src/transform/territorializar_municipios.R")
source("src/indicators/calcular_percurso_sih.R")
args <- commandArgs(trailingOnly = TRUE)
if (!length(args) %in% c(4L, 8L)) stop("Informe ACEITE.csv SHA_ACEITE PYTHON SAIDA_NOVA [MAPA VERSAO SHA_MAPA PROVAS_ATOS.csv].")
if (sha256_fonte_cnes(args[1]) != args[2]) stop("Aceite diverge do hash informado.")
a <- read.csv(args[1], colClasses = "character", check.names = FALSE)
if (!all(c("papel", "caminho", "sha256") %in% names(a)) || anyDuplicated(a$papel) ||
    !all(c("parametros", "dataset_csv", "plano_provas") %in% a$papel)) stop("Aceite sem provas mínimas.")
parametros <- read.csv(a$caminho[a$papel == "parametros"], colClasses = "character", na.strings = character())
contrato <- setNames(lapply(parametros$valor, function(v) strsplit(v, "|", fixed = TRUE)[[1]]), parametros$chave)
contrato$aceite_execucao <- args[1]; contrato$aceite_sha256 <- args[2]; contrato$python_validacao <- args[3]
dataset <- a$caminho[a$papel == "dataset_csv"]
rd <- read.csv(dataset, colClasses = "character", check.names = FALSE, na.strings = character())
mapa <- NULL
if (length(args) == 8L) {
  contrato$territorio_arquivo <- args[5]; contrato$territorio_versao <- args[6]
  contrato$territorio_sha256 <- args[7]; contrato$territorio_provas <- args[8]
  mapa <- read.csv(args[5], colClasses = "character", check.names = FALSE, na.strings = character())
}
repo <- normalizePath(".", winslash = "/", mustWork = TRUE)
destino <- file.path(normalizePath(dirname(args[4]), winslash = "/", mustWork = TRUE), basename(args[4]))
if (destino == repo || startsWith(destino, paste0(repo, "/"))) stop("Resultados empíricos devem ficar em data_root fora do checkout.")
if (file.exists(destino)) stop("Saída existente; preservar a versão anterior.")
resultado <- calcular_percurso_sih(rd, contrato, mapa, "empirico")
if (sha256_fonte_cnes(dataset) != a$sha256[a$papel == "dataset_csv"]) stop("Fonte mudou durante cálculo.")
staging <- tempfile("sih_staging_", tmpdir = dirname(destino));dir.create(staging)
# Em falha, staging incompleto fica preservado para diagnóstico; nunca é destino final.
for (nome in c("s03", "s04", "matriz", "matriz_origem_destino", "perdas", "perfil_ident")) {
  if (!is.null(resultado[[nome]])) write.csv(resultado[[nome]], file.path(staging, paste0(nome, ".csv")), row.names = FALSE, na = "NA")
}
write.csv(data.frame(competencia = contrato$competencia, conteudo_id = contrato$conteudo_id,
  estado = resultado$status, divulgacao_fluxos = resultado$divulgacao_fluxos,
  origem_nao_regionalizada = resultado$origem_nao_regionalizada),file.path(staging,"execucao.csv"),row.names=FALSE)
arquivos <- list.files(staging, full.names = TRUE)
write.csv(data.frame(arquivo = basename(arquivos), sha256 = vapply(arquivos, sha256_fonte_cnes, character(1))),
  file.path(staging,"manifesto.csv"),row.names=FALSE)
if (!file.rename(staging,destino)) stop("Falha na promoção local; staging preservado para diagnóstico.")
message("Cálculo local concluído com vínculos; revisão humana e divulgação não são inferidas.")
