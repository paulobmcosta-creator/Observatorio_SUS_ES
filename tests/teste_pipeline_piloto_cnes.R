# Testes mínimos do pipeline piloto CNES

source("src/extract/ler_arquivos_cnes.R")
source("src/transform/padronizar_cnes_interim.R")
source("src/validation/validar_pipeline_cnes.R")
source("src/transform/executar_pipeline_piloto_cnes.R")

executar_teste_pipeline_piloto_cnes <- function() {
    diretorio_teste <- file.path(tempdir(), "cnes_teste")
    dir.create(diretorio_teste, recursive = TRUE, showWarnings = FALSE)

    arquivo_fixture <- "tests/fixtures/cnes/cnes_piloto_exemplo.csv"
    if (!file.exists(arquivo_fixture)) {
        stop(
            paste0("Fixture de teste não encontrado: ", arquivo_fixture),
            call. = FALSE
        )
    }

    arquivo_entrada <- file.path(diretorio_teste, "cnes_exemplo.csv")
    file.copy(arquivo_fixture, arquivo_entrada, overwrite = TRUE)

    arquivo_saida <- file.path(tempdir(), "cnes_interim_teste.csv")
    arquivo_log <- file.path(tempdir(), "cnes_log_teste.csv")

    resultado <- executar_pipeline_piloto_cnes(
        diretorio_entrada = diretorio_teste,
        arquivo_saida = arquivo_saida,
        arquivo_log = arquivo_log,
        padrao_arquivo = "\\.csv$",
        coluna_competencia = "competencia"
    )

    stopifnot(file.exists(resultado$arquivo_saida))
    stopifnot(file.exists(resultado$arquivo_log))

    dados_saida <- utils::read.csv(resultado$arquivo_saida, stringsAsFactors = FALSE)
    stopifnot("competencia_aaaamm" %in% names(dados_saida))
    stopifnot("competencia_data_referencia" %in% names(dados_saida))

    dados_log <- utils::read.csv(resultado$arquivo_log, stringsAsFactors = FALSE)
    stopifnot("script_executado" %in% names(dados_log))
    stopifnot(nrow(dados_log) >= 1)

    message("Teste do pipeline piloto CNES executado com sucesso.")
}

if (sys.nframe() == 0) {
    executar_teste_pipeline_piloto_cnes()
}
