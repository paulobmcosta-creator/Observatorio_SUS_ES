#' Reproduzir uma dimensão histórica RUE, sem modificar ou homologar o legado.
#' @param estabelecimentos Data frame histórico; campos textuais preservados.
#' @param referencia Tabela municipal histórica com n_estab_urgencia_sus.
#' @return Tabela de comparação por código legado; não infere localização física.
#' @references Work CP09 E025/E040; script histórico analise_rue_cnes_202601.py L104–121.
reproduzir_dimensao_rue <- function(estabelecimentos, referencia) {
  campos <- c("cnes", "competencia", "cod_municipio", "atende_sus", "atendimento_prestado")
  if (!all(campos %in% names(estabelecimentos)) ||
      !all(c("cod_municipio", "n_estab_urgencia_sus") %in% names(referencia))) stop("Campos obrigatórios ausentes.")
  if (!nrow(estabelecimentos) || !nrow(referencia)) stop("Universo obrigatório vazio.")
  if (anyNA(estabelecimentos$competencia) || any(estabelecimentos$competencia != "202601")) stop("Competência histórica divergente.")
  for (campo in c("cnes", "cod_municipio")) {
    if (!is.character(estabelecimentos[[campo]]) || anyNA(estabelecimentos[[campo]]) ||
        any(trimws(estabelecimentos[[campo]]) == "")) stop("Chave histórica ausente ou não textual.")
  }
  codigos <- trimws(referencia$cod_municipio)
  if (anyNA(codigos) || any(!grepl("^[0-9]{6}$", codigos)) || anyDuplicated(codigos) ||
      !setequal(codigos, trimws(estabelecimentos$cod_municipio))) stop("Universos municipais divergentes.")
  ref <- suppressWarnings(as.integer(referencia$n_estab_urgencia_sus))
  if (anyNA(ref) || any(ref < 0) || any(as.character(ref) != referencia$n_estab_urgencia_sus)) stop("Contagem de referência inválida.")
  atendimento <- ifelse(is.na(estabelecimentos$atendimento_prestado), "", estabelecimentos$atendimento_prestado)
  token <- vapply(strsplit(atendimento, "|", fixed = TRUE), function(x) "URGENCIA" %in% trimws(x), logical(1))
  elegivel <- !is.na(estabelecimentos$atende_sus) & trimws(estabelecimentos$atende_sus) == "Sim" & token
  contagens <- vapply(codigos, function(codigo) length(unique(trimws(estabelecimentos$cnes[
    elegivel & trimws(estabelecimentos$cod_municipio) == codigo]))), integer(1))
  data.frame(cod_municipio_legado = codigos, competencia = "202601", observado = unname(contagens),
    referencia = ref, diferenca = unname(contagens) - ref, stringsAsFactors = FALSE)
}
