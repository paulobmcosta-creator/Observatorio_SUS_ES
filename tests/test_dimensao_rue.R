source("src/indicators/reproduzir_dimensao_rue.R")
est <- data.frame(cnes = c("0001", "0001", "0002", "0003", "0004"), competencia = "202601",
  cod_municipio = c("320010", "320010", "320010", "320010", "320016"),
  atende_sus = c("Sim", "Sim", "Sim", "Não", "Sim"),
  atendimento_prestado = c("AMBULATORIAL | URGENCIA", "URGENCIA", "SUBURGENCIA", "URGENCIA", NA_character_))
ref <- data.frame(cod_municipio = c("320010", "320016"), n_estab_urgencia_sus = c("1", "0"))
stopifnot(all(reproduzir_dimensao_rue(est, ref)$diferenca == 0L))
falha <- function(expr) stopifnot(inherits(tryCatch({force(expr); NULL}, error = identity), "error"))
falha(reproduzir_dimensao_rue(est[FALSE, ], ref))
falha(reproduzir_dimensao_rue(est, ref[c(1, 1), ]))
est$competencia[1] <- "202602"; falha(reproduzir_dimensao_rue(est, ref))
message("OK: token exato, distinct local, zero observado e recusas; fixture sintética")
