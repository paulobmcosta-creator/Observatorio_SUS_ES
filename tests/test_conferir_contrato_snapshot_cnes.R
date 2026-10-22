source("src/validation/conferir_contrato_snapshot_cnes.R")

# Casos sintéticos explícitos; nenhuma identidade real é reconstruída.
se <- ler_snapshot_cnes("metadata/cnes/schema_estabelecimentos_cnes.csv")
# Schema sintético mínimo para testar relações; CSV malformado é testado à parte.
sh <- data.frame(nome_campo = c("competencia", "co_unidade", "cnes", "cod_municipio", "uf",
    "codigo_habilitacao", "tipo_habilitacao", "usar_observatorio", "status_validacao", "linha_cuidado"),
    obrigatorio = "sim", stringsAsFactors = FALSE)
classif <- ler_snapshot_cnes("metadata/cnes/classificacao_habilitacoes_cnes.csv", ";")
dir_teste <- tempfile("contrato_cnes_")
dir.create(dir_teste)
est <- as.data.frame(setNames(rep(list("valor sintético"), nrow(se)), se$nome_campo), stringsAsFactors = FALSE)
est$competencia <- "202601"; est$cnes <- "0012345"
est$co_unidade <- "chave_operacional_sintetica"; est$cod_municipio <- "320530"; est$uf <- "ES"
# Uma habilitação sintética, explicitamente de teste, com chave da classificação.
hab <- as.data.frame(setNames(rep(list(""), nrow(sh)), sh$nome_campo), stringsAsFactors = FALSE)
for (campo in intersect(names(est), names(hab))) hab[[campo]] <- est[[campo]][1]
for (campo in intersect(names(classif), names(hab))) hab[[campo]] <- classif[[campo]][1]
for (campo in sh$nome_campo[sh$obrigatorio == "sim"]) {
    if (hab[[campo]] == "") hab[[campo]] <- "valor sintético"
}
checar <- function(e = est, h = hab, c = classif) conferir_contrato_snapshot_cnes(e, h, c, se, sh)
tem <- function(r, regra, estado, escopo) any(r$regra == regra & r$estado == estado & r$escopo == escopo)
cenarios <- 0L
testar <- function(nome, expressao) {
    force(expressao); cenarios <<- cenarios + 1L; message("OK: ", nome)
}
testar("caso sintético completo atende ao contrato", stopifnot(all(checar()$estado == "passou")))
testar("fixture histórica não é presumida equivalente ao contrato atual", {
    legado <- ler_snapshot_cnes("tests/fixtures/cnes/cnes_piloto_exemplo.csv")
    stopifnot(tem(checar(e = legado), "colunas_do_schema", "falhou", "estabelecimentos"))
})
testar("zeros à esquerda preservados no CSV", {
    e <- est; h <- hab; e$cnes[1] <- h$cnes[1] <- "0012345"
    arquivo <- file.path(dir_teste, "zeros.csv")
    write.csv(e, arquivo, row.names = FALSE)
    lido <- ler_snapshot_cnes(arquivo)
    stopifnot(identical(lido$cnes[1], "0012345"), all(checar(lido, h)$estado == "passou"))
})
testar("não inventar co_unidade nem usar cnes como chave substituta", {
    e <- est; e$co_unidade <- NULL
    r <- checar(e)
    stopifnot(tem(r, "colunas_do_schema", "falhou", "estabelecimentos"),
        tem(r, "habilitacoes_estabelecimentos", "nao_executado", "relacao"))
})
testar("identificador numérico não é silenciosamente convertido", {
    e <- est; e$cnes <- as.numeric(e$cnes)
    stopifnot(tem(checar(e), "tipo_textual:cnes", "falhou", "estabelecimentos"))
})
testar("código público longo é reprovado", {
    e <- est; e$cnes[1] <- "3200000012345"
    stopifnot(tem(checar(e), "dominio:cnes", "falhou", "estabelecimentos"))
})
testar("chave duplicada bloqueia relação muitos-para-um", {
    r <- checar(rbind(est, est[1, ]))
    stopifnot(tem(r, "chave_unica", "falhou", "estabelecimentos"),
        tem(r, "habilitacoes_estabelecimentos", "nao_executado", "relacao"))
})
testar("habilitação órfã é detectada", {
    h <- hab; h$co_unidade <- "chave_inexistente"
    stopifnot(tem(checar(h = h), "habilitacoes_estabelecimentos", "falhou", "relacao"))
})
testar("município divergente não é convertido", {
    h <- hab; h$cod_municipio <- "9999999"
    stopifnot(tem(checar(h = h), "igualdade:cod_municipio", "falhou", "relacao"))
})
testar("ausência e competência incorreta não viram zeros", {
    e <- est; e$co_unidade[1] <- NA_character_; e$competencia[1] <- "202613"
    r <- checar(e)
    stopifnot(tem(r, "preenchimento:co_unidade", "falhou", "estabelecimentos"),
        tem(r, "dominio:competencia", "falhou", "estabelecimentos"))
})
testar("divergência da classificação é detectada sem reclassificar", {
    h <- hab; h$usar_observatorio <- if (hab$usar_observatorio == "Sim") "Não" else "Sim"
    stopifnot(tem(checar(h = h), "classificacao:usar_observatorio", "falhou", "relacao"))
})
testar("chave composta da classificação inclui tipo", {
    c <- classif; nova <- classif[1, ]; nova$tipo_habilitacao <- "TESTE"
    stopifnot(all(checar(c = rbind(c, nova))$estado == "passou"))
    stopifnot(tem(checar(c = rbind(c, c[1, ])), "chave_unica", "falhou", "classificacao"))
})
testar("base vazia não passa por ausência de violações", {
    stopifnot(tem(checar(est[FALSE, ]), "base_nao_vazia", "falhou", "estabelecimentos"))
})
testar("CSV malformado não cria campos falsos", {
    arquivo <- file.path(dir_teste, "schema_invalido.csv")
    writeLines(c("nome_campo,tipo,obrigatorio", "cnes,texto,sim,extra"), arquivo)
    s <- ler_schema_snapshot_cnes(arquivo)
    stopifnot(!is.null(attr(s, "erro_csv")), nrow(s) == 0L)
    r <- conferir_contrato_snapshot_cnes(est, hab, classif, se, s)
    stopifnot(tem(r, "estrutura_csv_schema", "falhou", "habilitacoes"),
        tem(r, "colunas_do_schema", "nao_executado", "habilitacoes"))
})
testar("schema real de habilitações é CSV retangular e legível", {
    s <- ler_schema_snapshot_cnes("metadata/cnes/schema_habilitacoes_cnes.csv")
    stopifnot(is.null(attr(s, "erro_csv")), nrow(s) > 0L,
        all(c("co_unidade", "cnes", "data_atualizacao") %in% s$nome_campo))
})
unlink(dir_teste, recursive = TRUE)
message(cenarios, " cenários de contrato executados com sucesso.")
