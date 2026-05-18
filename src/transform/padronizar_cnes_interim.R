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
#' @param coluna_competencia Nome da coluna de competência temporal. O nome
#'   informado é padronizado pela mesma regra aplicada às colunas de entrada.
#' @param colunas_id Vetor com colunas de identificadores a preservar. Os nomes
#'   informados são padronizados pela mesma regra aplicada às colunas de entrada.
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

    padronizar_nome_coluna <- function(nome_coluna) {
        nome_padronizado <- tolower(nome_coluna)
        nome_padronizado <- iconv(nome_padronizado, to = "ASCII//TRANSLIT")
        nome_padronizado <- gsub("[^a-z0-9]+", "_", nome_padronizado)
        gsub("^_|_$", "", nome_padronizado)
    }

    nomes_padronizados <- padronizar_nome_coluna(names(dados_cnes))
    names(dados_cnes) <- nomes_padronizados

    coluna_competencia_padronizada <- padronizar_nome_coluna(coluna_competencia)
    colunas_id_padronizadas <- padronizar_nome_coluna(colunas_id)

    if (!coluna_competencia_padronizada %in% names(dados_cnes)) {
        stop(
            paste0(
                "Coluna de competência padronizada '",
                coluna_competencia_padronizada,
                "' não encontrada após padronização."
            ),
            call. = FALSE
        )
    }

    competencia_bruta <- as.character(dados_cnes[[coluna_competencia_padronizada]])
    competencia_apenas_digitos <- gsub("[^0-9]", "", competencia_bruta)
    competencia_ano <- substr(competencia_apenas_digitos, 1, 4)
    competencia_mes <- substr(competencia_apenas_digitos, 5, 6)
    competencia_mes_numero <- suppressWarnings(as.integer(competencia_mes))
    competencia_valida <- nchar(competencia_apenas_digitos) >= 6 &
        !is.na(competencia_mes_numero) &
        competencia_mes_numero >= 1 &
        competencia_mes_numero <= 12

    dados_cnes$competencia_aaaamm <- ifelse(
        competencia_valida,
        paste0(competencia_ano, "-", competencia_mes),
        NA_character_
    )

    dados_cnes$competencia_data_referencia <- as.Date(
        ifelse(
            competencia_valida,
            paste0(competencia_ano, competencia_mes, "01"),
            NA_character_
        ),
        format = "%Y%m%d"
    )

    ids_disponiveis <- intersect(colunas_id_padronizadas, names(dados_cnes))
    if (length(ids_disponiveis) == 0) {
        warning(
            "Nenhum identificador territorial/administrativo esperado foi encontrado."
        )
    }

    dados_cnes$versao_pipeline <- "piloto_tecnico_v1"
    dados_cnes
}
