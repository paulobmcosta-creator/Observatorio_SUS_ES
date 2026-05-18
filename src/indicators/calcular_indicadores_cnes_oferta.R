#' Calcular indicadores iniciais de oferta do CNES.
#'
#' @description
#' Calcula indicadores técnicos e conservadores a partir de um `data.frame`
#' já padronizado pela camada interim do pipeline piloto CNES. A rotina usa
#' apenas R base, ignora valores ausentes nos recortes e não produz indicadores
#' epidemiológicos finais nem avaliação de suficiência da rede assistencial.
#'
#' @param dados_cnes_interim `data.frame` da camada interim CNES contendo, no
#'   mínimo, as colunas `competencia_aaaamm`, `co_municipio_gestor` e `co_cnes`.
#'
#' @return `data.frame` em formato longo com as colunas `indicador`, `valor`,
#'   `unidade`, `recorte`, `categoria` e `observacao`.
calcular_indicadores_cnes_oferta <- function(dados_cnes_interim) {
    if (!is.data.frame(dados_cnes_interim)) {
        stop("O objeto de entrada deve ser um data.frame.", call. = FALSE)
    }

    if (nrow(dados_cnes_interim) == 0) {
        stop("O data.frame de entrada não pode estar vazio.", call. = FALSE)
    }

    colunas_minimas <- c("competencia_aaaamm", "co_municipio_gestor", "co_cnes")
    colunas_ausentes <- setdiff(colunas_minimas, names(dados_cnes_interim))
    if (length(colunas_ausentes) > 0) {
        stop(
            "Colunas mínimas ausentes na camada interim CNES: ",
            paste(colunas_ausentes, collapse = ", "),
            call. = FALSE
        )
    }

    remover_ausentes <- function(vetor) {
        vetor[!is.na(vetor)]
    }

    contar_distintos_sem_na <- function(vetor) {
        length(unique(remover_ausentes(vetor)))
    }

    criar_linha <- function(indicador, valor, unidade, recorte, categoria, observacao) {
        data.frame(
            indicador = indicador,
            valor = as.numeric(valor),
            unidade = unidade,
            recorte = recorte,
            categoria = as.character(categoria),
            observacao = observacao,
            stringsAsFactors = FALSE
        )
    }

    indicadores_gerais <- rbind(
        criar_linha(
            "total_registros",
            nrow(dados_cnes_interim),
            "registros",
            "geral",
            "geral",
            "Número total de linhas na camada interim CNES."
        ),
        criar_linha(
            "total_estabelecimentos_distintos",
            contar_distintos_sem_na(dados_cnes_interim$co_cnes),
            "estabelecimentos",
            "geral",
            "oferta",
            "Valores distintos de co_cnes, desconsiderando NA."
        ),
        criar_linha(
            "total_municipios_gestores_distintos",
            contar_distintos_sem_na(dados_cnes_interim$co_municipio_gestor),
            "municípios",
            "geral",
            "território",
            "Valores distintos de co_municipio_gestor, desconsiderando NA."
        ),
        criar_linha(
            "total_competencias_distintas",
            contar_distintos_sem_na(dados_cnes_interim$competencia_aaaamm),
            "competências",
            "geral",
            "temporal",
            "Valores distintos de competencia_aaaamm, desconsiderando NA."
        )
    )

    competencias_validas <- remover_ausentes(dados_cnes_interim$competencia_aaaamm)
    contagem_competencias <- table(competencias_validas)
    contagem_competencias <- contagem_competencias[order(names(contagem_competencias))]
    indicadores_competencia <- data.frame(
        indicador = character(0),
        valor = numeric(0),
        unidade = character(0),
        recorte = character(0),
        categoria = character(0),
        observacao = character(0),
        stringsAsFactors = FALSE
    )
    if (length(contagem_competencias) > 0) {
        indicadores_competencia <- data.frame(
            indicador = rep("registros_por_competencia", length(contagem_competencias)),
            valor = as.numeric(contagem_competencias),
            unidade = rep("registros", length(contagem_competencias)),
            recorte = rep("competencia_aaaamm", length(contagem_competencias)),
            categoria = names(contagem_competencias),
            observacao = rep("Registros por competência válida; competências NA são ignoradas.", length(contagem_competencias)),
            stringsAsFactors = FALSE
        )
    }

    dados_municipio <- dados_cnes_interim[!is.na(dados_cnes_interim$co_municipio_gestor), ]
    indicadores_municipio <- data.frame(
        indicador = character(0),
        valor = numeric(0),
        unidade = character(0),
        recorte = character(0),
        categoria = character(0),
        observacao = character(0),
        stringsAsFactors = FALSE
    )
    if (nrow(dados_municipio) > 0) {
        estabelecimentos_por_municipio <- tapply(
            dados_municipio$co_cnes,
            dados_municipio$co_municipio_gestor,
            contar_distintos_sem_na
        )
        estabelecimentos_por_municipio <- estabelecimentos_por_municipio[
            order(names(estabelecimentos_por_municipio))
        ]
        indicadores_municipio <- data.frame(
            indicador = rep(
                "estabelecimentos_distintos_por_municipio_gestor",
                length(estabelecimentos_por_municipio)
            ),
            valor = as.numeric(estabelecimentos_por_municipio),
            unidade = rep("estabelecimentos", length(estabelecimentos_por_municipio)),
            recorte = rep("co_municipio_gestor", length(estabelecimentos_por_municipio)),
            categoria = names(estabelecimentos_por_municipio),
            observacao = rep(
                "Estabelecimentos distintos por município gestor válido; co_cnes NA não conta como estabelecimento.",
                length(estabelecimentos_por_municipio)
            ),
            stringsAsFactors = FALSE
        )
    }

    resultado <- rbind(indicadores_gerais, indicadores_competencia, indicadores_municipio)
    rownames(resultado) <- NULL
    resultado
}
