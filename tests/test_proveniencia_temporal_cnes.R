# R22: fixture 202602 sintética derivada da fixture 202601; não toca no snapshot.
source("src/transform/preparar_estabelecimentos_cnes.R")
local({
  tmp <- tempfile("proveniencia_"); dir.create(tmp)
  on.exit(unlink(tmp, recursive = TRUE))
  dir.create(file.path(tmp, "202602"))
  for (f in list.files("tests/fixtures/cnes/202601", full.names = TRUE)) {
    file.copy(f, file.path(tmp, "202602", sub("202601", "202602", basename(f))))
  }
  saida <- file.path(tmp, "saida")
  res <- preparar_estabelecimentos_cnes(tmp, "202602", dir_interim = saida)
  stopifnot(all(res$competencia == "202602"), all(res$arquivo_origem == "tbEstabelecimento202602"),
            res$cnes == "0000001", res$co_unidade == "0001")
  falha <- function(expr, texto) {
    e <- tryCatch({force(expr); NULL}, error = identity)
    stopifnot(inherits(e, "error"), grepl(texto, conditionMessage(e), fixed = TRUE))
  }
  destino <- file.path(tmp, "nao_escrever")
  falha(preparar_estabelecimentos_cnes(tmp, "202602", dir_interim = destino,
    arquivo_estabelecimentos = "tests/fixtures/cnes/202601/tbEstabelecimento202601.csv"), "nome da fonte diverge")
  stopifnot(!dir.exists(destino))
  fonte <- file.path(tmp, "202602/tbEstabelecimento202602.csv")
  d <- read.csv(fonte, sep = ";", colClasses = "character")
  d$COMPETENCIA <- "202601"; write.table(d, fonte, sep = ";", row.names = FALSE)
  falha(preparar_estabelecimentos_cnes(tmp, "202602", dir_interim = destino), "registros diverge")
  stopifnot(!dir.exists(destino))
  falha(preparar_estabelecimentos_cnes(tmp, "202613", dir_interim = destino), "inválida")
  message("OK R22: nome e competência 202602; divergências recusadas antes da escrita; chaves textuais preservadas")
})
