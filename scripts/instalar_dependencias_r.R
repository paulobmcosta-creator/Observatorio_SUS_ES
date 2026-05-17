#' Instala dependências do pipeline CNES em ambiente R.
#'
#' @description
#' Lê a matriz de dependências declaradas em `config/dependencias_r.csv`
#' e instala apenas pacotes externos (fonte diferente de `built-in`) que
#' ainda não estiverem disponíveis no ambiente.

instalar_dependencias_r <- function(arquivo_dependencias = "config/dependencias_r.csv") {
    if (!file.exists(arquivo_dependencias)) {
        stop(
            paste0("Arquivo de dependências não encontrado: ", arquivo_dependencias),
            call. = FALSE
        )
    }

    dependencias <- utils::read.csv(
        arquivo_dependencias,
        stringsAsFactors = FALSE,
        check.names = FALSE
    )

    colunas_esperadas <- c("pacote", "fonte", "obrigatorio", "motivo")
    colunas_ausentes <- setdiff(colunas_esperadas, names(dependencias))

    if (length(colunas_ausentes) > 0) {
        stop(
            paste0(
                "Arquivo de dependências inválido. Colunas ausentes: ",
                paste(colunas_ausentes, collapse = ", ")
            ),
            call. = FALSE
        )
    }

    externas <- dependencias[dependencias$fonte != "built-in", , drop = FALSE]

    if (nrow(externas) == 0) {
        message("Nenhuma dependência externa para instalar.")
        return(invisible(TRUE))
    }

    pacotes <- unique(externas$pacote)
    nao_instalados <- pacotes[!vapply(pacotes, requireNamespace, logical(1), quietly = TRUE)]

    if (length(nao_instalados) > 0) {
        message("Instalando pacotes externos: ", paste(nao_instalados, collapse = ", "))
        utils::install.packages(nao_instalados, repos = "https://cloud.r-project.org")
    } else {
        message("Todas as dependências externas já estão instaladas.")
    }

    invisible(TRUE)
}

if (sys.nframe() == 0) {
    instalar_dependencias_r()
}
