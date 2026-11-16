source("src/extract/preparar_cache_cnes.R")
source("src/transform/preparar_estabelecimentos_cnes.R")
local({
  tmp <- tempfile("cnes alias com espacos "); dir.create(tmp); on.exit(unlink(tmp, recursive = TRUE))
  fonte <- "tests/fixtures/cnes/202601/tbEstabelecimento202601.csv"
  alias <- file.path(tmp, "alias.csv"); file.copy(fonte, alias)
  destino <- file.path(tmp, "nao_escrever")
  falha <- function(expr, texto) {
    e <- tryCatch({force(expr);NULL},error=identity)
    stopifnot(inherits(e,"error"),grepl(texto,conditionMessage(e),fixed=TRUE))
  }
  falha(preparar_estabelecimentos_cnes("tests/fixtures/cnes",dir_interim=destino,arquivo_estabelecimentos=alias),"evidência de competência")
  m <- file.path(tmp,"manifesto.csv")
  write.csv(data.frame(competencia="202601",sha256_csv=sha256_fonte_cnes(alias)),m,row.names=FALSE)
  r <- preparar_estabelecimentos_cnes("tests/fixtures/cnes",dir_interim=file.path(tmp,"ok"),arquivo_estabelecimentos=alias,manifesto_estabelecimentos=m)
  stopifnot(r$competencia=="202601",r$arquivo_origem=="alias")
  write.csv(data.frame(competencia="202602",sha256_csv=sha256_fonte_cnes(alias)),m,row.names=FALSE)
  falha(preparar_estabelecimentos_cnes("tests/fixtures/cnes",dir_interim=destino,arquivo_estabelecimentos=alias,manifesto_estabelecimentos=m),"divergente")
  falha(preparar_estabelecimentos_cnes("tests/fixtures/cnes",uf_interesse="RJ",dir_interim=destino),"restrito ao escopo ES")
  stopifnot(!dir.exists(destino))
  message("OK A08: alias exige competência/hash; manifesto divergente e UF fora do escopo recusados")
})
