#' Ler arquivos brutos do CNES para o pipeline piloto.
#'
#' @description
#' Lê um ou mais arquivos CSV de um diretório de entrada, adiciona metadados
#' básicos de rastreabilidade e retorna uma única tabela consolidada.
#' Esta função foi desenhada como base técnica para evolução futura do pipeline
#' CNES em múltiplas competências.
#'
#' @param diretorio_entrada Caminho relativo para diretório com arquivos CNES.
#' @param padrao_arquivo Expressão regular para filtrar os arquivos de entrada.
#' @param delimitador Delimitador dos arquivos CSV.
#'
#' @return `data.frame` com os arquivos combinados e coluna `arquivo_origem`.
#'   Todos os campos são lidos como texto para preservar códigos CNES e
#'   identificadores administrativos com zeros à esquerda.
#' @examples
#' # dados_cnes <- ler_arquivos_cnes("data_raw/cnes")
ler_arquivos_cnes <- function(
    diretorio_entrada = "data_raw/cnes",
    padrao_arquivo = "\\.csv$",
    delimitador = ","
) {
    combinar_tabelas_por_nome <- function(tabelas) {
        colunas <- unique(unlist(lapply(tabelas, names), use.names = FALSE))
        tabelas_alinhadas <- lapply(tabelas, function(tabela) {
            colunas_ausentes <- setdiff(colunas, names(tabela))
            for (coluna in colunas_ausentes) {
                tabela[[coluna]] <- NA_character_
            }
            tabela[colunas]
        })

        do.call(rbind, tabelas_alinhadas)
    }

    if (!dir.exists(diretorio_entrada)) {
        stop(
            paste0(
                "Diretório de entrada não encontrado: '",
                diretorio_entrada,
                "'."
            ),
            call. = FALSE
        )
    }

    arquivos <- list.files(
        path = diretorio_entrada,
        pattern = padrao_arquivo,
        full.names = TRUE
    )

    if (length(arquivos) == 0) {
        stop(
            paste0(
                "Nenhum arquivo encontrado em '",
                diretorio_entrada,
                "' com padrão '",
                padrao_arquivo,
                "'."
            ),
            call. = FALSE
        )
    }

    tabelas <- lapply(arquivos, function(arquivo_atual) {
        tabela <- utils::read.csv(
            file = arquivo_atual,
            sep = delimitador,
            stringsAsFactors = FALSE,
            check.names = FALSE,
            colClasses = "character",
            na.strings = c("", "NA")
        )

        tabela$arquivo_origem <- basename(arquivo_atual)
        tabela
    })

    dados <- combinar_tabelas_por_nome(tabelas)
    row.names(dados) <- NULL

    dados
}
