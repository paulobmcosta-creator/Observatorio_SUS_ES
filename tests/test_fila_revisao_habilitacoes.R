source("src/validation/preparar_fila_revisao_habilitacoes.R")
c <- data.frame(codigo_habilitacao = c("0001", "0001", "0002", "0003"), tipo_habilitacao = c("A", "B", "A", "A"),
  descricao_habilitacao = "Sintética", linha_cuidado = "Teste", usar_observatorio = c("Sim", "Sim", "Não", "Sim"),
  status_validacao = c("revisar", "validado", "revisar", "revisar"), fonte_normativa = "Revisar", criterio_classificacao = "Teste")
h <- data.frame(codigo_habilitacao = c("0001", "0001", "0001", "0002"), tipo_habilitacao = c("A", "A", "B", "A"), co_unidade = c("un1", "un2", "un1", "un1"))
c_antes <- c; h_antes <- h
f <- preparar_fila_revisao_habilitacoes(c, h)
stopifnot(identical(f$n_registros_observados, c(2L, 1L, 1L, 0L)), identical(f$n_estabelecimentos_observados, c(2L, 1L, 1L, 0L)),
  all(f$parecer_documental == "pendente_consulta_primaria"), identical(c, c_antes), identical(h, h_antes))
message("OK: chave composta; contagens reconciliadas; zero apenas na base; status interno não vira parecer documental")
falha <- function(expr) stopifnot(inherits(tryCatch({ force(expr); NULL }, error = identity), "error"))
falha(preparar_fila_revisao_habilitacoes(rbind(c, c[1, ]), h))
x <- h; x$codigo_habilitacao[1] <- "9999"; falha(preparar_fila_revisao_habilitacoes(c, x))
x <- h; x$codigo_habilitacao <- as.integer(x$codigo_habilitacao); falha(preparar_fila_revisao_habilitacoes(c, x))
stopifnot(all(preparar_fila_revisao_habilitacoes(c, h[FALSE, ])$n_registros_observados == 0L))
message("OK: duplicidade, código sem classificação e perda de tipo rejeitados; base vazia explícita")
