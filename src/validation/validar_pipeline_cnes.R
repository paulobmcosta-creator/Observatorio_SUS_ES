#' Validar insumos e produtos do pipeline piloto CNES.
#'
#' @description
#' Executa validações técnicas mínimas para o piloto CNES:
#' - existência de arquivos de entrada;
#' - presença de colunas esperadas após transformação;
#' - existência do arquivo de saída intermediária.
#'
#' @param diretorio_entrada Diretório com os arquivos brutos.
#' @param padrao_arquivo Regex para identificar arquivos de entrada.
#' @param dados_transformados `data.frame` gerado na etapa de transformação.
#' @param colunas_esperadas Vetor de colunas mínimas esperadas.
#' @param arquivo_saida Caminho do arquivo de saída esperado.
#'
#' @return `TRUE` quando todas as validações são aprovadas.
validar_pipeline_cnes <- function(
    diretorio_entrada,
    padrao_arquivo,
    dados_transformados,
    colunas_esperadas = c("competencia_aaaamm", "competencia_data_referencia"),
    arquivo_saida
) {
    arquivos_entrada <- list.files(
        path = diretorio_entrada,
        pattern = padrao_arquivo,
        full.names = TRUE
    )

    if (length(arquivos_entrada) == 0) {
        stop(
            paste0(
                "Validação falhou: nenhum arquivo de entrada encontrado em '",
                diretorio_entrada,
                "'."
            ),
            call. = FALSE
        )
    }

    if (!is.data.frame(dados_transformados) || nrow(dados_transformados) == 0) {
        stop(
            "Validação falhou: dados transformados ausentes ou vazios.",
            call. = FALSE
        )
    }

    colunas_ausentes <- setdiff(colunas_esperadas, names(dados_transformados))
    if (length(colunas_ausentes) > 0) {
        stop(
            paste0(
                "Validação falhou: colunas esperadas ausentes: ",
                paste(colunas_ausentes, collapse = ", "),
                "."
            ),
            call. = FALSE
        )
    }

    if (!file.exists(arquivo_saida)) {
        stop(
            paste0(
                "Validação falhou: arquivo de saída não encontrado em '",
                arquivo_saida,
                "'."
            ),
            call. = FALSE
        )
    }

    TRUE
}
