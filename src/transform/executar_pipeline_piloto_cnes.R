#' Executar pipeline piloto técnico do CNES.
#'
#' @description
#' Orquestra as etapas mínimas de extração, transformação, exportação,
#' validação e log do piloto técnico do CNES para infraestrutura reprodutível.
#'
#' @param diretorio_entrada Diretório com os arquivos brutos CNES.
#' @param arquivo_saida Caminho do CSV de saída em data_interim.
#' @param arquivo_log Caminho do CSV de log de execução.
#' @param padrao_arquivo Padrão regex para seleção dos arquivos de entrada.
#' @param delimitador Delimitador dos arquivos de entrada.
#' @param coluna_competencia Nome da coluna de competência temporal.
#'
#' @return Lista com caminho de saída e total de linhas exportadas.
executar_pipeline_piloto_cnes <- function(
    diretorio_entrada = "data_raw/cnes",
    arquivo_saida = "data_interim/cnes/cnes_piloto_interim.csv",
    arquivo_log = "data_interim/logs/pipeline_cnes_log.csv",
    padrao_arquivo = "\\.csv$",
    delimitador = ",",
    coluna_competencia = "competencia"
) {
    source("src/extract/ler_arquivos_cnes.R")
    source("src/transform/padronizar_cnes_interim.R")
    source("src/validation/validar_pipeline_cnes.R")

    timestamp_inicio <- Sys.time()

    dados_brutos <- ler_arquivos_cnes(
        diretorio_entrada = diretorio_entrada,
        padrao_arquivo = padrao_arquivo,
        delimitador = delimitador
    )

    dados_interim <- padronizar_cnes_interim(
        dados_cnes = dados_brutos,
        coluna_competencia = coluna_competencia
    )

    dir.create(dirname(arquivo_saida), recursive = TRUE, showWarnings = FALSE)
    utils::write.csv(dados_interim, arquivo_saida, row.names = FALSE, fileEncoding = "UTF-8")

    validar_pipeline_cnes(
        diretorio_entrada = diretorio_entrada,
        padrao_arquivo = padrao_arquivo,
        dados_transformados = dados_interim,
        arquivo_saida = arquivo_saida
    )

    dir.create(dirname(arquivo_log), recursive = TRUE, showWarnings = FALSE)

    registro_log <- data.frame(
        data_hora_execucao = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
        script_executado = "src/transform/executar_pipeline_piloto_cnes.R",
        input_utilizado = paste(list.files(diretorio_entrada, pattern = padrao_arquivo), collapse = ";"),
        output_gerado = arquivo_saida,
        observacoes = paste0(
            "pipeline_piloto_concluido; linhas_exportadas=",
            nrow(dados_interim),
            "; duracao_segundos=",
            round(as.numeric(difftime(Sys.time(), timestamp_inicio, units = "secs")), 2)
        ),
        stringsAsFactors = FALSE
    )

    append_log <- file.exists(arquivo_log)
    utils::write.table(
        registro_log,
        file = arquivo_log,
        sep = ",",
        row.names = FALSE,
        col.names = !append_log,
        append = append_log
    )

    list(
        arquivo_saida = arquivo_saida,
        arquivo_log = arquivo_log,
        linhas_exportadas = nrow(dados_interim)
    )
}

if (sys.nframe() == 0) {
    mensagem <- tryCatch(
        {
            resultado <- executar_pipeline_piloto_cnes()
            paste0(
                "Pipeline piloto CNES concluído com sucesso. Saída: ",
                resultado$arquivo_saida,
                "."
            )
        },
        error = function(erro) {
            paste0("Erro na execução do pipeline piloto CNES: ", erro$message)
        }
    )

    message(mensagem)
}
