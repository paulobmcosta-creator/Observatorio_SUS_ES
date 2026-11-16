#' Exigir provas verificáveis e vincular o data frame aos bytes recebidos.
#' @param rd Tabela textual a calcular.
#' @param contrato Contrato com aceite_execucao, aceite_sha256 e python_validacao.
#' @return Invisível TRUE; erro antes do cálculo se vínculo incompleto/alterado.
#' @details O validador Python confere fontes/manifestações locais; não autentica revisão humana.
validar_vinculos_sih <- function(rd, contrato) {
  exigidos <- c("aceite_execucao", "aceite_sha256", "python_validacao")
  if (!all(exigidos %in% names(contrato))) stop("Gates empíricos exigem evidências vinculadas; flags avulsas não bastam.")
  if (!exists("sha256_fonte_cnes", mode = "function")) stop("Carregue o verificador SHA-256 existente.")
  if (sha256_fonte_cnes(contrato$aceite_execucao) != contrato$aceite_sha256) stop("Aceite alterado.")
  a <- read.csv(contrato$aceite_execucao, colClasses = "character", check.names = FALSE)
  if (!all(c("papel", "caminho", "sha256", "competencia", "conteudo_id") %in% names(a)) ||
      anyDuplicated(a$papel) || any(a$competencia != contrato$competencia) || length(unique(a$conteudo_id)) != 1L) stop("Aceite sem vínculo inequívoco ao dataset/competência.")
  if (!all(c("plano_provas", "dataset_csv", "parametros") %in% a$papel)) stop("Evidências mínimas ausentes.")
  for (i in seq_len(nrow(a))) if (sha256_fonte_cnes(a$caminho[i]) != a$sha256[i]) stop("Evidência modificada: ", a$papel[i])
  comando <- c(shQuote("scripts/preparar_aceite_sih.py"), "--plano", shQuote(a$caminho[a$papel == "plano_provas"]),
    "--aceite", shQuote(contrato$aceite_execucao))
  status <- system2(contrato$python_validacao, comando, stdout = FALSE, stderr = FALSE, env = "PYTHONPATH=python")
  if (status != 0L) stop("Provas empíricas SIH não aprovadas pelo verificador de vínculos.")
  parametros <- read.csv(a$caminho[a$papel == "parametros"], colClasses = "character")
  for (chave in c("competencia", "ident_elegivel", "ident_dominio", "municipios_es", "municipios_destino_conhecidos")) {
    valor <- parametros$valor[parametros$chave == chave]
    if (length(valor) != 1L || !identical(contrato[[chave]], strsplit(valor, "|", fixed = TRUE)[[1]])) stop("Contrato diverge das evidências: ", chave)
  }
  origem <- read.csv(a$caminho[a$papel == "dataset_csv"], colClasses = "character", check.names = FALSE, na.strings = character())
  if (!identical(rd, origem)) stop("Tabela em memória diverge do dataset vinculado; calcular os mesmos bytes.")
  invisible(TRUE)
}

#' Vincular correspondência e atos a seus bytes, versão e revisão documental.
validar_vinculo_territorio_sih <- function(mapa, contrato) {
  exigidos <- c("territorio_arquivo", "territorio_sha256", "territorio_provas")
  if (!all(exigidos %in% names(contrato))) stop("S04 requer correspondência e atos integrais vinculados; flag textual não basta.")
  if (sha256_fonte_cnes(contrato$territorio_arquivo) != contrato$territorio_sha256) stop("Correspondência alterada.")
  real <- read.csv(contrato$territorio_arquivo, colClasses = "character", check.names = FALSE, na.strings = character())
  if (!identical(mapa, real)) stop("Mapa diverge dos bytes congelados.")
  provas <- read.csv(contrato$territorio_provas, colClasses = "character")
  if (!all(c("arquivo", "sha256", "revisor_funcional", "versao_territorial") %in% names(provas)) ||
      anyNA(provas) || any(trimws(provas$revisor_funcional) == "")) stop("Atos sem revisão documental identificada.")
  for (i in seq_len(nrow(provas))) if (sha256_fonte_cnes(provas$arquivo[i]) != provas$sha256[i]) stop("Ato territorial alterado.")
  m <- mapa[mapa$versao_territorial == contrato$territorio_versao, , drop = FALSE]
  fontes <- provas$sha256[provas$versao_territorial == contrato$territorio_versao]
  if (!length(fontes) || !all(m$sha256_fonte %in% fontes)) stop("Hash de fonte deve identificar ato integral, não derivado candidato.")
  invisible(TRUE)
}
