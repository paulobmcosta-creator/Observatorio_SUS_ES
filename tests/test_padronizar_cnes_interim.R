# Testes unitários da padronização interim CNES

source("src/transform/padronizar_cnes_interim.R")

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

capturar_aviso <- function(expr) {
    avisos <- character(0)
    valor <- withCallingHandlers(
        expr,
        warning = function(w) {
            avisos <<- c(avisos, conditionMessage(w))
            invokeRestart("muffleWarning")
        }
    )
    list(valor = valor, avisos = avisos)
}

executar_testes_padronizar_cnes_interim <- function() {
    fixture_valida <- file.path("tests", "fixtures", "cnes", "cnes_multiplos_registros.csv")
    dados_brutos <- utils::read.csv(fixture_valida, stringsAsFactors = FALSE, check.names = FALSE)

    dados_padronizados <- padronizar_cnes_interim(dados_brutos)
    stopifnot(is.data.frame(dados_padronizados))
    stopifnot(all(c("competencia", "co_municipio_gestor", "co_cnes") %in% names(dados_padronizados)))
    stopifnot("competencia_aaaamm" %in% names(dados_padronizados))
    stopifnot("competencia_data_referencia" %in% names(dados_padronizados))
    stopifnot("versao_pipeline" %in% names(dados_padronizados))
    stopifnot(identical(dados_padronizados$competencia_aaaamm, c("2026-01", "2026-02", "2026-03")))
    stopifnot(all(as.character(dados_padronizados$competencia_data_referencia) == c("2026-01-01", "2026-02-01", "2026-03-01")))
    stopifnot(identical(as.character(dados_padronizados$versao_pipeline), rep("piloto_tecnico_v1", 3)))
    stopifnot(identical(as.character(dados_padronizados$co_municipio_gestor), c("3205309", "3205309", "3205002")))
    stopifnot(identical(as.character(dados_padronizados$co_cnes), c("1234567", "7654321", "1111111")))

    fixture_sem_competencia <- file.path("tests", "fixtures", "cnes", "cnes_sem_competencia.csv")
    dados_sem_competencia <- utils::read.csv(fixture_sem_competencia, stringsAsFactors = FALSE, check.names = FALSE)
    esperar_erro(padronizar_cnes_interim(dados_sem_competencia))

    fixture_malformada <- file.path("tests", "fixtures", "cnes", "cnes_competencia_malformada.csv")
    dados_malformados <- utils::read.csv(fixture_malformada, stringsAsFactors = FALSE, check.names = FALSE)
    dados_malformados_padronizados <- padronizar_cnes_interim(dados_malformados)
    stopifnot("competencia_aaaamm" %in% names(dados_malformados_padronizados))
    stopifnot("competencia_data_referencia" %in% names(dados_malformados_padronizados))
    stopifnot(all(is.na(dados_malformados_padronizados$competencia_aaaamm)))
    stopifnot(all(is.na(dados_malformados_padronizados$competencia_data_referencia)))

    fixture_sem_identificadores <- file.path("tests", "fixtures", "cnes", "cnes_sem_identificadores.csv")
    dados_sem_identificadores <- utils::read.csv(fixture_sem_identificadores, stringsAsFactors = FALSE, check.names = FALSE)
    resultado_aviso <- capturar_aviso(padronizar_cnes_interim(dados_sem_identificadores))
    stopifnot(is.data.frame(resultado_aviso$valor))
    stopifnot(length(resultado_aviso$avisos) >= 1)
    stopifnot(any(grepl("Nenhum identificador", resultado_aviso$avisos)))

    message("Testes unitários de padronizar_cnes_interim executados com sucesso.")
}

if (sys.nframe() == 0) {
    executar_testes_padronizar_cnes_interim()
}
