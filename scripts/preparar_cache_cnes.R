# Executar na raiz do repositório; não faz download nem altera data_raw.
# Uso: Rscript scripts/preparar_cache_cnes.R FONTE_LOCAL [DIRETORIO_CACHE]
source("src/extract/preparar_cache_cnes.R")
args <- commandArgs(trailingOnly = TRUE)
if (!length(args) %in% c(1L, 2L)) stop("Informe FONTE_LOCAL [DIRETORIO_CACHE].")
cache <- if (length(args) == 2L) args[2] else ".cache/cnes/fontes"
cat(preparar_cache_cnes(args[1], "metadata/cnes/fontes/tbEstabelecimento202601.csv", cache), "\n")
