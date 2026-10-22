# Cache local verificável. Requer GNU sha256sum e gzip; nenhuma dependência R extra.

#' Calcular o SHA-256 dos bytes de um arquivo.
#' @param arquivo Arquivo local existente.
#' @return Hash hexadecimal de 64 posições.
sha256_fonte_cnes <- function(arquivo) {
  comando <- Sys.which("sha256sum")
  if (!nzchar(comando)) stop("Instale sha256sum para verificar a fonte.")
  saida <- system2(comando, c("--", shQuote(normalizePath(arquivo, mustWork = TRUE))), stdout = TRUE)
  if (!is.null(attr(saida, "status"))) stop("Falha ao calcular SHA-256.")
  hash <- sub("^\\\\?([a-f0-9]{64}).*$", "\\1", saida[1])
  if (!grepl("^[a-f0-9]{64}$", hash)) stop("SHA-256 inválido.")
  hash
}

#' Importar CSV ou CSV.GZ para cache comprimido identificado pelo conteúdo original.
#' @param arquivo Fonte local explícita; pode ser o objeto recuperado pelo Git LFS.
#' @param manifesto CSV de uma linha com sha256_csv e bytes_csv esperados.
#' @param dir_cache Diretório de cache descartável, fora das camadas de dados versionadas.
#' @return Caminho absoluto do gzip validado. Nunca substitui um cache divergente.
#' @references docs/ciclo_2026_2027/rodada_02_armazenamento_cnes.md
preparar_cache_cnes <- function(arquivo, manifesto, dir_cache = ".cache/cnes/fontes") {
  m <- read.csv(manifesto, colClasses = "character", check.names = FALSE)
  if (nrow(m) != 1L || !all(c("sha256_csv", "bytes_csv") %in% names(m)) ||
      !grepl("^[0-9a-f]{64}$", m$sha256_csv) || !grepl("^[1-9][0-9]*$", m$bytes_csv)) {
    stop("Manifesto inválido: esperados hash e tamanho de uma única fonte.")
  }
  gzip <- Sys.which("gzip")
  if (!nzchar(gzip)) stop("Instale gzip para preparar o cache.")
  arquivo <- normalizePath(arquivo, mustWork = TRUE)
  trabalho <- tempfile("cnes_fonte_")
  dir.create(trabalho)
  on.exit(unlink(trabalho, recursive = TRUE), add = TRUE)
  conferir <- function(caminho) {
    original <- caminho
    if (grepl("\\.gz$", caminho)) {
      original <- file.path(trabalho, "original.csv")
      status <- system2(gzip, c("-dc", "--", shQuote(caminho)), stdout = original)
      if (status != 0L) stop("Gzip inválido ou incompleto.")
    }
    if (file.info(original)$size != as.numeric(m$bytes_csv) ||
        sha256_fonte_cnes(original) != m$sha256_csv) {
      stop("Fonte divergente do manifesto (tamanho ou SHA-256).")
    }
    original
  }
  original <- conferir(arquivo)
  dir.create(dir_cache, recursive = TRUE, showWarnings = FALSE)
  destino <- file.path(normalizePath(dir_cache, mustWork = TRUE), paste0(m$sha256_csv, ".csv.gz"))
  if (file.exists(destino)) {
    conferir(destino)
    return(destino)
  }
  temporario <- tempfile("importacao_", tmpdir = dir_cache, fileext = ".csv.gz")
  on.exit(unlink(temporario), add = TRUE)
  status <- system2(gzip, c("-n", "-c", "--", shQuote(original)), stdout = temporario)
  if (status != 0L) stop("Falha na compressão da fonte.")
  conferir(temporario)
  if (!file.rename(temporario, destino)) stop("Não foi possível finalizar o cache.")
  destino
}
