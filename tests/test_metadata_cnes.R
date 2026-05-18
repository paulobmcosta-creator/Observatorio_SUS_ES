# Testes de metadados do pipeline piloto CNES.
# Usa apenas funções do pacote base de R para evitar dependências externas.

executar_testes_metadata_cnes <- function() {
    arquivos_obrigatorios <- c(
        "metadata/cnes/schema_cnes_piloto.yml",
        "metadata/cnes/dicionario_cnes_piloto.csv",
        "docs/cnes/metadados_cnes_piloto.md"
    )

    arquivos_ausentes <- arquivos_obrigatorios[!file.exists(arquivos_obrigatorios)]
    if (length(arquivos_ausentes) > 0) {
        stop(
            "Arquivos de metadados obrigatórios ausentes: ",
            paste(arquivos_ausentes, collapse = ", "),
            call. = FALSE
        )
    }

    colunas_esperadas <- c(
        "campo",
        "tipo",
        "obrigatorio",
        "origem",
        "descricao",
        "regra_preenchimento",
        "observacoes"
    )

    campos_minimos <- c(
        "competencia",
        "co_municipio_gestor",
        "co_cnes",
        "arquivo_origem",
        "competencia_aaaamm",
        "competencia_data_referencia",
        "versao_pipeline"
    )

    dicionario <- utils::read.csv(
        "metadata/cnes/dicionario_cnes_piloto.csv",
        stringsAsFactors = FALSE,
        check.names = FALSE
    )

    colunas_ausentes <- setdiff(colunas_esperadas, names(dicionario))
    if (length(colunas_ausentes) > 0) {
        stop(
            "Colunas esperadas ausentes no dicionário CNES: ",
            paste(colunas_ausentes, collapse = ", "),
            call. = FALSE
        )
    }

    campos_ausentes <- setdiff(campos_minimos, dicionario$campo)
    if (length(campos_ausentes) > 0) {
        stop(
            "Campos mínimos ausentes no dicionário CNES: ",
            paste(campos_ausentes, collapse = ", "),
            call. = FALSE
        )
    }

    duplicados <- unique(dicionario$campo[duplicated(dicionario$campo) & dicionario$campo %in% campos_minimos])
    if (length(duplicados) > 0) {
        stop(
            "Campos mínimos duplicados no dicionário CNES: ",
            paste(duplicados, collapse = ", "),
            call. = FALSE
        )
    }

    campos_documentacao_obrigatoria <- c(
        "competencia_aaaamm",
        "competencia_data_referencia",
        "arquivo_origem",
        "versao_pipeline"
    )
    linhas_campos_documentacao <- dicionario[dicionario$campo %in% campos_documentacao_obrigatoria, ]
    campos_sem_descricao <- linhas_campos_documentacao$campo[
        !nzchar(linhas_campos_documentacao$descricao) |
            !nzchar(linhas_campos_documentacao$regra_preenchimento) |
            !nzchar(linhas_campos_documentacao$observacoes)
    ]
    if (length(campos_sem_descricao) > 0) {
        stop(
            "Campos técnicos sem documentação completa no dicionário CNES: ",
            paste(campos_sem_descricao, collapse = ", "),
            call. = FALSE
        )
    }

    conteudo_schema <- paste(
        readLines("metadata/cnes/schema_cnes_piloto.yml", warn = FALSE),
        collapse = "\n"
    )
    campos_ausentes_schema <- campos_minimos[
        !vapply(campos_minimos, grepl, logical(1), x = conteudo_schema, fixed = TRUE)
    ]
    if (length(campos_ausentes_schema) > 0) {
        stop(
            "Campos mínimos ausentes no schema YAML CNES: ",
            paste(campos_ausentes_schema, collapse = ", "),
            call. = FALSE
        )
    }

    message("Testes de metadados CNES executados com sucesso.")
}

if (sys.nframe() == 0) {
    executar_testes_metadata_cnes()
}
