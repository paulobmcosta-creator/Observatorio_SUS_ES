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
#' @examples
#' # dados_cnes <- ler_arquivos_cnes("data_raw/cnes")
ler_arquivos_cnes <- function(
    diretorio_entrada = "data_raw/cnes",
    padrao_arquivo = "\\.csv$",
    delimitador = ","
) {
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
            check.names = FALSE
        )

        tabela$arquivo_origem <- basename(arquivo_atual)
        tabela
    })

    dados <- do.call(rbind, tabelas)
    row.names(dados) <- NULL

    dados
}
