source("src/validation/validar_correspondencia_territorial.R")
# Todos os códigos/regiões/fontes abaixo são sintéticos, sem validade territorial.
m <- data.frame(cod_municipio_cnes = c("000001", "000002"), cod_municipio_ibge = c("0000019", "0000027"),
  regiao_id = "SINTETICA", regiao_nome = "Região sintética de teste", vigencia_inicio = "2026-01-01", vigencia_fim = "2026-12-31",
  fonte_url = "https://example.invalid/ato", ato_referencia = "TESTE SEM VALIDADE", sha256_fonte = strrep("a", 64))
falha <- function(expr, texto) {
  e <- tryCatch({ force(expr); NULL }, error = identity)
  stopifnot(inherits(e, "error"), grepl(texto, conditionMessage(e), fixed = TRUE))
}
r <- conferir_correspondencia_territorial(c("000001", "000002"), m, "2026-01-31")
stopifnot(identical(r$cod_municipio_ibge, m$cod_municipio_ibge), all(r$papel_territorial == "municipio_gestor"))
message("OK: correspondência explícita preserva zeros e papel territorial")
r <- conferir_correspondencia_territorial(c("000001", "999999", "0000019", NA_character_), m, "2027-01-01")
stopifnot(identical(r$estado, c("fora_vigencia", "sem_correspondencia", "codigo_ausente_ou_invalido", "codigo_ausente_ou_invalido")), all(is.na(r$regiao_do_municipio_gestor)))
message("OK: lacunas e código de sete dígitos não viram região nem código convertido")
r <- conferir_correspondencia_territorial("000001", m[FALSE, ], "2026-01-31")
stopifnot(r$estado == "sem_correspondencia", is.na(r$cod_municipio_ibge))
falha(conferir_correspondencia_territorial(1, m, "2026-01-31"), "devem ser texto")
falha(conferir_correspondencia_territorial("000001", m, "2026-02-30"), "ISO válida")
message("OK: correspondência vazia explícita; tipos e datas inválidos rejeitados")
falha(conferir_correspondencia_territorial("000001", rbind(m, m[1, ]), "2026-01-31"), "sobrepostas")
nova <- m[1, ]; nova$vigencia_inicio <- "2027-01-01"; nova$vigencia_fim <- "2027-12-31"; nova$regiao_id <- "NOVA"
r <- conferir_correspondencia_territorial("000001", rbind(m, nova), "2027-01-01")
stopifnot(r$regiao_do_municipio_gestor == "NOVA")
nova$vigencia_inicio <- "2026-12-31"
falha(conferir_correspondencia_territorial("000001", rbind(m, nova), "2026-01-31"), "sobrepostas")
message("OK: mudança temporal respeitada; sobreposição inclusive nos extremos rejeitada")
x <- m; x$cod_municipio_ibge[2] <- x$cod_municipio_ibge[1]
falha(conferir_correspondencia_territorial("000001", x, "2026-01-31"), "um-para-um")
x <- m; x$regiao_nome[2] <- "Outro nome"
falha(conferir_correspondencia_territorial("000001", x, "2026-01-31"), "nomes conflitantes")
x <- m; x$sha256_fonte <- ""
falha(conferir_correspondencia_territorial("000001", x, "2026-01-31"), "campo obrigatório vazio")
x <- m; x$vigencia_fim <- "2025-12-31"
falha(conferir_correspondencia_territorial("000001", x, "2026-01-31"), "vigência inválido")
message("OK: cardinalidade, identidade regional, proveniência mínima e intervalo conferidos")
