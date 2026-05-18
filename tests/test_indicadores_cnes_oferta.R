# Testes unitários dos indicadores iniciais de oferta CNES.
# Usa apenas funções do pacote base de R para evitar dependências externas.

source("src/indicators/calcular_indicadores_cnes_oferta.R")

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

obter_valor <- function(indicadores, nome_indicador, recorte, categoria) {
    linha <- indicadores$indicador == nome_indicador &
        indicadores$recorte == recorte &
        indicadores$categoria == categoria
    stopifnot(sum(linha) == 1)
    indicadores$valor[linha]
}

executar_testes_indicadores_cnes_oferta <- function() {
    esperar_erro(calcular_indicadores_cnes_oferta("entrada inválida"))
    esperar_erro(calcular_indicadores_cnes_oferta(data.frame()))
    esperar_erro(calcular_indicadores_cnes_oferta(data.frame(
        competencia_aaaamm = "2026-01",
        co_cnes = "1234567",
        stringsAsFactors = FALSE
    )))

    dados_sinteticos <- data.frame(
        competencia_aaaamm = c("2026-01", "2026-01", "2026-02", NA, "2026-02", "2026-03"),
        co_municipio_gestor = c("3205309", "3205309", "3205002", "3205002", NA, "3205309"),
        co_cnes = c("1234567", "7654321", "1111111", NA, "2222222", "1234567"),
        stringsAsFactors = FALSE
    )

    indicadores <- calcular_indicadores_cnes_oferta(dados_sinteticos)
    colunas_esperadas <- c("indicador", "valor", "unidade", "recorte", "categoria", "observacao")
    stopifnot(is.data.frame(indicadores))
    stopifnot(all(colunas_esperadas %in% names(indicadores)))

    stopifnot(identical(
        obter_valor(indicadores, "total_registros", "geral", "geral"),
        6
    ))
    stopifnot(identical(
        obter_valor(indicadores, "total_estabelecimentos_distintos", "geral", "oferta"),
        4
    ))
    stopifnot(identical(
        obter_valor(indicadores, "total_municipios_gestores_distintos", "geral", "território"),
        2
    ))
    stopifnot(identical(
        obter_valor(indicadores, "total_competencias_distintas", "geral", "temporal"),
        3
    ))

    stopifnot(identical(
        obter_valor(indicadores, "registros_por_competencia", "competencia_aaaamm", "2026-01"),
        2
    ))
    stopifnot(identical(
        obter_valor(indicadores, "registros_por_competencia", "competencia_aaaamm", "2026-02"),
        2
    ))
    stopifnot(identical(
        obter_valor(indicadores, "registros_por_competencia", "competencia_aaaamm", "2026-03"),
        1
    ))
    stopifnot(!any(is.na(indicadores$categoria[indicadores$indicador == "registros_por_competencia"])))

    stopifnot(identical(
        obter_valor(
            indicadores,
            "estabelecimentos_distintos_por_municipio_gestor",
            "co_municipio_gestor",
            "3205309"
        ),
        2
    ))
    stopifnot(identical(
        obter_valor(
            indicadores,
            "estabelecimentos_distintos_por_municipio_gestor",
            "co_municipio_gestor",
            "3205002"
        ),
        1
    ))
    stopifnot(!any(is.na(indicadores$categoria[
        indicadores$indicador == "estabelecimentos_distintos_por_municipio_gestor"
    ])))

    message("Testes de indicadores CNES de oferta executados com sucesso.")
}

if (sys.nframe() == 0) {
    executar_testes_indicadores_cnes_oferta()
}
