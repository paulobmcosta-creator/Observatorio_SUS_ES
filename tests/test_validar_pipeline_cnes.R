# Testes unitários da validação do pipeline CNES

source("src/validation/validar_pipeline_cnes.R")

esperar_erro <- function(expr) {
    ocorreu_erro <- FALSE
    tryCatch(
        expr,
        error = function(e) {
            ocorreu_erro <<- TRUE
        }
    )
    stopifnot(ocorreu_erro)
}

criar_dados_transformados_validos <- function() {
    data.frame(
        competencia_aaaamm = c("2026-01", "2026-02"),
        competencia_data_referencia = as.Date(c("2026-01-01", "2026-02-01")),
        versao_pipeline = "piloto_tecnico_v1",
        stringsAsFactors = FALSE
    )
}

executar_testes_validar_pipeline_cnes <- function() {
    raiz_teste <- file.path(tempdir(), paste0("teste_validar_cnes_", Sys.getpid()))
    if (dir.exists(raiz_teste)) {
        unlink(raiz_teste, recursive = TRUE)
    }
    dir.create(raiz_teste, recursive = TRUE, showWarnings = FALSE)

    diretorio_entrada <- file.path(raiz_teste, "entrada")
    dir.create(diretorio_entrada, recursive = TRUE, showWarnings = FALSE)
    ok <- file.copy(
        file.path("tests", "fixtures", "cnes", "cnes_piloto_exemplo.csv"),
        file.path(diretorio_entrada, "cnes_piloto_exemplo.csv"),
        overwrite = TRUE
    )
    stopifnot(ok)

    dados_validos <- criar_dados_transformados_validos()
    arquivo_saida <- file.path(raiz_teste, "saida", "cnes_interim.csv")
    dir.create(dirname(arquivo_saida), recursive = TRUE, showWarnings = FALSE)
    utils::write.csv(dados_validos, arquivo_saida, row.names = FALSE)

    resultado_validacao <- validar_pipeline_cnes(
        diretorio_entrada = diretorio_entrada,
        padrao_arquivo = "\\.csv$",
        dados_transformados = dados_validos,
        arquivo_saida = arquivo_saida
    )
    stopifnot(isTRUE(resultado_validacao))

    diretorio_sem_entrada <- file.path(raiz_teste, "sem_entrada")
    dir.create(diretorio_sem_entrada, recursive = TRUE, showWarnings = FALSE)
    esperar_erro(validar_pipeline_cnes(diretorio_sem_entrada, "\\.csv$", dados_validos, arquivo_saida = arquivo_saida))

    esperar_erro(validar_pipeline_cnes(diretorio_entrada, "\\.csv$", list(a = 1), arquivo_saida = arquivo_saida))
    esperar_erro(validar_pipeline_cnes(diretorio_entrada, "\\.csv$", dados_validos[0, ], arquivo_saida = arquivo_saida))

    dados_sem_colunas <- data.frame(competencia_aaaamm = "2026-01", stringsAsFactors = FALSE)
    esperar_erro(validar_pipeline_cnes(diretorio_entrada, "\\.csv$", dados_sem_colunas, arquivo_saida = arquivo_saida))

    arquivo_saida_inexistente <- file.path(raiz_teste, "saida", "nao_existe.csv")
    esperar_erro(validar_pipeline_cnes(diretorio_entrada, "\\.csv$", dados_validos, arquivo_saida = arquivo_saida_inexistente))

    message("Testes unitários de validar_pipeline_cnes executados com sucesso.")
}

if (sys.nframe() == 0) {
    executar_testes_validar_pipeline_cnes()
}
