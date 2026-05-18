# Testes unitários da orquestração do pipeline piloto CNES

source("src/transform/executar_pipeline_piloto_cnes.R")

executar_testes_executar_pipeline_piloto_cnes <- function() {
    raiz_teste <- file.path(tempdir(), paste0("teste_executar_cnes_", Sys.getpid()))
    if (dir.exists(raiz_teste)) {
        unlink(raiz_teste, recursive = TRUE)
    }
    dir.create(raiz_teste, recursive = TRUE, showWarnings = FALSE)

    diretorio_entrada <- file.path(raiz_teste, "entrada")
    dir.create(diretorio_entrada, recursive = TRUE, showWarnings = FALSE)
    ok <- file.copy(
        file.path("tests", "fixtures", "cnes", "cnes_multiplos_registros.csv"),
        file.path(diretorio_entrada, "cnes_multiplos_registros.csv"),
        overwrite = TRUE
    )
    stopifnot(ok)

    arquivo_saida <- file.path(raiz_teste, "interim", "cnes_piloto_interim.csv")
    arquivo_log <- file.path(raiz_teste, "logs", "pipeline_cnes_log.csv")

    resultado <- executar_pipeline_piloto_cnes(
        diretorio_entrada = diretorio_entrada,
        arquivo_saida = arquivo_saida,
        arquivo_log = arquivo_log,
        padrao_arquivo = "\\.csv$",
        coluna_competencia = "competencia"
    )

    stopifnot(is.list(resultado))
    stopifnot(all(c("arquivo_saida", "arquivo_log", "linhas_exportadas") %in% names(resultado)))
    stopifnot(file.exists(resultado$arquivo_saida))
    stopifnot(file.exists(resultado$arquivo_log))
    stopifnot(identical(resultado$arquivo_saida, arquivo_saida))
    stopifnot(identical(resultado$arquivo_log, arquivo_log))
    stopifnot(resultado$linhas_exportadas == 3)

    dados_saida <- utils::read.csv(resultado$arquivo_saida, stringsAsFactors = FALSE)
    stopifnot(nrow(dados_saida) == 3)
    stopifnot("arquivo_origem" %in% names(dados_saida))
    stopifnot("competencia_aaaamm" %in% names(dados_saida))

    dados_log <- utils::read.csv(resultado$arquivo_log, stringsAsFactors = FALSE)
    stopifnot(nrow(dados_log) == 1)

    resultado_reexecucao <- executar_pipeline_piloto_cnes(
        diretorio_entrada = diretorio_entrada,
        arquivo_saida = arquivo_saida,
        arquivo_log = arquivo_log,
        padrao_arquivo = "\\.csv$",
        coluna_competencia = "competencia"
    )
    stopifnot(resultado_reexecucao$linhas_exportadas == 3)
    stopifnot(file.exists(resultado_reexecucao$arquivo_log))

    dados_log_reexecucao <- utils::read.csv(resultado_reexecucao$arquivo_log, stringsAsFactors = FALSE)
    stopifnot(nrow(dados_log_reexecucao) == 2)
    stopifnot("script_executado" %in% names(dados_log_reexecucao))

    message("Testes unitários de executar_pipeline_piloto_cnes executados com sucesso.")
}

if (sys.nframe() == 0) {
    executar_testes_executar_pipeline_piloto_cnes()
}
