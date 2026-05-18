# Testes unitários da leitura de arquivos CNES

source("src/extract/ler_arquivos_cnes.R")

copiar_fixture <- function(nome_fixture, diretorio_destino, nome_destino = nome_fixture) {
    origem <- file.path("tests", "fixtures", "cnes", nome_fixture)
    destino <- file.path(diretorio_destino, nome_destino)
    ok <- file.copy(origem, destino, overwrite = TRUE)
    stopifnot(ok)
    destino
}

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

executar_testes_ler_arquivos_cnes <- function() {
    raiz_teste <- file.path(tempdir(), paste0("teste_ler_cnes_", Sys.getpid()))
    if (dir.exists(raiz_teste)) {
        unlink(raiz_teste, recursive = TRUE)
    }
    dir.create(raiz_teste, recursive = TRUE, showWarnings = FALSE)

    diretorio_valido <- file.path(raiz_teste, "entrada_valida")
    dir.create(diretorio_valido, recursive = TRUE, showWarnings = FALSE)
    copiar_fixture("cnes_piloto_exemplo.csv", diretorio_valido)

    dados <- ler_arquivos_cnes(diretorio_entrada = diretorio_valido)
    stopifnot(is.data.frame(dados))
    stopifnot(nrow(dados) == 2)
    stopifnot("arquivo_origem" %in% names(dados))
    stopifnot(all(dados$arquivo_origem == "cnes_piloto_exemplo.csv"))

    diretorio_multiplos <- file.path(raiz_teste, "entrada_multiplos")
    dir.create(diretorio_multiplos, recursive = TRUE, showWarnings = FALSE)
    copiar_fixture("cnes_piloto_exemplo.csv", diretorio_multiplos, "cnes_202601.csv")
    copiar_fixture("cnes_multiplos_registros.csv", diretorio_multiplos, "cnes_202602.csv")

    dados_multiplos <- ler_arquivos_cnes(diretorio_entrada = diretorio_multiplos)
    stopifnot(is.data.frame(dados_multiplos))
    stopifnot(nrow(dados_multiplos) == 5)
    stopifnot("arquivo_origem" %in% names(dados_multiplos))
    stopifnot(length(unique(dados_multiplos$arquivo_origem)) == 2)

    diretorio_codigos <- file.path(raiz_teste, "entrada_codigos")
    dir.create(diretorio_codigos, recursive = TRUE, showWarnings = FALSE)
    writeLines(
        c(
            "competencia,co_municipio_gestor,co_cnes",
            "202601,03205309,0012345"
        ),
        file.path(diretorio_codigos, "cnes_codigos.csv")
    )
    dados_codigos <- ler_arquivos_cnes(diretorio_entrada = diretorio_codigos)
    stopifnot(identical(dados_codigos$co_municipio_gestor, "03205309"))
    stopifnot(identical(dados_codigos$co_cnes, "0012345"))

    diretorio_colunas_distintas <- file.path(raiz_teste, "entrada_colunas_distintas")
    dir.create(diretorio_colunas_distintas, recursive = TRUE, showWarnings = FALSE)
    writeLines(
        c(
            "competencia,co_cnes",
            "202601,1234567"
        ),
        file.path(diretorio_colunas_distintas, "cnes_a.csv")
    )
    writeLines(
        c(
            "competencia,co_municipio_gestor",
            "202602,3205309"
        ),
        file.path(diretorio_colunas_distintas, "cnes_b.csv")
    )
    dados_colunas_distintas <- ler_arquivos_cnes(diretorio_entrada = diretorio_colunas_distintas)
    stopifnot(nrow(dados_colunas_distintas) == 2)
    stopifnot(all(c("co_cnes", "co_municipio_gestor") %in% names(dados_colunas_distintas)))
    stopifnot(is.na(dados_colunas_distintas$co_municipio_gestor[1]))
    stopifnot(is.na(dados_colunas_distintas$co_cnes[2]))

    diretorio_inexistente <- file.path(raiz_teste, "nao_existe")
    esperar_erro(ler_arquivos_cnes(diretorio_entrada = diretorio_inexistente))

    diretorio_sem_csv <- file.path(raiz_teste, "sem_csv")
    dir.create(diretorio_sem_csv, recursive = TRUE, showWarnings = FALSE)
    writeLines("conteudo sintético", file.path(diretorio_sem_csv, "arquivo.txt"))
    esperar_erro(ler_arquivos_cnes(diretorio_entrada = diretorio_sem_csv, padrao_arquivo = "\\.csv$"))

    message("Testes unitários de ler_arquivos_cnes executados com sucesso.")
}

if (sys.nframe() == 0) {
    executar_testes_ler_arquivos_cnes()
}
