#' Organizar a revisão documental sem mudar a classificação de habilitações.
#' @param classificacao Classificação histórica com código/tipo e campos de curadoria.
#' @param habilitacoes Snapshot de habilitações com co_unidade e chave código/tipo.
#' @return Fila com todas as combinações da classificação, inclusive fora do escopo.
#' @references docs/ciclo_2026_2027/rodada_03_territorio_habilitacoes.md
#' @details Zeros significam ausência na base fornecida, não ausência de serviço.
preparar_fila_revisao_habilitacoes <- function(classificacao, habilitacoes) {
  campos <- c("codigo_habilitacao", "tipo_habilitacao", "descricao_habilitacao", "linha_cuidado",
    "usar_observatorio", "status_validacao", "fonte_normativa", "criterio_classificacao")
  if (!all(campos %in% names(classificacao)) || !all(c("codigo_habilitacao", "tipo_habilitacao", "co_unidade") %in% names(habilitacoes))) stop("Campos obrigatórios ausentes.")
  for (d in list(classificacao, habilitacoes)) {
    for (campo in c("codigo_habilitacao", "tipo_habilitacao")) {
      if (!is.character(d[[campo]]) || anyNA(d[[campo]]) || any(trimws(d[[campo]]) == "")) stop("Chave deve ser texto preenchido.")
    }
  }
  if (!is.character(habilitacoes$co_unidade) || anyNA(habilitacoes$co_unidade) || any(trimws(habilitacoes$co_unidade) == "")) stop("CO_UNIDADE deve ser texto preenchido.")
  chave <- function(d) paste(d$codigo_habilitacao, d$tipo_habilitacao, sep = "__")
  kc <- chave(classificacao); kh <- chave(habilitacoes)
  if (anyDuplicated(kc)) stop("Classificação com chave código/tipo duplicada.")
  if (any(!kh %in% kc)) stop("Habilitação observada sem correspondência na classificação.")
  if (anyNA(classificacao$usar_observatorio) || anyNA(classificacao$status_validacao) ||
      any(!classificacao$usar_observatorio %in% c("Sim", "Não")) || any(!classificacao$status_validacao %in% c("validado", "revisar"))) stop("Estado interno de classificação desconhecido.")
  fila <- classificacao[campos]
  fila$n_registros_observados <- vapply(kc, function(k) sum(kh == k), integer(1))
  fila$n_estabelecimentos_observados <- vapply(kc, function(k) length(unique(habilitacoes$co_unidade[kh == k])), integer(1))
  fila$grupo_revisao <- ifelse(fila$usar_observatorio == "Sim",
    ifelse(fila$n_registros_observados > 0,
      ifelse(fila$status_validacao == "revisar", "1_observado_selecionado_revisar", "2_observado_selecionado_validado_interno"),
      "4_selecionado_nao_observado"),
    ifelse(fila$n_registros_observados > 0, "3_observado_fora_escopo", "5_fora_escopo_nao_observado"))
  fila$parecer_documental <- "pendente_consulta_primaria"
  fila$decisao_nesta_rodada <- "classificacao_preservada"
  fila <- fila[order(fila$grupo_revisao, -fila$n_registros_observados, fila$codigo_habilitacao, fila$tipo_habilitacao), ]
  rownames(fila) <- NULL
  fila
}
