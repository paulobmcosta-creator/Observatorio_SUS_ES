source("src/validation/validar_vinculos_sih.R")
source("tests/test_percurso_sih.R")
# Strings APROVADO não autorizam fixture como empírico.
falso <- contrato
for (k in c("layout_documental", "coorte_documental", "paridade_leitores", "cobertura_nacional")) falso[[k]] <- "APROVADO"
erro <- tryCatch({calcular_percurso_sih(rd, falso, mapa); NULL}, error = identity)
stopifnot(inherits(erro, "error"), grepl("evidências vinculadas", conditionMessage(erro)))
# Mesma tabela inclui 2020 e 2024; domínio selecionado não inclui região inativa.
antigo <- mapa; antigo$versao_territorial <- "pdr2020-fixture"; antigo$regiao_id <- "ANTIGA"
antigo$regiao_nome <- "Região antiga sintética"; antigo$vigencia_inicio <- "2020-01-01"; antigo$vigencia_fim <- "2023-12-31"
futuro <- mapa; futuro$vigencia_inicio <- "2024-02-01"; futuro$vigencia_fim <- "2024-12-31"
futuro$regiao_id <- "FUTURA"; futuro$regiao_nome <- "Região futura sintética"
combinado <- rbind(antigo, mapa, futuro)
r <- calcular_percurso_sih(rd, contrato, combinado, "fixture_sintetica")
stopifnot(!any(r$s03$regiao_residencia %in% c("ANTIGA", "FUTURA")))
stopifnot(sum(r$matriz_origem_destino$registros) == 5L,
  "REGIAO_B" %in% r$matriz_origem_destino$destino_id,
  "UF_IBGE_33" %in% r$matriz_origem_destino$destino_id,
  "IGNORADO" %in% r$matriz_origem_destino$destino_id,
  grepl("BLOQUEADA", r$divulgacao_fluxos))
fora <- mapa; fora$vigencia_fim <- "2023-12-31"; fora$vigencia_inicio <- "2020-01-01"
r <- calcular_percurso_sih(rd, contrato, fora, "fixture_sintetica")
stopifnot(is.null(r$s04), all(r$s03$regiao_residencia %in% c("TOTAL_ES", "NAO_REGIONALIZADA")))
message("OK A02/A03/A04: flags recusadas; versão/vigência selecionadas; OD identificável reconciliada e divulgação bloqueada")
