# Uso: Rscript scripts/reproduzir_ponte_rue.R estabelecimentos.csv referencia.csv destino_novo
source("src/extract/preparar_cache_cnes.R")
source("src/indicators/reproduzir_dimensao_rue.R")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("Informe estabelecimentos.csv referencia.csv destino_novo.")
if (dir.exists(args[3]) || file.exists(args[3])) stop("Destino já existe; preservar versão anterior.")
hashes <- vapply(args[1:2], sha256_fonte_cnes, character(1))
inicio <- Sys.time()
est <- read.csv(args[1], colClasses = "character", check.names = FALSE, na.strings = "NA")
ref <- read.csv(args[2], colClasses = "character", check.names = FALSE, fileEncoding = "UTF-8-BOM")
out <- reproduzir_dimensao_rue(est, ref)
if (nrow(out) != 78L || any(out$diferenca != 0L)) stop("Contraprova RUE divergiu; nenhuma saída promovida.")
if (!identical(hashes, vapply(args[1:2], sha256_fonte_cnes, character(1)))) stop("Fonte alterada durante a leitura.")
dir.create(args[3], recursive = TRUE)
write.csv(out, file.path(args[3], "comparacao_municipal.csv"), row.names = FALSE)
manifesto <- data.frame(arquivo = args[1:2], sha256 = hashes, papel = c("intermediario_historico", "referencia_historica"))
write.csv(manifesto, file.path(args[3], "insumos.csv"), row.names = FALSE)
write.csv(data.frame(celulas = nrow(out), divergencias = sum(out$diferenca != 0),
  dimensoes_verificadas = 1L, segundos = as.numeric(difftime(Sys.time(), inicio, units = "secs")),
  ambiente = R.version.string, resultado = "CONTRAPROVA_REAL_DIMENSAO_HISTORICA"),
  file.path(args[3], "resultado.csv"), row.names = FALSE)
message("OK: 78/78 células; uma dimensão histórica. Não valida funcionamento, região ou demais dimensões.")
