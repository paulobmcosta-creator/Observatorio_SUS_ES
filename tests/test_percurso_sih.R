source("src/validation/validar_correspondencia_territorial.R")
source("src/transform/territorializar_municipios.R")
source("src/indicators/calcular_percurso_sih.R")
rd <- read.csv("tests/fixtures/sih/rd_sintetico.csv", colClasses = "character")
mapa <- data.frame(versao_territorial = "fixture-sintetica", cod_municipio_cnes = c("320010", "320016"),
  cod_municipio_ibge = c("3200102", "3200169"), regiao_id = c("A", "B"), regiao_nome = c("Fixture A", "Fixture B"),
  vigencia_inicio = "2024-01-01", vigencia_fim = "2024-01-31", fonte_url = "https://example.invalid/fixture",
  ato_referencia = "SINTETICO; nenhuma vigência legal", sha256_fonte = paste(rep("a", 64), collapse = ""))
contrato <- list(competencia = "202401", ident_elegivel = "1", ident_dominio = c("1", "3", "5"),
  municipios_es = c("320010", "320016"), municipios_destino_conhecidos = c("320010", "320016", "330010"), territorio_versao = "fixture-sintetica")
r <- calcular_percurso_sih(rd, contrato, mapa, "fixture_sintetica")
stopifnot(r$s03$registros_elegiveis[1] == 5L, sum(r$matriz$registros) == 5L,
  sum(r$perdas$registros) == nrow(rd), r$s04$numerador[1] == 2L, r$s04$denominador[1] == 3L,
  r$s04$destino_ignorado[1] == 1L, abs(r$s04$percentual_fora[1] - 200/3) < 1e-10,
  r$s04$denominador[2] == 0L, is.na(r$s04$percentual_fora[2]),
  r$perdas$registros[r$perdas$motivo == "ident_nao_elegivel"] == 2L)
# N_AIH repetido em duas linhas legítimas continua contado; não há filtro por data de admissão.
stopifnot(sum(r$s03$registros_elegiveis[-1]) == 5L, identical(rd$N_AIH[1:2], c("0000001", "0000001")))
falha <- tryCatch({calcular_percurso_sih(rd, contrato, mapa); NULL}, error = identity)
stopifnot(inherits(falha, "error"), grepl("Gates empíricos", conditionMessage(falha)))
sem_mapa <- calcular_percurso_sih(rd, contrato, modo = "fixture_sintetica")
stopifnot(is.null(sem_mapa$s04), sem_mapa$origem_nao_regionalizada == 5L)
# Export opcional apenas no ensaio de integração sintético R/SQL.
args <- commandArgs(trailingOnly = TRUE)
if (length(args)) {
  dir.create(args[1], recursive = TRUE)
  write.csv(r$s03, file.path(args[1], "s03_sintetico.csv"), row.names = FALSE)
  write.csv(r$s04, file.path(args[1], "s04_sintetico.csv"), row.names = FALSE)
}
message("OK SIH sintético: S03/S04/perdas; ignorado != fora ES; denominador zero indefinido; produção bloqueada")
