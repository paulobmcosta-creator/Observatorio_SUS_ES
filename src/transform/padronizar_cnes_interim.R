#' Padronizar estrutura mínima dos dados CNES para camada interim.
#'
#' @description
#' Aplica padronizações técnicas iniciais ao conjunto CNES:
#' 1) nomes de colunas em minúsculas com underscore;
#' 2) normalização da competência temporal para `AAAA-MM`;
#' 3) manutenção de identificadores administrativos relevantes.
#'
#' Esta rotina representa infraestrutura técnica inicial e não implementa
#' modelagem analítica final.
#'
#' @param dados_cnes `data.frame` de entrada já lido da camada bruta.
#' @param coluna_competencia Nome da coluna de competência temporal.
#' @param colunas_id Vetor com colunas de identificadores a preservar.
#'
#' @return `data.frame` padronizado para exportação em `data_interim/`.
padronizar_cnes_interim <- function(
    dados_cnes,
    coluna_competencia = "competencia",
    colunas_id = c("co_municipio_gestor", "co_cnes")
) {
    if (!is.data.frame(dados_cnes)) {
        stop("O objeto de entrada deve ser um data.frame.", call. = FALSE)
    }

    nomes_originais <- names(dados_cnes)
    nomes_padronizados <- tolower(nomes_originais)
    nomes_padronizados <- gsub("[^a-z0-9]+", "_", nomes_padronizados)
    nomes_padronizados <- gsub("^_|_$", "", nomes_padronizados)
    names(dados_cnes) <- nomes_padronizados

    if (!coluna_competencia %in% names(dados_cnes)) {
        stop(
            paste0(
                "Coluna de competência '",
                coluna_competencia,
                "' não encontrada após padronização."
            ),
            call. = FALSE
        )
    }

    competencia_bruta <- as.character(dados_cnes[[coluna_competencia]])
    competencia_apenas_digitos <- gsub("[^0-9]", "", competencia_bruta)

    dados_cnes$competencia_aaaamm <- ifelse(
        nchar(competencia_apenas_digitos) >= 6,
        substr(competencia_apenas_digitos, 1, 4),
        NA_character_
    )
    dados_cnes$competencia_aaaamm <- paste0(
        dados_cnes$competencia_aaaamm,
        "-",
        ifelse(
            nchar(competencia_apenas_digitos) >= 6,
            substr(competencia_apenas_digitos, 5, 6),
            NA_character_
        )
    )

    dados_cnes$competencia_data_referencia <- as.Date(
        paste0(gsub("-", "", dados_cnes$competencia_aaaamm), "01"),
        format = "%Y%m%d"
    )

    ids_disponiveis <- intersect(colunas_id, names(dados_cnes))
    if (length(ids_disponiveis) == 0) {
        warning(
            "Nenhum identificador territorial/administrativo esperado foi encontrado."
        )
    }

    dados_cnes$versao_pipeline <- "piloto_tecnico_v1"
    dados_cnes
}
