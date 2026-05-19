# Classifica habilitações CNES por chave composta.

classificar_habilitacoes_cnes <- function(base_habilitacoes, classificacao) {
  if (!is.data.frame(base_habilitacoes)) stop("base_habilitacoes deve ser data.frame.")
  if (!is.data.frame(classificacao)) stop("classificacao deve ser data.frame.")

  cols_base <- c("codigo_habilitacao", "tipo_habilitacao")
  cols_class <- c("codigo_habilitacao", "tipo_habilitacao")

  if (length(setdiff(cols_base, names(base_habilitacoes))) > 0) {
    stop("base_habilitacoes sem colunas obrigatórias: codigo_habilitacao e tipo_habilitacao.")
  }
  if (length(setdiff(cols_class, names(classificacao))) > 0) {
    stop("classificacao sem colunas obrigatórias: codigo_habilitacao e tipo_habilitacao.")
  }

  colunas_retorno <- c("codigo_habilitacao", "tipo_habilitacao", "linha_cuidado", "sublinha_cuidado", "componente_rede", "usar_observatorio", "prioridade")
  ausentes_retorno <- setdiff(colunas_retorno, names(classificacao))
  if (length(ausentes_retorno) > 0) {
    stop("classificacao sem colunas esperadas para enriquecimento: ", paste(ausentes_retorno, collapse = ", "))
  }

  merge(
    base_habilitacoes,
    classificacao[, colunas_retorno],
    by = c("codigo_habilitacao", "tipo_habilitacao"),
    all.x = TRUE,
    sort = FALSE
  )
}
